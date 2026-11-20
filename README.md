# SRAC reference pilot

SRAC (Safety Relevance Assertion Capability) is a proposed machine-readable
exchange format for existing mission assurance determinations. This independent,
synthetic pilot is not an adopted or recognized standard.

The mission assurance positioning, with safety as a subclass, is the model's
framing. SRAC communicates existing determinations. The receiving organization's
authorized engineering process makes assessments and classification decisions.

SPARTA CM0022 Criticality Analysis provides a representative context. No
affiliation with, endorsement by, or extension of SPARTA or NASA is implied.

## Implemented demonstration

The lookup follows CVE -> component name -> mission function -> recorded
determination, authority label and evidence references. It retains all matching
per-use assertions in the console and one complete text report per component.
Data and CVE-to-component associations are synthetic fixtures, including all
CVE-2026-* examples. They are not real vulnerability applicability statements.

The prototype does not determine vulnerability impact, calculate cybersecurity
risk, verify authority, or determine whether a review is actually needed.
requiresReview is a prepared fixture value. It prints evidence IDs without
fetching or validating the underlying assurance artifacts.

## Proposed capabilities and examples

Version/digest/pURL matching, architecture graph traversal, revision/staleness
checks, lifecycle management, signatures and distribution enforcement remain
proposed model capabilities, not implemented features of this lookup.

prototype/data/supplier-srac.json is an illustrative supplier assertion only.
Supplier exchange/import, validation and reconciliation are not implemented.
The small prototype/sbom/spdx.json file is an illustrative SBOM excerpt, not
a complete validated SPDX document, and the lookup does not ingest it.

## Run

Requires Python 3.9 or later; no third-party Python packages are needed.

    python impact-analysis.py CVE-2026-1234
    python impact-analysis.py "NASA CryptoLib"
    python -m unittest discover -s tests -v

On Windows, prototype.bat cve CVE-2026-1234,
prototype.bat impact "NASA CryptoLib", and prototype.bat test also work.
The launcher uses SRAC_PYTHON if set, then py -3, then python.
Data paths resolve relative to the script. Use --output-dir PATH to redirect
reports. A later query for the same component replaces that component's report
with a complete current snapshot. Reports are not an audit history.

## Slide 13 data

| Component | Function | Relationship | Outcome | Recorded review |
| --- | --- | --- | --- | --- |
| OpenSSL | AUTH-CMD-001 | PROTECTS | RELEVANT | Required |
| OpenSSL | UPD-VER-002 | SUPPORTS | RELEVANT | Required |
| NASA CryptoLib | UPD-VER-002 | PROTECTS | RELEVANT | Not required |

These rows match the corrected slide. The separate Telemetry Library assertion
uses TLM-001; there is no OpenSSL telemetry-formatting assertion in this pilot.

## Measured retrieval performance

Across 90 timed trials on a synthetic dataset containing three components and four assertions, the prototype retrieved existing determinations and evidence IDs and saved complete reports in a median 0.214 seconds, with a maximum of 0.355 seconds. All 90 reports passed completeness checks, including preservation of both OpenSSL function assertions.

Single-machine test with prepared metadata. Includes process startup, data reads and report generation. Data preparation, engineering assessment and approval are excluded. Savings against a human manual-review process have not been established.

The same 90-query workload also ran against a generic JSON-join script, which
produced byte-identical reports with a median 0.168 seconds. This is not
evidence of an SRAC-specific speed advantage. The measurement establishes
retrieval latency and report completeness for these prepared fixtures.

- [Benchmark method and limitations](docs/benchmark-method.md)
- [Recorded measurements and all 180 trial records](benchmarks/results/2026-11-19-lookup.json)
- [Timing report](prototype/reports/time-savings.md)

To reproduce the benchmark with Python 3.9 or later:

    python benchmarks/benchmark_efficiency.py --repo . --out benchmarks/generated --repeats 30

Fresh measurements are written to benchmarks/generated/results.json and do not
replace the published reference measurements. Performance on another machine
may differ.

## Remaining operational validation

The pilot has not demonstrated an IMPLEMENTS example, differing per-use
criticality classifications, version/configuration applicability evaluation,
verified supplier exchange, or interoperability with engineering tools.
A practitioner trial must compare equivalent tasks using existing artifacts
and include metadata preparation and maintenance effort before claiming savings.

The recorded [AI-assisted file review](benchmarks/observations/ai-assisted-review.json)
is a single familiar-case observation with additional catalog checks and
tool/model latency. Its 42 seconds is not a human manual-review baseline and
must not be converted into a speedup or savings percentage.
