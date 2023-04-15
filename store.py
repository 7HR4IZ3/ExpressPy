import json
from models import Session
from nodejs import require

session = require("express-session")


class SessionStore:
    def on(self, event, callback):
        print("On called.")
        return

    def all(self, callback):
        callback and callback(
            None, {x.sid: x.data for x in Session.objects.all()}
        )

    def destroy(self, sid, callback):
        Session.objects.delete(sid=sid)
        callback and callback()

    def clear(self, callback):
        [Session.objects.delete(id=x.id) for x in Session.objects.all()]
        callback(None)

    def length(self, callback):
        callback and callback(None, len(Session.objects.all()))

    def get(self, sid, callback):
        session = Session.objects.get_one(sid=sid)
        if session:
            callback and callback(None, json.loads(session.data))
        else:
            callback and callback("No such session.", None)

    def set(self, sid, session, callback):
        sess = Session.objects.get_one(sid=sid)
        if sess:
            sess.data = json.dumps(session.__cast__())
            sess.save()
            callback and callback(None)
        else:
            callback and callback("No such session.")

    def touch(self, sid, session, callback):
        currentSession = Session.objects.get_one(sid=sid)

        if currentSession:
            currentSession.data = json.dumps(session.__cast__())
            currentSession.save()

        callback and callback()
