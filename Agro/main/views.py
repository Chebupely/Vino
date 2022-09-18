from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')

def findvino(request):
    return render(request, 'main/findVino.html')

def res(request):
    if request.method == 'POST':
        return render(request, 'main/res.html')

def about1(request):
    return render(request, 'main/about1.html')

def about2(request):
    return render(request, 'main/about2.html')

