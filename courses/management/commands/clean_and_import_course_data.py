import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from courses.models import Course, Tutor

class Command(BaseCommand):
    help = 'Clean, format, and import course data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing course data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

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
                    coursefee = int(row.get('coursefee', 0))  # Default to 0 if empty
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

                    # Create a Course instance
                    course = Course(
                        tutor=tutor,
                        title=title,
                        coursecode=coursecode,
                        topic=topic,
                        description=description,
                        studentreq=studentreq,
                        coursefee=coursefee,
                        classsize=classsize,
                        durationhr=durationhr,
                        list_date=datetime.now()  # Default to now
                    )
                    courses_to_create.append(course)

                except Exception as e:
                    # Log invalid rows for debugging
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