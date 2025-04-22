from django.core.management.base import BaseCommand
import csv
import os
from datetime import datetime
from experience.models import TimelineEvent

class Command(BaseCommand):
    help = 'Import timeline events from CSV file'

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
                # Convert date string to date object
                event_date = datetime.strptime(row['event_date'], '%Y%m%d').date()
                
                TimelineEvent.objects.get_or_create(
                    title=row['title'],
                    description=row['description'],
                    event_date=event_date,
                    event_type=row['event_type'].lower(),
                    social_link=row['social_link'],
                    defaults={
                        'main_photo': row['main_photo']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported timeline events from CSV'))

        # python manage.py import_timeline_events c:\pj3d\GetDataImport\ExperienceData4.csv
        # run this command to import timeline events from CSV file