from nodejs import express, console

from utils import decorate
from models import Note
from routers.auth.utils import login_required


router = express.Router()
router.use(
    express.urlencoded({
        'extended': True
    })
)
router.use(login_required("/auth/login"))

get, post = decorate(
    router.get, router.post
)


@get("/")
def _(request, response, _):
    response.render("notes.html", {
        "notes": Note.objects.get(user=request.user).serialize()
    })


@get("/add")
@post("/add")
def _(request, response, _):
    if request.method == "GET":
        return response.render("add_note.html")
    else:
        name = request.body.note_name
        body = request.body.note_body
        if name and body:
            Note.objects.create(name=name, body=body, user=request.user.id)
            response.redirect("/notes")
        else:
            response.back()
