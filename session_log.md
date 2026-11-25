# Rule 2 session log

Working folder: `C:\Workdir\Develop\First Step\code\rule2_package` (rule2.py resolves `work\` next to itself).
Model running this session: claude-opus-5-5. Python 3.14.6.

## 2026-10-29  Setup and verification of the corrected files

### Commands
1. `Get-ChildItem -Recurse -File` (PDFs excluded from the listing): five package files present; `work\usr\` holds
   `answers_usr.jsonl` (381,160 B), `findings_base.csv` (35,677,068 B), `split_reports.csv` (131,311 B);
   `pdfs\` holds 3161 PDFs. `work\rule2\` did not exist before this session.
2. Read in full: CLAUDE_CODE_PROMPT_rule2.txt, PROTOCOL_rule2.md, codebook_rule2.json, README_R3_open_model.md,
   rule2.py (1068 lines).

### Verification of the requested changes
- A (paths): `HERE = Path(__file__).resolve().parent`, `USR = HERE/work/usr`, `OUT = HERE/work/rule2` (rule2.py:31-34). Confirmed.
- B (neutral codes): `stage_human` assigns `H{i:03d}` after the shuffle in `human_pick`, writes only code, title, text,
  factor columns and comment to the form; key written to `human_key_DO_NOT_OPEN.csv`; `analyze` maps codes back via
  the key (rule2.py:666-675, 702, 812-814). Confirmed.
- C (pilot outside human set): `extract --limit` removes `human_pick()` ids before slicing (rule2.py:603-605).
  `human_pick` includes all fresh findings, so the pilot also stays outside the control group. Confirmed.
- D (fresh PDFs): `work\rule2\fresh_pdfs\` is named in STEP 1b(b) of the prompt; the script does not read PDFs. Confirmed.
- F (cutoff check): STEP 0(d) present in the prompt. Confirmed.
- G (limitation): PROTOCOL section 7 states both limitations (prior exposure to corpus reports; exposure to the
  control findings while collecting and checking them). Confirmed.
- E (parent CLAUDE.md): to be checked in STEP 0(b).

### Remarks (no change made)
- rule2.py docstring line 5 still says "Run from ...\code"; line 17 says "60-finding" form (it is 100). Prompt
  header still names `...\code` as the start folder. Cosmetic.
- PROTOCOL section 7 says "The pilot findings of Section 6"; the pilot is not described in section 6.
  rule2.py:844 comment says decision rules are in "protocol section 6"; they are in section 9. Cosmetic.
- PROTOCOL section 3 names pilot prompt versions v0.2 to v0.2.3; answers_usr.jsonl holds only 0.2.1, 0.2.2, 0.2.3.
- `stage_sample` excludes every finding_id in answers_usr.jsonl regardless of version (matches the protocol).
- `stage_fresh` checks "not in corpus" by source_pdf file name only.
- `probe` prints `finding_id ... (truth <severity>)` to the console. The human form uses neutral codes, so this does
  not link to the form, but probe output should not be shown in detail.

### Pilot count before 'sample' (`python -I work\rule2\checks\count_pilot.py` plus one inline query)
- answers_usr.jsonl: 300 records, 0 unparsable, model claude-sonnet-5-5 for all.
- Prompt versions: 0.2.1 = 100, 0.2.2 = 100, 0.2.3 = 100 records (100 distinct finding_ids each).
- Distinct finding_ids: 200 (100 of them occur in more than one version); all 200 found in findings_base.csv.
- Reports containing a pilot finding: 123 (train 115, validation 2, test_random 3, test_temporal 3).
- split_reports.csv: train 1229, validation 218, test_random 153, test_temporal 232.
- **Train reports excluded from the selection sample as pilot reports: 115 of 1229.**

### Decisions
- User confirms excluding the 115 train reports.
- User asks to inspect `..\work\usr\answers_usr.jsonl1` read-only for v0.2 records.
- User asks to fix all minor problems before freezing, after seeing one combined diff.
- User: helper scripts go to `work\rule2\scripts\`; probe progress is reported as counts only.

## 2026-10-29  answers_usr.jsonl1 (read only) and proposed fixes

### Commands
1. Moved `work\rule2\checks\count_pilot.py` to `work\rule2\scripts\count_pilot.py` (removed empty `checks\`).
2. Read-only Python query on `C:\Workdir\Develop\First Step\code\work\usr\answers_usr.jsonl1`
   (33,902 B, 22/10/2026 14:09:17):
   - 30 records, 0 unparsable, model claude-sonnet-5-5.
   - No `_prompt_version` field (and no `rules_applied` field, which all 0.2.1-0.2.3 records have).
   - 30 distinct finding_ids, all in findings_base.csv, **all 30 already in answers_usr.jsonl**.
   - They come from 13 reports, all already among the 123 pilot reports: **0 additional train reports**.

### Decisions
- User chooses option (b) for PROTOCOL §3 (v0.2.1 to v0.2.3, unlabelled earlier file reported as a limitation)
  and the §6 pilot sentence.
- User asks to see the diff of the other fixes once more before everything is applied together.

- User confirmed; all fixes applied together (rule2.py docstring lines 5 and 17-18, comment now "section 9";
  prompt header, HARD RULES scripts line, STEP 1b(b) project/firm comparison; PROTOCOL §3 option (b), §6 pilot
  sentence). `python -I -c "ast.parse(rule2.py)"` OK; `python rule2.py --help` shows the new docstring.

## 2026-10-29  STEP 0  isolation check

Claude Code version 2.1.308 (`C:\Workdir\Programs\node-v24.20.0-win-x64\claude.ps1`).

### (a) `claude --help`: options that control settings, instruction files, memory, MCP, tools
- `--bare`: skips hooks, LSP, plugin sync, auto-memory, CLAUDE.md auto-discovery; auth only via ANTHROPIC_API_KEY
  or apiKeyHelper (OAuth/keychain not read).
- `--safe-mode`: disables CLAUDE.md, skills, plugins, hooks, MCP servers, custom commands/agents, output styles;
  auth and models unchanged.
- `--setting-sources <user,project,local>`, `--settings <file-or-json>`.
- `--strict-mcp-config` (only MCP servers from `--mcp-config`), `--mcp-config`.
- `--tools ""` (documented way to disable all built-in tools), `--disallowedTools`, `--allowedTools`.
- `--disable-slash-commands` (skills and commands off).
- `--system-prompt[-file]` replaces the default system prompt; `--append-system-prompt[-file]`.
- `--exclude-dynamic-system-prompt-sections` (only with the default system prompt).
- `--restricted` (removes code-running tools, ignores user/project/local settings).
- `--effort <low|medium|high|xhigh|max>`: not set in call_claude, so the effort level is not pinned.
- `--no-session-persistence`, `--max-turns`, `--output-format` (already used).

### (b) Instruction files, settings, memory, MCP
- CLAUDE.md: absent at `%USERPROFILE%\.claude\`, at every parent folder from `C:\` to `work\rule2\` (incl.
  `C:\Workdir\Develop\First Step\code\`), and at managed-policy locations. No CLAUDE.local.md, `.claude\` or
  `.mcp.json` in the parent chain.
- `%USERPROFILE%\.claude\settings.json`: `{"autoUpdatesChannel": "latest", "theme": "dark"}`; remote-settings `{}`;
  no settings.local.json.
- Memory: 7 project folders under `~\.claude\projects\`, every `memory\` folder empty or absent.
- MCP: `~\.claude.json` has no mcpServers (top level and the three First Step projects).
- Synced skills and plugins exist under `~\.claude\skills\synced` and `~\.claude\plugins\synced` (claude.ai).
- Environment of this session contains CLAUDECODE=1, CLAUDE_CODE_CHILD_SESSION=1, CLAUDE_CODE_ENTRYPOINT,
  CLAUDE_CODE_MESSAGING_SOCKET, CLAUDE_CODE_MESSAGING_TOKEN, CLAUDE_CODE_SESSION_ATTENDED, CLAUDE_CODE_SESSION_ID,
  CLAUDE_PID. call_claude passes the parent environment unchanged, so child calls started from this session
  inherit them.

### (c) Test call  `python -I work\rule2\scripts\step0c_isolation_test.py`
Exact call_claude flags, claude-opus-5-5, cwd `work\rule2\_isolated` (empty before and after). Raw output in
`work\rule2\scripts\step0c_output.json`. returncode 0, num_turns 1, modelUsage claude-opus-5-5,
cache_creation_input_tokens 799, output 871 (thinking 272).
Model's report of context besides the system prompt and the message:
- a system-reminder with the user's account e-mail address ("userEmail" context attached by Claude Code);
- an "# Environment" block: working directory (`...\work\rule2\_isolated`), not a git repo, win32, PowerShell,
  Windows 11 version, a note on untrusted downloads, model name and ID, "Assistant knowledge cutoff is June 2026",
  a token budget line, "Today's date is 2026-10-29".
- Tools: NONE.
- System prompt: "You are a Claude agent, built on Anthropic's Claude Agent SDK." prepended to the supplied text.
No CLAUDE.md, memory, skill listing, MCP instruction or project content appeared.

### (d) Training data cutoff (fetched 2026-10-29)
- https://platform.claude.com/docs/en/models/sonnet-5-5/overview : "Training data cutoff | Jun 2026";
  "Reliable knowledge cutoff | Jun 2026"; released September 28, 2026.
- https://platform.claude.com/docs/en/models/opus-5-5/overview : "Training data cutoff | Jun 2026";
  "Reliable knowledge cutoff | Jun 2026"; released September 22, 2026.
Both match the protocol (June 2026). No stop needed.

### Decisions
- User: keep call_claude flags unchanged (no --safe-mode, --strict-mcp-config, --disable-slash-commands,
  --effort, no environment filtering). Reason given by user: the injected context (account e-mail,
  environment block with date and model name, SDK system-prompt prefix) carries no information about any finding
  and is identical for every call, so it cannot bias factor answers.
- PROTOCOL §4: added after "...no user-level instruction file or memory is loaded into these calls.":
  "The command-line client adds a fixed environment block (date, operating system, model name) and the account
  e-mail to every call; this context is identical across findings and contains no information about them."
- User: proceed to STEP 1.

## 2026-10-29  STEP 1  sample

### `python -I rule2.py sample`
```
eligible findings 2230 in 938 train reports (pilot reports excluded: 123)
selection sample: 300 findings from 182 reports; fit set: 1047 reports
findings per firm: Sherlock=45, QuillAudits=45, Zellic=45, Trail of Bits=37, Spearbit=26, Nethermind=22, Cyfrin=21, CoinFabrik=19, Sigma Prime=17, Unidentified=8, BlockApex=8, ABDK=7
years: 2017=2, 2018=6, 2019=5, 2020=4, 2021=17, 2022=53, 2023=71, 2024=92, 2025=36, ?=14
```
Note: "pilot reports excluded: 123" counts pilot reports in all splits; 115 of them are train reports.
Wrote selection_sample.csv, selection_reports.csv, fit_reports.csv.

### `python -I work\rule2\scripts\check_sample.py` (independent check)
- Selection reports in fit_reports.csv: **0**; no duplicates in either file; selection + fit = all 1229 train
  reports exactly; none outside train.
- 300 distinct findings; all in selection reports; every selection report contributes >= 1 finding
  (64 reports with 1, 118 with 2; max 2 per report).
- 0 from pilot reports, 0 pilot findings, 0 EXCLUDED verdicts, 0 texts < 200 characters.
- Max per firm 45 (cap 45, reached by Sherlock, QuillAudits, Zellic).
- The 115 pilot train reports are in the fit set (protocol §3: all other train reports form the fit set).
- 14 sampled findings have an empty report_date (year "?"); 8 have firm "Unidentified" in split_reports.csv.

### Decisions
- Pilot reports belong to the fit set by design (protocol §3); this will be stated in the paper.
- User requests, before STEP 1b and before freezing: (1) seeded random processing order in stage_extract and
  stage_probe (`random.Random(SEED + "-order-" + rater_or_stage)`, before --limit; pilot rule unchanged);
  (2) reworded §4 sentence. Diff shown; awaiting confirmation.
- User confirmed. Applied: stage_probe builds all jobs, shuffles with `SEED + "-order-probe"`, then drops done
  jobs; stage_extract shuffles all rows with `SEED + "-order-" + rater`, then drops done ones; --limit pilot
  rule unchanged. PROTOCOL §4 sentence reworded as requested. `ast.parse` OK; `rule2.py status`:
  sample 300, redacted 0, frozen False.

## 2026-10-29  STEP 1b  control group (fresh findings)

User instruction (mid-step): batch checks into fewer, larger scripts in work\rule2\scripts\; stop only at decision
points (fresh report table, redaction diffs, freeze, pilot); never delete files outside work\rule2\ and $env:TEMP.

### (a) Search  (scripts in work\rule2\scripts\)
1. `fresh_list_repos.py`: GitHub tree listing of Cyfrin, spearbit/portfolio, trailofbits, Zellic, sigp, Nethermind,
   sherlock-reports, QuillAudit_Reports, pashov/audits (PDF names containing "2026": Cyfrin 88, ToB 61,
   Sherlock 18, Pashov 29; Spearbit portfolio has none (12 PDFs), Zellic/SigP/Nethermind/Quill names undated).
2. `fresh_commit_files.py`: PDFs added since 2026-08-01 by commit (Zellic 18, Sigma Prime 4, Nethermind 21).
3. `fresh_download.py`: 76 candidate PDFs downloaded to work\rule2\fresh_pdfs\ (urllib took ~85 s/file on this
   machine; switched to curl.exe, ~1.5 s/file; a stopped background run left no partial file). Pre-filtered out:
   clearly off-chain ToB reviews (Wikimedia, Amazon, Google, OpenAI, Sigstore, genesis file), Cyfrin frontend and
   executive summary, Zellic Zcash Sapling, Pashov "Agentic" (AI-generated) Lodestar report.
4. `fresh_period_detail.py`, `fresh_batch3.py`, `fresh_batch4.py`: audit-period text for unclear reports,
   QuillAudits uploads (6 more PDFs, 82 in total), corpus check by firm + project-name tokens.
5. `fresh_table.py` -> work\rule2\fresh_reports_table.md / .csv (82 rows, with URL, sha256, download date).

### (b) Result
- QUALIFIES 24 (Cyfrin 10, Pashov 4, QuillAudits 3, Zellic 3, Sherlock 2, Trail of Bits 2); AMBIGUOUS 1
  (Zellic Anza Token-2022: executive summary Sep 16-18, 2026; key-dates table Sep 16-18, 2025; report dated
  2026-09-24); NO START DATE 9 (Nethermind: only initial/final report dates, initial reports Aug 10 - Oct 8, 2026);
  EXCLUDED 48 (start before 2026-08-01, period not stated, duplicate, no findings, attestation).
- Sigma Prime reports state no audit period (only version month) -> excluded.
- Corpus check: no candidate file name in pdfs\ or split_reports.csv. Same-project earlier reports in the corpus:
  Securitize (6 qualifying Cyfrin reports), Flare (Zellic Flare Relay). No other qualifying report matches.

### Decisions (user, 2026-10-29)
1. Reports without a stated audit start (e.g. Nethermind): eligible if the first report date is on or after
   2026-09-01; that date is recorded as audit_start with start_from_report_date=yes. Protocol amendment §5 applied:
   "If a report states no audit start, the date of its first report is used, and only reports first issued on or
   after 1 September 2026 are eligible." Sigma Prime (version month only) stays excluded.
2. Zellic Anza Token-2022 excluded (conflicting dates).
3. Same-project reports kept with column prior_project_in_corpus=yes/no; PROTOCOL §10 amendment applied:
   "The contamination check (section 5) is repeated without the control findings whose project has an earlier
   report in the corpus (prior_project_in_corpus = yes)." Non-EVM reports excluded (Cyfrin vaultregistrar,
   stellar-dstoken, jump-router-market). Same project/engagement = one project, at most 2 findings per project.
4. Search more sources: Code4rena, Cantina/Spearbit, OpenZeppelin, ChainSecurity, Ackee, Consensys Diligence,
   Hacken, Halborn (contests: contest start date).
- Language check (`fresh_lang_check.py`): all remaining candidates Solidity; Pashov K3 has no language markers
  (4 pages); Nethermind Vana Deposit mostly Go (Prysm) plus a Solidity deposit contract.
- Proposed rule2.py / §5 / prompt changes drafted in work\rule2\scripts\proposed_step1b_changes.diff (not applied).
- Code4rena search (agent): no contest started on or after 2026-08-01 (latest starts April 2026; news of
  May 2026 reports Code4rena winding down). No candidates.
- User (switching to accept-edits mode): never edit rule2.py, PROTOCOL_rule2.md, codebook_rule2.json or
  CLAUDE_CODE_PROMPT_rule2.txt without first showing the diff and receiving an explicit "apply".

- OpenZeppelin/Consensys search (agent): no qualifying report. OpenZeppelin: only in-range start is Miden USDCx
  (2026-08-17 to 08-28; Miden Assembly/Rust, non-EVM); ONCHAINID 2026-07-27 to 08-07 (before cutoff); all other
  2026 reports started earlier. Consensys Diligence site blocked by a Cloudflare challenge (not bypassed); search
  snapshots show no Aug-Oct 2026 report; Fhenix (Oct 2026) unverified. Agent claims to be checked only if used.

- User (2026-10-29): "dont ask me again do what is best for the quality of research". Interpretation logged: proceed
  without stopping at decision points; still show every protected-file diff in the message and log it; stop only
  where the protocol needs the user's own work (visual check of 50 redacted texts, "freeze", human coding).
  A plan was written and approved (C:\Users\U0185368\.claude\plans\encapsulated-dazzling-hippo.md).

### Protected-file changes applied (diffs shown in chat)
- rule2.py: FRESH_FIELDS + project, start_from_report_date, prior_project_in_corpus; FRESH_FROM_REPORT_DATE =
  2026-09-01; stage_fresh eligibility checks for the new columns; draw grouped by project (<= 2 per project);
  summary line with projects and prior-project count; stage_analyze contamination check run twice (primary and
  "sensitivity: without prior_project_in_corpus=yes"), rows labelled by an `analysis` column.
- PROTOCOL §5: EVM-only, prior_project_in_corpus recorded, "at most two findings per project (reports on the same
  project or engagement count as one project)". Prompt STEP 1b(c): new column list.
- `ast.parse` OK; `rule2.py status` OK.

### More sources (agents; every claim re-checked from the downloaded report text, fresh_batch5.py)
- Cantina: 20 Solidity reports, periods Aug 6 - Oct 13 stated as "From <Mon> <d> to ..." without a year; year 2026
  from the cover date (logged as year-from-cover). Sky deployment-verification entry not used.
- ChainSecurity: 5 reports; audit_start = "Version 1 ... Initial review" date of the version table.
- Halborn: XMAQUINA (Sep 15-21) and NUVA (Aug 13-14) pages state periods, but finding descriptions are rendered by
  JavaScript and no PDF link exists -> excluded (no finding text).
- Code4rena none; OpenZeppelin none EVM; Consensys and Hacken sites blocked; Ackee none in range.
- Decision (quality): Sky/Spark engagements = one project "sky" (incl. ChainSecurity Sky LZ Deploy, which reviews
  the same lz-deploy commit as Cantina); Grove (Cantina grove-periphery + ChainSecurity Grove x2) = "grove"; Maple
  (Sherlock + Cantina) = "maple". prior_project_in_corpus=yes for Sky (MakerDAO Endgame), Maple, Optimism,
  Offchain/Arbitrum BoLD, Vana, Infrared, Dromos (Velodrome/Aerodrome), Securitize, Flare; no for the rest
  (Coinbase products differ from the Coinbase codebases in the corpus).

### (c) Extraction  `python -I work\rule2\scripts\fresh_extract.py`
- Corpus excerpt rule measured on findings_base.csv (n=5169): 4453 texts end with "\n[...excerpt ends]"; body
  length p5/p50/p95 = 7002/7030/7088 (7000 chars + rest of line); title starts at median 28 chars, i.e. the
  excerpt starts two lines above the title line. Fresh texts are built with the same rule so that both groups
  look alike (neighbouring-finding fragments included, as in the corpus).
- Per-firm heading parsers (Cyfrin, Cantina, ToB, Sherlock, Pashov, Zellic, QuillAudits, Nethermind,
  ChainSecurity). Detection equals the stated totals where reports state them (Cyfrin, Cantina, Dromos 33/33).
- Skipped and logged (fresh_extraction_log.csv): 19 pure documentation findings, 18 off-chain findings
  (deploy scripts .ts, Prysm .go, scripts).
- Result: 400 candidate findings, 28 projects, 9 firms -> work\rule2\fresh_findings.csv (FR-001..FR-400).

### (d) 10-row check  `python -I work\rule2\scripts\fresh_check10.py` (seed scvss-rule2-2026-fresh-check)
- FR-220, FR-025, FR-300, FR-032, FR-026, FR-202, FR-400, FR-272, FR-118, FR-326: all verbatim slices of the PDF
  text, title at the heading, severity matches the report, window rule holds (FR-118 ends at report end, no
  marker), audit_start matches the stated period. No error found.

### (e) `python -I rule2.py fresh`
```
fresh sample: 40 findings from 24 reports, 21 projects (11 with prior_project_in_corpus=yes); Cantina=12, Cyfrin=6, Nethermind=6, QuillAudits=5, ChainSecurity=3, Trail of Bits=3, Pashov=2, Zellic=2, Sherlock=1
```
- Independent check (`fresh_final.py`): 40 drawn, 0 duplicates, rows identical to fresh_findings.csv, max 2 per
  project, max 12 per firm, 0 starts before 2026-08-01, 6 start_from_report_date=yes all >= 2026-09-01.
- Severity as written: Informational/Info 24, Low 11, Medium 3, High 1, Gas 1. Note for the paper: the control
  group is lighter in severity than the corpus; this is a property of the eligible reports, not of the draw, and
  is reported as a limitation of the contamination check.
- Final table: work\rule2\fresh_reports_final.md.

## 2026-10-29  STEP 2  redaction and leak review

- First run `python -I rule2.py redact-audit`: 340 texts (40 fresh), 309 (90.9 %) without residual cue.
- Layer 1 pattern scan + over-redaction audit (`scripts/leak_scan.py`); layer 2 full reading of all 340 texts by four
  independent reviewer agents (85 each, 85/85 read in every chunk); layer 3 regression probe of 57 reviewer-quoted
  leak fragments (`scripts/leak_probe.py`).
- REDACTIONS in rule2.py revised in several rounds (all before freezing; protocol: "the only stage where the
  redaction rules may still change"). Full list of patterns and actions in work\rule2\leak_review.md. Main points:
  zero-width/bidi stripping; URL rule before firm rule; discussion removal limited to the next issue (repairs four
  texts that had lost the target finding); firm IDs and severity IDs -> "[ID]"; status, response, rating-prose,
  summary-count, TOC, boilerplate and date rules; OpenZeppelin, compiler versions, code lines, epoch 1970 and
  technical "escalated"/"resolved" kept.
- PROTOCOL §4 updated: redaction also removes firm-specific finding identifiers and dates; library names are kept.
- Final run: 339 of 340 (99.7 %) without residual cue (remaining flag FR-380 is a technical false positive); none of
  the 57 quoted leak fragments remains; median redacted length selection 6439 / control 6505.
- window_fix.py: tried to re-cut excerpts that lack the finding; titles in findings_base.csv are paraphrased and do
  not occur verbatim in the PDFs, so no excerpt could be re-cut reliably; no change made (empty window_fixes.csv
  deleted). Known data limitations listed in leak_review.md (F02179, F04885, F03039, F04073).

## 2026-10-29  Severity-stratified control draw (user request; diff shown, user: "apply")

- Combined diff of rule2.py and PROTOCOL_rule2.md since the last explicit review (file-history baselines
  rule2.py@v3 and PROTOCOL@v4, 07:58) shown to the user: work\rule2\review\combined_diff_since_review.diff.
- Applied: SEV_ORDER, severity_targets() (largest remainder on the selection distribution), stratified draw with
  nearest-stratum fill (most severe first; ties -> more severe), report lines; cosmetic comment fix (escalation);
  PROTOCOL §5 sentence (user wording) + fill-rule sentence.
- `python -I rule2.py fresh --force`:
```
fresh sample: 40 findings from 25 reports, 21 projects (14 with prior_project_in_corpus=yes); Cantina=11, Cyfrin=8, Nethermind=6, QuillAudits=4, Sherlock=3, Zellic=3, Pashov=2, ChainSecurity=2, Trail of Bits=1
severity target Critical=4, High=17, Medium=9, Low=9, Informational=1 | drawn Critical=1, High=9, Medium=13, Low=16, Informational=1
  stratum shortfall: Critical: 3 filled from High
  stratum shortfall: High: 11 filled from Medium
  stratum shortfall: Medium: 7 filled from Low
```
  Candidate pool: Critical 1, High 10 (6 projects), Medium 44, Low 116, Informational 229. fresh_final.py check:
  0 duplicates, rows identical to fresh_findings.csv, max 2 per project, max 11 per firm, eligibility rules hold.
- `redact-audit`: 340/340 without residual cue; redaction_audit.xlsx regenerated (0 flagged). Pattern scan of the 40
  new control texts: no severity label, status word, firm name or year (FR-229 "2000" is a number in code).
  Full read of the 40 new control texts by an independent reviewer: running.
- User requested a further sensitivity analysis (contamination check on Medium and Low findings only); diff shown,
  awaiting "apply".
- Full read of the 40 new control texts (independent reviewer, 40/40): unlabelled fix descriptions, "<Client>:"
  reply blocks, ratings in prose ("(Medium)", "low-to-moderate likelihood", "-to-High"), firm page furniture
  ("Back to Contents / Page x of y", "Smart Contract Security Assessment", "- SECURITY REVIEW", "| ©"), firm-named
  PoC folders (test/solace-pocs/), fix-commit URLs, URL tails. New rules (both groups): fix_desc, party_label
  (narrowed twice after the over-redaction audit showed technical labels such as "Is the same as writing:" being
  removed), sev_paren, page_furniture, poc_folder, commit_url, url_tail; sev_adj covers "x-to-y". "no longer" and
  "was removed" deliberately not used (common in genuine descriptions).
- Final `redact-audit`: 339/340 without residual cue (FR-380 false positive [corrected 2026-11-25: FR-380 was not in the redacted set after the redraw; flagged ID mis-recorded]); probes: 0 real leaks of 57 + 24 of 26
  control-review fragments gone (remaining: FR-379 "PUBLIC" header word). redaction_audit.xlsx regenerated.

### 2026-10-29 User over-redaction review: narrowing of six rules (diff shown, awaiting "apply")
- User request: narrow escalation, response_sentence, response_heading, summary_counts, rating_sentence2; check
  section_line; add ten technical test sentences as an over-redaction regression test; Medium/Low-only sensitivity
  analysis of the contamination check (PROTOCOL §10 + analyze).
- `scripts/overredaction_diag.py`: under the current rules all 10 test sentences are deleted (rules: escalation,
  response_sentence x5, response_heading, summary_counts x2, rating_sentence2).
- section_line: 342 firings in 113 texts (selection 314, control 28). 10 seeded-random firings
  (seed "scvss-rule2-section-line-check"): all section numbers. Full scan (`scripts/section_line_all.py`): 332 followed
  by a heading, 9 by a subsection number (5.3 -> 5.3.1), 1 a formula value (F00362 "0.50" between \times lines).
  Proposal: keep the rule but exclude numbers starting with 0 (section numbers start at 1), instead of dropping it.
- Dry run of the proposed rules in memory (`scripts/proposed_narrowing.py`, output proposed_narrowing.txt): the user's
  narrowing re-exposed leaks in 6 texts (F02388/89 "now fixed by developers", F03240 "Reserve states that this is
  done intentionally", F01377 "escalations have been accepted", F02723/25 "opted not to make changes ... in response
  to this finding", F02197/98 "All these were fixed", "issues that have not been fixed"); targeted patterns added.
  Final dry run: 10/10 test sentences unchanged, 21/21 reply/judging test lines still removed, 14 of 340 texts
  change, every re-exposed span read: all technical (F00562 methodology boilerplate, F02197/98 "They do" fragment).
  Residual-cue share unchanged (339/340); 57-fragment probe: 3 hits, the same known false positives.
- leak_probe.py: probe list moved to `scripts/leak_probe_list.py`; new section (0) over-redaction regression test.

- User: "apply". Applied the diff as shown to rule2.py (summary_counts, section_line, rating_sentence2,
  response_sentence, response_heading, escalation, sherlock_meta, stage_analyze Medium/Low variant) and PROTOCOL §10.
  rule2.py parses and imports (61 rules). Rerun held until the user has read the two-line summary they asked for.
- User: "rerun". `python -I rule2.py redact-audit`: 339/340 (99.7 %) without residual cue (FR-380 [corrected 2026-11-25: not in the redacted set after the redraw; flagged ID mis-recorded], known false
  positive); redaction_audit.xlsx regenerated. Texts changed versus the previous redacted.jsonl: 14 (F00362, F00562,
  F01506, F02197, F02198, F02557, F03659, F03944, F04102, F04103, FR-252, FR-261, FR-262, FR-340), identical to the
  dry run; all changes are re-kept technical text. leak_scan.py rerun. leak_probe.py: (0) 0 of 10 test sentences
  changed; (1) 3 hits, the known false positives (F00058, F02479, F01399; F05090 epoch kept by design); the 7
  round-one control fragments (FR-241, FR-001, FR-048, FR-014, FR-156, FR-357, FR-281) belong to findings no longer
  in the stratified control group; (2) unchanged.

### 2026-10-29 Control severity mix and primary contamination check
- Reported to user: selection (295 with severity) C 33 / H 125 / M 69 / L 63 / I 5 (+5 none); control C 1 / H 9 /
  M 13 / L 16 / I 1; targets C4 H17 M9 L9 I1; shortfalls C 3 (to High), H 11 (to Medium), M 7 (to Low).
- User decision: the Medium/Low-only comparison becomes the primary contamination check; all findings and
  without prior_project_in_corpus=yes (kept over all severities) are secondary. Diff shown; user: "apply".
  Applied: PROTOCOL §5 (user's sentence), §10 (reworded: severity used only to select M/L for the primary check;
  secondary analyses listed), §11 (user's sentence on ~26 vs 29 human-coded findings, weak evidence); rule2.py
  contam_variants reordered and relabelled (primary: Medium and Low findings only; secondary: all findings;
  secondary: without prior_project_in_corpus=yes). rule2.py imports; `status` runs.

### 2026-10-29 User visual check, round 1: nine leak types (diff shown, awaiting "apply")
- User reported leaks in F00172, F04321, F04526, F00568, F03977, F03039, F00402/F01801, F04993 and orphan
  punctuation lines. redaction_audit.xlsx had no entries filled (0/50); the user's findings came by message.
- Diagnostics: scripts/visual_round1_cases.py, visual_round1_probe2.py (outputs *.txt).
  F04321: the window (116 lines) is entirely a Sherlock judging discussion; its "Discussion" heading lies above the
  window, so sherlock_discussion (needs the heading) missed it; no finding body in the window.
  Orphan lines: texts with them, original selection 61/300 vs control 4/40; redacted 58-82/300 vs 12/40 (cue).
  Generic "severity word at line end" would hit prose (F01563, F05144, ...): restricted to ToB type categories.
  Generic firm IDs at line start: all hits are firm IDs (DRV4-, CVF-, CAR-, PEC-, BRAV-, ...); standards excluded.
- Dry run (scripts/proposed_round1.py, _attrib.py, outputs proposed_round1*.txt): first version over-removed
  (update_from continuation ran into next titles in F00864/F00865 because section_no had already removed the
  "6.14.2" stop line; response_sentence's 400-char tail ate the next title in F00952). Revised: update_block runs
  early; PR/commit rule separate and line-bounded. Final dry run: all 9 case tests removed, 10/10 regression
  sentences unchanged, 156 of 340 texts change (selection 138, control 18), every removed span read; residual
  share 339/340; probes 57+9: 3 hits (known false positives); orphan-line texts 0/0; F04321 becomes empty (0 chars).
- leak_probe_list.py: +9 fragments, ORPHAN pattern; leak_probe.py: checks (3) orphan lines by group, (4) short texts.

- User: "apply", with one change: "escalat\w*" removed from JUDGE (technical "privilege escalation"), plus a
  regression test (non-Sherlock text with "privilege escalation" twice must not be shortened).
  redaction_audit.xlsx archived as redaction_audit_round1.xlsx. Applied to rule2.py (constants SEVW, TOB_TYPES,
  JUDGE, NOT_ISSUE; rules sherlock_source, sherlock_discussion_lead, status_block, findings_summary, tob_type_sev,
  rating_change, update_block, firm_finding_id2, fix_commit, orphan_punct; team_response; [ID] mapping; stage_redact
  round 2 seed "-audit-round2" excluding round-1 texts, round-1 sheet carried over) and PROTOCOL §4. 71 rules; status ok.
- `redact-audit`: 339/340 without residual cue (FR-380 [corrected 2026-11-25: FR-380 was not in the redacted set after the stratified redraw; the flagged ID was mis-recorded]); 156 texts changed (selection 138, control 18), as in the dry
  run. leak_scan rerun ("found_by" 4 hits: prose "would have been found by any test" x2 per text in F02556/F02557, and
  a heading "Issues Found by" in F01274: not leaks). leak_probe: (0) 0 of 11 changed; (1) 3 of 66 present, the known
  false positives; (3) orphan lines selection 0, control 0; (4) texts < 200 chars: F04321 (0 chars).
- Workbook: round1_random_50 identical to the archived round-1 sheet (same 50 IDs); round 2: 50 new texts, no overlap
  with round 1 (6 control). Sheet name "round2_random_50_for_visual_check" has 33 characters (> Excel's 31):
  rename proposed to the user (diff shown).
- User: "apply". Sheet renamed to "round2_random_50_visual_check" (29 chars) in stage_redact; `redact-audit` rerun:
  redacted.jsonl byte-identical, 339/340 without residual cue; workbook sheets round2_random_50_visual_check (50),
  round1_random_50 (50, IDs identical to the archived round-1 sheet), residual_flags (1).

### 2026-10-29 Visual check round 2 (user) and freeze
- User: "I completed the round-2 visual check: no leaks found in any of the 50 texts (leak_found filled and saved).
  Record this in session_log.md, then freeze."
- Verified in redaction_audit.xlsx (saved 15:41:24), sheet round2_random_50_visual_check: 50 rows, leak_found "no"
  in 50/50, what_leaked empty in 50/50. Result reported per PROTOCOL §4: 0 of 50 texts with a leak (round 2; texts
  not used for tuning). Round 1 (50 texts, used to tune the rules) found nine leak types, fixed before round 2.
- Final redaction: 339/340 (99.7 %) without residual cue (F01578 [corrected 2026-11-25; was "FR-380 false positive"]: a neighbouring Sherlock finding's status line "Verified. Fixed in", a real residual). Known limitations (leak_review.md):
  F04321 empty after redaction (window = judging discussion), F02179 one character per line, ToB windows F04885,
  F03039, F04073 without the finding body, unlabelled fix prose may remain, gaps where rating words were removed.
- redaction_audit.xlsx must not be regenerated from now on (redact-audit would overwrite the user's entries).
- `python -I rule2.py freeze` at 2026-10-29T15:53:17 -> work\rule2\freeze.json. SHA-256: protocol da134ae7...bd3e,
  codebook bb3a5694...bcb, script e46446f8...daa; prompts v1 35e77a1c..., v2 66206609..., v3 82850819...;
  sample 48bcf20a..., redacted b3d00316..., fresh_sample 30b758a6.... From now on rule2.py, codebook_rule2.json and
  PROTOCOL_rule2.md are not edited. Next: STEP 4 pilot (10 findings), on the user's go-ahead.

### 2026-10-29 STEP 4 pilot (user: "go")
- `python -I rule2.py extract --rater R1 --limit 10` (log work\rule2\pilot_R1_run.log), 15:58:11-15:58:58, model
  claude-opus-5-5, variant 1. Findings (outside the human-coded set, chosen by the script): F01554, F03236, F02218,
  F04549, F04736, F03779, F03530, F02478, F03029, F04942. 10/10 parsed.
- `scripts/pilot_check.py` (output pilot_check.txt), independent re-check: 170 answers; JSON/letter problems 0;
  decoding mismatches 0; CD rate 36/170 = 21.2 % (by factor: F04 9, F15 6, F17 6, F02 3, F10 3, F03 2, F07 2,
  F05/F06/F08/F09/F11 1); quote options chosen 80, unverified 3 (3.8 %): F01554 F15 and F02218 F15 with an empty
  quote (correctly CD); F04736 F11 quote "if (_flashnum == 0) {" occurs verbatim but has 11 alphanumeric characters,
  below quote_ok's 12-character minimum, so it was turned into CD (a conservative false negative of the frozen rule).
  All other 77 quotes occur verbatim in the redacted text.
- Waiting for the user's "continue" (STEP 5).

### 2026-10-29 STEP 5 full extraction (user: "continue")
- `python -I rule2.py extract --rater R1` (log extract_R1_run.log): 330 to do, 10 done (pilot); usage limit reached
  8 times (script waited 15 min each and resumed); finished ~18:17. `status`: R1=340 parsed. 
- `scripts/rater_report.py R1` (aggregates only; rater_report.txt): 340/340 parsed, 0 failed records, model
  claude-opus-5-5. CD rate overall 24.4 %; per factor F01 7.6, F02 30.3, F03 35.6, F04 72.4, F05 20.9, F06 8.5,
  F07 18.8, F08 20.6, F09 15.6, F10 34.1, F11 12.4, F12 3.2, F13 0.3, F14 9.7, F15 57.1, F16 1.8, F17 66.8 %.
  Unverified quotes 139/5780 = 2.4 % (F15 16.8 %, F17 10.3 %, F11 4.1 %, F08 3.8 %, others <= 0.9 %).
  Unverified quotes by cause (aggregate): empty quote 128, not found in text 9, verbatim but < 12 alphanumeric
  characters 2. Empty quotes = a [quote] option chosen without a passage; turned into CD as the prompt rule requires.
- R1b started next.
- `python -I rule2.py extract --rater R1b` (log extract_R1b_run.log): 340 to do; usage limit reached 24 times; the
  last 4 calls (F00111, F04689, F00050, F01643) returned no parsable answer (limit). Rerun of the same command
  (extract_R1b_retry.log, 23:11): 4/4 parsed. `status`: R1=340, R1b=340.
- rater_report R1b: 340/340 parsed (4 failed records kept in the file, superseded), model claude-opus-5-5. CD overall
  24.6 %; per factor F01 7.4, F02 31.2, F03 34.1, F04 73.2, F05 21.8, F06 8.5, F07 19.4, F08 22.4, F09 15.0,
  F10 34.7, F11 12.1, F12 3.5, F13 0.9, F14 10.0, F15 54.4, F16 1.8, F17 67.4 %. Unverified quotes 126 = 2.2 %
  (F15 13.8, F17 9.7, F11 5.3, F08 4.7 %).
- R2 started next.
- `python -I rule2.py extract --rater R2` (extract_R2_run.log): claude-sonnet-5-5, variant 2; 340 to do; no usage
  limit; 1 unparsed (FR-005). Rerun (extract_R2_retry.log, 23:39): 1/1 parsed. `status`: R1=340, R1b=340, R2=340.
- rater_report R2: 340/340 parsed (1 failed record superseded). CD overall 23.2 %; per factor F01 7.4, F02 31.5,
  F03 32.4, F04 52.9, F05 22.1, F06 7.1, F07 26.8, F08 38.2, F09 15.6, F10 21.8, F11 7.4, F12 5.0, F13 2.6,
  F14 11.5, F15 63.8, F16 4.1, F17 43.8 %. Unverified quotes 224 = 3.9 % (F15 18.5, F08 16.2, F07 8.5, F17 7.4,
  F05 5.3, F04 4.1 %); by cause: empty quote 209, not found 11, verbatim but < 12 alphanumeric characters 4.
- R3 (open-weight model, local endpoint) is not part of the STEP 5 commands; not run. Next: STEP 6 probe.

### 2026-10-29/30 STEP 6 probe and STEP 7 human form
- `python -I rule2.py probe` (probe_run.log): 140 findings (100 selection, 40 control), 280 calls; no usage limit;
  280/280 parsed (100+100 selection A/B, 40+40 control A/B). Results not inspected (they appear in the analysis).
- `python -I rule2.py human-form` -> work\rule2\human_coding_form.xlsx: 100 findings (40 control, not marked), 15 firms.
- `scripts/human_form_check.py` (human_form_check.txt; does not open the key, the coding values or model answers):
  sheets coding/codebook/read_me; coding columns exactly code, title, text, F01-F17, comment; codes H001-H100;
  composition 60 selection (12 firms x 5, round robin) + 40 control; order: 49 group runs (49.0 expected under random
  order), 21 of 40 control in the first half; titles/texts equal the redacted ones (3 rows differ only by control
  characters removed for Excel); no "FR-nnn" id in any row; the word "fresh" occurs as ordinary prose in 9 texts of both
  groups (e.g. "stale prices can appear fresh"), not a marker; codebook sheet shows option codes and texts, CD, and
  whether evidence is needed. Stopped here (STEP 7); STEP 8 only after the user's coding is finished.

### Pending (user)
- Visual check of the 50 texts in work\rule2\redaction_audit.xlsx (sheet random_50_for_visual_check: fill
  leak_found / what_leaked), then "freeze".

### 2026-11-25 Correction: residual-scanner flag
- The frozen redacted.jsonl (sha256 b3d00316..., equal to freeze.json) flags one text with a residual cue: F01578
  (main sample; "Verified. Fixed in", the status line of a neighbouring Sherlock finding). Earlier entries named FR-380;
  FR-380 has not been in the redacted set since the severity-stratified redraw of the control group, so those mentions
  were mis-recorded. Corrected in place (marked "[corrected 2026-11-25]") in the final-state line; the entry before the
  redraw (line "Final run: 339 of 340 ... FR-380") is left as recorded. Handling: Amendment 01f item 3.
