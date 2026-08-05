import unittest

from src.framework_demo import VERSION, health


class FrameworkDemoTest(unittest.TestCase):
    def test_health_reports_status_and_version(self) -> None:
        self.assertEqual(
            health(),
            {"status": "ok", "version": VERSION},
        )


if __name__ == "__main__":
    unittest.main()
