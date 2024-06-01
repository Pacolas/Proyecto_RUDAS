from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def healthCheck(request):
    return HttpResponse('ok')

def health_check(request):
    return JsonResponse({'message': 'OK'}, status=200)