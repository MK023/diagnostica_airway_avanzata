# tests/test_ping.py - Test coverage per network/ping.py (ping3, pingparsing, scapy)
import pytest
from network.ping import run_ping_diag

class DummyLogger:
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg, exc_info=False): pass

@pytest.mark.parametrize("address,expected", [
    ("8.8.8.8", True),
    ("invalid_address", False)
])
def test_run_ping_diag_basic(monkeypatch, address, expected):
    # Mock ping3_ping
    monkeypatch.setattr("network.ping.ping3_ping", lambda addr, unit: 42 if addr == "8.8.8.8" else None)
    # Mock pingparsing
    class DummyPingParsing:
        def parse(self, _): return DummyStats()
    class DummyStats:
        def as_dict(self): return {"min_rtt": 1, "avg_rtt": 2, "max_rtt": 3, "packet_loss_rate": 0}
    class DummyTransmitter:
        def __init__(self): self.destination = ""; self.count = 0
        def ping(self): return ""
    monkeypatch.setattr("network.ping.pingparsing", type("Dummy", (), {
        "PingParsing": DummyPingParsing,
        "PingTransmitter": DummyTransmitter
    }))
    # Mock scapy
    monkeypatch.setattr("network.ping.sr1", lambda pkt, timeout, verbose: type("Dummy", (), {"time": 2, "sent_time": 1})())
    monkeypatch.setattr("network.ping.IP", lambda dst: type("Dummy", (), {"sent_time": 1})())
    monkeypatch.setattr("network.ping.ICMP", lambda: None)

    logger = DummyLogger()
    os_type = "linux"
    # No exception expected for valid address, function handles errors internally
    run_ping_diag(address, logger, os_type)
    # For invalid, just check that function doesn't crash

def test_run_ping_diag_advanced(monkeypatch):
    monkeypatch.setattr("network.ping.ping3_ping", lambda addr, unit: 52)
    class DummyPingParsing:
        def parse(self, _): return DummyStats()
    class DummyStats:
        def as_dict(self): return {"min_rtt": 1, "avg_rtt": 2, "max_rtt": 3, "packet_loss_rate": 0}
    class DummyTransmitter:
        def __init__(self): self.destination = ""; self.count = 0
        def ping(self): return ""
    monkeypatch.setattr("network.ping.pingparsing", type("Dummy", (), {
        "PingParsing": DummyPingParsing,
        "PingTransmitter": DummyTransmitter
    }))
    monkeypatch.setattr("network.ping.sr1", lambda pkt, timeout, verbose: type("Dummy", (), {"time": 2, "sent_time": 1})())
    monkeypatch.setattr("network.ping.IP", lambda dst: type("Dummy", (), {"sent_time": 1})())
    monkeypatch.setattr("network.ping.ICMP", lambda: None)

    logger = DummyLogger()
    os_type = "linux"
    run_ping_diag("8.8.8.8", logger, os_type, advanced=True, csvfile="test_ping.csv")
