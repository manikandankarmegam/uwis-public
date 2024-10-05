from django.shortcuts import render

# Create your views here.

# aboutus
def aboutus(request):
    return render (request,'aboutus.html')