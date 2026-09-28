from __future__ import annotations

import re

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_static_page_links_css() -> None:
    page = client.get("/")
    assert page.status_code == 200
    assert "Статическая страница лабораторной работы: вариант 3" in page.text
    match = re.search(r'href="([^"]*main\.css)"', page.text)
    assert match is not None
    css = client.get(match.group(1))
    assert css.status_code == 200
    assert "body" in css.text


def test_bootstrap_reference() -> None:
    page = client.get("/bootstrap")
    assert page.status_code == 200
    assert "bootstrap" in page.text
    assert "bootstrap@5.3.3" in page.text


def test_jinja_renders_supplied_data() -> None:
    page = client.get("/card", params={"course": "МТП", "topic": "Шаблоны"})
    assert page.status_code == 200
    assert "МТП" in page.text
    assert "Шаблоны" in page.text


def test_auth_rejects_then_accepts() -> None:
    anonymous = client.get("/private")
    assert anonymous.status_code == 401
    wrong = client.get("/private", auth=("student", "nope"))
    assert wrong.status_code == 401
    ok = client.get("/private", auth=("student", "lab-221141"))
    assert ok.status_code == 200
    assert "доступ разрешён" in ok.text
