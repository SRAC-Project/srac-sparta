"""Independent generic JSON join baseline over the SAME prepared pilot data."""
import json
from pathlib import Path
import re
import sys

root, query, output_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
with (root / 'prototype/data/cves.json').open(encoding='utf-8') as stream:
    mappings = json.load(stream)['cves']
component = next((x['component'] for x in mappings if x['cve'].casefold() == query.casefold()), query)
with (root / 'prototype/srac/srac-assertions.json').open(encoding='utf-8') as stream:
    assertions = json.load(stream)['assertions']
matches = [x for x in assertions if x['component'].casefold() == component.casefold()]
if not matches:
    print('No SRAC relationship found.')
    sys.exit(1)
blocks = ['SRAC DETERMINATION RETRIEVAL (SYNTHETIC PILOT)',
          f'Input: {query}\nResolved Component: {component}\nAssertions: {len(matches)}',
          'Retrieves prepared assertions and evidence IDs. Review flags are recorded\n'
          'fixture values, not computed vulnerability impact or risk determinations.']
for x in matches:
    status = 'REVIEW REQUIRED' if x.get('requiresReview') is True else (
        'NO REVIEW REQUIRED' if x.get('requiresReview') is False else 'UNDETERMINED')
    lines = [f"Component: {x['component']}", f"Mission Function: {x['missionFunctionId']}",
             f"Relationship: {x.get('relationshipType', 'UNSPECIFIED')}",
             f"Recorded Outcome: {x.get('missionAssuranceOutcome', 'UNSPECIFIED')}",
             f"Recorded Authority: {x['authority']}"]
    if 'safetyRelated' in x:
        lines.append(f"Safety Related: {x['safetyRelated'] if x['safetyRelated'] is not None else 'UNDETERMINED'}")
    lines.extend([f'Recorded Review Status: {status}', 'Evidence references:'])
    lines.extend(x['evidence'])
    blocks.append('\n'.join(lines))
output = '\n\n'.join(blocks) + '\n'
output_dir.mkdir(parents=True, exist_ok=True)
filename = re.sub(r'[^A-Za-z0-9._-]+', '_', matches[0]['component'])
report_path = output_dir / f'{filename}-impact.txt'
report_path.write_text(output, encoding='utf-8')
print(output)
print(f'Report saved to: {report_path}')
