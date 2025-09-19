from fastapi.testclient import TestClient
from server.app import app, RUNS
from pathlib import Path


def test_pack_flow(tmp_path: Path):
    client = TestClient(app)
    # Submit a note-only run
    r = client.post(
        "/submit",
        data={
            "note": "hello",
            "timestamp": "2025-09-17T00:00:00Z",
            "tags": "test",
            "consent": "true",
        },
    )
    assert r.status_code == 200
    run_id = r.text.split()[-1]

    # List runs
    r2 = client.get("/runs")
    assert r2.status_code == 200
    assert any(it["id"] == run_id for it in r2.json())

    # Create pack
    r3 = client.get(f"/pack/{run_id}")
    assert r3.status_code == 200
    assert r3.headers.get("content-type") == "application/zip"
