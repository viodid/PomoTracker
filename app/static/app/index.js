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

// Switch version notes visibility
const toogleNotes = document.querySelectorAll('#toggle-notes');
toogleNotes.forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelector('.version-notes').classList.toggle('hidden');
  });
});

document.querySelector('#start').addEventListener('click', () => {
  console.log(settings);
  runTimer();
});

document.querySelector('#save').addEventListener('click', () => {
  postPomodoro(settings.token);
});

document.querySelector('#cancel').addEventListener('click', () => {
  if (confirm('Sure?')) {
    hideTimer();
    stopTimer();
  }
});

document.addEventListener('keydown', (event) => {
  if (event.code === 'Enter' && document.querySelector('#save').style.display === 'block') {
    postPomodoro(settings.token);
  } else if (event.code === 'Space' && (overlay.style.visibility === 'hidden' || overlay.style.visibility === '')) {
    runTimer();
  } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
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
  document.querySelector('.focus').innerHTML = 'Focus';
  const atStart = performance.now();
  startFocusTimer(atStart, settings.focusTime);
}
