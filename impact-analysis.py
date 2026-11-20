"""Retrieve existing synthetic determinations; do not assess mission or cyber risk."""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent


def load_json(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def find_assertions(search_value, root=ROOT):
    """Resolve a fixture CVE and retain every matching component use."""
    component = search_value
    cve_path = root / "prototype/data/cves.json"
    if cve_path.exists():
        for entry in load_json(cve_path)["cves"]:
            if entry["cve"].casefold() == search_value.casefold():
                component = entry["component"]
                break
    assertions = load_json(root / "prototype/srac/srac-assertions.json")["assertions"]
    return component, [item for item in assertions
                       if item["component"].casefold() == component.casefold()]


def format_assertion(item):
    lines = [
        f"Component: {item['component']}",
        f"Mission Function: {item['missionFunctionId']}",
        f"Relationship: {item.get('relationshipType', 'UNSPECIFIED')}",
        f"Recorded Outcome: {item.get('missionAssuranceOutcome', 'UNSPECIFIED')}",
        f"Recorded Authority: {item['authority']}",
    ]
    if "safetyRelated" in item:
        safety = item["safetyRelated"]
        lines.append(f"Safety Related: {safety if safety is not None else 'UNDETERMINED'}")
    review = item.get("requiresReview")
    status = "REVIEW REQUIRED" if review is True else (
        "NO REVIEW REQUIRED" if review is False else "UNDETERMINED")
    lines.extend([f"Recorded Review Status: {status}", "Evidence references:"])
    lines.extend(item["evidence"])
    return "\n".join(lines)


def analyze(search_value, root=ROOT, output_dir=None):
    component, matches = find_assertions(search_value, root)
    if not matches:
        return None, "No SRAC relationship found."
    blocks = [
        "SRAC DETERMINATION RETRIEVAL (SYNTHETIC PILOT)",
        f"Input: {search_value}\nResolved Component: {component}\nAssertions: {len(matches)}",
        "Retrieves prepared assertions and evidence IDs. Review flags are recorded\n"
        "fixture values, not computed vulnerability impact or risk determinations.",
    ]
    blocks.extend(format_assertion(item) for item in matches)
    output = "\n\n".join(blocks) + "\n"
    directory = Path(output_dir) if output_dir is not None else root / "prototype/reports"
    directory.mkdir(parents=True, exist_ok=True)
    filename = re.sub(r"[^A-Za-z0-9._-]+", "_", matches[0]["component"])
    report_path = directory / f"{filename}-impact.txt"
    # One write per component retains every assertion in the saved report.
    report_path.write_text(output, encoding="utf-8")
    return report_path, output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("component_or_cve", nargs="+")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)
    try:
        path, output = analyze(" ".join(args.component_or_cve), output_dir=args.output_dir)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Cannot retrieve SRAC data: {error}", file=sys.stderr)
        return 2
    print(output)
    if path is None:
        return 1
    print(f"Report saved to: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
