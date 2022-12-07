/* eslint-disable no-multi-spaces */
/* eslint-disable import/extensions */
/* eslint-disable no-alert */
import { switchDarkMode, changeLightbulb } from './theme_toggle.js';
import * as time from './timer.js';

const overlay = document.querySelector('#overlay');
const minutes = document.querySelector('#minute');
const seconds = document.querySelector('#second');
let   focus = true;
// future fetch settings user
const focusTime = 1;
const focusColor = '#f1c232';
const breakTime = 5;
const breakColor = 'greenyellow';
const startSound = '#ding';
const stopSound = '#blaublau';

function runTimer() {
  time.showTimer();
  time.renderTimer(focusTime, focusColor);
  const atStart = performance.now();
  time.startTimer(startSound, atStart);
}

function stopTimer() {
  time.hideTimer();
  time.stopTimer(stopSound);
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#start').addEventListener('click', () => {
    runTimer();
  });

  document.querySelector('#cancel').addEventListener('click', () => {
    // eslint-disable-next-line no-restricted-globals
    if (confirm('Sure?')) {
      stopTimer();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.code === 'Space' && (overlay.style.visibility === 'hidden' || overlay.style.visibility === '')) {
      runTimer();
    } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
      // eslint-disable-next-line no-restricted-globals
      if (confirm('Sure?')) {
        stopTimer();
      }
    }
  });

  document.querySelector('#slider').addEventListener('click', () => {
    switchDarkMode();
    changeLightbulb();
  });
});
