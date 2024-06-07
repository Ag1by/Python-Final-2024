from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.blog import Blogs, BlogForm

router = APIRouter(prefix="", tags=["Home"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    blogs = await Blogs.find().to_list()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "blogs": blogs
    })


@router.get("/blogs/add", response_class=HTMLResponse)
async def get_blog_add(request: Request):
    return templates.TemplateResponse("blog_add.html", {
        "request": request
    })


@router.post("/blogs/add", response_class=HTMLResponse)
async def create_blog(request: Request):
    form = BlogForm(request=request)
    await form.create_form_data()

    new_blog = Blogs(
        title=form.form_data["title"],
        author=form.form_data["author"],
        description=form.form_data["description"],
        body=form.form_data["body"],
        image_link=form.form_data["image_link"]
    )
    try:
        await new_blog.insert()
        return templates.TemplateResponse("blog_add.html", {
            "request": request,
            "msg": "Success",
            "msg_type": "success"
        })
    except Exception as err:
        print(err)
        return templates.TemplateResponse("blog_add.html", {
            "request": request,
            "msg": "Error",
            "err": err,
            "msg_type": "danger"
        })


@router.get("/blogs/{blog_id}", response_class=HTMLResponse)
async def get_blog_by_id(request: Request, blog_id: str):
    blog = await Blogs.get(blog_id)
    return templates.TemplateResponse("blog_detail.html", {
        "request": request,
        "blog": blog
    })


@router.get("/blogs/update/{blog_id}", response_class=HTMLResponse)
async def get_update_blog_page(request: Request, blog_id: str):
    blog = await Blogs.get(blog_id)
    return templates.TemplateResponse("blog_update.html", {
        "request": request,
        "blog": blog
    })


@router.post("/blogs/update/{blog_id}", response_class=HTMLResponse)
async def update_blog(request: Request, blog_id: str):
    blog = await Blogs.get(blog_id)
    try:
        form = BlogForm(request=request)
        await form.create_form_data()

        blog.title = form.form_data["title"]
        blog.author = form.form_data["author"]
        blog.description = form.form_data["description"]
        blog.body = form.form_data["body"]
        blog.image_link = form.form_data["image_link"]

        await blog.save()

        return templates.TemplateResponse("blog_detail.html", {
            "request": request,
            "blog": blog
        })

    except Exception as err:
        print(err)
        return templates.TemplateResponse("blog_update.html", {
            "request": request,
            "blog": blog
        })


@router.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request
    })
