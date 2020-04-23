from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from exceltest import models
import requests
import json
import os
from pathlib import Path
import glob
import itertools as it
from collections import namedtuple
import shutil

base_dir = os.path.dirname(__file__)


def download(to_folder: Path):

    stimuls = models.Stimulus.objects.exclude(url__isnull=True)
    reviews = models.Review.objects.exclude(url__isnull=True)
    choices = models.Choice.objects.exclude(url__isnull=True)

    for o in it.chain(stimuls, reviews, choices):
        url = o.url
        filename = url.split('/')[-1]
        fn = to_folder / filename

        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with fn.open('wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                o.filename = filename
                o.save()


class Command(BaseCommand):
    """Django command to download resource from excel test"""

    def handle(self, *args, **options):
        self.stdout.write('Downloading...')
        current_folder = Path(base_dir)
        to_folder = current_folder.parents[1] / 'static' / 'resources'

        download(to_folder)

        self.stdout.write(self.style.SUCCESS('All done! '))
