from django.http import HttpResponse

def home(request):
    return HttpResponse("Nexa Social is running 🚀")