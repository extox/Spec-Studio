"use client";

import { useState } from "react";
import Link from "next/link";
import { ChevronDown, ChevronRight, ExternalLink } from "lucide-react";
import { useI18n, type TranslationKey } from "@/lib/i18n";
import type { Issue } from "./IssueList";

interface Step {
  text: string;
  example?: string;
  linkLabel?: string;
  linkHref?: string;
}

/** Build the step-by-step recovery plan for a given issue. */
function buildSteps(
  issue: Issue,
  projectId: number,
  t: (k: TranslationKey, p?: Record<string, string>) => string
): Step[] | null {
  const anchor = issue.anchor ?? "";
  const fileLink = issue.file_id
    ? `/projects/${projectId}/files?fileId=${issue.file_id}`
    : null;
  const traceLink = anchor
    ? `/projects/${projectId}/traceability?focus=${encodeURIComponent(anchor)}`
    : null;

  switch (issue.rule_id) {
    case "fr_covered_by_story":
      return [
        {
          text: t("guide.fr_covered_by_story.step1", { anchor }),
          linkLabel: t("guide.openPRD"),
          linkHref: fileLink ?? undefined,
        },
        {
          text: t("guide.fr_covered_by_story.step2"),
        },
        {
          text: t("guide.fr_covered_by_story.step3", { anchor }),
          example: `<!-- derived_from: PRD#${anchor} -->\n# Story: ...\n## Acceptance Criteria\n- [ ] ...`,
        },
        {
          text: t("guide.fr_covered_by_story.step4"),
        },
        {
          text: t("guide.fr_covered_by_story.altDeferred", { anchor }),
        },
      ];

    case "nfr_referenced_in_architecture":
      return [
        {
          text: t("guide.nfr_referenced_in_architecture.step1", { anchor }),
          linkLabel: t("guide.openPRD"),
          linkHref: fileLink ?? undefined,
        },
        {
          text: t("guide.nfr_referenced_in_architecture.step2"),
        },
        {
          text: t("guide.nfr_referenced_in_architecture.step3", { anchor }),
          example: `## Component C-3: API Gateway\nAddresses: PRD#${anchor} (response time < 200ms p95)\n...`,
        },
        {
          text: t("guide.nfr_referenced_in_architecture.altADR", { anchor }),
          example: `## ADR-007: Adopt Redis cache to satisfy ${anchor}\nContext: PRD#${anchor} requires sub-200ms p95.\nDecision: ...`,
        },
      ];

    case "ux_flow_aligned_with_journey":
      return [
        {
          text: t("guide.ux_flow_aligned_with_journey.step1", { anchor }),
        },
        {
          text: t("guide.ux_flow_aligned_with_journey.step2"),
          linkLabel: t("guide.openPRD"),
          linkHref: `/projects/${projectId}/files`,
        },
        {
          text: t("guide.ux_flow_aligned_with_journey.step3"),
          example: `<!-- derived_from: PRD#UJ-002 -->\n## User Flow ${anchor}: ...`,
        },
        {
          text: t("guide.ux_flow_aligned_with_journey.altCreateUJ"),
        },
      ];

    case "orphan_anchor": {
      // Anchor prefix → expected connection target. Tells the user *which*
      // artifact should be linking to this anchor (or being linked from it).
      const anchorPrefix = anchor.match(/^([A-Z]+)/)?.[1] ?? "";
      const variant = (() => {
        switch (anchorPrefix) {
          case "UJ":
            return {
              expects: t("guide.orphan_anchor.expects.UJ"),
              example: `<!-- derived_from: PRD#${anchor || "UJ-001"} -->\n## User Flow UF-002: ...`,
              targetLabel: t("guide.openUX"),
              targetHref: `/projects/${projectId}/files`,
            };
          case "FR":
            return {
              expects: t("guide.orphan_anchor.expects.FR"),
              example: `<!-- derived_from: PRD#${anchor || "FR-001"} -->\n# Story: ...`,
              targetLabel: t("guide.openStoryFolder"),
              targetHref: `/projects/${projectId}/files`,
            };
          case "NFR":
            return {
              expects: t("guide.orphan_anchor.expects.NFR"),
              example: `## Component C-3: API Gateway\nAddresses: PRD#${anchor || "NFR-001"} (...)`,
              targetLabel: t("guide.openARCH"),
              targetHref: `/projects/${projectId}/files`,
            };
          case "UF":
            return {
              expects: t("guide.orphan_anchor.expects.UF"),
              example: `<!-- derived_from: PRD#UJ-001 -->\n## User Flow ${anchor || "UF-001"}: ...`,
              targetLabel: t("guide.openPRD"),
              targetHref: `/projects/${projectId}/files`,
            };
          case "C":
            return {
              expects: t("guide.orphan_anchor.expects.C"),
              example: `## Component ${anchor || "C-1"}\nAddresses: PRD#NFR-002, PRD#FR-005`,
              targetLabel: t("guide.openARCH"),
              targetHref: `/projects/${projectId}/files`,
            };
          case "ADR":
            return {
              expects: t("guide.orphan_anchor.expects.ADR"),
              example: `## ${anchor || "ADR-001"}: Adopt X to satisfy NFR-002\nContext: PRD#NFR-002 ...`,
              targetLabel: t("guide.openARCH"),
              targetHref: `/projects/${projectId}/files`,
            };
          case "E":
            return {
              expects: t("guide.orphan_anchor.expects.E"),
              example: `## ${anchor || "E-001"}: ...\nCovers: PRD#FR-001, PRD#FR-002`,
              targetLabel: t("guide.openPRD"),
              targetHref: `/projects/${projectId}/files`,
            };
          case "S":
            return {
              expects: t("guide.orphan_anchor.expects.S"),
              example: `<!-- derived_from: EPIC#E-001, PRD#FR-001 -->\n# Story ${anchor || "S-001"}: ...`,
              targetLabel: t("guide.openEPIC"),
              targetHref: `/projects/${projectId}/files`,
            };
          default:
            return {
              expects: t("guide.orphan_anchor.expects.default"),
              example: `<!-- derived_from: PRD#FR-001, ARCH#C-2 -->`,
              targetLabel: t("guide.openInTrace"),
              targetHref: traceLink ?? undefined,
            };
        }
      })();

      return [
        {
          text: t("guide.orphan_anchor.step1", { anchor }),
          linkLabel: t("guide.openInTrace"),
          linkHref: traceLink ?? undefined,
        },
        {
          text: variant.expects,
          linkLabel: variant.targetLabel,
          linkHref: variant.targetHref,
        },
        {
          text: t("guide.orphan_anchor.step3"),
          example: variant.example,
        },
        {
          text: t("guide.orphan_anchor.altRemove", { anchor }),
        },
      ];
    }

    case "estimation_sanity":
      return [
        {
          text: t("guide.estimation_sanity.step1"),
          linkLabel: t("guide.openArtifact"),
          linkHref: fileLink ?? undefined,
        },
        {
          text: t("guide.estimation_sanity.step2"),
        },
        {
          text: t("guide.estimation_sanity.step3"),
        },
      ];

    case "contradictory_terms":
      return [
        {
          text: t("guide.contradictory_terms.step1"),
        },
        {
          text: t("guide.contradictory_terms.step2"),
          linkLabel: t("guide.openInTrace"),
          linkHref: traceLink ?? undefined,
        },
        {
          text: t("guide.contradictory_terms.step3"),
        },
        {
          text: t("guide.contradictory_terms.note"),
        },
      ];

    default:
      return null;
  }
}

