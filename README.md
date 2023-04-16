# PomoTracker
PomoTracker is a powerful and flexible pomodoro timer app that helps users boost their productivity and manage their time more effectively.

With PomoTracker, users can create custom timers tailored to their specific needs, save them for future use, and track their progress over
time with detailed graphs and statistics.

Whether you're a student, a professional, or anyone in between, PomoTracker has everything you need to stay focused and on task.

<details close>
<summary><h2>API reference</h2></summary>
Django API for Pomodoro App

This API allows you to manage pomodoros, tags, and user settings for a Pomodoro app built with Django.
```
1. GET /api/:username/:endpoint

Retrieve all pomodoros or tag statistics for a specific user.
Parameters

username: The username of the user.
endpoint: Can be either 'pomodoros' or 'tag'.

Responses

200 OK: Returns a JSON array of all pomodoros or a JSON object containing tag statistics.
400 Bad Request: Returned if the request method is not 'GET'.
401 Unauthorized: Returned if the user does not exist.

2. GET /api/settings/:token

Get the user settings for a given token.
Parameters

token: The user's token.

Responses

200 OK: Returns a JSON object containing the user's settings.
400 Bad Request: Returned if the request method is not 'GET'.
401 Unauthorized: Returned if the token is invalid.

3. POST /api/create/:token

Create a new pomodoro for a user with a specific tag.
Parameters

token: The user's token.

Request Body

tag: The tag to associate with the new pomodoro.

Responses

201 Created: Returns a JSON object indicating the pomodoro was created successfully.
400 Bad Request: Returned if the request method is not 'POST' or if there is a problem with the request data.
401 Unauthorized: Returned if the token is invalid.
422 Unprocessable Entity: Returned if the pomodoro would overlap with an existing one.

4. PATCH /api/updateTags/:token/:tag_to_replace

Update all pomodoros associated with a given tag for a user.
Parameters

token: The user's token.
tag_to_replace: The tag to be replaced.

Request Body

tag: The new tag to associate with the pomodoros.

Responses

201 Created: Returns a JSON object indicating the tags were updated successfully.
400 Bad Request: Returned if the request method is not 'PATCH' or if there is a problem with the request data.
401 Unauthorized: Returned if the token is invalid or if the tag does not belong to the user.

5. PUT or DELETE /api/updateDelete/:token/:pomodoro_id

Update or delete a specific pomodoro.
Parameters

token: The user's token.
pomodoro_id: The ID of the pomodoro to update or delete.

Request Body (PUT)

  tag: The new tag to associate with the pomodoro.

  Responses

  201 Created: Returns a JSON object indicating the pomodoro was updated or deleted successfully.
  400 Bad Request: Returned if the request method is not 'PUT' or 'DELETE', or if there is a problem with the request data.
  401 Unauthorized: Returned if the token is invalid, the pomodoro does not belong to the user, or the pomodoro ID is invalid.

  6. PUT /api/updateSettings/:token

  Update a user's settings.
  Parameters

  token: The user's token.

  Request Body

  white_theme: The new theme setting for the user.

  Responses

  201 Created: Returns a JSON object indicating the settings were updated successfully.
  400 Bad Request: Returned if the request method is not 'PUT' or if there is a problem with the request data.
  `401 Unauthorized
  ```
  </details>
