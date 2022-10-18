from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from app.models import *


# GET request
def getAll(request, token):

    if request.method != 'GET':
        return JsonResponse({"error": "GET request required."}, status=400)

    try:
        token = UserToken.objects.get(token=token)

    except UserToken.DoesNotExist:
        return JsonResponse({
            "error": f'Invalid token'
        }, status=401)

    user = token.user
    pomodoros = Pomodoro.objects.filter(user=user).order_by('-datetime')

    return JsonResponse([pomodoro.serialize() for pomodoro in pomodoros], safe=False, status=200)


# POST request
@csrf_exempt
def create(request, token):

    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        token = UserToken.objects.get(token=token)

    except UserToken.DoesNotExist:
        return JsonResponse({
            "error": f'Invalid token'
        }, status=401)

    data = json.loads(request.body)

    try:
        tag = data['tag']
    except KeyError:
        return JsonResponse({"error": "POST request error."}, status=400)

    user = token.user
    Tag(tag=tag).save()
    Pomodoro(user=user, tag=Tag.objects.get(tag=tag)).save()

    if Pomodoro.objects.last().checkLastCreated():
        return JsonResponse({'message': 'Pomodoro created successfully'}, status=201)

    return JsonResponse({'error':'Must not overlap saved pomodoros, please wait 24 minutes and 59 seconds.'}, status=422)



