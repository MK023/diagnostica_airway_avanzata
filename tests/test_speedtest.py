# tests/test_speedtest.py - Test coverage per network/speedtest.py
import pytest
from network.speedtest import run_speedtest_diag

class DummyLogger:
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg, exc_info=False): pass

def test_run_speedtest_diag_success(monkeypatch):
    class DummySpeedtest:
        def get_best_server(self): pass
        def download(self): return 1e6
        def upload(self): return 2e6
        class results:
            ping = 10
    monkeypatch.setattr("network.speedtest.speedtest", type("Dummy", (), {"Speedtest": DummySpeedtest}))
    logger = DummyLogger()
    run_speedtest_diag(logger, max_attempts=1)

def test_run_speedtest_diag_fail(monkeypatch):
    monkeypatch.setattr("network.speedtest.speedtest", None)
    logger = DummyLogger()
    run_speedtest_diag(logger, max_attempts=1)