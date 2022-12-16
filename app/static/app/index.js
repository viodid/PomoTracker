/* eslint-disable no-use-before-define */
/* eslint-disable no-multi-spaces */
/* eslint-disable import/extensions */
/* eslint-disable no-alert */
import { switchDarkMode, changeLightbulb } from './theme_toggle.js';
import * as settings from './user_settings.js';
import {
  showTimer,
  renderTimer,
  startFocusTimer,
  stopTimer,
  hideTimer,
  postPomodoro,
} from './timer.js';

const overlay = document.querySelector('#overlay');
const token = document.querySelector('#token').value;

document.querySelector('#start').addEventListener('click', () => {
  runTimer();
});

document.querySelector('#save').addEventListener('click', () => {
  postPomodoro(token);
});

document.querySelector('#cancel').addEventListener('click', () => {
  // eslint-disable-next-line no-restricted-globals
  if (confirm('Sure?')) {
    hideTimer();
    stopTimer();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.code === 'Enter' && document.querySelector('#save').style.display === 'block') {
    postPomodoro(token);
  } else if (event.code === 'Space' && (overlay.style.visibility === 'hidden' || overlay.style.visibility === '')) {
    runTimer();
  } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
    // eslint-disable-next-line no-restricted-globals
    if (confirm('Sure?')) {
      hideTimer();
      stopTimer();
    }
  }
});

document.querySelector('#slider').addEventListener('click', () => {
  switchDarkMode();
  changeLightbulb();
});

function runTimer() {
  showTimer();
  renderTimer(settings.focusTime, settings.focusColor);
  const atStart = performance.now();
  document.querySelector('.focus').innerHTML = 'Focus';
  startFocusTimer(atStart, settings.focusTime);
}
