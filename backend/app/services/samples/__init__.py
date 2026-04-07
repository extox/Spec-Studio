from app.services.samples.taskflow import TASKFLOW_FILES
from app.services.samples.groupware import GROUPWARE_FILES
from app.services.samples.b2b_commerce import B2B_COMMERCE_FILES

SAMPLE_CATALOG = [
    {
        "id": "taskflow",
        "name": "TaskFlow - AI 기반 할일 관리 서비스",
        "description": "Python/FastAPI/PostgreSQL/AWS 기술 기반의 AI 스마트 할일 관리 웹 앱 구축 프로젝트",
        "tech": "Python, FastAPI, PostgreSQL, AWS",
    },
    {
        "id": "groupware",
        "name": "SmartWork - 기업용 그룹웨어 시스템",
        "description": "JAVA/Spring/PostgreSQL/Azure 기술 기반의 포탈, 전자결재, 게시판을 포함하는 기업용 그룹웨어 구축 프로젝트",
        "tech": "Java, Spring Boot, PostgreSQL, Azure",
    },
    {
        "id": "b2b-commerce",
        "name": "TradeHub - B2B 이커머스 플랫폼",
        "description": "JAVA/Spring/PostgreSQL/Azure 기술 기반의 기업 간 거래를 위한 B2B 이커머스 플랫폼 구축 프로젝트",
        "tech": "Java, Spring Boot, PostgreSQL, Azure",
    },
]

SAMPLE_FILES_MAP = {
    "taskflow": lambda: TASKFLOW_FILES,
    "groupware": lambda: GROUPWARE_FILES,
    "b2b-commerce": lambda: B2B_COMMERCE_FILES,
}
