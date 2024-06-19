from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from markdown import markdown

from models.blog import Blogs, BlogForm
from models.event import Events,EventForm

router = APIRouter(prefix="", tags=["Home"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    events = await Events.find().to_list()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "events": events
    })


@router.get("/Events/add", response_class=HTMLResponse)
async def get_event_add(request: Request):
    return templates.TemplateResponse("event_add.html", {
        "request": request
    })


@router.post("/Events/add", response_class=HTMLResponse)
async def create_event(request: Request):
    form = EventForm(request=request)
    await form.create_form_data()

    new_event = Events(
        title=form.form_data["title"],
        author=form.form_data["author"],
        description=form.form_data["description"],
        body=form.form_data["body"],
        month=form.form_data["month"],
        day=form.form_data["day"]
    )
    try:
        await new_event.insert()
        return templates.TemplateResponse("event_add.html", {
            "request": request,
            "msg": "Success",
            "msg_type": "success"
        })
    except Exception as err:
        print(err)
        return templates.TemplateResponse("event_add.html", {
            "request": request,
            "msg": "Error",
            "err": err,
            "msg_type": "danger"
        })


@router.get("/events/{event_id}", response_class=HTMLResponse)
async def get_event_by_id(request: Request, event_id: str):
    event = await Events.get(event_id)
    event.body = markdown(event.body)
    return templates.TemplateResponse("blog_detail.html", {
        "request": request,
        "event": event
    })


@router.get("/events/update/{event_id}", response_class=HTMLResponse)
async def get_update_event_page(request: Request, event_id: str):
    event = await Events.get(event_id)
    return templates.TemplateResponse("event_update.html", {
        "request": request,
        "event": event
    })


@router.post("/events/update/{event_id}", response_class=HTMLResponse)
async def update_event(request: Request, event_id: str):
    event = await Events.get(event_id)
    try:
        form = EventForm(request=request)
        await form.create_form_data()

        event.title = form.form_data["title"]
        event.author = form.form_data["author"]
        event.description = form.form_data["description"]
        event.body = form.form_data["body"]
        event.month = form.form_data["month"]
        event.day = form.form_data["day"]

        await event.save()

        return templates.TemplateResponse("event_detail.html", {
            "request": request,
            "event": event
        })

    except Exception as err:
        print(err)
        return templates.TemplateResponse("event_update.html", {
            "request": request,
            "event": event
        })

@router.get("/events/delete/{event_id}", response_class=RedirectResponse)
async def delete_event(event_id: str):
    try:
        event = await Events.get(event_id)
        await event.delete()
        return RedirectResponse(url="/")

    except Exception as err:
        print(err)
        return RedirectResponse(url=f"/events/{event_id}")
@router.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {
        "request": request
    })
