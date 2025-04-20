from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile for users without one'

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}'))
        self.stdout.write(self.style.SUCCESS('Profile creation completed'))