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

function showTimer() {
  overlay.style.visibility = 'visible';
  overlay.style.opacity = 0.97;
}

function hideTimer() {
  overlay.style.visibility = 'hidden';
}

function changeStop() {
  document.querySelector(settings.stopSound).play();
  minutes.innerHTML = '--';
  seconds.innerHTML = '--';
}

function resetStroke() {
  const sheet = window.document.styleSheets[0];
  sheet.deleteRule(sheet.cssRules.length - 1);
}

function resetTitle() {
  document.title = 'Pomodoro Timer Online | PomoTracker';
}

function stopTimer() {
  resetStroke();
  resetTitle();
  changeStop();
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
        resetStroke();

        if (parseInt(cycle, 10) % 4 == 0) {
          const atStart = performance.now();
          startBreakTimer(atStart, settings.longBreak);
        } else {
          const atStart = performance.now();
          startBreakTimer(atStart, settings.breakTime);
        }

        changeLabels(false);
        document.querySelector('.focus').innerHTML = 'Break';
        appendPomodoro(tag);

      } else if (response.status === 422) {
        alert('Must not overlap saved pomodoros, please wait 24 minutes and 59 seconds.');
      }
      changeLabels(false);
    });
}

function changeTimer() {
  // Check if user is logged in to save the pomodoro
  const userLogged = document.querySelector('#user-logged');
  if (userLogged.innerHTML !== 'Sign Out') {
    alert('Sign in to collect and save your Pomodoros!');
    // eslint-disable-next-line no-restricted-globals
    location.reload();
    // displaySocial();
  }
}

function startFocusTimer(atStart, time) {
  // Timer manual stop
  if (minutes.innerHTML === '--' && minutes.innerHTML === '--') {
    changeLabels(false);
    hideTimer();
    return;
  }
  // Change clock when finished
  if (minutes.innerHTML === '00' && seconds.innerHTML === '00') {
    document.querySelector(settings.startSound).play();
    changeLabels(true);
    changeTimer();
    return;
  }
  [minutes.innerHTML, seconds.innerHTML] = formatTime(atStart, time);
  setTimeout(startFocusTimer, 1000, atStart, time);
}

function startBreakTimer(atStart, time) {
  // Timer manual stop
  if (minutes.innerHTML === '--' && seconds.innerHTML === '--') {
    hideTimer();
    changeLabels(false);
    return;
  }
  // Change clock when finished
  if (minutes.innerHTML === '00' && seconds.innerHTML === '00') {
    document.querySelector(settings.stopSound).play();
    hideTimer();
    stopTimer();
    changeLabels(false);
    return;
  }
  [minutes.innerHTML, seconds.innerHTML] = formatTime(atStart, time);
  setTimeout(startBreakTimer, 1000, atStart, time);
}

export {
  showTimer,
  renderTimer,
  hideTimer,
  startBreakTimer,
  startFocusTimer,
  stopTimer,
  postPomodoro,
};
