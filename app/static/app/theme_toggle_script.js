/* eslint-disable import/extensions */
import { switchDarkMode, changeLightbulb } from './theme_toggle.js';

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#slider').addEventListener('click', () => {
    switchDarkMode();
    changeLightbulb();
  });
});
