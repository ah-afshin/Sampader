import db

# print(db.user.new_user("ahafshin", "whatever", "afshin", "hello!", "a.jpg", "b.jpg", "202", "pass"))
# print(db.user.new_user("mhk488", "mmd", "mamad", "hi!", "a.jpg", "b.jpg", "201", "password"))

aha = db.user.get_user_by_username("ahafshin")
mmd = db.user.get_user_by_username("mhk488")
# print(aha.name, mmd.name)

# print(db.user.follow(aha.userID, mmd.userID))
# print(db.user.unfollow(aha.userID, mmd.userID))

# print(db.user.is_followed(aha.userID, mmd.userID))
# print(db.user.is_followed(mmd.userID, aha.userID))
# print([i.username for i in db.user.followers(mmd.userID)])

# print(db.post.new_post(aha.userID, "hello world!"))
# print(aha.posts[0].author.username)
# print(db.post.get_post("06a863e1-1eff-4bc4-88e0-9acf0abcd877").author)
# p = aha.posts[0]
# print(db.post.add_like(aha.userID, p.postID))
# print(db.post.is_liked(aha.userID, p.postID))
# print(db.post.get_post_likes(p.postID))
# print(db.post.remove_like(aha.userID, p.postID))
# print(db.post.is_liked(aha.userID, p.postID))
# print(db.post.get_post_likes(p.postID))

print(db.user.block(aha.userID, mmd.userID))
print(db.user.is_blocked(aha.userID, mmd.userID))
print(db.user.unblock(aha.userID, mmd.userID))