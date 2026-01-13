import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    def __init__(self):
        self.status_count = defaultdict(int)
        self.results_dir = None

    def open_spider(self, spider):

        feeds = spider.crawler.settings.getdict('FEEDS', {})

        for feed_path in feeds.keys():
            if isinstance(feed_path, (str, Path)):
                feed_path_obj = Path(
                    feed_path) if isinstance(feed_path, str) else feed_path
                if feed_path_obj.parent.name == 'results':
                    self.results_dir = feed_path_obj.parent
                    break
        if self.results_dir is None:
            self.results_dir = Path('results')
        self.results_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        status = item.get('status')
        if status:
            self.status_count[status] += 1
        return item

    def close_spider(self, spider):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'status_summary_{timestamp}.csv'
        file_path = self.results_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])

            for status, count in sorted(self.status_count.items()):
                writer.writerow([status, count])

            total = sum(self.status_count.values())
            writer.writerow(['Total', total])
