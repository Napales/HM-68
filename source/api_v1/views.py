import json

from django.http import HttpResponseNotAllowed, HttpResponse, JsonResponse

from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


def add(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if isinstance(body['A'], (int, float)) and isinstance(body['B'], (int, float)):
            return JsonResponse({"answer": body['A'] + body['B']}, status=200)
        else:
            return JsonResponse({"error": "Invalid format, only int and float"}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


def subtract(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if isinstance(body['A'], (int, float)) and isinstance(body['B'], (int, float)):
            return JsonResponse({"answer": body['A'] - body['B']}, status=200)
        else:
            return JsonResponse({"error": "Invalid format, only int and float"}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


def multiply(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if isinstance(body['A'], (int, float)) and isinstance(body['B'], (int, float)):
            return JsonResponse({"answer": body['A'] * body['B']}, status=200)
        else:
            return JsonResponse({"error": "Invalid format, only int and float"}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])


def divide(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        if isinstance(body['A'], (int, float)) and isinstance(body['B'], (int, float)) and body['B'] != 0:
            return JsonResponse({"answer": body['A'] / body['B']}, status=200)
        else:
            return JsonResponse({"error": "Invalid format, only int, float and 'B' can't be 0"}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])
