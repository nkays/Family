from django.http import HttpResponse
from django.shortcuts import render

def healthz_view(request):
    return HttpResponse("OK")