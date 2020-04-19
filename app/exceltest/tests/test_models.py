from django.test import TestCase
from exceltest import models


sample_question = {
    "id": 5748,
    "text": "<p>What is the probability that this spinner will land on red?</p>",
            "test_id": 238,
            "type": "MultipleChoice",
            "category": "Numeracy / Chance and Data / Probability",
            "hint": "<ul>\n<li>The spinner has 12 edges.</li>\n<li>Count the number of edges for the green area and express this as a fraction of the total edges.</li>\n</ul>",
}


class ModelTests(TestCase):

    def setUp(self):
        self.q = models.Question(**sample_question)
        self.q.save()

    def test_create_question_successful(self):
        """Test creating a question is successful"""
        assert self.q.id == 5748

    def test_create_question_with_stimulus(self):
        """Test creating a question with stimulus successful"""
        stimulus_1 = {

            "text": "<p>This spinner is used in a game.</p>",
            "order": 1
        }

        s1 = models.Stimulus(**stimulus_1)

        s1.question_id = self.q

        s1.save()
        assert self.q.stimulus.count() == 1
        assert s1.id > 0

    def test_create_question_with_review(self):
        """Test creating a question with review successful"""
        review_1 = {
            "column_1_text": "<p><span class=\"test_heading_2\">Tip</span></p>\n<p><span style=\"font-family: arial, helvetica, sans-serif; font-size: 14pt;\">In probability you need to consider whether the events are equally likely. For example, although there are only two sectors on this spinner, they are not the same size so there is a greater chance of landing on green.</span></p>",
            "order": 1
        }

        r1 = models.Review(**review_1)

        r1.question_id = self.q

        r1.save()

        assert r1.id > 0
        assert self.q.reviews.count() == 1

    def test_create_question_with_choices(self):
        """Test creating a question with choices successful"""

        choice_1 = {

            "label": "",
            "url": "https://exceltestzone-upload-production.s3.ap-southeast-2.amazonaws.com/png/5835_answer_23337.png",
            "order": 1,
        }

        choice_2 = {
            "url": "https://exceltestzone-upload-production.s3.ap-southeast-2.amazonaws.com/png/5835_answer_23339.png",
            "order": 2,
            "correct": True
        }

        c1 = models.Choice(**choice_1)
        c2 = models.Choice(**choice_2)
        c1.question_id = self.q
        c2.question_id = self.q
        c1.save()
        c2.save()

        assert c1.id > 0
        assert c2.id > 0
        assert self.q.choices.count() == 2
