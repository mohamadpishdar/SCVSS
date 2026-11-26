Amendment 02a: handling of missing answers of raters R3 and R4, decided 2026-11-26

This amendment was written after the R3 and R4 runs of Amendment 02 and after their answer files and run log were hashed (amendments.json entry 31). It was written before any answer content, parsed value or analysis output had been opened, printed or summarised. Only call metadata (call status, provider, model, token usage and error message) was read.

1. Primary handling. Item 11 of Amendment 02 is unchanged. A finding with no fully parsed answer after the retry limit (four attempts per call and one rerun) is treated as missing for that rater in all primary analyses.

2. Reporting of missing answers. Missing rates are reported per rater (R1, R1b, R2, R3, R4) and per group (main sample, original control, control-B). The identifiers of the missing findings are listed in a supplement. The counts observed from the call metadata are:

| Rater | Missing | Main sample | Original control | Control-B |
|---|---|---|---|---|
| R3 | 10/363 | 9 | 1 | 0 |
| R4 | 29/363 | 20 | 7 | 2 |

3. Sensitivity analysis A (partial answers). For records in which the output was received but at least one factor could not be decoded, the decodable factors are retained and only the undecodable factors are treated as missing. Records whose output could not be read as a single answer remain missing. Rule 2 and the contamination test are repeated on this basis for R3 and R4.

4. Sensitivity analysis B (complete cases). Rule 2 agreement and the contamination test are repeated on the findings that have a parsed answer from each of R1, R2, R3 and R4.

5. Missingness by group. For each rater, the proportion of missing answers in the main sample is compared with that in the original control and control-B combined, using Fisher's exact test, and the results are reported. No imputation is performed.

6. Status of the results. The primary results remain as defined in the protocol and in Amendment 02. The sensitivity results are reported alongside the primary results and do not replace them.
