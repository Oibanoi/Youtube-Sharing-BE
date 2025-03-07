import faker.providers

from tests.faker.user_provider import UserProvider
from tests.faker.video_provider import VideoProvider

fake = faker.Faker()

fake.add_provider(UserProvider)
fake.add_provider(VideoProvider)
