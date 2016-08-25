from django.core.management.base import BaseCommand, CommandParser, CommandError
from argparse import FileType
import pytz
import math
from datetime import datetime, timedelta
from notes.models import Note
from django.db.models import Avg


class Command(BaseCommand):
    help = 'Return computer friendly statistics related to note creation'

    def add_arguments(self, parser):
        #parser.add_arguments('-')
        pass

    def handle(self, *args, **options):
        current = (datetime.now(pytz.utc) - timedelta(days=3),
                   datetime.now(pytz.utc))

        before = (datetime.now(pytz.utc) - timedelta(days=4),
                  datetime.now(pytz.utc) - timedelta(days=1))

        c_rk1, c_rk_gt1, c_rk_avg = self.compute_values(*current)
        b_rk1, b_rk_gt1, b_rk_avg = self.compute_values(*before)

        rk1_sts = self.change_status(c_rk1, b_rk1)
        rk_gt1_sts = self.change_status(c_rk_gt1, b_rk_gt1)
        rk_avg_sts = self.change_status(c_rk_avg, b_rk_avg)

        out = " ".join(str(n) for n in [c_rk1, rk1_sts, c_rk_gt1, rk_gt1_sts, "%0.2f" % c_rk_avg, rk_avg_sts])
        self.stdout.write(out)

    def compute_values(self, _from, to):
        notes = Note.objects.filter(user_id=1, created__lt=to).all()

        in_span = notes.filter(created__gt=_from)

        rk1 = in_span.filter(rank=1)
        rk_gt1 = in_span.filter(rank__gt=1)

        rk1_no = rk1.count()
        rk_gt1_no = rk_gt1.count()

        dval = notes.aggregate(Avg('rank')).values()
        rk_avg = list(dval)[0]

        return (rk1_no, rk_gt1_no, rk_avg)

    def change_status(self, now, before):
        if math.fabs(now - before) < (before * 0.05):
            return 0
        elif now < before:
            return -1
        else:
            return 1
