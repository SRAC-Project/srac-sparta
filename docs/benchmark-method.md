# Retrieval benchmark method and limitations

## Supported result

Across 90 timed trials on a synthetic dataset containing three components and four assertions, the prototype retrieved existing determinations and evidence IDs and saved complete reports in a median 0.214 seconds, with a maximum of 0.355 seconds. All 90 reports passed completeness checks, including preservation of both OpenSSL function assertions.

Single-machine test with prepared metadata. Includes process startup, data reads and report generation. Data preparation, engineering assessment and approval are excluded. Savings against a human manual-review process have not been established.

## Method

Measured on November 19, 2026 (America/Los_Angeles), completing at
2026-11-20T04:37:57.843531+00:00 UTC-offset timestamp. The recorded environment was
Windows 11, Python 3.12.14, Intel64 Family 6 Model 186 Stepping 3, GenuineIntel.

The dataset contained three synthetic CVE mappings, three components and four
assertions. The two input JSON files occupied 252 and
1377 bytes. These identifiers and applicability
associations are fixtures, not real vulnerability findings.

Thirty runs of each of three queries were executed for each implementation,
giving 90 prototype and 90 generic-baseline trials. Order was randomized with a
fixed seed, serially on one machine. Each run used a fresh Python process and a
new report directory. No warm-up runs were excluded. The OS file cache was not
cleared; fresh-process timings are not cold-cache measurements.

The timer included process creation, JSON reads, lookup, formatting, directory
creation, the report write, captured console output and process exit. Report
verification was outside the timed interval. File close follows normal Python
behavior without an explicit durable-storage flush.

All reports were verified for the expected functions, relationships, recorded
outcomes, authority labels, safety attributes, review flags and exact evidence
IDs. Console and saved reports agreed. Both OpenSSL uses were retained.
For each query, complete report contents were byte-identical across the two
implementations and all repetitions.

## Results in seconds

| Implementation | Trials | Median | Mean | P95 | Maximum |
| --- | ---: | ---: | ---: | ---: | ---: |
| Corrected prototype | 90 | 0.214 | 0.220 | 0.279 | 0.355 |
| Generic JSON join | 90 | 0.168 | 0.173 | 0.201 | 0.278 |

The baseline consumes the same already-prepared SRAC-shaped data and performs
the same lookup/report task. It is an automation control, not a comparison with
existing mission engineering tools. It was faster in this observation, so no
SRAC-specific speed advantage is claimed.

## Reproduce and audit

    python benchmarks/benchmark_efficiency.py --repo . --out benchmarks/generated --repeats 30

The reference [raw results](../benchmarks/results/2026-11-19-lookup.json) contain
all 180 measurements, tested source/input SHA-256 hashes and environment details.
The harness and independent baseline are in benchmarks/. The corrected
impact-analysis.py and input fixtures match the recorded hashes. Harness path
defaults were adjusted for this repository layout without changing its timing
or validation logic.

## Scope boundaries

No underlying engineering evidence is fetched or validated. No risk or review
decision is computed. The test excludes data preparation, metadata maintenance,
engineering-tool integration, engineering assessment and approval. It is a
single-machine, small synthetic dataset observation conducted by the assistant,
not an independent operational evaluation, a scalability study or a guarantee.

The supplementary AI-assisted file review involved known fixtures, tool/model
latency and additional catalog checks. It is not equivalent to a human manual
workflow. Neither that observation nor this benchmark establishes human effort
savings. Earlier estimated manual-versus-lookup comparisons are withdrawn as
performance evidence.

Before asserting savings, conduct a practitioner trial with representative
source artifacts, matched task scope and output correctness criteria. Include
the cost of preparing and maintaining the exchanged information.
