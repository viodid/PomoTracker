import { switchDarkMode, changeLightbulb } from './theme_toggle.js';
import * as settings from './user_settings.js';
import {
  showTimer,
  renderTimer,
  startFocusTimer,
  hideTimer,
  postPomodoro,
} from './timer.js';

const overlay = document.querySelector('#overlay');

// Switch version notes visibility
const toogleNotes = document.querySelectorAll('#toggle-notes');
toogleNotes.forEach((btn) => {
  btn.addEventListener('click', () => {
    const notes = document.querySelector('.version-notes');
    notes.classList.toggle('hidden');
    notes.scrollIntoView({ behavior: 'smooth' });
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

// navbar expand in mobile
    const open = document.querySelector('#open-sidebar');
    let hamburger = false;
    open.addEventListener('click', ()=>{
        if (!hamburger) {
            document.querySelector("#sidebar").classList.toggle("hidden");
            document.querySelector("#sidebar").style.height = "300px";
            document.querySelector("#sidebar").style.width = "100%";
            // document.querySelector("#sidebar").style.display = "flex";
            document.querySelector("main").style.marginTop = "376px";
            // box shadow
            document.querySelector("nav").style.boxShadow = "none";
            open.style.transform = "rotate(90deg)";
            hamburger = true;
        } else {
            document.querySelector("#sidebar").classList.toggle("hidden");
            document.querySelector("#sidebar").style.height = "0";
            document.querySelector("#sidebar").style.width = "0";
            // document.querySelector("#sidebar").style.display = "none";
            document.querySelector("main").style.marginTop = "77px";
            // box shadow
            document.querySelector("nav").style.boxShadow = "0.5px 0.5px 6px black";
            open.style.transform = "rotate(0deg)";
            hamburger = false;
        }
    }
    );
