import requests

from datetime import datetime, timedelta

LOCALHOST_URL = "http://localhost:8000/api"
DEFAULT_TOKEN = "changeme"

# This code can be used as a template to interact with the management API.
# It contains methods that execute the available HTTP requests against the Fakebook management API.
# It does not implement the full API, it's missing support for binary data like images on the user creation route.
# An implementation of the /advertisement route is also MISSING!

class ApiAccessor:

    base_url: str
    token: str

    def __init__(self, base_url: str = LOCALHOST_URL, token: str = DEFAULT_TOKEN) -> None:
        self.base_url = base_url
        self.token = token

    def request(self, method: str, route: str, files=None, **params) -> requests.Response:
        url = f"{self.base_url}{route}"
        
        params_present = False

        for p in params:
            url += "?" if not params_present else "&"
            params_present = True

            url += f"{p}={params[p]}"

        response = requests.request(method, url, headers={ "Token": self.token }, files=files)

        if response.status_code != 200:
            raise Exception("Returned non-OK status code", route, response.status_code, response.text)
        
        return response



    def create_user(self, username: str, password: str, email: str, display_name: str) -> int:
        response = self.request("POST", "/user", username=username, password=password, email=email, firstName=display_name)
        return response.json()["profileId"]


    def create_relationship(self, profile_id_1: int, profile_id_2: int) -> None:
        self.request("POST", "/profile/relationship", profileId1=profile_id_1, profileId2=profile_id_2)
    
    
    def create_post(self, profile_id: int, created: str, content: str, image_path: str) -> int:
        image = {"image": open(image_path, "rb")} if image_path is not None else None

        response = self.request("POST", "/profile/post", files=image, profileId=profile_id, created=created, content=content)
        return response.json()["postId"]
    
    def create_like(self, profile_id: int, target_id: int, time_delta_min: int, post_offset: int):
        time_delta_secs = time_delta_min * 60
        
        response = self.request("POST", "/profile/post/reaction", profileId=profile_id, type="Like", timeDelta=time_delta_secs, targetProfileId=target_id, postOffset=post_offset)
        return response.json()["plannedReactionId"]

    def create_like_on_existing_post(self, profile_id: int, time_delta_min: int, post_id: int):
        time_delta_secs = time_delta_min * 60
        
        response = self.request("POST", "/profile/post/reaction", profileId=profile_id, type="Like", timeDelta=time_delta_secs, postId=post_id)
        return response.json()["plannedReactionId"]
