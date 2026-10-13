"""Check for common HTTP security headers on a website you may assess."""

import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

SECURITY_HEADERS = {
    "Content-Security-Policy": "Helps control which sources a browser may load.",
    "Strict-Transport-Security": "Tells browsers to prefer HTTPS for future requests.",
    "X-Content-Type-Options": "Helps prevent MIME-type sniffing; commonly set to nosniff.",
    "X-Frame-Options": "Legacy browser control for framing; CSP frame-ancestors is more flexible.",
    "Referrer-Policy": "Controls how much referrer information browsers send.",
    "Permissions-Policy": "Controls access to selected browser features.",
}


def normalize_url(value: str) -> str:
    """Require a hostname and add HTTPS when the scheme is omitted."""
    value = value.strip()
    if "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    hostname = parsed.hostname
    if (
        parsed.scheme not in ("http", "https")
        or not hostname
        or " " in hostname
        or "." not in hostname
    ):
        raise ValueError("Enter a valid http:// or https:// URL with a hostname.")
    return value


def audit_headers(headers) -> dict:
    """Return a mapping of header names to whether they are present."""
    return {
        name: bool(headers.get(name))
        for name in SECURITY_HEADERS
    }


def fetch_headers(url: str, timeout: int = 8):
    """Make one GET request and return status code plus response headers."""
    request = Request(
        url,
        headers={"User-Agent": "WebSecurityHeaderAudit/1.0 (learning project)"},
        method="GET",
    )
    with urlopen(request, timeout=timeout) as response:
        return response.status, response.headers


def print_report(url: str, status: int, headers) -> int:
    results = audit_headers(headers)
    print(f"Target: {url}")
    print(f"HTTP status: {status}\n")
    for name, present in results.items():
        marker = "PASS" if present else "WARN"
        state = "present" if present else "missing"
        print(f"[{marker}] {name}: {state}")
        if not present:
            print(f"       Why it matters: {SECURITY_HEADERS[name]}")
    present_count = sum(results.values())
    missing_count = len(results) - present_count
    print(f"\nSummary: {present_count} present, {missing_count} missing")
    print("Note: Header presence alone does not guarantee a secure configuration.")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Usage: python header_audit.py <website-url>")
        return 2

    try:
        url = normalize_url(argv[0])
        status, headers = fetch_headers(url)
    except ValueError as exc:
        print(f"Input error: {exc}")
        return 2
    except HTTPError as exc:
        # HTTP error responses still include useful response headers.
        return print_report(url, exc.code, exc.headers)
    except (URLError, TimeoutError, OSError) as exc:
        print(f"Request failed: {exc}")
        return 1

    return print_report(url, status, headers)


if __name__ == "__main__":
    raise SystemExit(main())
