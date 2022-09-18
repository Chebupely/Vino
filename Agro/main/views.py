from django.shortcuts import render, redirect
from .forms import InfoForm

def index(request):
    return render(request, 'main/index.html')

def findvino(request):
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            vino = form.cleaned_data.get("vino")
            height = form.cleaned_data.get("height")
            aspect = form.cleaned_data.get("aspect")
            slope = form.cleaned_data.get("slope")
            water = form.cleaned_data.get("water")

            return redirect('result')
        else:
            return redirect('home')
    form = InfoForm()
    context = {
        'form': form
    }
    return render(request, 'main/findVino.html', context)

def res(request):
    form = InfoForm()
    context = {
        'form': form
    }
    return render(request, 'main/res.html', context)

def about1(request):
    return render(request, 'main/about1.html')

def about2(request):
    return render(request, 'main/about2.html')

