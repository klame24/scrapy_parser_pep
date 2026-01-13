import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    def __init__(self):
        self.results_dir = Path(__file__).parent.parent / 'results'
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.statuss = defaultdict(int)

    def process_item(self, item, spider):
        status = item.get('status')
        if status:
            self.statuss[status] += 1
        return item

    def close_spider(self, spider):
        csv_files = list(Path('.').glob('**/*.csv'))

        if csv_files:
            results_dir = csv_files[0].parent
        else:
            results_dir = Path('results')
            results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{timestamp}.csv'
        file_path = results_dir / filename

        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])

            for status, count in sorted(self.statuss.items()):
                writer.writerow([status, count])

            total = sum(self.statuss.values())
            writer.writerow(['Total', total])
