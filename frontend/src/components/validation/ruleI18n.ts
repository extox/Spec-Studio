import type { TranslationKey } from "@/lib/i18n";
import type { Issue } from "./IssueList";

/**
 * Translate a rule's message/suggestion via i18n keys when available.
 * Falls back to the backend-supplied English text for rules with dynamic
 * content (e.g. LLM rules, ratios that aren't carried on the issue row).
 */
function variantSuffix(issue: Issue): string {
  // Special variant: fr_covered_by_story emits a project-level summary issue
  // (anchor=null) when zero Story files exist. Use a different message key.
  if (issue.rule_id === "fr_covered_by_story" && !issue.anchor) {
    return ".no_story_files";
  }
  return "";
}

export function translateRuleMessage(
  t: (key: TranslationKey, params?: Record<string, string>) => string,
  issue: Issue
): string {
  const key = `valid.rule.${issue.rule_id}${variantSuffix(issue)}.message` as TranslationKey;
  const translated = t(key, {
    anchor: issue.anchor ?? "",
    related: issue.related_anchor ?? "",
  });
  // i18n returns the key itself when not found.
  if (translated === key) return issue.message;
  return translated;
}

export function translateRuleSuggestion(
  t: (key: TranslationKey, params?: Record<string, string>) => string,
  issue: Issue
): string | null {
  if (!issue.suggestion) return null;
  const key = `valid.rule.${issue.rule_id}${variantSuffix(issue)}.suggestion` as TranslationKey;
  const translated = t(key, {
    anchor: issue.anchor ?? "",
    related: issue.related_anchor ?? "",
  });
  if (translated === key) return issue.suggestion;
  return translated;
}
