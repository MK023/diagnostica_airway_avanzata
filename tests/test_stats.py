# tests/test_stats.py - Test coverage per network/stats.py
import pytest

from network.stats import run_stats_diag


class DummyLogger:
    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg, exc_info=False):
        pass


def test_run_stats_diag(monkeypatch):
    class DummyStats:
        bytes_sent = 100
        bytes_recv = 200
        packets_sent = 5
        packets_recv = 6
        errin = 0
        errout = 0
        dropin = 0
        dropout = 0

    monkeypatch.setattr(
        "network.stats.psutil",
        type("Dummy", (), {"net_io_counters": lambda pernic: {"eth0": DummyStats()}}),
    )
    logger = DummyLogger()
    run_stats_diag(logger)


def test_run_stats_diag_no_module(monkeypatch):
    monkeypatch.setattr("network.stats.psutil", None)
    logger = DummyLogger()
    run_stats_diag(logger)
