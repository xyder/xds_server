from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'main_interface/index.html', context)
