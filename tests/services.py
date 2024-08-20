import services as s


print(s.new_user("ahafshin", "whatever", "afshin", "hello!", "a.jpg", "b.jpg", "202", "pass"))
print(s.new_user("mhk488", "mmd", "mamad", "hi!", "a.jpg", "b.jpg", "201", "password"))

aha = s.get_user_by_username("ahafshin")
mmd = s.get_user_by_username("mhk488")
print("users were created: ", aha, mmd)

print()
print("following: ", s.follow(aha.userID, mmd.userID))
print(s.is_followed(aha.userID, mmd.userID))
print(s.is_followed(mmd.userID, aha.userID))
print([i.username for i in s.followers(mmd.userID)])

print()
print("unfollowing: ", s.unfollow(aha.userID, mmd.userID))
print(s.is_followed(aha.userID, mmd.userID))
print(s.is_followed(mmd.userID, aha.userID))
print([i.username for i in s.followers(mmd.userID)])

print()
print("new post: ", s.new_post(aha.userID, "hello world!"))
print(aha.posts[0].author.username)
p = aha.posts[0]

print()
print("like: ", s.add_like(aha.userID, p.postID))
print(s.is_liked(aha.userID, p.postID))
print(s.get_post_likes(p.postID))
print(s.get_user_likes(aha.userID))
print(s.remove_like(aha.userID, p.postID))
print(s.is_liked(aha.userID, p.postID))
print(s.get_post_likes(p.postID))

print()
print(s.new_post(aha.userID, "this is a comment", p.postID, "c.jpg"))
print(s.get_comments(p.postID))
print(s.new_post(aha.userID, "this is second comment", p.postID))
c = s.get_comments(p.postID)[1]
print(s.add_like(mmd.userID, c.postID))
print(s.get_comments(p.postID)[0].text)


print()
print("to block: ", s.block(aha.userID, mmd.userID))
print(s.is_blocked(aha.userID, mmd.userID))
print(s.unblock(aha.userID, mmd.userID))
print(s.is_blocked(aha.userID, mmd.userID))

print()
print(s.check_user(aha.username, "pass"))
print(s.update_password(aha.userID, "new_pass"))
print(s.check_user(aha.username, "pass"))
print(s.check_user(aha.username, "new_pass"))

print()
print()
print("these things should not work:")
# testing results with invalid inputs: what if we pass our functions some bullshit?
print(s.get_user_by_username("bullshit"))
print(s.new_post("bullshit", "hi there"))
# it's not a bug, it's a feature :)
print(s.new_post(mmd.userID, "wassup?", parentID="bullshit"))
print(s.add_like("bullshit", p.postID))
print(s.add_like(aha.userID, "cfyscfiunfvg"))
print(s.follow("bullshit", mmd.userID))
print(s.block("bullshit", mmd.userID))
print(s.follow(aha.userID, "bullshit"))
print(s.block(aha.userID, "bullshit"))
print(s.is_blocked("bullshit", mmd.userID))
print(s.is_blocked(aha.userID, "bullshit"))
print(s.is_followed("bullshit", mmd.userID))
print(s.is_followed(aha.userID, "bullshit"))
print(s.get_post_likes("bullshit"))
# it's not a bug, it's a feature :)
print(s.new_post(aha.userID, "this content does not exist", contents="bullshit"))

print()
print(s.delete_post(p.postID))
