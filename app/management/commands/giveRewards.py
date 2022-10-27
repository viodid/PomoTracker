from django.core.management.base import  BaseCommand
from app.models import Rewards, SlicePomodoros, User


class Command(BaseCommand):
    help = 'Check every month\'s first day who are the winners in the leaderboard.'

    def handle(self, *args, **options):

        slice_pomodoro_users = []
        for user in User.objects.all():
            pomodoros = SlicePomodoros(user.pomodoros, user)
            slice_pomodoro_users.append(pomodoros)

        month = sorted(slice_pomodoro_users, key=lambda pomos: pomos.month.count(), reverse=True)

        if len(month) > 3:
            first = Rewards.objects.get(user=month[0].user)
            first.gold += 1
            first.save()
            second = Rewards.objects.get(user=month[1].user)
            second.silver += 1
            second.save()
            third = Rewards.objects.get(user=month[2].user)
            third.bronze += 1
            third.save()
            self.stdout.write('Done!')
            return None

        self.stdout.write('Not enough participants!')
        return None

