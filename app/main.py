from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from database import session, engine
from schemas import Article
import models

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def home(request: Request):
    all_articles = session.query(models.Article).filter(models.Article.hidden==False).all()[::-1]
    return app.templates.TemplateResponse(
        request=request, name="home.html", context={"articles": all_articles}
    )

@app.get("/news/{news_id}")
async def article_page(request: Request, news_id: int):
    article = session.query(models.Article).filter(models.Article.id==news_id).first()
    return app.templates.TemplateResponse(
        request=request, name="article.html", context={"article": article}
    )

@app.get("/about")
def about(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="about.html"
    )

### ADMIN ROUTES ###
@app.get("/admin")
async def admin_page(request: Request):
    all_articles = session.query(models.Article).all()
    return app.templates.TemplateResponse(
        request=request, name="admin/home.html", context={"articles": all_articles}
    )

@app.get("/admin/edit-article/{article_id}")
async def edit_article_page(request: Request, article_id: int):
    article = session.query(models.Article).filter(models.Article.id==article_id).first()
    return app.templates.TemplateResponse(
        request=request, name="admin/edit_article.html", context={"article": article}
    )

@app.get("/admin/create-article")
async def create_article_page(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="admin/create_article.html"
    )

### ARTICLE API ROUTES ###
@app.post("/api/articles")
async def create_article(article: Article):
    new_article = models.Article(title=article.title, content=article.content, hidden=True)
    session.add(new_article)
    session.commit()
    return "created"

@app.get("/api/articles/all")
async def get_articles():
    all_articles = session.query(models.Article).all()
    return all_articles

@app.delete("/api/articles/delete/{article_id}")
async def delete_article(article_id: int):
    session.query(models.Article).filter(models.Article.id==article_id).delete()
    return "deleted"

@app.put("/api/articles/update/{article_id}")
async def update_article(article: Article, article_id: int):
    session.query(models.Article).filter(models.Article.id==article_id).update(
        { "title": article.title, "content": article.content, "hidden": article.hidden }
    )
    return "updated"

