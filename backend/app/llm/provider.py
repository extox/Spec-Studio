from typing import AsyncGenerator
import json

import litellm
import httpx


class DifyResult:
    """Container for Dify streaming result, captures conversation_id."""
    def __init__(self):
        self.conversation_id: str | None = None


async def stream_chat(
    provider: str,
    model: str,
    api_key: str,
    messages: list[dict],
    base_url: str | None = None,
    conversation_id: str | None = None,
    dify_result: DifyResult | None = None,
    file_ids: list[str] | None = None,
) -> AsyncGenerator[str, None]:
    """Unified LLM streaming call. Routes to Dify or litellm based on provider."""
    if provider == "aion-u":
        async for chunk in _stream_dify_chat(
            api_key, messages, base_url,
            conversation_id=conversation_id,
            dify_result=dify_result,
            file_ids=file_ids,
        ):
            yield chunk
    else:
        model_name = f"{provider}/{model}" if provider != "openai" else model
        response = await litellm.acompletion(
            model=model_name,
            messages=messages,
            api_key=api_key,
            stream=True,
        )
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content


async def non_stream_chat(
    provider: str,
    model: str,
    api_key: str,
    messages: list[dict],
    base_url: str | None = None,
    conversation_id: str | None = None,
) -> str:
    """Unified LLM non-streaming call."""
    if provider == "aion-u":
        # Dify Agent App does not support blocking mode; use streaming and collect
        result = []
        async for chunk in _stream_dify_chat(
            api_key, messages, base_url,
            conversation_id=conversation_id,
            streaming=True,
        ):
            result.append(chunk)
        return "".join(result)
    else:
        model_name = f"{provider}/{model}" if provider != "openai" else model
        response = await litellm.acompletion(
            model=model_name,
            messages=messages,
            api_key=api_key,
            stream=False,
        )
        return response.choices[0].message.content


def _build_dify_query(messages: list[dict], has_conversation: bool = False) -> str:
    """Build the query string for Dify API.

    - First message in a conversation: include system prompt + user query
    - Subsequent messages (has_conversation=True): only user query,
      since Dify maintains context via conversation_id
    """
    # Find the last user message
    last_user_msg = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            last_user_msg = msg["content"]
            break

    # If continuing a conversation, just send the user message
    if has_conversation:
        return last_user_msg or "Hello"

    # First message: include system instructions
    system_parts = [m["content"] for m in messages if m["role"] == "system"]
    if system_parts and last_user_msg:
        system_context = "\n".join(system_parts)
        return f"[System Instructions]\n{system_context}\n\n[User Query]\n{last_user_msg}"

    return last_user_msg or "Hello"


async def _stream_dify_chat(
    api_key: str,
    messages: list[dict],
    base_url: str | None = None,
    streaming: bool = True,
    conversation_id: str | None = None,
    dify_result: DifyResult | None = None,
    file_ids: list[str] | None = None,
) -> AsyncGenerator[str, None]:
    """Stream chat via Dify Chat API (SSE).

    Dify API: POST {base_url}/v1/chat-messages
    - Authorization: Bearer {api_key}
    - Body: { inputs: {}, query: str, response_mode: "streaming",
              conversation_id: str, user: "web-bmad-user" }
    - Response: SSE with conversation_id for session continuity
    """
    if not base_url:
        raise ValueError("AI:ON-U (Dify) provider requires a Base URL.")

    # Normalize base_url
    normalized = base_url.rstrip("/")
    if normalized.endswith("/v1"):
        normalized = normalized[:-3]
    url = f"{normalized}/v1/chat-messages"

    has_conversation = conversation_id is not None and conversation_id != ""
    query = _build_dify_query(messages, has_conversation=has_conversation)

    payload: dict = {
        "inputs": {},
        "query": query,
        "response_mode": "streaming" if streaming else "blocking",
        "user": "web-bmad-user",
    }

    # Include conversation_id to maintain context across messages
    if has_conversation:
        payload["conversation_id"] = conversation_id

    # Include uploaded files (AI:ON-U/Dify format)
    if file_ids:
        payload["files"] = [
            {"type": "image", "transfer_method": "local_file", "upload_file_id": fid}
            for fid in file_ids
        ]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        if streaming:
            async with client.stream("POST", url, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    body = await response.aread()
                    raise Exception(f"AI:ON-U API error ({response.status_code}): {body.decode()}")

                async for line in response.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    data_str = line[5:].strip()
                    if not data_str:
                        continue
                    try:
                        data = json.loads(data_str)
                    except json.JSONDecodeError:
                        continue

                    event = data.get("event", "")

                    # Capture conversation_id from any event
                    if dify_result and "conversation_id" in data:
                        dify_result.conversation_id = data["conversation_id"]

                    if event == "message":
                        answer = data.get("answer", "")
                        if answer:
                            yield answer
                    elif event == "message_end":
                        if dify_result and "conversation_id" in data:
                            dify_result.conversation_id = data["conversation_id"]
                        break
                    elif event == "error":
                        error_msg = data.get("message", "Unknown Dify error")
                        raise Exception(f"AI:ON-U error: {error_msg}")
        else:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                raise Exception(f"AI:ON-U API error ({response.status_code}): {response.text}")
            data = response.json()
            if dify_result and "conversation_id" in data:
                dify_result.conversation_id = data["conversation_id"]
            answer = data.get("answer", "")
            if answer:
                yield answer


MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


async def upload_file_to_aion_u(
    api_key: str,
    base_url: str,
    file_content: bytes,
    filename: str,
    user: str = "web-bmad-user",
) -> dict:
    """Upload a file to AI:ON-U (Dify) API.

    POST {base_url}/v1/files/upload
    - Authorization: Bearer {api_key}
    - Body (multipart/form-data):
      - file: 업로드할 파일 (지원 형식: png, jpg, jpeg, webp, gif)
      - user: 사용자 식별 문자열
    - Response: { id, name, size, extension, mime_type, created_by, created_at }
    """
    if not base_url:
        raise ValueError("AI:ON-U provider requires a Base URL.")

    normalized = base_url.rstrip("/")
    if normalized.endswith("/v1"):
        normalized = normalized[:-3]
    url = f"{normalized}/v1/files/upload"

    import io
    import os

    ext = os.path.splitext(filename)[1].lower()
    mime_type = MIME_MAP.get(ext, "image/png")

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        files = {"file": (filename, io.BytesIO(file_content), mime_type)}
        data = {"user": user}
        response = await client.post(url, headers=headers, files=files, data=data)

        if response.status_code not in (200, 201):
            raise Exception(f"AI:ON-U file upload error ({response.status_code}): {response.text}")

        return response.json()
