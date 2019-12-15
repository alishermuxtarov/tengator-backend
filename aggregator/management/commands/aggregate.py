from datetime import date, timedelta

from django.core.files.base import ContentFile
from django.core.management import base

from grab import Grab, GrabError

from aggregator import models, utils


class Skip(Exception):
    pass


class Command(base.BaseCommand):
    LOT_STRUCT = ['bid_date', 'bid_id', 'region_id', 'area_id', 'title', 'start_price', 'has_request']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g = None
        self.url = None
        self.region = {}
        self.area = {}
        self.category = {}
        self.subcategory = {}

    def get(self, url):
        try:
            self.g.go(url)
        except GrabError:
            try:
                self.g.go(url)
            except Exception as msg:
                raise Skip(msg)

    def load_area_and_region(self):
        for obj in models.Region.objects.all():
            self.region[obj.title] = obj.pk
        for obj in models.Area.objects.all():
            self.area[obj.title] = obj.pk
        for obj in models.Category.objects.all():
            self.category[obj.title] = obj.pk
        for obj in models.SubCategory.objects.all():
            self.subcategory[obj.title] = obj.pk

    def get_sites(self):
        e, s = date.today() + timedelta(days=60), date.today()
        e, s = e.strftime('%d.%m.%Y'), s.strftime('%d.%m.%Y')
        return {
            'https://exarid.uzex.uz/ru/ajax/filter?PageSize=1000&Src=AllMarkets&Type=trade&PageIndex=1': 'https://exarid.uzex.uz/ru/trade/lot/{}/',
            'https://dxarid.uzex.uz/ru/ajax/filter?PageSize=1000&EndDate={}&Src=AllMarkets&Type=trade&startdate={}&PageIndex=1'.format(e, s): 'https://dxarid.uzex.uz/ru/trade/lot/{}/',
        }

    def handle(self, *args, **options):
        self.load_area_and_region()
        for url, self.url in self.get_sites().items():
            try:
                self.g = Grab()
                self.get(url)
                self.parse_bids()
            except Skip:
                continue

    def parse_bids(self):
        bids = self.g.doc.select('//tr')
        if bids.count() < 1:
            print('Лоты не найдены!')
            return

        for el in bids[1:]:
            try:
                self.save_bid(
                    [e.text() for e in el.select('td')[1:8]])
            except Skip:
                print('Skip')
                continue

    def save_bid(self, bid):
        if '.' in bid[1]:
            bid[0], bid[1] = bid[1], bid[0]
        data = dict(zip(self.LOT_STRUCT, bid))
        data['has_request'] = data['has_request'] != 'Пока не подана'
        bpk = data['bid_id']
        if not models.Lot.objects.bid_exists(bpk):
            data.update(self.get_bid_info(bpk))
            data['region_id'] = self.region[data['region_id']]
            data['area_id'] = self.area[data['area_id']]
            data['subcategories'] = [t.strip() for t in data['title'].split(',')]
            models.Lot.objects.bid_create(self.subcategory, **data)
        elif data['has_request'] is True:
            models.Lot.objects.bid_update_requests(bpk, data['has_request'])

    def get_bid_info(self, bid_id):
        lot_url = self.url.format(bid_id)
        self.get(lot_url)
        info = self.g.doc.select('//ul[@class="product_info"]')
        info = '\n'.join(e.text().strip() for e in info.select('li'))
        cond = self.g.doc.select('//ul[@class="conditionsList"]')
        cond = '\n'.join(e.text().strip() for e in cond.select('li'))
        desc = self.g.doc.select('//div[@class="full_block content"]/p')
        titles = self.g.doc.select('//h3[@class="min_title"]')
        cat = self.g.doc.select('//h1[@class="form_title"]/strong').text().strip()

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

        if cat not in self.category:
            print('Category "{}" not found'.format(cat))
            co = models.Category.objects.create(title=cat)
            self.category[cat] = co.pk

        return {
            'category_id': self.category[cat],
            'conditions': cond,
            'customer_info': info,
            'description': description,
            'files': files,
            'url': lot_url,
        }
