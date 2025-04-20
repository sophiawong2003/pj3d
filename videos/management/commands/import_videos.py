import json
from django.core.management.base import BaseCommand
from videos.models import Video  # 假設 Video 是 videos 應用的模型

class Command(BaseCommand):
    help = 'Import videos from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                for item in data:
                    # 假設模型字段與 JSON 鍵匹配
                    Video.objects.create(
                        title=item.get('title', '默認標題'),
                        url=item.get('url', ''),
                        description=item.get('description', '')
                    )
            self.stdout.write(self.style.SUCCESS('Successfully imported videos'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing videos: {e}'))