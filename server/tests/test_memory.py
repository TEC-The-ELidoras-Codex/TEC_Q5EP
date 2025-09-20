from fastapi.testclient import TestClient
from server.app import app


client = TestClient(app)


def test_memory_crud_and_search():
    # Create a memory
    payload = {
        "user_id": "tester",
        "tags": ["unit", "memory"],
        "content": "The quick brown fox jumps over the lazy dog",
        "metadata": {"note": "pangram"},
    }
    r = client.post('/memory', json=payload)
    assert r.status_code == 200, r.text
    item = r.json()
    assert item["id"]
    mem_id = item["id"]
    assert item["user_id"] == "tester"
    assert item["tags"] == ["unit", "memory"]
    assert item["content"].startswith("The quick brown fox")

    # List memories includes a summary for our item
    r = client.get('/memory')
    assert r.status_code == 200
    summaries = r.json()
    assert any(s["id"] == mem_id and s["content_chars"] >= 10 for s in summaries)

    # Get the memory by id
    r = client.get(f'/memory/{mem_id}')
    assert r.status_code == 200
    fetched = r.json()
    assert fetched["content"] == payload["content"]

    # Search by substring in content
    r = client.post('/memory/search', json={"q": "brown fox", "tags": [], "limit": 5})
    assert r.status_code == 200
    results = r.json()
    assert any(x["id"] == mem_id for x in results)

    # Search by tag intersection
    r = client.post('/memory/search', json={"q": "", "tags": ["memory"], "limit": 5})
    assert r.status_code == 200
    results = r.json()
    assert any(x["id"] == mem_id for x in results)

    # Delete the memory
    r = client.delete(f'/memory/{mem_id}')
    assert r.status_code == 200
    assert r.text == 'OK'

    # Ensure it's gone
    r = client.get(f'/memory/{mem_id}')
    assert r.status_code == 404
