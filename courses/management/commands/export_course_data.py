import csv
from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand):
    help = 'Export course data from the database to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to save the exported data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Get all Course objects
        courses = Course.objects.all()

        # Define the CSV headers
        headers = [
            'tutor', 'title', 'coursecode', 'topic', 'description', 'studentreq',
            'coursefee', 'classsize', 'durationhr', 'list_date', 'photo_main'
        ]

        # Write data to the CSV file
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write the header row

            for course in courses:
                writer.writerow([
                    course.tutor.name if course.tutor else '',
                    course.title,
                    course.coursecode,
                    course.topic,
                    course.description,
                    course.studentreq,
                    course.coursefee,
                    course.classsize,
                    course.durationhr,
                    course.list_date.strftime('%Y-%m-%d %H:%M:%S') if course.list_date else '',
                    course.photo_main.name if course.photo_main else '',
                ])

        self.stdout.write(self.style.SUCCESS(f'Data successfully exported to {csv_file}'))