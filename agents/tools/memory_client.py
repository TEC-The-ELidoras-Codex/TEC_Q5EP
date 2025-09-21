from __future__ import annotations
import requests
from typing import Dict, Any, List


def make_memory_client(base_url: str):
    def add(item: Dict[str, Any]) -> Dict[str, Any]:
        r = requests.post(f"{base_url}/memory", json=item, timeout=10)
        r.raise_for_status()
        return r.json()

    def search(params: Dict[str, Any]) -> List[Dict[str, Any]]:
        r = requests.post(f"{base_url}/memory/search", json=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def get(item_id: str) -> Dict[str, Any]:
        r = requests.get(f"{base_url}/memory/{item_id}", timeout=10)
        r.raise_for_status()
        return r.json()

    def list_summaries() -> List[Dict[str, Any]]:
        r = requests.get(f"{base_url}/memory", timeout=10)
        r.raise_for_status()
        return r.json()

    def delete(item_id: str) -> str:
        r = requests.delete(f"{base_url}/memory/{item_id}", timeout=10)
        r.raise_for_status()
        return r.text

    return {"add": add, "search": search, "get": get, "list": list_summaries, "delete": delete}