interface ResolutionGuideProps {
  issue: Issue;
  projectId: number;
}

export function ResolutionGuide({ issue, projectId }: ResolutionGuideProps) {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  const steps = buildSteps(issue, projectId, t);
  if (!steps) return null;

  return (
    <section className="rounded-md border border-emerald-200 bg-emerald-50/40 text-xs">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center gap-1 px-3 py-2 text-[11px] font-semibold text-emerald-800 hover:bg-emerald-100/50 rounded-md transition-colors"
      >
        {open ? (
          <ChevronDown className="h-3 w-3" />
        ) : (
          <ChevronRight className="h-3 w-3" />
        )}
        🛠 {t("guide.title")}
        <span className="text-[10px] font-normal text-emerald-700/70 ml-auto">
          {open ? t("guide.collapse") : t("guide.expand")}
        </span>
      </button>
      {open && (
        <div className="px-3 pb-3 pt-1">
          <ol className="space-y-2 list-decimal pl-5">
            {steps.map((s, idx) => (
              <li key={idx} className="space-y-1">
                <p className="text-[12px] leading-relaxed">{s.text}</p>
                {s.example && (
                  <pre className="bg-slate-900 text-slate-100 text-[10.5px] rounded px-2 py-1.5 overflow-x-auto whitespace-pre">
                    {s.example}
                  </pre>
                )}
                {s.linkHref && s.linkLabel && (
                  <Link
                    href={s.linkHref}
                    className="inline-flex items-center gap-1 text-[11px] text-sky-700 hover:underline"
                  >
                    <ExternalLink className="h-3 w-3" />
                    {s.linkLabel}
                  </Link>
                )}
              </li>
            ))}
          </ol>
          <p className="text-[10px] italic text-emerald-700/80 mt-2">
            {t("guide.afterFix")}
          </p>
        </div>
      )}
    </section>
  );
}
