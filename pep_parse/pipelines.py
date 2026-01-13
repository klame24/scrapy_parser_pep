import csv
from collections import defaultdict
from datetime import datetime
from pep_parse.settings import RESULTS, BASE_DIR


class PepParsePipeline:
    def __init__(self):
        self.results_dir = BASE_DIR / RESULTS
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.status_count = defaultdict(int)

    def process_item(self, item, spider):
        status = item.get('status')
        if status:
            self.status_count[status] += 1
        return item

    def close_spider(self, spider):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{timestamp}.csv'
        file_path = self.results_dir / filename

        data_to_write = [
            ['Статус', 'Количество'],
            *sorted(self.status_count.items()),
            ['Total', sum(self.status_count.values())]
        ]

        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data_to_write)
