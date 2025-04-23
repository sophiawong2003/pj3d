import csv
import os
from django.core.management.base import BaseCommand
from experience.models import TimelineEvent
from django.conf import settings

class Command(BaseCommand):
    help = 'Export experience data from the database to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to save the exported data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Get all TimelineEvent objects
        events = TimelineEvent.objects.all()

        # Define the CSV headers
        headers = [
            'event_type', 'title', 'description', 'event_date', 'social_link',
            'main_photo', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6'
        ]

        # Write data to the CSV file
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write the header row

            for event in events:
                writer.writerow([
                    event.event_type,
                    event.title,
                    event.description,
                    event.event_date.strftime('%Y%m%d') if event.event_date else '',
                    event.social_link,
                    event.main_photo.name if event.main_photo else '',
                    event.photo_1.name if event.photo_1 else '',
                    event.photo_2.name if event.photo_2 else '',
                    event.photo_3.name if event.photo_3 else '',
                    event.photo_4.name if event.photo_4 else '',
                    event.photo_5.name if event.photo_5 else '',
                    event.photo_6.name if event.photo_6 else '',
                ])

        self.stdout.write(self.style.SUCCESS(f'Data successfully exported to {csv_file}'))