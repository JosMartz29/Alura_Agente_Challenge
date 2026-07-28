import os
import sys
import types
import unittest
from pathlib import Path

from google.api_core.exceptions import ResourceExhausted

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import agent as agent_module
from src.agent import ask


class AskTests(unittest.TestCase):
    def test_ask_returns_fallback_when_quota_is_exhausted(self):
        class FakeAgent:
            def invoke(self, payload):
                raise ResourceExhausted("Quota exceeded")

        answer, sources = ask(FakeAgent(), "¿Qué dice el documento?")

        self.assertIn("No pude completar la respuesta", answer)
        self.assertEqual([], sources)

    def test_get_secret_prefers_streamlit_secrets_when_env_missing(self):
        original = os.environ.get("COHERE_API_KEY")
        os.environ.pop("COHERE_API_KEY", None)

        fake_st = types.SimpleNamespace(secrets={"COHERE_API_KEY": "secret-from-streamlit"})
        sys.modules["streamlit"] = fake_st

        try:
            value = agent_module._get_secret("COHERE_API_KEY")
        finally:
            if original is not None:
                os.environ["COHERE_API_KEY"] = original
            sys.modules.pop("streamlit", None)

        self.assertEqual("secret-from-streamlit", value)


if __name__ == "__main__":
    unittest.main()
