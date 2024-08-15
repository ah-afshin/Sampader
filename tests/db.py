import db

print(db.user.new_user("ahafshin", "whatever", "afshin", "hello!", "a.jpg", "b.jpg", "202", "pass"))
print(db.user.new_user("mhk488", "mmd", "mamad", "hi!", "a.jpg", "b.jpg", "201", "password"))

aha = db.user.get_user_by_username("ahafshin")
mmd = db.user.get_user_by_username("mhk488")
print("users were created: ", aha, mmd)

print()
print("following: ", db.user.follow(aha.userID, mmd.userID))
print(db.user.is_followed(aha.userID, mmd.userID))
print(db.user.is_followed(mmd.userID, aha.userID))
print([i.username for i in db.user.followers(mmd.userID)])

print()
print("unfollowing: ", db.user.unfollow(aha.userID, mmd.userID))
print(db.user.is_followed(aha.userID, mmd.userID))
print(db.user.is_followed(mmd.userID, aha.userID))
print([i.username for i in db.user.followers(mmd.userID)])

print()
print("new post: ", db.post.new_post(aha.userID, "hello world!"))
print(aha.posts[0].author.username)
p = aha.posts[0]

print()
print("like: ", db.post.add_like(aha.userID, p.postID))
print(db.post.is_liked(aha.userID, p.postID))
print(db.post.get_post_likes(p.postID))
print(db.user.get_user_likes(aha.userID))
print(db.post.remove_like(aha.userID, p.postID))
print(db.post.is_liked(aha.userID, p.postID))
print(db.post.get_post_likes(p.postID))

print()
print(db.post.new_post(aha.userID, "this is a comment", p.postID, "c.jpg"))
print(db.post.get_comments(p.postID))
print(db.post.new_post(aha.userID, "this is second comment", p.postID))
c = db.post.get_comments(p.postID)[1]
print(db.post.add_like(mmd.userID, c.postID))
print(db.post.get_comments(p.postID)[0].text)


print()
print("to block: ", db.user.block(aha.userID, mmd.userID))
print(db.user.is_blocked(aha.userID, mmd.userID))
print(db.user.unblock(aha.userID, mmd.userID))
print(db.user.is_blocked(aha.userID, mmd.userID))

print()
print(db.user.check_user(aha.username, "pass"))
print(db.user.update_password(aha.userID, "new_pass"))
print(db.user.check_user(aha.username, "pass"))
print(db.user.check_user(aha.username, "new_pass"))

print()
print()
print("these things should not work:")
# testing results with invalid inputs: what if we pass our functions some bullshit?
print(db.user.get_user_by_username("bullshit"))
print(db.post.new_post("bullshit", "hi there"))
# it's not a bug, it's a feature :)
print(db.post.new_post(mmd.userID, "wassup?", parentID="bullshit"))
print(db.post.add_like("bullshit", p.postID))
print(db.post.add_like(aha.userID, "cfyscfiunfvg"))
print(db.user.follow("bullshit", mmd.userID))
print(db.user.block("bullshit", mmd.userID))
print(db.user.follow(aha.userID, "bullshit"))
print(db.user.block(aha.userID, "bullshit"))
print(db.user.is_blocked("bullshit", mmd.userID))
print(db.user.is_blocked(aha.userID, "bullshit"))
print(db.user.is_followed("bullshit", mmd.userID))
print(db.user.is_followed(aha.userID, "bullshit"))
print(db.post.get_post_likes("bullshit"))
# it's not a bug, it's a feature :)
print(db.post.new_post(aha.userID, "this content does not exist", contents="bullshit"))

print()
print(db.post.delete_post(p.postID))