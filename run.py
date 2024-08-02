import db

# print(db.user.new_user("ahafshin", "a.h.afshin@mowz.com", "afshin", "mowz", "a.jpg", "b.jpg", "202", "meg"))
# print(db.user.new_user("mhk448", "mhk@mowz.com", "mamad", "xxx", "a.jpg", "b.jpg", "202", "nerd"))
# print(db.user.new_user("ahafshin", "a.h.afshin@mowz.com", "afshin", "mowz", "a.jpg", "b.jpg", "202", "meg"))
# print(db.user.new_user("iigames", "iigames@mowz.com", "ilia", "fff", "a.jpg", "b.jpg", "201", "hacker"))
# print(db.user.check_user("ahafshin", "meg"))
# print(db.user.get_user_by_username("mhk448"))
# print(db.user.search_user("mmd"))

# print(db.block.block("46645e7d-06e2-45d1-a482-e0d8927e68cc", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.block.is_blocked("46645e7d-06e2-45d1-a482-e0d8927e68cc", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.block.unblock("46645e7d-06e2-45d1-a482-e0d8927e68cc", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.block.is_blocked("46645e7d-06e2-45d1-a482-e0d8927e68cc", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))

# print(db.follow.follow("46645e7d-06e2-45d1-a482-e0d8927e68cc", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.follow.follow("46645e7d-06e2-45d1-a482-e0d8927e68cc", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.follow.follow("8be04094-d80c-4020-9ee0-df4d3e5e6923", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.follow.is_followed("8be04094-d80c-4020-9ee0-df4d3e5e6923", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.follow.unfollow("8be04094-d80c-4020-9ee0-df4d3e5e6923", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.follow.is_followed("8be04094-d80c-4020-9ee0-df4d3e5e6923", "7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.follow.followers("46645e7d-06e2-45d1-a482-e0d8927e68cc"))
# print(db.follow.followers("7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))
# print(db.follow.followings("46645e7d-06e2-45d1-a482-e0d8927e68cc"))
# print(db.follow.followings("7d7fcff0-2e02-42e5-89be-7d5ac21797b3"))

# print(db.post.new_post("0a818810-0342-4c39-b48c-6ed913f577b4", "hello world"))
# print(db.post.get_last_posts(3))
# print(db.post.get_users_posts("0a818810-0342-4c39-b48c-6ed913f577b4"))
# print(db.post.get_users_last_posts("0a818810-0342-4c39-b48c-6ed913f577b4", 1))
# print(db.post.get_post("eb81c9c6-243f-4737-b0ea-1e5cc17e8dd9").text)
# print(db.post.new_post("0a818810-0342-4c39-b48c-6ed913f577b4", "1st post"))
# print(db.post.new_post("0a818810-0342-4c39-b48c-6ed913f577b4", "2nd post"))
# print(db.post.new_post("0a818810-0342-4c39-b48c-6ed913f577b4", "3rd post"))
# print(db.post.new_post("0a818810-0342-4c39-b48c-6ed913f577b4", "4th post"))
# print(db.post.new_post("0a818810-0342-4c39-b48c-6ed913f577b4", "5th post"))
# print(db.post.delete_post("eb81c9c6-243f-4737-b0ea-1e5cc17e8dd9"))
# print(db.post.delete_post("4e256b35-9be8-4e40-9447-8ef6cb834ad5"))
# print(db.post.delete_post("4bafa72f-49af-4611-a30c-e27d4d197425"))
# print(db.post.delete_post("f09b6be8-d587-4e09-a1bd-785e43f87f05"))
# print(db.post.delete_post("91aca372-4319-402c-8fec-79743ddce752"))
# print(db.post.delete_post("d58f349a-0c40-485a-91e3-fe66d4dac56a"))
# print(list(map(
#     lambda a: a.text,
#     db.post.get_last_posts(3)
# )))
# print(list(map(
#     lambda a: a.text,
#     db.post.get_users_last_posts("0a818810-0342-4c39-b48c-6ed913f577b4", 4)
# )))

# print(db.post.new_post("xxxx", "hello world"))


# print(db.like.add_like("me", "somepost"))
# print(db.like.is_liked("me", "somepost"))
# print(db.like.add_like("me", "somepost"))
print(db.like.remove_like("me", "somepost"))
print(db.like.is_liked("me", "somepost"))
print(db.like.add_like("me", "somepost"))
print(db.like.get_user_likes("me"))
print(db.like.get_post_likes("somepost"))