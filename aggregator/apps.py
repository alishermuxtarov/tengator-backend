from django.apps import AppConfig


class AggregatorConfig(AppConfig):
    name = 'aggregator'
    verbose_name = 'Агрегатор'

    def ready(self):
        import aggregator.signals

