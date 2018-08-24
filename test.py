import jwt
import requests

import conf
import dbutil


origin = 'http://localhost:{}'.format(conf.port)


def describe(message):
    print '-' * 20, message


def post(path, data):
    return requests.post(origin + path, json=data)


def assert_status_code(r, status_code):
    if r.status_code != status_code:
        assert False, 'expect {}, got {} | {}'.format(
            status_code,
            r.status_code,
            repr(r.text),
        )


def assert_user(r, username, has_cookie=True):
    assert_username(user_from_token(r.text), username)
    if has_cookie:
        assert_username(user_from_token(r.cookies.get('token')), username)


def assert_username(user, username):
    actual_username = user.get('username')
    if actual_username != username:
        assert False, 'expect {}, got {}'.format(username, actual_username)


def user_from_token(token):
    try:
        return jwt.decode(token, conf.pubkey, algorithm='RS512')
    except Exception:
        return None


dbutil.remove_user('foo')

describe('register without username and password')
r = post('/register', {})
assert_status_code(r, 400)

describe('register without password')
r = post('/register', {'username': ''})
assert_status_code(r, 400)

describe('register without username')
r = post('/register', {'password': ''})
assert_status_code(r, 400)

describe('register with empty username')
r = post('/register', {'username': '', 'password': ''})
assert_status_code(r, 400)

describe('register with too long username')
r = post('/register', {'username': 'a' * 128, 'password': '?'})
assert_status_code(r, 400)

describe('register with invalid username')
r = post('/register', {'username': '?', 'password': ''})
assert_status_code(r, 400)

describe('register with empty password')
r = post('/register', {'username': 'foo', 'password': ''})
assert_status_code(r, 400)

describe('register with too long password')
r = post('/register', {'username': 'foo', 'password': 'a' * 128})
assert_status_code(r, 400)

describe('valid register')
r = post('/register', {'username': 'foo', 'password': 'foo'})
assert_status_code(r, 200)
assert_user(r, 'foo')

describe('register existing user')
r = post('/register', {'username': 'foo', 'password': 'bar'})
assert_status_code(r, 400)


describe('login without username and password')
r = post('/login', {})
assert_status_code(r, 400)

describe('login without password')
r = post('/login', {'username': ''})
assert_status_code(r, 400)

describe('login without username')
r = post('/login', {'password': ''})
assert_status_code(r, 400)

describe('login with empty username')
r = post('/login', {'username': '', 'password': ''})
assert_status_code(r, 400)

describe('login with too long username')
r = post('/login', {'username': 'a' * 128, 'password': '?'})
assert_status_code(r, 400)

describe('login with invalid username')
r = post('/login', {'username': '?', 'password': ''})
assert_status_code(r, 400)

describe('login with empty password')
r = post('/login', {'username': 'foo', 'password': ''})
assert_status_code(r, 400)

describe('login with too long password')
r = post('/login', {'username': 'foo', 'password': 'a' * 128})
assert_status_code(r, 400)

describe('valid login')
r = post('/login', {'username': 'foo', 'password': 'foo'})
assert_status_code(r, 200)
assert_user(r, 'foo')