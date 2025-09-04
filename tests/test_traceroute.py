# tests/test_traceroute.py - Test coverage per network/traceroute.py
import pytest

from network.traceroute import run_traceroute_diag


class DummyLogger:
    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg, exc_info=False):
        pass


def test_run_traceroute_diag_valid(monkeypatch):
    # Mock traceroute function
    class DummyPkt:
        sent_time = 1

    class DummyRcv:
        src = "1.2.3.4"
        time = 2

    def dummy_traceroute(addr, maxttl, timeout, verbose):
        return ([(DummyPkt(), DummyRcv())], None)

    monkeypatch.setattr("network.traceroute.traceroute", dummy_traceroute)
    logger = DummyLogger()
    run_traceroute_diag("8.8.8.8", logger, "linux", max_hops=3, timeout=1)


def test_run_traceroute_diag_invalid(monkeypatch):
    monkeypatch.setattr("network.traceroute.traceroute", None)
    logger = DummyLogger()
    run_traceroute_diag("invalid_address", logger, "linux", max_hops=3, timeout=1)
