from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from app.models import Pomodoro, UserSettings, Tag, User, Statistics
from datetime import datetime
import pytz


# GET request
def getAll(request, username, endpoint):

    if request.method != 'GET':
        return JsonResponse({"error": "GET request required."}, status=400)

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return JsonResponse({
            "error": "Username does not exist."
        }, status=401)

    if endpoint == 'pomodoros':
        pomodoros = Pomodoro.objects.filter(user=user).order_by('-datetime')
        return JsonResponse([pomodoro.serialize() for pomodoro in pomodoros],
                            safe=False, status=200)

    elif endpoint == 'tag':
        tagDict = Statistics.aggregatePomodorosByTag(user)
        return JsonResponse(tagDict, safe=False, status=200)


def getSettings(request, token):

    if request.method != 'GET':
        return JsonResponse({"error": "GET request required."}, status=400)

    try:
        token = UserSettings.objects.get(token=token)

    except UserSettings.DoesNotExist:
        return JsonResponse({
            "error": "Invalid token"
        }, status=401)

    user = token.user
    settings = UserSettings.objects.get(user=user)

    return JsonResponse(settings.serialize(), safe=False, status=200)


# POST request
@csrf_exempt
def create(request, token):

    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        token = UserSettings.objects.get(token=token)

    except UserSettings.DoesNotExist:
        return JsonResponse({
            "error": "Invalid token"
        }, status=401)

    data = json.loads(request.body)

    try:
        tag = data['tag']
        tag = tag.upper()
        tag = tag.replace(' ', '_')
    except KeyError:
        return JsonResponse({"error": "POST request error."}, status=400)

    user = token.user
    # Create new Tag only if it doesn't exist already
    if not Tag.objects.filter(tag=tag):
        Tag(tag=tag).save()

    timezone = user.settings.timezone

    Pomodoro(user=user, tag=Tag.objects.get(tag=tag),
             datetime=datetime.now(pytz.timezone(timezone))).save()

    if user.pomodoros.last().checkLastCreated():
        return JsonResponse({'message': 'Pomodoro created successfully'}, status=201)

    user.pomodoros.last().delete()
    return JsonResponse({'error': 'Must not overlap saved pomodoros, please wait 24 minutes and 59 seconds.'},
                        status=422)



@csrf_exempt
def updateTags(request, token, tag_to_replace):

        if request.method != 'PATCH':
            return JsonResponse({"error": "PATCH request required."}, status=400)

        try:
            token = UserSettings.objects.get(token=token)

        except UserSettings.DoesNotExist:
            return JsonResponse({
                "error": "Invalid token"
            }, status=401)

        # Check if tag_to_replace exists
        if not Tag.objects.filter(tag=tag_to_replace):
            return JsonResponse({"error": "Invalid tag"}, status=401)

        # Check format data and get user from token
        data = json.loads(request.body)
        try:
            new_tag = data['tag']
            new_tag = new_tag.upper()
            new_tag = new_tag.replace(' ', '_')
        except KeyError:
            return JsonResponse({"error": "PATCH request error."}, status=400)

        user = token.user

        # Create new Tag only if it doesn't exist already
        if not Tag.objects.filter(tag=new_tag):
            Tag(tag=new_tag).save()

        new_tag = Tag.objects.get(tag=new_tag)

        # Update all pomodoros with the same tag
        pomodoros = Pomodoro.objects.filter(tag__tag=tag_to_replace)
        for pomodoro in pomodoros:
            if pomodoro.user != user:
                return JsonResponse({'message': f'Tag does not belong to {user.username}'},
                                    status=401)
            pomodoro.tag = new_tag
            pomodoro.save()

        return JsonResponse({"message": "Tags updated successfully"},
                            status=201)


@csrf_exempt
def updateDelete(request, token, pomodoro_id):

    try:
        token = UserSettings.objects.get(token=token)

    except UserSettings.DoesNotExist:
        return JsonResponse({
            "error": "Invalid token"
        }, status=401)

    # Get user from token
    user = token.user

    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            tag = data['tag']
            tag = tag.upper()
            tag = tag.replace(' ', '_')
        except KeyError:
            return JsonResponse({"error": "PUT request error."}, status=400)

        # Create new Tag only if it doesn't exist already
        if not Tag.objects.filter(tag=tag):
            Tag(tag=tag).save()

        tag = Tag.objects.get(tag=tag)

        # Save updated pomodoro only if pomodoro_id is valid
        if request.method == 'PUT' and Pomodoro.objects.filter(id=pomodoro_id):
            pomodoro = Pomodoro.objects.get(id=pomodoro_id)
            if pomodoro.user != user:
                return JsonResponse({'message':
                                    f'Pomodoro does not belong to {user.username}'},
                                    status=401)
            pomodoro.tag = tag
            pomodoro.save()

            return JsonResponse({"message": "Pomodoro updated successfully"},
                                status=201)

    elif request.method == 'DELETE':

        # Check pomodo_id is correct and correspond to the token's user
        if Pomodoro.objects.filter(id=pomodoro_id) and user.pomodoros.filter(id=pomodoro_id):

            Pomodoro.objects.filter(id=pomodoro_id).delete()

            return JsonResponse({"message": "Pomodoro removed successfully"},
                                status=201)

        return JsonResponse({"error": "Invalid pomodoro id"},
                            status=401)

    return JsonResponse({"error": "PUT or DELETE method required."},
                        status=400)


@csrf_exempt
def updateSettings(request, token):

    try:
        token = UserSettings.objects.get(token=token)

    except UserSettings.DoesNotExist:
        return JsonResponse({
            "error": "Invalid token"
        }, status=401)

    data = json.loads(request.body)
    # Get user from token
    user = token.user

    if request.method == 'PUT':
        try:
            theme = data['white_theme']
        except KeyError:
            return JsonResponse({"error": "PUT request error."}, status=400)

        settings = UserSettings.objects.get(user=user)
        settings.theme = theme
        settings.save()
        return JsonResponse({"message": "Settings updated successfully"},
                            status=201)

    return JsonResponse({"error": "PUT method required."}, status=400)
