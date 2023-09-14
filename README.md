
![Logo](https://pomotracker.s3.eu-central-1.amazonaws.com/pomotracker_logo_sticker.png)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
## Distinctiveness and Complexity

#### PomoTracker: A Pomodoro Technique Study Timer Tracker

PomoTracker is a powerful and flexible pomodoro timer app that helps users boost their productivity and manage their time more effectively.

With PomoTracker, users can create custom timers tailored to their specific needs, save them for future use, and track their progress over time with detailed graphs and statistics.

Here's why PomoTracker satisfies the distinctiveness and complexity requirements.




- **Data Collection and Statistics:** PomoTracker collects statistics on user activity to provide insights into their productivity. It tracks the number of hours worked per day and analyzes when users are most focused. This data-driven approach sets PomoTracker apart by helping users make informed decisions about their work habits.
<div align="center">
  <img src="https://pomotracker.s3.eu-central-1.amazonaws.com/charts_santi.png" style="border-radius:10px;" alt="User profile's graphs">
  <img src="https://pomotracker.s3.eu-central-1.amazonaws.com/contributor_graph.png" style="border-radius:10px;" alt="contributor graph">
</div>
<br>

- **Community Engagement:** PomoTracker fosters a sense of community by implementing a user league and leaderboard system. Users can compete with each other based on their Pomodoro sessions. The leaderboard displays information such as total Pomodoros completed, average Pomodoros, and rewards for top performers. This gamification element adds a unique and engaging aspect to the application.
<div align="center">
  <img src="https://pomotracker.s3.eu-central-1.amazonaws.com/leaderboard.png" style="border-radius:10px;" alt="leaderboard users">
</div>
<br>

-  **Pomodoro Technique Integration:** PomoTracker is centered around the Pomodoro Technique, a time management method that promotes focused work and breaks. It allows users to customize their work and break intervals, making it flexible for different productivity preferences.
<div align="center">
  <img src="https://pomotracker.s3.eu-central-1.amazonaws.com/timer.gif" style="border-radius:10px;" alt="timer">
</div>
<br>

- **Yet another pomodoro app?**
Before PomoTracker came to be, I was an avid user of a website called "tomato.es". As the app I cherished was hosted on Heroku, our journey together encountered a bump in the road when Heroku decided to discontinue their free product plans, starting from November 28th, 2022 (Source: <a href="https://help.heroku.com/RSBRUH58/removal-of-heroku-free-product-plans-faq">Heroku FAQ</a>). Suddenly, many of us found ourselves in a bit of a pickle, as we were used to the convenience and vibrant community that "tomato.es" provided. What I loved most about "tomato.es" were its nifty charts and a leaderboard that kept us motivated with daily, monthly, and yearly rankings. It was simple, but it worked like a charm. To my surprise, I couldn't find any other alternatives that offered the same cozy features I had grown to love. And so, PomoTracker was born, my way of giving back and creating a Pomodoro app that's even more awesome and feature-packed.


## Contents of Each File

PomoTracker is organized into two main apps, each serving distinct purposes:

**Main App (Web Application):**

- **app:** This directory houses the main app for the web application. It includes the following key components:
  - **Views:** Contains Django views responsible for rendering the web pages.
  - **Models:** Defines the data models used within the application.
  - **Static Files:** Includes static assets such as CSS, JavaScript, and image files.
  - **Templates:** Contains HTML templates for rendering web pages.

**API App (Client-Side Rendering and Future iOS Integration):**
- **api:** This directory contains the API app, designed to serve as the backend for client-side rendering (CSR) and future integration with an iOS app. Key components within this app include:
  - **Views:** Includes views responsible for handling API requests and responses.

This clear separation of the main web application and the API app allows for flexibility and future expansion, making it easier to integrate with various client platforms, including web-based CSR and iOS applications.


## Run Locally

Clone the project and navigate to the project directory:

```bash
  git clone https://github.com/viodid/PomoTracker.git && cd PomoTracker
```

There are two ways to run the application:

1. **Using Docker:**

  - Install Docker Compose if you haven't already. You can find installation instructions <a href="https://docs.docker.com/compose/install/">here</a>.
  - In the project's root folder, run the following command to build and start the containers:
  ```bash
    docker-compose -f docker-compose.yml up --build
  ```

2. **Using a Virtual Environment (Pipenv or Virtualenv):**

  - Install pipenv if you haven't already. You can find installation instructions <a href="https://pipenv.pypa.io/en/latest/installation/#make-sure-you-have-python-and-pip">here</a>.
  - In the root folder, run `pipenv shell` to install the project's dependencies:
  - Start the Django development server:
  ```Bash
    python manage.py runserver 0.0.0.0:1337
  ```
> [!IMPORTANT]
> Make sure to set the required environment variables, configure a PostgreSQL database, and set up a Redis server as specified in the documentation. (Only required using the virtual environment method.)

Access the application in your web browser at http://localhost:1337. Ensure that port 1337 is not used by any other program.

# PomoTracker API Documentation

This documentation provides detailed information about the PomoTracker API, which is used for managing Pomodoro sessions and user settings. Below are the available API endpoints, their descriptions, and expected input/output formats.

## Get All User Tags

**Endpoint**: `GET /api/user/{username}/tags`

**Description**: Retrieve all tags associated with a specific user.

**Parameters**:

- `username` (path parameter) - Username of the user. *(Required)*

**Responses**:

- `200 OK` - Successful response with a list of user tags.

## Get All User Pomodoros Dates

**Endpoint**: `GET /api/user/{username}/pomodoros/dates`

**Description**: Retrieve dates on which a user has completed Pomodoro sessions.

**Parameters**:

- `username` (path parameter) - Username of the user. *(Required)*

**Responses**:

- `200 OK` - Successful response with a list of dates.

## Get All User Pomodoros

**Endpoint**: `GET /api/user/{username}/pomodoros`

**Description**: Retrieve details of all Pomodoro sessions associated with a specific user.

**Parameters**:

- `username` (path parameter) - Username of the user. *(Required)*

**Responses**:

- `200 OK` - Successful response with a list of Pomodoro sessions.

## Get All Pomodoros

**Endpoint**: `GET /api/pomodoros`

**Description**: Retrieve details of all Pomodoro sessions across all users.

**Responses**:

- `200 OK` - Successful response with a list of all Pomodoro sessions.

## Get User Settings

**Endpoint**: `GET /api/settings/{token}`

**Description**: Retrieve user-specific settings, including theme preferences.

**Parameters**:

- `token` (path parameter) - User's API token. *(Required)*

**Responses**:

- `200 OK` - Successful response with user settings.

## Update User Settings

**Endpoint**: `PUT /api/settings/{token}`

**Description**: Update user-specific settings, including theme preferences.

**Parameters**:

- `token` (path parameter) - User's API token. *(Required)*

**Responses**:

- `201 Created` - Settings updated successfully.

## Create a New Pomodoro

**Endpoint**: `POST /api/pomodoros/{token}`

**Description**: Create a new Pomodoro session for a user.

**Parameters**:

- `token` (path parameter) - User's API token. *(Required)*

**Responses**:

- `201 Created` - Pomodoro created successfully.

## Update Tags

**Endpoint**: `PATCH /api/pomodoros/{token}/tags/{tag_to_replace}`

**Description**: Update tags associated with a user's Pomodoro sessions.

**Parameters**:

- `token` (path parameter) - User's API token. *(Required)*
- `tag_to_replace` (path parameter) - Tag to replace. *(Required)*

**Responses**:

- `201 Created` - Tags updated successfully.

## Update a Pomodoro

**Endpoint**: `PUT /api/pomodoros/{token}/{pomodoro_id}`

**Description**: Update details of a specific Pomodoro session.

**Parameters**:

- `token` (path parameter) - User's API token. *(Required)*
- `pomodoro_id` (path parameter) - ID of the Pomodoro to update. *(Required)*

**Responses**:

- `201 Created` - Pomodoro updated successfully.

## Delete a Pomodoro

**Endpoint**: `DELETE /api/pomodoros/{token}/{pomodoro_id}`

**Description**: Delete a specific Pomodoro session.

**Parameters**:

- `token` (path parameter) - User's API token. *(Required)*
- `pomodoro_id` (path parameter) - ID of the Pomodoro to delete. *(Required)*

**Responses**:

- `201 Created` - Pomodoro removed successfully.





## API Reference

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.



## Tech Stack

**Client:** React, Redux, TailwindCSS

**Server:** Node, Express


## Feedback

If you have any feedback, please reach out to me at webmaster@pomotracker.app


## Acknowledgements

 - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [How to write a Good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## Demo

Insert gif or link to demo


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`


## Features

- Light/dark mode toggle
- Live previews
- Fullscreen mode
- Cross platform


## Lessons Learned

What did you learn while building this project? What challenges did you face and how did you overcome them?


## Optimizations

What optimizations did you make in your code? E.g. refactors, performance improvements, accessibility


## Roadmap

- Additional browser support

- Add more integrations


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Support

For support, email fake@fake.com or join our Slack channel.

