import hashlib
import os
from base64 import b64decode, b64encode


def hash_password(username, pwd, salt=None):
    """Hash username and password, generating salt value if required
    Use PBKDF2 from Beaker

    :returns: base-64 encoded str.
    """
    if salt is None:
        salt = os.urandom(32)

    assert isinstance(salt, bytes)
    assert len(salt) == 32, "Incorrect salt length"

    username = username.encode('utf-8')
    assert isinstance(username, bytes)

    pwd = pwd.encode('utf-8')
    assert isinstance(pwd, bytes)

    cleartext = username + b'\0' + pwd
    h = hashlib.pbkdf2_hmac('sha1', cleartext, salt, 10, dklen=32)

    # 'p' for PBKDF2
    hashed = b'p' + salt + h
    return b64encode(hashed)


def verify_password(username, pwd, salted_hash):
    """Verity username/password pair against a salted hash

    :returns: bool
    """
    assert isinstance(salted_hash, bytes)
    decoded = b64decode(salted_hash)
    hash_type = decoded[0]
    if isinstance(hash_type, int):
        hash_type = chr(hash_type)

    salt = decoded[1:33]

    if hash_type == 'p':  # PBKDF2
        h = hash_password(username, pwd, salt)
        return salted_hash == h

    raise RuntimeError("Unknown hashing algorithm in hash: %r" % decoded)


def login_required(redirect_url=None):
    def _(req, res, next):
        if req.isAuthenticated():
            next()
        else:
            if redirect_url:
                res.redirect(redirect_url)
            else:
                res.sendStatus(401)
    return _


def unauthorized_only(redirect_url=None):
    def _(req, res, next):
        if req.isUnauthenticated():
            next()
        else:
            if redirect_url:
                res.redirect(redirect_url)
            else:
                res.sendStatus(401)
    return _
