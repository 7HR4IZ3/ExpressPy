def decorate(*targets):
    ret = []

    def main(target):
        def middle(route, before=None, after=None):
            def wrapper(func):
                target(route, *(before or []), func, *(after or []))
                return func
            return wrapper
        return middle

    for target in targets:
        ret.append(main(target))

    return ret[0] if len(ret) == 1 else ret


def request_logger(req, res, next):
    print(f"* Request: [{req.method}] '{req.url}'")
    next()
