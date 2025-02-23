from faker import Faker


async def generate_fake_users(num_users=5):
    fake = Faker()
    users = list()

    for _ in range(num_users):
        username = fake.user_name()
        password = fake.password(length=10)
        email = fake.email()
        users.append(
            {
                "username": username,
                "password": password,
                "email": email,
            }
        )

    return users
