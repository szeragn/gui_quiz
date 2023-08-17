from django.test import TestCase
from hp_quiz_app.models import Question, Options, Answer
from unittest.mock import patch
from hp_quiz_app.quiz import Quiz
from django.urls import reverse
import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from hp_quiz_app.models import Question, Options


class QuizTestCase(TestCase):
    def setUp(self):
        question1 = Question.objects.create(question="Kérdés1", correct_option="A")
        question2 = Question.objects.create(question="Kérdés2", correct_option="B")
        question3 = Question.objects.create(question="Kérdés3", correct_option="C")

        Options.objects.create(
            option_a="A1 válasz",
            option_b="B1 válasz",
            option_c="C1 válasz",
            option_d="D1 válasz",
            question=question1,
        )
        Options.objects.create(
            option_a="A2 válasz",
            option_b="B2 válasz",
            option_c="C2 válasz",
            option_d="D2 válasz",
            question=question2,
        )
        Options.objects.create(
            option_a="A3 válasz",
            option_b="B3 válasz",
            option_c="C3 válasz",
            option_d="D3 válasz",
            question=question3,
        )

        self.question1 = question1
        self.question2 = question2
        self.question3 = question3
        self.options1 = Options.objects.get(question=self.question1)
        self.options2 = Options.objects.get(question=self.question2)
        self.options3 = Options.objects.get(question=self.question3)

    @patch("hp_quiz_app.quiz.Options")
    def test_megjelenit_kerdes(self, mock_Options):
        # Mockoljuk az Options.objects tulajdonságot
        mock_options_instance = mock_Options.objects.get.return_value
        mock_options_instance.option_a = "A1 válasz"
        mock_options_instance.option_b = "B1 válasz"
        mock_options_instance.option_c = "C1 válasz"
        mock_options_instance.option_d = "D1 válasz"

        # Létrehozunk egy kvízjáték példányt a teszt kérdésekkel
        quiz = Quiz(
            [self.question1, self.question2, self.question3],
            [self.options1, self.options2, self.options3],
        )

        # A megjelenit_kerdes() metódust meghívjuk
        question_text, option_texts = quiz.megjelenit_kerdes()

        # Ellenőrizzük, hogy a metódus meghívódott-e
        self.assertTrue(mock_Options.objects.get.called)

        # Ellenőrizzük, hogy a metódus a várt paraméterekkel lett meghívva
        mock_Options.objects.get.assert_called_once_with(question=self.question1)

        # Ellenőrizzük, hogy a metódus a várt eredményt adja-e vissza
        self.assertEqual(question_text, "Kérdés1")
        self.assertEqual(
            option_texts, ["A1 válasz", "B1 válasz", "C1 válasz", "D1 válasz"]
        )

    def test_question_and_options(self):
        # Kérdések és válaszlehetőségek lekérdezése
        questions = Question.objects.all()
        options = Options.objects.all()

        # Ellenőrzés, hogy vannak-e kérdések és válaszlehetőségek
        self.assertGreater(len(questions), 0)
        self.assertGreater(len(options), 0)

        # Ellenőrzés, hogy a kérdések és válaszlehetőségek helyesen kerültek-e létrehozásra
        self.assertEqual(questions[0].question, "Kérdés1")
        self.assertEqual(options[0].option_a, "A1 válasz")

        self.assertEqual(questions[1].question, "Kérdés2")
        self.assertEqual(options[1].option_b, "B2 válasz")

        self.assertEqual(questions[2].question, "Kérdés3")
        self.assertEqual(options[2].option_c, "C3 válasz")

    def test_question_order(self):
        # Létrehozunk egy kvízjáték példányt a teszt kérdésekkel
        quiz = Quiz(
            [self.question1, self.question2, self.question3],
            [self.options1, self.options2, self.options3],
        )

        # Ellenőrizzük, hogy a kérdések megfelelő sorrendben vannak-e
        self.assertEqual(quiz.questions[0], self.question1)
        self.assertEqual(quiz.questions[1], self.question2)
        self.assertEqual(quiz.questions[2], self.question3)


