# malformed-input tests for /call/create_event
import os
import httpx

SERVER = os.environ.get("SERVER_URL", "http://localhost:8000")

bad_payloads = [
    {},  # missing fields
    {"title": "", "when": "2024-01-01T00:00:00Z"},  # empty title
    {"title": "Meeting", "when": "not-a-datetime"}  # invalid datetime
]


def run():
    with httpx.Client(timeout=5.0) as client:
        for i, payload in enumerate(bad_payloads, start=1):
            r = client.post(f"{SERVER}/call/create_event", json=payload)
            status = r.status_code
            print(f"[W0] malformed #{i}: status={status}, body={r.text[:200]}")


if __name__ == "__main__":
    run()
