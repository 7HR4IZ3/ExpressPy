session = require("express-session")


class SessionStore {
    constructor(Session) {
        this.Session = Session
    }

    on(event, callback) {
        print("On called.")
        return

    }

    async all(callback) {
        let all = await this.Session.objects.all();
        let data = {}

        for (let item of all) {
            data[item.sid] = item.data
        }

        callback && callback(null, data)
    }

    destroy(sid, callback) {
        this.Session.objects.delete(sid=sid)
        callback && callback()
    }

    async clear(callback) {
        for (x of await this.Session.objects.all()) {
            this.Session.objects.delete(id=x.id)
        }
        callback(null)
    }

    async length(callback) {
        callback && callback(null, (await this.Session.objects.all()).length)

    }

    async get(sid, callback) {
        let session = await this.Session.objects.get_one(sid=sid)
        if (session) {
            callback && callback(null, JSON.parse(session.data))
        }
        else {
            callback && callback("No such this.session.", null)
        }

    }

    async set(sid, session, callback) {
        let sess = await this.Session.objects.get_one(sid=sid)
        if (sess) {
            sess.data = JSON.stringify(session)
            sess.save()
            callback && callback(null)
        }
        else {
            callback && callback("No such this.session.")
        }

    }

    async touch(sid, session, callback) {
        currentSession = this.Session.objects.get_one(sid=sid)

        if (currentSession) {
            currentSession.data = JSON.stringify(session)
            currentSession.save()
        }

        callback && callback()

    }

}
