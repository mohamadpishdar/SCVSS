Amendment 01 to the Rule 2 protocol (registered 2026-11-25, before any Rule 2 or contamination result was viewed)

Reason. A description of the frozen sample (rule2_sample_description.csv) shows that 15 of the 40 control findings come from firms absent from the main sample (Cantina 11, ChainSecurity 2, Pashov 2), and that control has fewer Critical/High findings (25% vs 53%). A difference between groups could therefore reflect firm writing style rather than model memorisation, and the planned Medium/Low contamination test would rest on about 29 control findings.

Change. We add a second control set (control-B) of about 40 findings:
- reports published after 31 August 2026, EVM only;
- only firms present in the main sample, in proportions close to their share of the main sample, as far as fresh reports exist;
- auditor severity Medium or Low only;
- at most 2 findings per report and per project; no overlap with existing samples;
- random selection with the fixed seed scvss-rule2-controlB-2026-11-25 (2733501808478523922935011633241447754127193775684228779019966117999090571823028287594534833610193162256508450852770496898942976670903287567690373519837244809413400407858066155725103169052884211762522462558162132330583636373966646, derived as int.from_bytes(s + SHA-512(s), "big") with s the UTF-8 bytes of the seed string, which is the integer Python's random.Random(seed) uses for a string seed (version 2), as for the existing seeds in rule2.py).
Control-B is redacted with the frozen redaction pipeline and coded by the frozen R1, R1b and R2 configurations. Prompts, codebook and decision rules are unchanged. The human coding form is unchanged.

Analysis. The primary contamination test compares main vs (original control + control-B) on Medium/Low findings from firms present in both groups, with firm as a covariate. The original 40-finding comparison is reported as secondary.

Status. No answer file, probe result or group comparison had been opened when this amendment was written.

Note on firm labels. Five main-sample reports labelled "Unidentified" were attributed from their title pages (work/rule2/firm_attribution_fix.csv): four to Trail of Bits and one (Octolend) to QuillAudits. The sample is unchanged. With the corrected labels, QuillAudits holds 46 of 300 main findings (15.3%), one above the 15% cap that was applied to the original labels; we report this as a known deviation and do not redraw the sample.
