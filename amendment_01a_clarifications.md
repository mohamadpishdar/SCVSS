Amendment 01a: clarifications to Amendment 01 (control-B), decided 2026-11-25 before any control-B finding was extracted or drawn and before any Rule 2 or contamination result was viewed

1. Eligibility. A control-B report must meet both rules: it was published after 31 August 2026 (Amendment 01), and it meets the audit-start rule of protocol section 5 (the audit started on or after 1 August 2026; if the report states no audit start, its first report was issued on or after 1 September 2026).

2. Spearbit. Spearbit is excluded from control-B because its public repository contains no report published after 31 August 2026. Reports published under the Cantina name are not counted as Spearbit. Spearbit's share is reallocated to the other main-sample firms.

3. Caps. The limits of at most 2 findings per report and at most 2 findings per project apply to the original control group and control-B combined. Findings already in the original control group count towards these limits, and no finding is drawn twice.

## 01b (2026-11-25): final decisions for control-B, made from candidate counts only, before any draw and before any Rule 2 or contamination result was viewed

1. Eligibility. Both rules apply: the report was published after 31 August 2026, and it meets the audit-start rule of protocol section 5 (as in item 1 above; unchanged).

2. Spearbit. Spearbit is excluded; reports published under the Cantina name are not counted as Spearbit (as in item 2 above; unchanged).

3. Caps. The limits of at most 2 findings per report and at most 2 findings per project apply within control-B only. This replaces item 3 above. Reason: with the caps applied across both control sets, only about 13 findings qualify, 7 of them from QuillAudits. Findings already in the original control group are still not drawn again.

4. Analysis. The pooled contamination test (main vs original control + control-B, Medium/Low findings, firms present in both groups) models project as a random effect, or uses standard errors clustered by project, and keeps firm as a covariate.

5. Firm shares. Each firm contributes at most its target share of 40 (rounded as in the table); firms below target contribute all drawable findings; no reallocation of the shortfall (Spearbit's share was reallocated when the targets of 40 were computed, as in item 2 above; shortfalls of firms below target are not reallocated). Expected size 23 (QuillAudits 7, Sherlock 4, Zellic 4, Trail of Bits 2, Nethermind 3, Cyfrin 3). Decided from candidate counts only, before any draw.

## 01c (2026-11-25): handling of prior-report overlap, decided from controlB_prior_overlap.csv before redaction and before any Rule 2 or contamination result was viewed
1. Findings judged "same issue" as a finding in an earlier corpus report of the same project (CB-250) are excluded from the primary contamination test and reported separately.
2. Findings judged "related" (CB-038, CB-101, CB-222, CB-227, CB-252) stay in the primary test; a sensitivity analysis repeats the test without them.
3. No other control-B finding is excluded on content grounds; CB-233 is kept under the frozen extraction rule and noted in the report.
4. The primary contamination test therefore uses 22 control-B findings.

## 01d (2026-11-25): redaction of control-B, decided from the automatic leak checks (controlB_leak_scan.txt) before the visual check and before any rater run or Rule 2 or contamination result was viewed
1. No manual edits. All 23 control-B texts stay as produced by the frozen redaction pipeline (rule2.redact). CB-100's residual status text ("Fixed (commit ...)") stays, consistent with F00211 in the main sample; a sensitivity analysis excludes CB-100 and F00211.
2. Numbered QuillAudits titles (CB-132, CB-134, CB-144, CB-145) stay, as in the original control group (FR-339, FR-340); firm is already a covariate.
3. CB-190, CB-212, CB-213, CB-233 and CB-134 stay as redacted by the frozen pipeline.

## 01e (2026-11-25): residual rating sentences, decided from rating_sentence_scan.txt after the visual check and before any rater run or Rule 2 or contamination result was viewed
1. Rule R-01e removes a capitalised severity word (Critical, High, Medium, Low, Informational) used as a rating in forms A-C of rating_sentence_scan.py: (A) together with a preceding "hence/thus/therefore/so/making it|this"; (B) a sentence consisting only of the word, removed whole; (C) the word in "<Sev> for ...", leaving the rest of the clause. No other text is changed.
2. R-01e applies to all three groups. In the main sample and the original control it matches nothing, so the frozen redacted.jsonl is unchanged; it changes control-B texts CB-144, CB-145, CB-190 and CB-213 only.
3. F01554 (main sample, lowercase "high") is not matched by R-01e and stays; it is added to the sensitivity analysis that excludes CB-100 and F00211.
