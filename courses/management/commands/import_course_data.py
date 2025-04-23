import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from courses.models import Course, Tutor

class Command(BaseCommand):
    help = 'Import Course data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Check if the CSV file exists
        if not os.path.isfile(csv_file):
            self.stdout.write(self.style.ERROR('The specified CSV file does not exist.'))
            return

        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            courses_to_create = []
            
            for row in reader:
                # Print headers to see available columns
                if reader.line_num == 1:
                    self.stdout.write(f"Available columns: {', '.join(reader.fieldnames)}")
                
                # Get the tutor based on their name (assuming 'Tutor' or 'TutorName' in CSV)
                tutor_name = row.get('tutor') 
                if tutor_name:
                    tutor = Tutor.objects.filter(name=tutor_name).first()
                else:
                    tutor = None

                # Create a Course instance
                course = Course(
                    tutor=tutor,
                    title=row['title'],
                    coursecode=row['coursecode'],
                    topic=row['topic'],  # Ensure topic is a valid choice
                    description=row['description'],
                    studentreq=row['studentreq'],
                    coursefee=int(row['coursefee']),
                    classsize=int(row['classsize']),
                    durationhr=float(row['durationhr']),  # Convert to float
                    list_date=datetime.now()  # Default to now
                )

                courses_to_create.append(course)

            # Bulk create Course instances
            if courses_to_create:  # Check if there are courses to create
                Course.objects.bulk_create(courses_to_create)
        
        self.stdout.write(self.style.SUCCESS(f'{len(courses_to_create)} Courses imported successfully.'))