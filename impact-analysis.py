import json
import sys
import os

if len(sys.argv) < 2:
    print("Usage: impact-analysis.py <component_or_cve>")
    sys.exit(1)

search_value = " ".join(sys.argv[1:])
component = search_value

#
# Resolve CVE -> Component
#

try:
    with open("prototype/data/cves.json", "r") as f:
        cve_data = json.load(f)

    for cve in cve_data["cves"]:

        if cve["cve"].lower() == search_value.lower():

            print(f"Resolved {search_value} -> {cve['component']}")
            print()

            component = cve["component"]
            break

except FileNotFoundError:
    pass

#
# Load SRAC Assertions
#

with open("prototype/srac/srac-assertions.json", "r") as f:
    data = json.load(f)

#
# Ensure Reports Folder Exists
#

os.makedirs("prototype/reports", exist_ok=True)

found = False

for item in data["assertions"]:

    if item["component"].lower() == component.lower():

        found = True

        report = []

        report.append("========================================")
        report.append("SRAC IMPACT ANALYSIS")
        report.append("========================================")
        report.append("")

        report.append(f"Input: {search_value}")
        report.append(f"Component: {item['component']}")
        report.append("")

        report.append(f"Mission Function: {item['missionFunctionId']}")
        report.append(f"Authority: {item['authority']}")
        report.append("")

        if "safetyRelated" in item:
            report.append(f"Safety Related: {item['safetyRelated']}")

        if "requiresReview" in item:

            if item["requiresReview"]:
                report.append("Review Status: REVIEW REQUIRED")
            else:
                report.append("Review Status: NO REVIEW REQUIRED")

        report.append("")
        report.append("Evidence:")

        for evidence in item["evidence"]:
            report.append(evidence)

        output = "\n".join(report)

        #
        # Display
        #

        print(output)

        #
        # Save Report
        #

        filename = item["component"].replace(" ", "_")

        report_file = (
            f"prototype/reports/{filename}-impact.txt"
        )

        with open(report_file, "w") as f:
            f.write(output)

        print()
        print(f"Report saved to: {report_file}")
        print()

if not found:

    print("No SRAC relationship found.")