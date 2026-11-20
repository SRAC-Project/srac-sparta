"""Measure full fresh-process lookup/report time and verify every report."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(values):
    ordered = sorted(values)
    return {'n': len(values), 'min_s': min(values), 'median_s': statistics.median(values),
            'mean_s': statistics.mean(values),
            'p95_s': ordered[math.ceil(.95 * len(values)) - 1],
            'max_s': max(values), 'under_10_s': sum(v < 10 for v in values)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=HERE.parent)
    parser.add_argument('--out', type=Path, default=HERE / 'generated')
    parser.add_argument('--repeats', type=int, default=30)
    args = parser.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.repeats < 1:
        parser.error('--repeats must be positive')
    cve_file = repo / 'prototype/data/cves.json'
    assertion_file = repo / 'prototype/srac/srac-assertions.json'
    cves = json.loads(cve_file.read_text(encoding='utf-8'))['cves']
    assertions = json.loads(assertion_file.read_text(encoding='utf-8'))['assertions']
    cases = [('CVE-2026-1234', 'OpenSSL', ['AUTH-CMD-001', 'UPD-VER-002']),
             ('CVE-2026-5678', 'NASA CryptoLib', ['UPD-VER-002']),
             ('CVE-2026-9012', 'Telemetry Library', ['TLM-001'])]
    trials = []
    jobs = [(engine, i, query, component, functions)
            for i in range(args.repeats) for query, component, functions in cases
            for engine in ('prototype', 'generic_baseline')]
    random.Random(20261119).shuffle(jobs)
    for index, (engine, repeat, query, component, functions) in enumerate(jobs):
        output_dir = out / 'trial-reports' / f'{index:03d}-{engine}'
        if engine == 'prototype':
            command = [sys.executable, str(repo / 'impact-analysis.py'), query, '--output-dir', str(output_dir)]
        else:
            command = [sys.executable, str(HERE / 'benchmark_baseline.py'), str(repo), query, str(output_dir)]
        start = time.perf_counter_ns()
        run = subprocess.run(command, cwd=HERE, capture_output=True, text=True, encoding='utf-8', timeout=30)
        elapsed = (time.perf_counter_ns() - start) / 1e9
        assert run.returncode == 0, (command, run.stdout, run.stderr)
        files = list(output_dir.glob('*.txt'))
        assert len(files) == 1, files
        report = files[0].read_text(encoding='utf-8')
        assert report in run.stdout, 'Saved report differs from console report'
        found_functions = [line.removeprefix('Mission Function: ') for line in report.splitlines()
                           if line.startswith('Mission Function: ')]
        assert found_functions == functions, (found_functions, functions)
        expected = [x for x in assertions if x['component'] == component]
        blocks = [block for block in report.split('\n\n') if block.startswith('Component: ')]
        assert len(blocks) == len(expected)
        for block, record in zip(blocks, expected):
            for label, field in [('Component', 'component'), ('Mission Function', 'missionFunctionId'),
                                 ('Relationship', 'relationshipType'), ('Recorded Outcome', 'missionAssuranceOutcome'),
                                 ('Recorded Authority', 'authority'), ('Safety Related', 'safetyRelated')]:
                assert f'{label}: {record[field]}' in block, (label, block)
            assert block.split('Evidence references:\n')[1].strip().splitlines() == record['evidence']
            status = 'REVIEW REQUIRED' if record['requiresReview'] else 'NO REVIEW REQUIRED'
            assert f'Recorded Review Status: {status}' in block
        trials.append({'order': index, 'engine': engine, 'repeat': repeat, 'query': query,
                       'duration_s': elapsed, 'assertion_count': len(blocks),
                       'verified': True, 'report_sha256': digest(files[0])})
        if (index + 1) % 30 == 0:
            print(f'Completed and verified {index + 1}/{len(jobs)} trials', flush=True)
    # Match output bytes for every query across both independent implementations.
    for query, _, _ in cases:
        hashes = {t['report_sha256'] for t in trials if t['query'] == query}
        assert len(hashes) == 1, f'Output mismatch for {query}'
    result = {
        'completed_utc': datetime.now(timezone.utc).isoformat(),
        'platform': platform.platform(), 'processor': platform.processor(),
        'python': platform.python_version(), 'timer': 'perf_counter_ns',
        'method': 'Fresh Python process, JSON file reads, lookup, formatting, new output directory, report write, captured console output and process exit. Verification is outside timed interval.',
        'cache_policy': 'No warm-up trials excluded. OS file cache not cleared; fresh process is not a cold-cache test.',
        'dataset': {'cve_mappings': len(cves), 'assertions': len(assertions),
                    'components': len({x['component'] for x in assertions}),
                    'cve_bytes': cve_file.stat().st_size, 'assertion_bytes': assertion_file.stat().st_size},
        'source_sha256': {str(p.relative_to(repo)): digest(p) for p in [repo/'impact-analysis.py', cve_file, assertion_file]},
        'repeats_per_case_per_engine': args.repeats, 'all_outputs_verified': True,
        'summaries': {engine: summary([t['duration_s'] for t in trials if t['engine'] == engine])
                      for engine in ['prototype', 'generic_baseline']},
        'by_case': {engine: {query: summary([t['duration_s'] for t in trials if t['engine'] == engine and t['query'] == query])
                             for query, _, _ in cases} for engine in ['prototype', 'generic_baseline']},
        'limits': ['Synthetic prepared dataset only; no engineering evidence fetched or validated.',
                   'No human/manual timing measured; 40-minute claim and end-to-end savings remain unverified.',
                   'Generic baseline reads the same SRAC-shaped fixture data; this tests scripting overhead, not existing engineering tools or interoperability.',
                   'Preparation, maintenance, integration, assessment and approval costs excluded.',
                   'Single machine and serial execution; no scale, concurrency or cold-cache conclusion.'],
        'trials': trials,
    }
    (out/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({key: result[key] for key in ['dataset', 'summaries', 'all_outputs_verified', 'limits']}, indent=2))


if __name__ == '__main__':
    main()
