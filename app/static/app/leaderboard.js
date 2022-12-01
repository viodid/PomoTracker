import { switchDarkMode, changeLightbulb } from './theme_toggle';

document.addEventListener('DOMContentLoaded', () => {
  // Denote element by changing its color
  const path = window.location.pathname.split('/').pop();
  document.querySelector(`#${path}-leaderboard`).style.color = '#f1c232';

  document.querySelector('#slider').addEventListener('click', () => {
    switchDarkMode();
    changeLightbulb();
  });
});
