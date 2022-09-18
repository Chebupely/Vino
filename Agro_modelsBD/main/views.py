from django.shortcuts import render


# def index(request):
#     return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def about1(request):
    return render(request, 'main/about1.html')

def about2(request):
    return render(request, 'main/about2.html')

def vinograd(request):
    return render(request, 'main/vinograd.html')

def vinogradnikrequest():
    vineyardBD = vinogradnik.object.all()
    return render(request, "main/vinograd.html", {"vineyardBD": vineyardBD})

def create(request):
    if request.metod == "POST":
        vineyard = vinogradnik()
        vineyard.name = request.POST.get("name_Vinogradnik")
        vineyard.number = request.POST.get("number_Vinogradnik")
        vineyard.shirota = request.POST.get("shirota_Vinogradnik")
        vineyard.dolgota = request.POST.get("dolgota_Vinogradnik")
        vineyard.description = request.POST.get("description_Vinogradnik")
        vineyard.save()
    return HttpResponseRedirect("/")

