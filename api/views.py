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
            "error": "Invalid token"
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
            "error": "Invalid token"
        }, status=401)

    data = json.loads(request.body)

    try:
        tag = data['tag']
        tag = tag.upper()
    except KeyError:
        return JsonResponse({"error": "POST request error."}, status=400)

    user = token.user
    # Create new Tag only if doesn't exist already
    if not Tag.objects.filter(tag=tag):
        Tag(tag=tag).save()

    Pomodoro(user=user, tag=Tag.objects.get(tag=tag)).save()

    if Pomodoro.objects.last().checkLastCreated():
        return JsonResponse({'message': 'Pomodoro created successfully'}, status=201)

    Pomodoro.objects.filter(id=Pomodoro.objects.last().id).delete()
    return JsonResponse({'error':'Must not overlap saved pomodoros, please wait 24 minutes and 59 seconds.'}, status=422)


@csrf_exempt
def updateDelete(request, token, pomodoro_id):

    if request.method != 'PUT' and request.method != 'DELETE':
        return JsonResponse({"error":"PUT or DELETE method required."})

    try:
        token = UserToken.objects.get(token=token)

    except UserToken.DoesNotExist:
        return JsonResponse({
            "error": "Invalid token"
        }, status=401)

    data = json.loads(request.body)

    if request.method == 'PUT':
        try:
            tag = data['tag']
            tag = tag.upper()
        except KeyError:
            return JsonResponse({"error": "PUT request error."}, status=400)

        # Create new Tag only if doesn't exist already
        if not Tag.objects.filter(tag=tag):
            Tag(tag=tag).save()

        tag = Tag.objects.get(tag=tag)

        # Save updated pomodoro only if pomodoro_id is valid
        if Pomodoro.objects.filter(id=pomodoro_id):
            pomodoro = Pomodoro.objects.get(id=pomodoro_id)
            pomodoro.tag = tag
            pomodoro.save()

            return JsonResponse({"message":"Pomodoro updated successfully"}, status=201)

        return JsonResponse({"error":"Invalid pomodoro id"})

