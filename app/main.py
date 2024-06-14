from fastapi import FastAPI, Request, UploadFile, File, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from database import session, engine
from schemas import Article, LoginCredentials
import models
from typing import List
import uuid
import hashlib

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

ADMIN_SESSIONS = {}
HASHED_PASSWORD = '7ae8b0fd49a7f2965934ee8c907d3a67e8ec9c8e656cf7e89b094a2cbe19e7c9'

@app.get("/")
async def home(request: Request):
    all_articles = session.query(models.Article).filter(models.Article.hidden==False).all()[::-1]
    return app.templates.TemplateResponse(
        request=request, name="home.html", context={"articles": all_articles}
    )

@app.get("/about")
def about(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="about.html"
    )

@app.get("/cooperate")
def about(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="cooperate.html"
    )

@app.get("/documentation")
def about(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="documentation.html"
    )

@app.get("/news/{news_id}")
async def article_page(request: Request, news_id: int):
    article = session.query(models.Article).filter(models.Article.id==news_id).first()
    return app.templates.TemplateResponse(
        request=request, name="article.html", context={"article": article}
    )


### ADMIN ROUTES ###

@app.get("/admin")
async def admin_page(request: Request):
    session_id = request.cookies.get("Authorization")
    if not session_id or session_id not in ADMIN_SESSIONS or ADMIN_SESSIONS[session_id] != "admin":
        return RedirectResponse("/admin/login")
    all_articles = session.query(models.Article).all()
    return app.templates.TemplateResponse(
        request=request, name="admin/home.html", context={"articles": all_articles}
    )

@app.get("/admin/login")
async def admin_login_page(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="admin/login.html"
    )

@app.get("/admin/edit-article/{article_id}")
async def edit_article_page(request: Request, article_id: int):
    session_id = request.cookies.get("Authorization")
    if not session_id or session_id not in ADMIN_SESSIONS or ADMIN_SESSIONS[session_id] != "admin":
        return RedirectResponse("/admin/login")
    article = session.query(models.Article).filter(models.Article.id==article_id).first()
    return app.templates.TemplateResponse(
        request=request, name="admin/edit_article.html", context={"article": article}
    )

@app.post("/api/admin/login")
def admin_login(credentials: LoginCredentials):
    password_hash = hashlib.sha256(credentials.password.encode("utf-8")).hexdigest()
    if password_hash==HASHED_PASSWORD:
        session_id = str(uuid.uuid4())
        ADMIN_SESSIONS[session_id] = "admin"
        response = Response(status_code=status.HTTP_200_OK)
        response.set_cookie(key="Authorization", value=session_id)
        return response
    else:
        response = Response()
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    
@app.post("/api/admin/logout")
async def admin_logout(request: Request):
    del ADMIN_SESSIONS[request.cookies.get("Authorization")]
    response = Response(status_code=status.HTTP_200_OK)
    return response


### ARTICLE API ROUTES ###

@app.post("/api/articles")
async def create_article(request: Request, article: Article):
    session_id = request.cookies.get("Authorization")
    if not session_id or session_id not in ADMIN_SESSIONS or ADMIN_SESSIONS[session_id] != "admin":
        return RedirectResponse("/admin/login")
    new_article = models.Article(title=article.title, content=article.content, hidden=article.hidden, image="")
    session.add(new_article)
    session.commit()
    return "created"

@app.delete("/api/articles/delete")
async def delete_article(request: Request, article_id: int):
    session_id = request.cookies.get("Authorization")
    if not session_id or session_id not in ADMIN_SESSIONS or ADMIN_SESSIONS[session_id] != "admin":
        return RedirectResponse("/admin/login")
    session.query(models.Article).filter(models.Article.id==article_id).delete()
    session.commit()
    response = Response(status_code=status.HTTP_200_OK)
    return response

@app.post("/api/articles/update")
def update_article(request: Request, article_id: int, article: Article = Depends(), files: List[UploadFile] = File(None)):
    session_id = request.cookies.get("Authorization")
    if not session_id or session_id not in ADMIN_SESSIONS or ADMIN_SESSIONS[session_id] != "admin":
        return RedirectResponse("/admin/login")
    if files:
        file = files[0]
        file_path = f"./static/article_images/{file.filename}"
        try:
            with open(file_path, "wb") as f:
                f.write(file.file.read())
        except Exception as e:
            return {"error saving image": e.args}
        session.query(models.Article).filter(models.Article.id==article_id).update(
            { "title": article.title, "content": article.content, "hidden": article.hidden, "image": {file.filename} }
        )
        session.commit()
    else:
        session.query(models.Article).filter(models.Article.id==article_id).update(
            { "title": article.title, "content": article.content, "hidden": article.hidden}
        )
        session.commit() 
    response = Response(status_code=status.HTTP_200_OK)
    return response
