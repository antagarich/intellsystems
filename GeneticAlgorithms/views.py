from django.http import JsonResponse
from genetic_algo import GeneticAlgorithm
from django.views.generic import TemplateView
from django.shortcuts import render_to_response

g = GeneticAlgorithm()

class Beginning(TemplateView):
    template_name = "main.html"


class GA(TemplateView):
    template_name = "ga.html"


def genetic_init_config(request):
    global g
    conf = request.POST
    g.init_config(conf)
    return render_to_response("config.html", conf)


def genetic_step(request):
    global g
    g.step()
    state = g.get_state()
    return JsonResponse({"status": "ok", state: state})


def genetic_clear(request):
    global g
    g.clear()
    return JsonResponse({"status": "ok"})