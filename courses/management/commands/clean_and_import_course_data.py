import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from courses.models import Course, Tutor
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = 'Clean, format, and import course data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing course data')
        parser.add_argument('--keep-existing', action='store_true', help='Keep existing data in database')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        keep_existing = kwargs.get('keep-existing', False)

        # Clean existing data unless --keep-existing flag is used
        if not keep_existing:
            Course.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleaned existing course data from database.'))

        # Check if the CSV file exists
        if not os.path.isfile(csv_file):
            self.stdout.write(self.style.ERROR('The specified CSV file does not exist.'))
            return

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            courses_to_create = []
            invalid_rows = []

            for row in reader:
                try:
                    # Clean and format data
                    tutor_name = row.get('tutor', '').strip()
                    title = row.get('title', '').strip()
                    coursecode = row.get('coursecode', '').strip()
                    topic = row.get('topic', '').strip().lower()  # Normalize topic to lowercase
                    description = row.get('description', '').strip()
                    studentreq = row.get('studentreq', '').strip()
                    # Clean and format coursefee (remove '$' and ',' characters)
                    coursefee_str = row.get('coursefee', '0').strip().replace('$', '').replace(',', '')
                    coursefee = int(coursefee_str) if coursefee_str else 0
                    classsize = int(row.get('classsize', 0))  # Default to 0 if empty
                    durationhr = float(row.get('durationhr', 0.0))  # Default to 0.0 if empty

                    # Validate topic (ensure it's a valid choice)
                    valid_topics = [choice[0] for choice in Course._meta.get_field('topic').choices]
                    if topic not in valid_topics:
                        raise ValueError(f"Invalid topic: {topic}")

                    # Get or create the tutor
                    tutor = None
                    if tutor_name:
                        tutor, _ = Tutor.objects.get_or_create(name=tutor_name)

                    # Handle photo fields
                    photos = {}
                    for photo_field in ['photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6']:
                        photo_filename = row.get(photo_field, '').strip()
                        if photo_filename:
                            photo_path = os.path.join(settings.MEDIA_ROOT, 'photos/courses', photo_filename)
                            if not os.path.isfile(photo_path):
                                raise FileNotFoundError(f"Photo file '{photo_filename}' not found in '{photo_path}'")
                            photos[photo_field] = photo_path

                    # Create Course instance with cleaned coursefee
                    course = Course(
                        tutor=tutor,
                        title=title,
                        coursecode=coursecode,
                        topic=topic,
                        description=description,
                        studentreq=studentreq,
                        coursefee=coursefee,  # Only include coursefee once
                        classsize=classsize,
                        durationhr=durationhr,
                        list_date=datetime.now()
                    )

                    # Attach photos
                    for photo_field, photo_path in photos.items():
                        with open(photo_path, 'rb') as photo_file:
                            getattr(course, photo_field).save(
                                os.path.basename(photo_path),
                                File(photo_file),
                                save=False
                            )

                    courses_to_create.append(course)

                except Exception as e:
                    invalid_rows.append({'row': row, 'error': str(e)})

            # Bulk create Course instances
            if courses_to_create:
                Course.objects.bulk_create(courses_to_create)
                self.stdout.write(self.style.SUCCESS(f'{len(courses_to_create)} courses imported successfully.'))

            # Log invalid rows
            if invalid_rows:
                self.stdout.write(self.style.WARNING(f'{len(invalid_rows)} rows were skipped due to errors.'))
                for invalid_row in invalid_rows:
                    self.stdout.write(self.style.ERROR(f"Row: {invalid_row['row']} - Error: {invalid_row['error']}"))