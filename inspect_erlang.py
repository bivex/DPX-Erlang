from pattern_detector.bootstrap.container import create_container
from pattern_detector.ports.inbound import ScanOptions

container = create_container()
scanner = container.get_scanner()

print("--- Inspecting Poolboy Findings ---")
report_pb = scanner.scan_path("/Volumes/External/Code/DPX-Erlang/benchmarks/poolboy", options=ScanOptions())
for d in report_pb.detections:
    print(f"[{d.pattern_type.value.upper()}] {d.target_name} ({d.target_kind}, {d.confidence.percentage_str}) at {d.primary_location}")
    for ev in d.evidences:
        print(f"   -> {ev.rule_code}: {ev.description}")

print("\n--- Inspecting Cowboy Top Findings ---")
report_cb = scanner.scan_path("/Volumes/External/Code/DPX-Erlang/benchmarks/cowboy", options=ScanOptions())
for d in report_cb.detections[:10]:
    print(f"[{d.pattern_type.value.upper()}] {d.target_name} ({d.target_kind}, {d.confidence.percentage_str}) at {d.primary_location}")
    for ev in d.evidences:
        print(f"   -> {ev.rule_code}: {ev.description}")
