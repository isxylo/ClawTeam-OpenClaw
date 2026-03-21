"""Tests for AgentIdentity model field."""

from clawteam.identity import AgentIdentity


class TestAgentIdentityModel:
    def test_model_defaults_none(self):
        ident = AgentIdentity()
        assert ident.model is None

    def test_model_from_env(self, monkeypatch):
        monkeypatch.setenv("CLAWTEAM_MODEL", "opus")
        ident = AgentIdentity.from_env()
        assert ident.model == "opus"

    def test_model_from_openclaw_env(self, monkeypatch):
        monkeypatch.delenv("CLAWTEAM_MODEL", raising=False)
        monkeypatch.setenv("OPENCLAW_MODEL", "sonnet-4.6")
        ident = AgentIdentity.from_env()
        assert ident.model == "sonnet-4.6"

    def test_model_not_set(self, monkeypatch):
        monkeypatch.delenv("CLAWTEAM_MODEL", raising=False)
        monkeypatch.delenv("OPENCLAW_MODEL", raising=False)
        monkeypatch.delenv("CLAUDE_CODE_MODEL", raising=False)
        ident = AgentIdentity.from_env()
        assert ident.model is None

    def test_to_env_includes_model(self):
        ident = AgentIdentity(model="opus")
        env = ident.to_env()
        assert env["CLAWTEAM_MODEL"] == "opus"

    def test_to_env_omits_model_when_none(self):
        ident = AgentIdentity()
        env = ident.to_env()
        assert "CLAWTEAM_MODEL" not in env
