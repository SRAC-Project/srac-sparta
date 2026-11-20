# Measured retrieval performance

Across 90 timed trials on a synthetic dataset containing three components and four assertions, the prototype retrieved existing determinations and evidence IDs and saved complete reports in a median 0.214 seconds, with a maximum of 0.355 seconds. All 90 reports passed completeness checks, including preservation of both OpenSSL function assertions.

Single-machine test with prepared metadata. Includes process startup, data reads and report generation. Data preparation, engineering assessment and approval are excluded. Savings against a human manual-review process have not been established.

| Measurement | Seconds |
| --- | ---: |
| Prototype median, 90 trials | 0.214 |
| Prototype P95 | 0.279 |
| Prototype maximum | 0.355 |
| Generic JSON-join median, 90 trials | 0.168 |

The generic baseline produced identical report contents and was faster in this
test. No SRAC-specific speed advantage or quantified manual-review saving is
claimed. Prior manual-effort estimates are not used as performance evidence.

See [method and limitations](../../docs/benchmark-method.md),
[raw trial records](../../benchmarks/results/2026-11-19-lookup.json), and
[reproduction instructions](../../README.md#measured-retrieval-performance).
