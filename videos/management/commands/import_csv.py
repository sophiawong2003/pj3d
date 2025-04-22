import csv
from django.core.management.base import BaseCommand
from videos.models import Video
import os

class Command(BaseCommand):
    help = 'Import videos from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        if not os.path.isfile(csv_file):
            self.stdout.write(self.style.ERROR('The specified CSV file does not exist.'))
            return
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Video.objects.get_or_create(
                    title=row.get('title', '默認標題'),
                    youtube_url=row.get('url', ''),
                    description=row.get('description', '')
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported videos from CSV'))