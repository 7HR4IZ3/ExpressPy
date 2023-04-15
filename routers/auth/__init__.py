from nodejs import express, passport, passport__local
from utils import decorate
from models import User

from .utils import hash_password, login_required, unauthorized_only


LocalStrategy = passport__local.Strategy

router = express.Router()

router.use(
    express.urlencoded({
        'extended': True
    })
)

get, post = decorate(
    router.get, router.post
)


def deserializeUser(user_id, done):
    user = User.objects.get_one(id=user_id)
    if user:
        return done(None, user)
    else:
        return done("No such user..", None)


def verify_auth(username, password, done):
    try:
        if not (username or password):
            raise Exception("Username or password not specified.")

        user = User.objects.get_one(name=username)
        if not user:
            raise Exception('No such user.')
        if not user.verify_password(password):
            raise Exception('Invalid password.')

        return done(None, {"id": user.id})
    except Exception as e:
        return done(str(e), None)

passport.use(LocalStrategy.new(verify_auth))

passport.serializeUser(lambda user, done: done(None, user.id))
passport.deserializeUser(deserializeUser)


@get("/login", [unauthorized_only("/auth/profile")])
def _(request, response, _next):
    response.render("login.html")


@post("/login", [
    # unauthorized_only("/auth/profile"),
    passport.authenticate('local')
])
def _(req, res, _):
    res.redirect("/auth/profile")


@get("/register", [unauthorized_only("/auth/profile")])
def _(request, response, _):
    response.render("register.html")


@post("/register", [unauthorized_only("/auth/profile")])
def _(request, response, _):
    username = request.body.username
    password = request.body.password
    age = request.body.age if request.body.age else 19

    if (username and password):
        User.objects.create(
            name=username, password=hash_password(username, password), age=age
        )
        response.redirect("/auth/login")
    else:
        response.redirect("/auth/register")


@post("/logout", [login_required("/auth/login")])
def _(request, response, _):
    request.logout(lambda: True)
    return response.redirect("/auth/login")


@get("/profile", [login_required("/auth/login")])
def _(req, res, _):
    print(req.user)
    res.send(
        f"Hello {req.user.name} </br>"
        '''<form action="/auth/logout" method="post">
            <button type="submit">Logout</button>
        </form>'''
    )
