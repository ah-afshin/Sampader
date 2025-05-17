from asyncio import run
from models import init_models



init_models()

ahafshin_token: str


async def test_auth_service():
    from services.auth_service import register_user
    done1, msg1 = await register_user("ahafshin", "afshin@email.com", "418", "afshin", "hello world!")
    done2, msg2 = await register_user("iigames", "ilia@email.com", "11", "ilia soli", "hi there!")
    done3, msg3 = await register_user("ahafshin", "afshin@email.com", "418", "afshin", "hello world!")

    assert done1 is True
    assert done2 is True
    assert done3 is False
    print(msg1)
    print(msg2)
    print(msg3)
    
    from services.auth_service import login_user
    token1 = await login_user("ahafshin", "488")
    print(token1 is None)
    token2 = await login_user("iigames", "11")
    token3 = await login_user("ahafshin", "418")
    print(token2)
    print(token3)
    global ahafshin_token
    ahafshin_token = token3


async def test_user_service():
    from services.user_service import get_by_userid, get_by_username
    from core.dependencies import get_current_user
    global ahafshin_token
    aha_by_name = await get_by_username("ahafshin")
    assert aha_by_name is not None
    print(aha_by_name)
    token_id = await get_current_user(ahafshin_token)
    aha_by_id = await get_by_userid(token_id)
    print(aha_by_id)

    from services.user_service import search_user
    u_list = await search_user("afshin")
    print(u_list)

    from services.user_service import update_user_profile
    done = await update_user_profile(token_id, bio="hello sampader!")
    assert done is True


async def test_follow_block_service():
    from services.user_service import get_by_username

    from services.user_service import follow_user
    from services.user_service import is_user_followed
    from services.user_service import unfollow_user
    iigames = await get_by_username("iigames")
    ahafshin = await get_by_username("ahafshin")
    done = await follow_user(ahafshin.userID, iigames.userID)
    assert done is True
    is_it = await is_user_followed(ahafshin.userID, iigames.userID)
    assert is_it is True
    done = await unfollow_user(ahafshin.userID, iigames.userID)
    assert done is True
    is_it = await is_user_followed(ahafshin.userID, iigames.userID)
    assert is_it is False

    from services.user_service import block_user
    from services.user_service import is_user_blocked
    from services.user_service import unblock_user
    iigames = await get_by_username("iigames")
    ahafshin = await get_by_username("ahafshin")
    done = await block_user(ahafshin.userID, iigames.userID)
    assert done is True
    is_it = await is_user_blocked(ahafshin.userID, iigames.userID)
    assert is_it is True
    done = await unblock_user(ahafshin.userID, iigames.userID)
    assert done is True
    is_it = await is_user_blocked(ahafshin.userID, iigames.userID)
    assert is_it is False


async def test_post_service():
    from services.user_service import get_by_username
    iigames = await get_by_username("iigames")
    ahafshin = await get_by_username("ahafshin")
    
    # post
    from services.post_service import new_post, find_post, get_users_posts
    p1 = await new_post(ahafshin.userID, "my first post!")
    assert p1 is not None
    print(p1)
    p2 = await new_post(ahafshin.userID, "my second post!")
    assert p2 is not None
    print(p2)
    res = await find_post(p1.postID)
    print(res)
    print(p1)
    assert res == p1
    res = await get_users_posts(ahafshin.userID)
    print(res)
    
    # like
    
    # comment


async def test_notif_service():
    ...


async def test_home_service():
    ...


async def test_search_service():
    ...



if __name__=="__main__":
    # run(test_auth_service())
    # run(test_user_service())
    # run(test_follow_block_service())
    run(test_post_service())
    # run(test_notif_service())
    # run(test_home_service())
    # run(test_search_service())
