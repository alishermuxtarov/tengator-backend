from datetime import date, timedelta

from django.core.files.base import ContentFile
from django.core.management import base

from grab import Grab

from aggregator import models, utils


class Command(base.BaseCommand):
    LOT_STRUCT = ['bid_date', 'bid_id', 'region_id', 'area_id', 'title', 'start_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g = None
        self.url = None
        self.region = {}
        self.area = {}

    def load_area_and_region(self):
        for obj in models.Region.objects.all():
            self.region[obj.title] = obj.pk
        for obj in models.Area.objects.all():
            self.area[obj.title] = obj.pk

    def get_sites(self):
        e, s = date.today() + timedelta(days=60), date.today()
        e, s = e.strftime('%d.%m.%Y'), s.strftime('%d.%m.%Y')
        return {
            'https://exarid.uzex.uz/ru/ajax/filter?PageSize=100&Src=AllMarkets&Type=trade&PageIndex=1': 'https://exarid.uzex.uz/ru/trade/lot/{}/',
            'https://dxarid.uzex.uz/ru/ajax/filter?PageSize=100&EndDate={}&Src=AllMarkets&Type=trade&startdate={}&PageIndex=1'.format(e, s): 'https://dxarid.uzex.uz/ru/trade/lot/{}/',
        }

    def handle(self, *args, **options):
        self.load_area_and_region()
        for url, self.url in self.get_sites().items():
            self.g = Grab()
            self.g.go(url)
            self.parse_bids()

    def parse_bids(self):
        bids = self.g.doc.select('//tr')
        if bids.count() < 1:
            print('Лоты не найдены!')
            return

        for el in bids[1:]:
            self.save_bid(
                [e.text() for e in el.select('td')[1:7]]
            )

    def save_bid(self, bid):
        if '.' in bid[1]:
            bid[0], bid[1] = bid[1], bid[0]
        data = dict(zip(self.LOT_STRUCT, bid))
        bpk = data['bid_id']
        if not models.Lot.objects.bid_exists(bpk):
            data.update(self.get_bid_info(bpk))
            data['region_id'] = self.region[data['region_id']]
            data['area_id'] = self.area[data['area_id']]
            models.Lot.objects.bid_create(**data)

    def get_bid_info(self, bid_id):
        url = self.url.format(bid_id)
        self.g.go(url)
        info = self.g.doc.select('//ul[@class="product_info"]')
        info = '\n'.join(e.text() for e in info.select('li'))
        cond = self.g.doc.select('//ul[@class="conditionsList"]')
        cond = '\n'.join(e.text() for e in cond.select('li'))
        desc = self.g.doc.select('//div[@class="full_block content"]/p')
        titles = self.g.doc.select('//h3[@class="min_title"]')

        description = ''
        for i, title in enumerate(titles):
            description += '{}\n{}\n\n'.format(title.text(), desc[i].text())
        files = []

        for f in self.g.doc.select('//a[@class="product_file"]'):
            url = f.attr('href')
            ext = url.split('.')[-1].lower()
            self.g.go(url)
            filename = '{}.{}'.format(utils.md5_text(url), ext)
            files.append(ContentFile(self.g.doc.body, filename))

        return {
            'conditions': cond,
            'customer_info': info,
            'description': description,
            'files': files,
            'url': url,
        }
