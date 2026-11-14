# Website Uptime Monitor

A dependency-free Python CLI for measuring HTTP(S) availability and response time, saving history to SQLite, and summarizing uptime from stored checks.

**Python:** 3.10+ • **Dependencies:** standard library only

## Quick start

```bash
python -m uptime_monitor --url https://example.com --db uptime-history.sqlite3
python -m uptime_monitor --file sites.example.txt --count 3 --interval 60 --json
python -m uptime_monitor --db uptime-history.sqlite3 --report
python -m uptime_monitor --db uptime-history.sqlite3 --report --json
python -m unittest discover -s tests -v
```

The report shows each site's check count, successful checks, uptime percentage, average successful-request latency, and latest state.

## Arguments

- `--url`: one HTTP(S) target (repeatable)
- `--file`: text file of targets, one per line; `#` starts a comment
- `--timeout`: seconds per request (default 5)
- `--count`: rounds to run (default 1)
- `--interval`: seconds between rounds (default 60)
- `--db`: SQLite history database
- `--json`: JSON Lines for monitoring, JSON array for reports
- `--report`: summarize recorded checks; no network requests

## Notes

Only monitor sites you are authorized to query and choose polite intervals. The CLI supports HTTP(S) sites; it does not crawl them. HTTP 2xx/3xx responses are classified as up, while HTTP 4xx/5xx and network errors are down. Python's urllib follows redirects.

For safety, do not put API keys or sensitive data in URLs. The history database is locally stored and excluded from Git. Unit tests use mocked HTTP requests, not live websites.

## Files

- [HTTP checks](uptime_monitor/monitor.py)
- [SQLite storage and reporting](uptime_monitor/storage.py)
- [CLI](uptime_monitor/__main__.py)
- [Unit tests](tests/test_monitor.py)
