from django.core.management import base, call_command
from aggregator.models import Lot


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        ids = [1092, 273]
        for pk in ids:
            lot = Lot.objects.filter(pk=pk)
            if lot.exists():
                lot.delete()
        call_command('aggregate')
