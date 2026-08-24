from pattern_detector.bootstrap.container import create_container
from pattern_detector.ports.inbound import ScanOptions

def test_scanning_service_memory():
    container = create_container()
    scanner = container.get_scanner()

    sources = {
        "chat_sup.erl": """
        -module(chat_sup).
        -behaviour(supervisor).
        -export([start_link/0, init/1]).
        start_link() -> supervisor:start_link(?MODULE, []).
        init([]) -> {ok, {#{strategy => one_for_all, intensity => 3, period => 5}, []}}.
        """
    }

    report = scanner.scan_sources(sources, options=ScanOptions())
    assert report.scanned_files_count == 1
    assert report.total_detections_count >= 1
    assert "otp_behaviour" in report.summary_by_category
