/* eslint-disable no-use-before-define */
/* eslint-disable object-shorthand */
/* eslint-disable no-alert */
/* eslint-disable import/extensions */
import {
  appendPomodoro,
  changeLabels,
  formatTime,
  renderTimer,
} from './timer_helpers.js';
import * as settings from './user_settings.js';

const overlay = document.querySelector('#overlay');
const minutes = document.querySelector('#minute');
const seconds = document.querySelector('#second');
let focus = true;

function showTimer() {
  overlay.style.visibility = 'visible';
  overlay.style.opacity = 0.97;
}

function hideTimer() {
  overlay.style.visibility = 'hidden';
}

function stopTimer() {
  document.querySelector(settings.stopSound).play();
  minutes.innerHTML = '-0';
  seconds.innerHTML = '00';
  const sheet = window.document.styleSheets[0];
  sheet.insertRule('svg circle.meter {'
    + 'animation: none'
    + '}', sheet.cssRules.length);
}

function postPomodoro(token) {
  const tag = document.querySelector('#text-input').value;

  fetch(`/api/${token}/create`, {
    method: 'POST',
    body: JSON.stringify({
      tag: tag,
    }),
  })
    .then((response) => {
      // append pomodoro to the index: count and today's
      if (response.status === 201) {
        // Render timer and set time
        let cycle = document.querySelector('#today').innerHTML;
        cycle = parseInt(cycle, 10) + 1;

        if (parseInt(cycle, 10) % 4 === 0) {
          renderTimer(15, settings.breakColor);
        } else renderTimer(settings.breakTime, settings.breakColor);
        changeLabels(true);
        document.querySelector('.focus').innerHTML = 'Break';
        const atStart = performance.now();
        startTimer(atStart, settings.breakTime);
        appendPomodoro(tag);
      } else if (response.status === 422) {
        alert('Must not overlap saved pomodoros, please wait 24 minutes and 59 seconds.');
      }
      changeLabels(false);
    });
}

function savePomodoro() {
  // Save pomodoro to the API
  const token = document.querySelector('#token').value;

  document.addEventListener('keydown', (event) => {
    if (event.code === 'Enter' && document.querySelector('#save').style.display === 'block') {
      postPomodoro(token);
    }
  });

  document.querySelector('#save').addEventListener('click', () => {
    postPomodoro(token);
  });
}

function changeTimer() {
  if (!focus) {
    changeLabels(true);
    // Check if user is logged in to save the pomodoro
    const userLogged = document.querySelector('#user-logged');
    if (userLogged.innerHTML === 'Sign Out') {
      savePomodoro();
    } else {
      alert('Sign in to collect and save your Pomodoros!');
      // eslint-disable-next-line no-restricted-globals
      location.reload();
      // displaySocial();
    }
  } else {
    hideTimer();
    stopTimer();
  }
}

function startTimer(atStart, time) {
  // Timer manual stop
  if (minutes.innerHTML === '-0') {
    changeLabels(false);
    hideTimer();
    stopTimer();
    return;
  }
  // Change clock when finished
  if (minutes.innerHTML === '00' && seconds.innerHTML === '00') {
    document.querySelector(settings.startSound).play();
    if (focus) {
      focus = false;
    } else {
      focus = true;
    }
    changeTimer(focus);
    return;
  }
  [minutes.innerHTML, seconds.innerHTML] = formatTime(atStart, time);
  setTimeout(startTimer, 1000, atStart, time);
}

export {
  showTimer,
  renderTimer,
  hideTimer,
  startTimer,
  stopTimer,
};
