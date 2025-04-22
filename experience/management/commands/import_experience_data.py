import csv
import os
from django.core.management.base import BaseCommand
from experience.models import TimelineEvent
from django.core.files import File
from datetime import datetime
from django.conf import settings  # Import settings to use MEDIA_ROOT

class Command(BaseCommand):
    help = 'Clean, format, and import experience data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing experience data')
        parser.add_argument('--keep-existing', action='store_true', help='Keep existing data in database')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        keep_existing = kwargs.get('keep-existing', False)

        # Clean existing data unless --keep-existing flag is used
        if not keep_existing:
            TimelineEvent.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleaned existing data from database.'))

        # Check if the CSV file exists
        if not os.path.isfile(csv_file):
            self.stdout.write(self.style.ERROR('The specified CSV file does not exist.'))
            return

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            events_to_create = []
            invalid_rows = []

            for row in reader:
                try:
                    # Clean and format data
                    event_type = row.get('event_type', '').strip().lower()
                    title = row.get('title', '').strip()
                    description = row.get('description', '').strip()
                    event_date = row.get('event_date', '').strip()
                    social_link = row.get('social_link', '').strip()

                    # Validate event type
                    valid_event_types = [choice[0] for choice in TimelineEvent.EVENT_TYPES]
                    if event_type not in valid_event_types:
                        raise ValueError(f"Invalid event type: {event_type}")

                    # Validate and attach photos
                    photos = {}
                    for photo_field in ['main_photo', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6']:
                        photo_filename = row.get(photo_field, '').strip()
                        if photo_filename:
                            photo_path = os.path.join(settings.MEDIA_ROOT, 'experience/photos/main', photo_filename)
                            if not os.path.isfile(photo_path):
                                raise FileNotFoundError(f"Photo file '{photo_filename}' not found in '{photo_path}'")
                            photos[photo_field] = photo_path

                    # Create a TimelineEvent instance
                    event = TimelineEvent(
                        event_type=event_type,
                        title=title,
                        description=description,
                        event_date=datetime.strptime(event_date, '%Y%m%d').date(),
                        social_link=social_link,
                    )

                    # Attach photos
                    for photo_field, photo_path in photos.items():
                        with open(photo_path, 'rb') as photo_file:
                            getattr(event, photo_field).save(os.path.basename(photo_path), File(photo_file), save=False)

                    events_to_create.append(event)

                except Exception as e:
                    # Log invalid rows for debugging
                    invalid_rows.append({'row': row, 'error': str(e)})

            # Bulk create TimelineEvent instances
            if events_to_create:
                TimelineEvent.objects.bulk_create(events_to_create)
                self.stdout.write(self.style.SUCCESS(f'{len(events_to_create)} events imported successfully.'))

            # Log invalid rows
            if invalid_rows:
                self.stdout.write(self.style.WARNING(f'{len(invalid_rows)} rows were skipped due to errors.'))
                for invalid_row in invalid_rows:
                    self.stdout.write(self.style.ERROR(f"Row: {invalid_row['row']} - Error: {invalid_row['error']}"))