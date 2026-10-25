"""
Sloth Digest — FastAPI API Endpoint Tests
"""

import pytest
from starlette.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["is_offline"] is True
    assert "status" in data
    assert "active_model" in data


def test_get_latest_digest():
    response = client.get("/api/digest/latest")
    assert response.status_code == 200


def test_synthetic_samples_list():
    response = client.get("/api/synthetic/samples")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    sample_ids = [s["id"] for s in data]
    assert "sample_hackathon_team" in sample_ids


def test_tidier_scan_and_apply():
    response = client.get("/api/tidier/scan")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_upload_chat_txt():
    chat_content = """
[24/10/2026, 11:00:00] Alice: Please send the presentation slides by Monday.
[24/10/2026, 11:01:00] Bob: Sure thing!
[24/10/2026, 11:02:00] Charlie: Great meme!
"""
    files = {"file": ("test_chat.txt", chat_content.encode("utf-8"), "text/plain")}
    response = client.post("/api/digest/upload", files=files)
    assert response.status_code == 200
    digest = response.json()
    assert digest["total_messages"] == 3
    assert "two_line_summary" in digest
