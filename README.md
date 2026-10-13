# Web Security Header Audit

A beginner-friendly Python project that reviews common HTTP security headers on a website you own or are authorized to assess.

## Why I built this

I'm building foundational skills in cybersecurity, Python, Linux command-line tools, and secure software workflows. This project gives me a small, repeatable way to inspect a site's response headers, explain what the results mean, and test my code automatically with GitHub Actions.

## What it checks

- `Content-Security-Policy` (CSP)
- `Strict-Transport-Security` (HSTS)
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Referrer-Policy`
- `Permissions-Policy`

The tool reports whether each header is present. It does **not** exploit vulnerabilities, crawl a site, test authentication, or prove that a website is secure. Header recommendations depend on the application's architecture, so results need human review.

## Requirements

- Python 3.10+
- No third-party Python packages required

## Run it

```bash
python header_audit.py https://example.com
```

Use it only on websites you own or have permission to assess. The script makes a single ordinary HTTP request and prints a basic report.

## Example output

```text
Target: https://example.com
HTTP status: 200

[PASS] Strict-Transport-Security: present
[WARN] Content-Security-Policy: missing
[PASS] X-Content-Type-Options: present
[WARN] X-Frame-Options: missing
[PASS] Referrer-Policy: present
[WARN] Permissions-Policy: missing

Summary: 3 present, 3 missing
Note: Header presence alone does not guarantee a secure configuration.
```

The exact output depends on the target's response. The example above is illustrative, not a scan result.

## Secure development workflow

This repository includes a GitHub Actions workflow that runs automated unit tests when code is pushed or a pull request is opened. The tests use mocked responses, so they do not contact an external website.

## Possible next improvements

- Add JSON output for easier reporting
- Validate selected header values, not just presence
- Add command-line options for timeout and output file
- Add a dependency or static-analysis check if dependencies are introduced

## Learning references

- [MDN: HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)

## Project status

Learning project — actively developing foundational skills. Not a substitute for a professional security assessment.
