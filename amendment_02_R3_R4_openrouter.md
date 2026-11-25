Amendment 02: raters R3 and R4 via OpenRouter, decided 2026-11-25 before any R3 or R4 call and before any Rule 2 or contamination result was viewed

1. Platform. Protocol section 6 and README_R3_open_model.md plan R3 as an open-weight model served locally with vLLM on VSC. This is replaced by the OpenRouter chat-completions API (https://openrouter.ai/api/v1/chat/completions). The model identity, the pinned provider and the provider's weight precision are recorded and reported.

2. Models and providers. Fallbacks are disabled: a call that the pinned provider cannot serve fails and is retried later; it is never routed to another provider or model.

| Rater | OpenRouter model ID | Model | Pinned provider (OpenRouter slug) | Precision listed by OpenRouter |
|---|---|---|---|---|
| R3 | qwen/qwen3-235b-a22b-2507 | Qwen3-235B-A22B-Instruct-2507 (Alibaba Qwen) | Parasail (`parasail`) | fp8 |
| R4 | deepseek/deepseek-chat-v3-0324 | DeepSeek-V3-0324 (DeepSeek) | SiliconFlow (`siliconflow`) | fp8 |

   Routing object sent with every request: `"provider": {"order": [<slug>], "allow_fallbacks": false, "require_parameters": true, "data_collection": "deny"}`. With `data_collection: "deny"`, OpenRouter refuses a provider that may train on or retain prompts. A request refused for this reason counts as a failed call and is not re-routed.
   Precision. On 2026-11-25 OpenRouter listed no full-precision (bf16) endpoint for either model.
   - R3: all listed providers serve fp8 (DeepInfra, Parasail, Venice).
   - R4: SiliconFlow serves fp8 and Featherless fp4.
   - DeepSeek-V3-0324 is released by DeepSeek with fp8 weights, so fp8 is its native precision. Qwen3-235B-A22B-Instruct-2507 is released in bf16 with an official fp8 version from Qwen; R3 therefore runs on quantised weights, and this is reported.
   Choice of provider:
   - R3 Parasail: fp8, supports `seed`, 1-day uptime 100 % on 2026-11-25, a single service tier. DeepInfra lists three service tiers of the same model; Venice does not support `seed`.
   - R4 SiliconFlow: native fp8. The only alternative, Featherless, serves fp4.
   The provider listing saved on 2026-11-25 (endpoints and providers JSON) is registered with this amendment.

3. Call settings, as in rule2.py's R3 backend (call_openai):
   - `temperature` 0, `max_tokens` 6000.
   - Messages: system = rule2.SYSTEM_PROMPT, user = rule2.render_user(codebook, variant, title, text). The prompts are the frozen ones (prompt hashes in freeze.json).
   - The answer is the first `{...}` block of the response, decoded with rule2.decode; quotes are verified as for R1 and R2.
   - Timeout 900 s per attempt, up to 4 attempts per call, then a failed record. One rerun of the same command retries the failed findings only (as for R1b and R2). Item 11 says how a call that still fails is handled.
   - 2 workers. Finding order is a seeded shuffle with SEED + "-order-" + rater over all 363 texts.
   - Seed:
     - R3 sends `seed` 20261125 (Parasail supports it).
     - SiliconFlow does not support `seed`, so R4 sends none. With `require_parameters: true`, a provider that ignores a sent parameter is not used.
   - No other sampling parameter is sent; provider defaults apply and are reported as such.
   Because rule2.call_openai sends no authorisation header, no provider routing and no seed, the calls are made by a new script, scripts/openrouter_raters.py, which imports the frozen rule2.py (render_user, decode, SYSTEM_PROMPT, codebook, check_freeze) and changes nothing in it.
   API key handling:
   - The script reads the key at runtime from C:\Workdir\Develop\secrets\openrouter_key.txt and strips whitespace.
   - The key is never written to any log, output or error message.
   What each record stores:
   - finding_id, rater, the requested and returned model, the provider named in the response, the OpenRouter generation id, token usage, seed, variant, replicate, parsed, answers, flags, raw and time.

4. Prompt variant.
   - R3 uses variant 3, as specified for R3 in protocol section 6.
   - R4 also uses variant 3. Only variants 1-3 are frozen (freeze.json), so a new variant would be an unfrozen prompt. Variant 3 keeps R3 and R4, the two open-weight raters, comparable to each other. R3 and R4 then differ only by model and provider, while R1 (variant 1) and R2 (variant 2) differ from them in both model and option layout, as R3 already did in the original design.

5. Scope. All 363 texts:
   - the 300 main-sample texts and 40 original-control texts of the frozen redacted.jsonl;
   - the 23 control-B texts of controlB_redacted_v2.jsonl (amendments.json entry 15).
   Texts excluded from analyses by Amendment 01f (CB-222, F04321, and F04885, F03039 and F04073 in the primary analyses) are still coded, as for R1, R1b and R2. There is no pilot; item 10 describes a technical smoke test.

6. Output files. R3 and R4 answers are written to work/rule2/answers_R3_openrouter.jsonl and work/rule2/answers_R4_openrouter.jsonl, not to answers_rule2.jsonl. This step of README_R3_open_model.md is replaced: its step 4 appends R3 lines to answers_rule2.jsonl, where the frozen 'analyze' would read them. The SHA-256 of each answer file and run log is registered in amendments.json after the runs, before any content is opened.

7. Role in the analysis. The Rule 2 decision rules (protocol sections 4-5; thresholds ALPHA_MIN, CD_MAX, MODAL_MAX, V_MERGE, MIN_NEFF) are unchanged.
   - R3 is the third primary rater, as planned in protocol section 6, with prompt variant 3. For the primary analysis, the R3 answers in answers_R3_openrouter.jsonl are read exactly as if they were appended to answers_rule2.jsonl. The primary analysis therefore uses R1, R2 and R3 (R1b for test-retest only), and the label "provisional" is dropped.
   - R4 is an additional robustness rater that is not in the frozen protocol. It never enters the Rule 2 decision rules and is reported separately.

8. Timing. This amendment, the provider listing and scripts/openrouter_raters.py are registered (SHA-256 in amendments.json and an external commit) before any R3 or R4 call and before any Rule 2 or contamination result was viewed.

9. Expected cost (OpenRouter list prices of 2026-11-25; 363 texts per rater).
   - Input: about 4.82 million characters of prompt, about 1.2-1.4 million tokens per rater.
   - Output: an assumed 1,000-3,000 tokens per call; at most 6,000 (max_tokens).

| Rater | Input $/M | Output $/M | Estimate | Upper bound (6,000 output tokens per call) |
|---|---|---|---|---|
| R3 (Parasail) | 0.14 | 0.80 | about USD 0.50-1.10 | about USD 1.95 |
| R4 (SiliconFlow) | 0.25 | 1.00 | about USD 0.65-1.45 | about USD 2.55 |

   Retries of failed calls and OpenRouter's credit-purchase fee come on top; a budget of USD 10 covers both raters.

10. Technical smoke test. Before the full run, each rater (R3, R4) codes 3 texts.
   - The texts are the first 3 of that rater's seeded order (item 3) that are not in the human coding form (rule2.human_pick).
   - Only these are reported: call status, parse success, provider, and prompt and completion token counts. Answer content is never reported.
   - If all 3 texts parse for both raters, the full run proceeds and these 3 records count as final records (they are not re-run).
   - Otherwise the run stops and the failure is reported before anything is changed.

11. Failed calls. A finding whose call still fails after the retry limit (4 attempts per call and one rerun, item 3) is reported as missing for that rater. No substitute provider or model is used.
