from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'blank/404.html')

def blank(request):
    return render(request,'blank/blank.html')