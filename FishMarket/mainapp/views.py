from django.shortcuts import render, redirect


def main(request):
    return render(request, 'mainapp/index.html')

def delivery(request):
    return render(request, 'mainapp/delivery.html')

def about(request):
    return render(request, 'mainapp/about.html')

def logout(request):
    return render(request, 'mainapp/about.html')