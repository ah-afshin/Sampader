async def test_signin():
    from services import register_user
    _, token = await register_user("ahafshin", "a.h.afshin@email.com", "1234", "afshin", "hello world!")
    print(token)
    _, token = await register_user("iigames", "ilia.sol@email.com", "0000", "ilia", "hi!")
    print(token)

token = ""

async def test_login():
    from services import login_user
    global token
    token = await login_user("ahafshin", "1234")
    print(token)


async def test_get_current_user():
    from core.dependencies import get_current_user
    global token
    uid = await get_current_user(token)
    print("kos", uid)
    
    from services import get_by_userid
    u = await get_by_userid(uid)
    print(u)

    from services import get_by_username
    u2 = await get_by_username(u.username)
    print(u2.username)

async def test_follow():
    from services import follow