class QuizScoringTestCase(TestCase):
    def setUp(self):
        self.question1 = Question.objects.create(
            question="Melyik ház a leghíresebb a Roxfortban?", correct_option="A"
        )
        self.options1 = Options.objects.create(
            question=self.question1,
            option_a="Griffendél",
            option_b="Mardekár",
            option_c="Hollóhát",
            option_d="Hugrabug",
        )

        self.question2 = Question.objects.create(
            question="Ki a Roxfort igazgatója?", correct_option="B"
        )
        self.options2 = Options.objects.create(
            question=self.question2,
            option_a="Rémus Lupin",
            option_b="Albus Dumbledore",
            option_c="Minerva McGalagony",
            option_d="Perselus Piton",
        )

        self.question3 = Question.objects.create(
            question="Mi az első tanítási évben vásárolható varázspálca?",
            correct_option="C",
        )
        self.options3 = Options.objects.create(
            question=self.question3,
            option_a="Fűzfa és fenékfa",
            option_b="Tiszafenyő és fenékfa",
            option_c="Fűzfa és sárkányhegyű",
            option_d="Diófa és fenékfa",
        )

    def test_score_calculation(self):
        # Létrehozunk egy kvízjáték példányt a teszt kérdésekkel
        quiz = Quiz(
            [self.question1, self.question2, self.question3],
            [self.options1, self.options2, self.options3],
        )

        quiz.ellenoriz(0)
        self.assertEqual(quiz.score, 1)

        quiz.ellenoriz(1)
        self.assertNotEqual(quiz.score, 1)

        quiz.ellenoriz(2)
        self.assertNotEqual(quiz.score, 1)

    def test_save_answers(self):
        # Létrehozunk egy kvízjáték példányt a teszt kérdésekkel
        quiz = Quiz(
            [self.question1, self.question2, self.question3],
            [self.options1, self.options2, self.options3],
        )

        # Ellenőrizzük, hogy a válaszok mentése helyesen működik
        quiz.ellenoriz(0)
        self.assertEqual(quiz.score, 1)

        quiz.ellenoriz(1)
        self.assertEqual(quiz.score, 2)

        quiz.ellenoriz(2)
        self.assertEqual(quiz.score, 3)

        # Ellenőrizzük, hogy az adatbázisban megfelelően vannak-e mentve a válaszok
        answers = Answer.objects.all()
        self.assertEqual(len(answers), 3)

        self.assertEqual(answers[0].question, self.question1)
        self.assertEqual(answers[0].selected_option, "A")

        self.assertEqual(answers[1].question, self.question2)
        self.assertEqual(answers[1].selected_option, "B")

        self.assertEqual(answers[2].question, self.question3)
        self.assertEqual(answers[2].selected_option, "C")

    def tearDown(self):
        # Töröljük az összes adatbázisban lévő kérdést, válaszlehetőséget és választ
        Question.objects.all().delete()
        Options.objects.all().delete()
        Answer.objects.all().delete()


class ModelsTestCase(TestCase):
    def setUp(self):
        self.question1 = Question.objects.create(
            question="Melyik ház a leghíresebb a Roxfortban?", correct_option="A"
        )
        self.options1 = Options.objects.create(
            question=self.question1,
            option_a="Griffendél",
            option_b="Mardekár",
            option_c="Hollóhát",
            option_d="Hugrabug",
        )

        self.question2 = Question.objects.create(
            question="Ki a Roxfort igazgatója?", correct_option="B"
        )
        self.options2 = Options.objects.create(
            question=self.question2,
            option_a="Rémus Lupin",
            option_b="Albus Dumbledore",
            option_c="Minerva McGalagony",
            option_d="Perselus Piton",
        )

        self.question3 = Question.objects.create(
            question="Mi az első tanítási évben vásárolható varázspálca?",
            correct_option="C",
        )
        self.options3 = Options.objects.create(
            question=self.question3,
            option_a="Fűzfa és fenékfa",
            option_b="Tiszafenyő és fenékfa",
            option_c="Fűzfa és sárkányhegyű",
            option_d="Diófa és fenékfa",
        )

    def test_create_question(self):
        self.assertEqual(
            self.question1.question, "Melyik ház a leghíresebb a Roxfortban?"
        )
        self.assertEqual(self.question1.correct_option, "A")

    def test_create_options(self):
        self.assertEqual(self.options1.option_a, "Griffendél")
        self.assertEqual(self.options2.option_b, "Albus Dumbledore")
        self.assertEqual(self.options3.option_c, "Fűzfa és sárkányhegyű")

    def test_create_answer(self):
        answer1 = Answer.objects.create(question=self.question1, selected_option="A")
        answer2 = Answer.objects.create(question=self.question2, selected_option="B")
        answer3 = Answer.objects.create(question=self.question3, selected_option="C")

        answers = Answer.objects.all()
        self.assertEqual(len(answers), 3)

        self.assertEqual(answer1.selected_option, "A")
        self.assertEqual(answer2.selected_option, "B")
        self.assertEqual(answer3.selected_option, "C")

    def tearDown(self):
        Question.objects.all().delete()
        Options.objects.all().delete()
        Answer.objects.all().delete()


class QuestionTestCase(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question="Teszt kérdés", correct_option="A"
        )

    def test_question_str_method(self):
        expected_str = "Teszt kérdés A"
        self.assertEqual(str(self.question), expected_str)


class IndexTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

        # Tartalom ellenőrzése
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(response.content, "html.parser")
        header_text = soup.find("h1").text
        self.assertEqual(header_text, "Kérdések")


class ViewsTestCase(TestCase):
    def test_index_view(self):
        url = reverse("index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Kérdések", response.content.decode("utf-8"))

    def test_add_question(self):
        url = reverse("add_question")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "question.html")

    def test_add_options_view(self):
        url = reverse("add_options")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "options.html")
