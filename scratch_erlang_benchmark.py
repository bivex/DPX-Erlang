import time
import os
import sys
from pathlib import Path
from pattern_detector.bootstrap.container import create_container
from pattern_detector.ports.inbound import ScanOptions

container = create_container()
scanner = container.get_scanner()

bench_dir = Path("/Volumes/External/Code/DPX-Erlang/benchmarks")
repos = [d for d in bench_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

print(f"=========================================================================================")
print(f"🔴 DPX-ERLANG BENCHMARK: SCANNING {len(repos)} REAL-WORLD ERLANG CODEBASES")
print(f"=========================================================================================")

total_files = 0
total_dets = 0
start_all = time.perf_counter()

for repo in sorted(repos, key=lambda x: x.name):
    t0 = time.perf_counter()
    try:
        options = ScanOptions(verbose=False)
        report = scanner.scan_path(str(repo), options=options)
        elapsed = time.perf_counter() - t0
        total_files += report.scanned_files_count
        total_dets += report.total_detections_count
        cats = report.summary_by_category
        print(f"📦 {repo.name:<16} | {report.scanned_files_count:>5} files | {report.total_detections_count:>5} detections | {elapsed:>6.3f}s | "
              f"OTP: {cats.get('otp_behaviour', 0):>3}, Con: {cats.get('actor_concurrency', 0):>3}, Str: {cats.get('structural', 0):>3}, "
              f"Beh: {cats.get('behavioral', 0):>3}, Smells: {cats.get('principle', 0) + cats.get('safety', 0) + cats.get('resilience', 0):>3}")
    except Exception as e:
        print(f"❌ {repo.name:<16} | CRASH! {e}")
        import traceback
        traceback.print_exc()

total_elapsed = time.perf_counter() - start_all
print(f"=========================================================================================")
print(f"📊 SUMMARY: {total_files} Erlang files scanned across {len(repos)} projects in {total_elapsed:.3f}s")
print(f"🎯 Total Architectural Findings Detected: {total_dets}")
print(f"⚡ Average Throughput: {total_files / total_elapsed:.1f} files/sec ({total_dets / total_elapsed:.1f} detections/sec)")
print(f"=========================================================================================")
