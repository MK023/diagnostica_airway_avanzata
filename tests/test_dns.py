# tests/test_dns.py - Test coverage per network/dns.py
import pytest

from network.dns_utils import run_dns_diag


class DummyLogger:
    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg, exc_info=False):
        pass


def test_run_dns_diag_valid(monkeypatch):
    # Mock socket and dnspython
    monkeypatch.setattr("network.dns.socket.gethostbyname", lambda addr: "8.8.8.8")
    monkeypatch.setattr(
        "network.dns.socket.gethostbyaddr", lambda ip: ("testhost", [], [ip])
    )

    class DummyAnswer:
        def __str__(self):
            return "answer"

    class DummyResolver:
        timeout = 3

        def resolve(self, address, rtype):
            return [DummyAnswer()]

    monkeypatch.setattr(
        "network.dns.dns",
        type(
            "Dummy", (), {"resolver": type("Dummy2", (), {"Resolver": DummyResolver})}
        ),
    )
    run_dns_diag("google.com", DummyLogger())


def test_run_dns_diag_invalid(monkeypatch):
    monkeypatch.setattr(
        "network.dns.socket.gethostbyname",
        lambda addr: (_ for _ in ()).throw(Exception("fail")),
    )
    run_dns_diag("invalid_domain", DummyLogger())
