import csv
import os
from django.core.management.base import BaseCommand
from tutors.models import Tutor
from django.db import models
from datetime import datetime

class Command(BaseCommand):
    help = 'Import Tutor data from CSV file excluding the photo'

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
            tutors_to_create = []
            
            for row in reader:
                # Create a Tutor instance excluding the photo field
                tutor = Tutor(
                    name=row['name'],
                    description=row['description'],
                    phone=row['phone'],
                    email=row['email'],
                    hire_date = models.DateTimeField(auto_now_add=True),
                
                )

                tutors_to_create.append(tutor)

            # Bulk create Tutor instances
            if tutors_to_create:  # Check if there are tutors to create
                Tutor.objects.bulk_create(tutors_to_create)
        
        self.stdout.write(self.style.SUCCESS(f'{len(tutors_to_create)} Tutors imported successfully.'))      