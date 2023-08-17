from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404, render
from django.urls import reverse
from django.template import loader
from hp_quiz_app.models import Question, Options, Answer


def index(request):
    questions = Question.objects.all()
    options = Options.objects.all()
    return render(
        request,
        "index.html",
        {
            "questions": questions,
            "options": options,
        },
    )


def add_question(request):
    return HttpResponse(loader.get_template("question.html").render({}, request))


def add_question_record(request):
    question_text = request.POST.get("question")
    correct_option = request.POST.get("correct_option")
    question = Question(question=question_text, correct_option=correct_option)
    question.save()

    return HttpResponseRedirect(reverse("index"))


def update_question(request, id):
    return HttpResponse(
        loader.get_template("question.html").render(
            {"question": Question.objects.get(id=id)},
            {"correct_option": Question.objects.get(question.correct_option)},
            request,
        )
    )


def update_question_record(request, id):
    question = Question.objects.get(id=id)
    question.question = request.POST.get("question")
    correct_option = request.POST.get("correct_option")
    question = Question(question=question, correct_option=correct_option)
    question.save()
    return HttpResponseRedirect(reverse("index"))


def delete_question(request, id):
    question = get_object_or_404(Question, id=id)

    try:
        answer = Answer.objects.get(question_id=id)
        answer.delete()
    except Answer.DoesNotExist:
        # Ha nincs válasz az adott kérdéshez, nem kell törölni
        pass

    # Töröljük az összes kapcsolódó opciót
    Options.objects.filter(question_id=id).delete()

    question.delete()
    return HttpResponseRedirect(reverse("index"))


def add_options(request):
    return HttpResponse(
        loader.get_template("options.html").render(
            {
                "questions": Question.objects.all(),
            },
            request,
        )
    )


def add_options_record(request):
    question_id = request.POST.get("question_id")
    option_a = request.POST.get("option_a")
    option_b = request.POST.get("option_b")
    option_c = request.POST.get("option_c")
    option_d = request.POST.get("option_d")
    # correct_answer = request.POST.get('correct_answer')

    question = Question.objects.get(id=question_id)
    options = Options(
        question=question,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
    )
    options.save()

    return HttpResponseRedirect(reverse("index"))


def update_options(request, id):
    return HttpResponse(
        loader.get_template("options.html").render(
            {
                "question": Question.objects.get(id=id),
                "options": Options.objects.all(),
            },
            request,
        )
    )


def update_options_record(request, id):
    question = Question.objects.get(id=id)

    option = Options.objects.get(question=question)

    option.option_a = request.POST.get("option_a")
    option.option_b = request.POST.get("option_b")
    option.option_c = request.POST.get("option_c")
    option.option_d = request.POST.get("option_d")
    option.save()

    return HttpResponseRedirect(reverse("index"))


def delete_options(request, id):
    option = get_object_or_404(Options, id=id)
    option.delete()
    return redirect("index")
