from django.core.management.base import BaseCommand, CommandParser, CommandError
from argparse import FileType
from notes.models import Note
import matplotlib.pyplot as plt
from django.db.models import Count


class Command(BaseCommand):
    help = 'Return computer friendly statistics related to note creation'

    def add_arguments(self, parser):
        #parser.add_arguments('-')
        pass

    def handle(self, *args, **options):
        notes = Note.objects.filter(user_id=1)
        orig = notes.filter(original=True)

        rk_dist = orig.values('rank').annotate(count=Count('rank'))
        x, y = self.compute_rank_distribution_data(rk_dist)

        plt.plot(x, y, 's')
        plt.show()


    def compute_rank_distribution_data(self, dist):
        data, rk_max = {}, 0
        for d in dist:
            if d['rank'] > rk_max:
                rk_max = d['rank']
            data[d['rank']] = d['count']

        return [[i+1 for i in range(rk_max)], [data.get(i+1, 0) for i in range(rk_max)]]
