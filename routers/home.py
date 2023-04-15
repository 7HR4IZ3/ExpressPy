from nodejs import express
from utils import decorate

router = express.Router()

get, post = decorate(
    router.get,
    router.post
)


@get("/")
def _(request, response, next):
    response.render("index.html")
