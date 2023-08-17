from django.db import models


class Question(models.Model):
    question = models.CharField(max_length=200)
    correct_option = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
        default="",
    )

    def __str__(self):
        return f"{self.question} {self.correct_option}"


class Options(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_a = models.CharField(max_length=40, null=False, blank=False)
    option_b = models.CharField(max_length=40, null=False, blank=False)
    option_c = models.CharField(max_length=40, null=False, blank=False)
    option_d = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return f"{self.option_a} {self.option_b} {self.option_c} {self.option_d}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(
        max_length=1, choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]
    )

    def __str__(self):
        return f"{self.question.question} - {self.selected_option}"
