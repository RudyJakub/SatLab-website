from fastapi import FastAPI, Request, UploadFile, File, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import session, engine
from schemas import Article
import models
from typing import List

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

@app.get("/about")
def about(request: Request):
    return app.templates.TemplateResponse(
        request=request, name="about.html"
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


### ARTICLE API ROUTES ###

@app.post("/api/articles")
async def create_article(article: Article):
    new_article = models.Article(title=article.title, content=article.content, hidden=article.hidden, image="")
    session.add(new_article)
    session.commit()
    return "created"

@app.delete("/api/articles/delete/{article_id}")
async def delete_article(article_id: int):
    session.query(models.Article).filter(models.Article.id==article_id).delete()
    session.commit()
    return "deleted"

@app.post("/api/articles/update/{article_id}")
def update_article(article_id: int, article: Article = Depends(), files: List[UploadFile] = File(None)):
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
    return "updated"