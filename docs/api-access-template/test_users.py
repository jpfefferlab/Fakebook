from api import ApiAccessor

api = ApiAccessor()

# The following code creates 2000 users and relationships between them for performance testing

for i in range(0, 2000):
    profile_id = api.create_user(f"apiTestUser{i}", "test", f"test{i}@example.com", f"TestUser{i}")

    print("created user", profile_id)


for i in range(10, 1997):
    if i % 7 == 0:
        for j in range(i+1, i+7):
            api.create_relationship(profile_id_1=i, profile_id_2=j)
            print(f"created friendship between {i} and {j}")

