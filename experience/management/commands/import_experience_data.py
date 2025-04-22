import csv
import os
from django.core.management.base import BaseCommand
from experience.models import TimelineEvent
from datetime import datetime

class Command(BaseCommand):
    help = 'Clean, format, and import experience data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing experience data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

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

                    # 确保日期格式正确（添加20到两位数年份前）
                    if len(event_date) == 6:
                        event_date = '20' + event_date

                    # 验证事件类型
                    valid_event_types = [choice[0].lower() for choice in TimelineEvent.EVENT_TYPES]
                    if event_type.lower() not in valid_event_types:
                        raise ValueError(f"Invalid event type: {event_type}")

                    # 创建 TimelineEvent 实例
                    event = TimelineEvent(
                        event_type=event_type,
                        title=title,
                        description=description,
                        event_date=datetime.strptime(event_date, '%Y%m%d').date(),
                        social_link=social_link,
                    )

                    events_to_create.append(event)

                except Exception as e:
                    invalid_rows.append({'row': row, 'error': str(e)})

            # 批量创建 TimelineEvent 实例
            if events_to_create:
                TimelineEvent.objects.bulk_create(events_to_create)
                self.stdout.write(self.style.SUCCESS(f'成功导入 {len(events_to_create)} 个事件。'))

            # 记录无效行
            if invalid_rows:
                self.stdout.write(self.style.WARNING(f'{len(invalid_rows)} 行因错误而被跳过。'))
                for invalid_row in invalid_rows:
                    self.stdout.write(self.style.ERROR(f"行: {invalid_row['row']} - 错误: {invalid_row['error']}"))