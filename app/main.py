from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from database import session

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.templates = Jinja2Templates(directory="templates")

# session.execute(text("SELECT 1")) # szybki test

@app.get("/")
def home(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="home.html"
    )

@app.get("/informacje")
def about(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="about.html"
    )

import uvicorn
uvicorn.run(app, host="localhost", port=8000)