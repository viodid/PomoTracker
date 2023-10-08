
![Logo](https://pomotracker.s3.eu-central-1.amazonaws.com/pomotracker_logo_sticker.png)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Table of Contents
1. [Distinctiveness and Complexity](#Distinctiveness-and-Complexity)
2. [Features](#features)
3. [Contents of each file](#Contents-of-Each-File)
4. [Run locally](#run-locally)
5. [Tech stack](#tech-stack)
6. [API Reference](#api-reference)
7. [Roadmap](#roadmap)
8. [Acknowledgements](#acknowledgements)
9. [Contributing](#contributing)
10. [Feedback & Support](#feedback--support)

## Distinctiveness and Complexity

#### PomoTracker: A Pomodoro Technique Study Timer Tracker

PomoTracker is a powerful and flexible pomodoro timer app that helps users boost their productivity and manage their time more effectively.

With PomoTracker, users can create custom timers tailored to their specific needs, save them for future use, and track their progress over time with detailed graphs and statistics.

Here's why PomoTracker satisfies the distinctiveness and complexity requirements.


- **Data Collection and Statistics:** PomoTracker collects statistics on user activity to provide insights into their productivity. It tracks the number of hours worked per day and analyzes when users are most focused.<br>
This data-driven approach sets PomoTracker apart by helping users make informed decisions about their work habits.
<div align="center">
  <img src="https://pomotracker.s3.eu-central-1.amazonaws.com/charts_santi.png" style="border-radius:10px;" alt="User profile's graphs">
  <img src="https://pomotracker.s3.eu-central-1.amazonaws.com/contributor_graph.png" style="border-radius:10px;" alt="contributor graph">
</div>
<br>

- **Community Engagement:** PomoTracker fosters a sense of community by implementing a user league and leaderboard system. Users can compete with each other based on their Pomodoro sessions.<br>
  The leaderboard displays information such as total Pomodoros completed, average Pomodoros, and rewards for top performers.<br>
  This gamification element adds a unique and engaging aspect to the application.
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
Before PomoTracker came to be, I was an avid user of a website called "tomato.es". As the app I cherished was hosted on Heroku, our journey together encountered a bump in the road when Heroku decided to discontinue their free product plans, starting from November 28th, 2022 (Source: <a href="https://help.heroku.com/RSBRUH58/removal-of-heroku-free-product-plans-faq">Heroku FAQ</a>). Suddenly, many of us found ourselves in a bit of a pickle, as we were used to the convenience and vibrant community that "tomato.es" provided.<br>
What I loved most about "tomato.es" were its nifty charts and a leaderboard that kept us motivated with daily, monthly, and yearly rankings. It was simple, but it worked like a charm.<br>
 To my surprise, I couldn't find any other alternatives that offered the same cozy features I had grown to love. And so, PomoTracker was born, my way of giving back and creating a Pomodoro app that's even more awesome and feature-packed.


## Features

1. **Responsive Design:** 📱 PomoTracker boasts a fully responsive design, ensuring a seamless and enjoyable experience across all your devices, from desktops to mobile phones.

2. **Customizable Themes:** 🌈 Personalize your PomoTracker to match your unique style. Choose from a variety of theme colors in the settings, allowing you to create an environment that suits your preferences.

3. **Leaderboard Engagement:** 🥇 Get ready for some friendly competition! The integrated leaderboard is just a click away, right from the timer page. See how your productivity stacks up against others and stay motivated to achieve your goals.

4. **User-Friendly Settings:** ⚙️ I've designed the user settings interface with simplicity in mind. You'll appreciate the seamless form interface and helpful error messages, making it easy to tailor PomoTracker to your needs.

5. **Visual Productivity Insights:** 📈 Gain valuable insights into your productivity with visually engaging charts. Track your pomodoros per hour and per day, and visualize your productivity journey with a GitHub-like density chart right on the main page.

6. **Optimized Performance:** 📊 PomoTracker is built for speed and efficiency. I've fine-tuned data handling to reduce load times, minimize API calls for faster responses, and ensure a smooth and responsive user experience.


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
    docker compose -f docker-compose.yml up --build
  ```

2. **Using a Virtual Environment (Pipenv or Virtualenv):**

  - Install pipenv if you haven't already. You can find installation instructions <a href="https://pipenv.pypa.io/en/latest/installation/#make-sure-you-have-python-and-pip">here</a>.
  - In the root folder, run `pipenv shell` and `pipenv install` to install the project's dependencies.
  - Start the Django development server:
  ```Bash
    python manage.py runserver 0.0.0.0:1337
  ```
> [!IMPORTANT]
> Ensure you've configured the required environment variables based on the content of the [.env file](https://github.com/viodid/PomoTracker/blob/main/PomoTracker/.dev.env) used in the Docker method. Additionally, set up a PostgreSQL database and configure a Redis server.
**Please note that this step is only necessary when using the virtual environment method.**

Access the application in your web browser at http://localhost:1337. Ensure that port 1337 is not used by any other program.


## Tech Stack

**Client**
- HTML
- CSS
- JavaScript

**Server**
- Django (Python Web Framework)
- PostgreSQL
- Redis (For caching)
- Gunicorn (WSGI HTTP Server)
- Nginx (Web Server)

**Containerization and Deployment**
- Docker & Docker Compose
- Azure DevOps (CI/CD)

## API Reference

If you're interested in integrating with PomoTracker or accessing its API, the [API Reference](https://pomotracker.app/api_reference) provides comprehensive documentation. This reference will guide you through the available endpoints, request methods, authentication requirements, and response formats.


#### Key Features:

- **User Data:** Access and manage user-specific data, including tags, pomodoro dates, and settings.
- **Pomodoro Sessions:** Create, update, and delete Pomodoro sessions, allowing users to track their work and breaks.
- **Statistics:** Retrieve comprehensive statistics, including aggregated Pomodoro data and leaderboard standings.
- **Customization:** Personalize settings, such as themes and session preferences, for a tailored user experience.


Feel free to reach out at webmaster@pomotracker.app if you have any questions or need assistance while working with the API.


## Roadmap

Here's a sneak peek into the future features of PomoTracker:


- **Line Chart Comparisons:** 📊 Implement a line chart that compares the current month's statistics with previous months, offering valuable insights into your progress.
- **Focus Metrics:** 🎯 Keep track of your focused hours, days accessed, and streaks, helping you stay on top of your productivity game.
- **Timeline with Tags:** 📆 Create a timeline chart with tags for a comprehensive overview of your productivity journey, making it easier to spot trends.
- **Educational Content:** 📚 Provide resources explaining what Pomotracker is and the Pomodoro Technique, ensuring users have a clear understanding.
- **Sound Volume Control:** 🔊 Offer volume controls for audio notifications to customize your PomoTracker experience.
- **Data Export:** 📤 Enable data export in CSV format, allowing users to analyze their Pomodoro data in external tools.
- **Import from Other Apps:** 📥 Implement the ability to input Pomodoro sessions from CSV files exported from other productivity apps.
- **Enhanced 404 Page:** 🚫 Create a user-friendly and informative 404 error page to improve the user experience.
- **Session Storage:** 💾 Store Pomodoro sessions in sessions (no login required) for quick and convenient tracking.
- **GitHub Integration:** 🌐 Introduce GitHub login functionality for access.
- **Clicking Sound:** 🔊 Customize the clicking sound timer.

Stay tuned for these exciting updates and enhancements in the near future!


## Acknowledgments

PomoTracker is, in fact, the culmination of my journey through the [CS50w](https://cs50.harvard.edu/web/2020/) course. I'd like to acknowledge the pivotal role that this course has played in providing the knowledge and tools necessary to create PomoTracker, the final project.

I also owe a debt of gratitude to the original "tomato.es" web app, which served as the fundamental idea for the concept behind PomoTracker.


## Contributing

Contributions are always welcome!

See [`contributing.md`](https://github.com/viodid/PomoTracker/blob/main/CONTRIBUTING.md) for ways to get started.

Please adhere to this project's [`code of conduct`](https://github.com/viodid/PomoTracker/blob/main/CODE_OF_CONDUCT.md).


## Feedback & Support

If you have any feedback, please reach out to me at webmaster@pomotracker.app
