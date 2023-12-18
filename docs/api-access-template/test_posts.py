from api import ApiAccessor
from datetime import datetime

api = ApiAccessor()

# the following code creates 10000 posts for performance testing

for profile in range(20, 2000):
    for post in range(5):
        post_id = api.create_post(profile, datetime.now().timestamp(), f"Post {post + 1} from profile {profile}", image_path=None)

        print(f"created post {post} for profile {profile} with id {post_id}")

        # api.create_like_on_existing_post(profile - 1, 15, post_id)
        # api.create_like_on_existing_post(profile - 2, 15, post_id)
        # api.create_like_on_existing_post(profile - 3, 15, post_id)

