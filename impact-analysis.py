import json
import sys
import os

if len(sys.argv) < 2:
    print("Usage: impact-analysis.py <component>")
    sys.exit(1)

component = " ".join(sys.argv[1:])

with open("prototype/srac/srac-assertions.json") as f:
    data = json.load(f)

found = False

# Create reports folder if missing
os.makedirs("prototype/reports", exist_ok=True)

for item in data["assertions"]:

    if item["component"].lower() == component.lower():

        found = True

        report = []

        report.append("========================================")
        report.append("SRAC IMPACT ANALYSIS")
        report.append("========================================")
        report.append("")
        report.append(f"Component: {item['component']}")
        report.append("")
        report.append(f"Mission Function: {item['missionFunctionId']}")
        report.append("")
        report.append(f"Authority: {item['authority']}")
        report.append("")
        report.append("Evidence:")

        for evidence in item["evidence"]:
            report.append(evidence)

        output = "\n".join(report)

        # Display
        print(output)

        # Save file
        filename = item["component"].replace(" ", "_")
        report_file = f"prototype/reports/{filename}-impact.txt"

        with open(report_file, "w") as f:
            f.write(output)

        print()
        print(f"Report saved to: {report_file}")

if not found:
    print("No SRAC relationship found.")