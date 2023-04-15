from py_bridge import nodejs
from utils import request_logger


with nodejs(keep_alive=True) as node:

    from nodejs import (
        express, passport,
        express__session as session,
        # connect__sqlite3 as sqlite3,
        nunjucks
    )
    # from nodejs.express.lib.utils import isAbsolute
    from routers import HomeRouter, UsersRouter, AuthRouter, NotesRouter
    # from store import SessionStore

    # SQLiteStore = sqlite3(session)

    # print("Router", isAbsolute)

    app = express()

    nunjucks.configure('views', {
        "autoescape": True,
        "express": app
    })

    app.use(express.json())
    app.use(request_logger)

    app.use(session({
        'secret': 'my-secret-key',
        'resave': False,
        'saveUninitialized': False
    }))

    app.use(passport.session())
    app.use(passport.initialize())

    app.use('/', HomeRouter)
    app.use('/auth', AuthRouter)
    app.use('/users', UsersRouter)
    app.use("/notes", NotesRouter)

    app.listen(3000, lambda: print(
        "* Server: Started On 'http://localhost:3000'."
    ))
