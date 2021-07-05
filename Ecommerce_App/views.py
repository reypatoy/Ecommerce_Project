from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def demo_view(request):
    return HttpResponse("demo page")


def demopage_template(request):
    return render(request, "demo.html")
