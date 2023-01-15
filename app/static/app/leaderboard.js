/* eslint-disable import/extensions */
import { switchDarkMode, changeLightbulb } from './theme_toggle.js';
import { whiteTheme } from './user_settings.js';

// Denote element by changing its color
const path = window.location.pathname.split('/').pop();
const selection = document.querySelector(`#${path}-leaderboard`);
selection.style.color = '#f1c232';
const parent = selection.parentElement;
console.log(whiteTheme);
if (!whiteTheme) {
  parent.style.color = '#efefef';
  parent.style.backgroundColor = '#202020';
} else {
  parent.style.color = '#121212';
  parent.style.backgroundColor = '#ebebeb';
}
parent.style.borderTop = '2px solid #f1c232';

document.querySelector('#slider').addEventListener('click', () => {
  switchDarkMode();
  changeLightbulb();
});
