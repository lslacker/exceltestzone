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

base_dir = os.path.dirname(__file__)


def load_json(fn):
    with open(fn) as f:
        return json.load(f)


question_map = {
    'question_id': 'id',
    'question_text': 'text',
    'question_test_id': 'test_id',
    'question_type': 'type',
    'question_category_path': 'category',
    'question_hint': 'hint'
}

stimulus_map = {
    'text': 'text',
    'image_url': 'url',
    'pdf_url': 'url',
}

review_map = {
    'column_1_text': 'column_1_text',
    'column_2_text': 'column_2_text',
    'image_url': 'url',
    'pdf_url': 'url'
}

choice_map = {
    'label': 'label',
    'value': 'correct',
    'image_url': 'url',
    'pdf_url': 'url'
}


class JsonParser:

    resources = []

    def get_obj_from_a_map(self, question_map):
        transform_map = {}

        for k, v in question_map.items():
            attr_value = getattr(self, k)

            if attr_value:
                transform_map[v] = attr_value
                if 'https' in str(attr_value):
                    self.resources += [attr_value]

        return transform_map

    def get_obj_from_a_map_with_pred(self, stimulus_map, pred):
        attrs = [getattr(self, k) for k in self.__dict__.keys() if pred(k)]
        parsers = [JsonParser.from_json(x) for x in attrs]
        objs = [p.get_obj_from_a_map(stimulus_map) for p in parsers]
        return [x for x in objs if x]

    @classmethod
    def from_json(cls, question):
        kls = cls()
        kls.__dict__.update(**question)
        return kls


def parse(question):

    parser = JsonParser.from_json(question)
    stimulus = parser.get_obj_from_a_map_with_pred(
        stimulus_map, lambda k: k.startswith('stimulus_'))
    reviews = parser.get_obj_from_a_map_with_pred(
        review_map, lambda k: k.startswith('review_'))
    choices = parser.get_obj_from_a_map_with_pred(
        choice_map, lambda k: k.startswith('choice_'))
    question_obj = parser.get_obj_from_a_map(question_map)

    insert_to_db(question_obj, stimulus, choices, reviews)


def insert_to_db(question, stimulus, choices, reviews):

    q = models.Question(**question)

    q.save()

    for idx, s in enumerate(stimulus):
        s1 = models.Stimulus(**s)
        s1.order = idx + 1
        s1.question_id = q
        s1.save()

    for idx, r in enumerate(reviews):
        r1 = models.Review(**r)
        r1.order = idx + 1
        r1.question_id = q
        r1.save()

    for idx, c in enumerate(choices):
        c1 = models.Choice(**c)
        c1.order = idx + 1
        c1.question_id = q
        c1.save()


def parse_and_import(cache_folder: Path):

    files = cache_folder.glob('[1-9]*.json')
    questions = list(it.chain.from_iterable(
        load_json(f)['success'] for f in files))

    for question in questions[1:]:
        parse(question)


class Command(BaseCommand):
    """Django command to parse quesitons in json format into database"""

    def handle(self, *args, **options):
        self.stdout.write('Importig...')
        current_folder = Path(base_dir)
        cache_folder = current_folder.parents[1] / 'static' / 'json'

        parse_and_import(cache_folder)

        self.stdout.write(self.style.SUCCESS('All done! '))
