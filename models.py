from sqlite import SqliteDatabase

db = SqliteDatabase("./db.sqlite")


@db.on("error")
def _(err):
    raise err


class Session(db.Model):
    sid: int
    data: str


class User(db.Model):
    name: str
    age: int
    password: bytes

    def verify_password(self, password):
        from routers.auth.utils import verify_password
        return verify_password(
            self.name, password, self.password
        )


class Note(db.Model):
    name: str
    body: str
    user: User
