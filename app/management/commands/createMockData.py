import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from app.models import Pomodoro, Tag, UserSettings, Rewards


MOCK_USERS = [
    {"username": "alice_dev", "tags": ["coding", "review", "design", "reading"]},
    {"username": "bob_learns", "tags": ["study", "math", "writing", "exercise"]},
    {"username": "carol_work", "tags": ["meetings", "planning", "deep-work", "emails"]},
]


class Command(BaseCommand):
    help = "Create mock users with random pomodoros for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max-pomos",
            type=int,
            default=300,
            help="Maximum pomodoros per user (default: 300)",
        )

    def handle(self, *args, **options):
        max_pomos = options["max_pomos"]
        now = timezone.now()

        for mock in MOCK_USERS:
            username = mock["username"]
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(username=username, password="testpass123!")
                UserSettings.objects.create(user=user)
                Rewards.objects.create(user=user)

            tags = []
            for tag_name in mock["tags"]:
                tag, _ = Tag.objects.get_or_create(tag=tag_name)
                tags.append(tag)

            num_pomos = random.randint(max_pomos // 2, max_pomos)
            pomodoros = []
            for _ in range(num_pomos):
                days_ago = random.randint(0, 365)
                hour = random.randint(6, 23)
                minute = random.randint(0, 59)
                dt = now - timedelta(days=days_ago, hours=hour, minutes=minute)
                pomodoros.append(
                    Pomodoro(user=user, tag=random.choice(tags), datetime=dt)
                )

            Pomodoro.objects.bulk_create(pomodoros)
            self.stdout.write(f"Created '{username}' with {num_pomos} pomodoros.")

        self.stdout.write(self.style.SUCCESS("Done!"))

