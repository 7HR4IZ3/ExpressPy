from nodejs import express
from utils import decorate

from models import User

from .auth.utils import login_required

router = express.Router()
# router.use(login_required("/auth/login"))

get, post, put, delete = decorate(
    router.get,
    router.post,
    router.put,
    router.delete
)


@get("")
def users_homepage(req, res, _next):
    res.type("application/json")
    res.send(User.objects.all().serialize())


@get("/:id")
def users_singlepage(req, res, _next):
    user = User.objects.get_one(id=str(req.params.id))

    if user:
        res.send(user.serialize(skip=['password']))
    else:
        res.send({})
