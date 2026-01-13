import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        pep_links = response.css(
            'tbody tr a[href^="pep-"]::attr(href)').getall()

        for link in pep_links:
            if link:
                yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = response.url.rstrip('/').split('/')[-1]
        if number.startswith('pep-'):
            number = number.replace('pep-', '')

        title_text = response.css('h1.page-title::text').get()

        parts = title_text.split()
        if len(parts) >= 3 and parts[0] == 'PEP':
            name_parts = parts[2:]
            name = ' '.join(name_parts).strip()

            separators = ['–', '--', '-', ':']
            for sep in separators:
                if name.startswith(sep):
                    name = name[len(sep):].strip()

        status = response.css('dt:contains("Status") + dd abbr::text').get()
        if not status:
            status = response.css('dt:contains("Status") + dd::text').get()

        if status:
            status = status.strip()
        else:
            status = 'Unknown'

        yield PepParseItem(
            number=number,
            name=name,
            status=status
        )
