import json
import os
import random
import lorem

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

from post.models import Post


with open("config.json", "r") as config_file:
    config = json.load(config_file)

number_of_users = config.get("number_of_users")
max_posts_per_user = config.get("max_posts_per_user")
max_likes_per_user = config.get("max_likes_per_user")


def signup_users():
    for user_id in range(1, number_of_users + 1):
        username = f"user_{user_id}"
        email = f"user_{user_id}@example.com"
        password = "password"

        if not get_user_model().objects.filter(email=email).exists():
            get_user_model().objects.create_user(username=username, email=email, password=password)


def generate_content():
    return lorem.paragraph()


def create_posts():
    users = get_user_model().objects.all()
    for user in users:
        for _ in range(random.randint(1, max_posts_per_user)):
            content = generate_content()
            Post.objects.create(user=user, content=content)


def like_posts():
    users = get_user_model().objects.all()
    for user in users:
        liked_posts = random.sample(
            list(Post.objects.all()), random.randint(1, max_likes_per_user)
        )
        user.liked_posts.set(liked_posts)


if __name__ == "__main__":
    signup_users()
    create_posts()
    like_posts()
