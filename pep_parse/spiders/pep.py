import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_links = response.css(
            'section#numerical-index tbody a::attr(href)').getall()

        for link in pep_links:
            if link and '/pep-' in link:
                yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = response.url.split('/')[-2]
        if number.startswith('pep-'):
            number = number.replace('pep-', '')

        title = response.css('h1.page-title::text').get()
        if title:
            if ' – ' in title:
                name = title.split(' – ', 1)[1].strip()
            elif ' -- ' in title:
                name = title.split(' -- ', 1)[1].strip()
            elif ' - ' in title:
                name = title.split(' - ', 1)[1].strip()
            else:
                name = title.replace(f'PEP {number}', '').strip()
        else:
            name = ''

        status = response.css('dt:contains("Status") + dd::text').get()
        if not status:
            status = response.css('dd abbr::text').get()
        if not status:
            status = response.xpath(
                '//dt[contains(text(), "Status")]'
                '/following-sibling::dd[1]//text()'
            ).get()

        if status:
            status = status.strip()
        else:
            status = 'Unknown'

        yield PepParseItem(
            number=number,
            name=name,
            status=status
        )
