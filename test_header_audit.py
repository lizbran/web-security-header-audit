import unittest
from email.message import Message

from header_audit import audit_headers, normalize_url


class HeaderAuditTests(unittest.TestCase):
    def test_normalize_url_adds_https(self):
        self.assertEqual(normalize_url("example.com"), "https://example.com")

    def test_normalize_url_keeps_https(self):
        self.assertEqual(normalize_url("https://example.com"), "https://example.com")

    def test_normalize_url_rejects_invalid_input(self):
        with self.assertRaises(ValueError):
            normalize_url("not a valid url")

    def test_audit_headers_detects_present_and_missing(self):
        headers = Message()
        headers["Strict-Transport-Security"] = "max-age=31536000"
        headers["X-Content-Type-Options"] = "nosniff"

        results = audit_headers(headers)

        self.assertTrue(results["Strict-Transport-Security"])
        self.assertTrue(results["X-Content-Type-Options"])
        self.assertFalse(results["Content-Security-Policy"])
        self.assertEqual(len(results), 6)


if __name__ == "__main__":
    unittest.main()
