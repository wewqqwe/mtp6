"""Веб варианта 3: статика, Bootstrap, Jinja2, Basic-авторизация."""

from __future__ import annotations

import secrets
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE = Path(__file__).resolve().parent
USER = "student"
PASSWORD = "lab-221141"

app = FastAPI(title="Сайт Алины, вариант 3")
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE / "templates"))
security = HTTPBasic()


def require_student(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    user_ok = secrets.compare_digest(credentials.username, USER)
    pass_ok = secrets.compare_digest(credentials.password, PASSWORD)
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=401,
            detail="unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="/static/main.css">
  <title>Вариант 3</title>
</head>
<body>
  <p>Статическая страница лабораторной работы: вариант 3</p>
</body>
</html>
"""
    return HTMLResponse(html)


@app.get("/bootstrap", response_class=HTMLResponse)
def bootstrap_page() -> HTMLResponse:
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <title>Bootstrap</title>
</head>
<body class="container">
  <h1>Страница с Bootstrap</h1>
</body>
</html>
"""
    return HTMLResponse(html)


@app.get("/card", response_class=HTMLResponse)
def card(request: Request, course: str = "", topic: str = "") -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="card.html",
        context={"course": course, "topic": topic},
    )


@app.get("/private", response_class=HTMLResponse)
def private_page(_user: str = Depends(require_student)) -> HTMLResponse:
    return HTMLResponse("<p>доступ разрешён</p>")
