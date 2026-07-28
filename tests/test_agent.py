import sys
import unittest
from pathlib import Path

from google.api_core.exceptions import ResourceExhausted

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agent import ask


class AskTests(unittest.TestCase):
    def test_ask_returns_fallback_when_quota_is_exhausted(self):
        class FakeAgent:
            def invoke(self, payload):
                raise ResourceExhausted("Quota exceeded")

        answer, sources = ask(FakeAgent(), "¿Qué dice el documento?")

        self.assertIn("No pude completar la respuesta", answer)
        self.assertEqual([], sources)


if __name__ == "__main__":
    unittest.main()
