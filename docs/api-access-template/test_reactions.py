from api import ApiAccessor

api = ApiAccessor()

# The following code creates 10000 planned reactions for performance testing

for profile in range(20, 2000):
    for post_offset in range(0, 5):
        target_profile = profile - (profile % 7)
        reaction_id = api.create_like(profile, target_profile, 15, post_offset)

        print(f"created like {reaction_id} on profile {profile}, target: {target_profile}, offset: {post_offset}")

