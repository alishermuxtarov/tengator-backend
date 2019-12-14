from django.core.management import base

from grab import Grab

from aggregator import models


class Command(base.BaseCommand):
    LIST_URL = 'https://exarid.uzex.uz/ru/ajax/filter?' \
               'PageSize=100&Src=AllMarkets&Type=trade&PageIndex=1'
    INFO_URL = 'https://exarid.uzex.uz/ru/trade/lot/{}'
    LOT_STRUCT = ['bid_date', 'bid_id', 'region', 'area', 'title', 'start_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g = None

    def handle(self, *args, **options):
        self.g = Grab()
        self.g.go(self.LIST_URL)
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
        data = dict(zip(self.LOT_STRUCT, bid))
        bpk = data['bid_id']
        if not models.Lot.objects.bid_exists(bpk):
            data.update(self.get_bid_info(bpk))
            models.Lot.objects.bid_create(**data)

    def get_bid_info(self, bid_id):
        self.g.go(self.INFO_URL.format(bid_id))
        info = self.g.doc.select('//ul[@class="product_info"]')
        info = '\n'.join(e.text() for e in info.select('li'))
        cond = self.g.doc.select('//ul[@class="conditionsList"]')
        cond = '\n'.join(e.text() for e in cond.select('li'))
        return {
            'conditions': cond,
            'customer_info': info,
        }
