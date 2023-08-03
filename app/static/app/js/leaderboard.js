import { theme } from './user_settings.js';

// Denote element by changing its color
const path = window.location.pathname.split('/').pop();
const selection = document.querySelector(`#${path}-leaderboard`);
const parent = selection.parentElement;
parent.style.color = '#efefef';
if (theme === 'default') {
  parent.style.backgroundColor = '#202020';
  parent.style.borderTop = '2px solid #f1c232';
  selection.style.color = '#f1c232';
} else if (theme === 'forest') {
  parent.style.backgroundColor = '#253c34';
  selection.style.color = '#EAE7B1';
  parent.style.borderTop = '2px solid #EAE7B1';
} else if (theme === 'aquamarine') {
  parent.style.backgroundColor = '#022727';
  selection.style.color = '#6baaaa';
  parent.style.borderTop = '2px solid #6baaaa';
} else if (theme === 'garnet') {
  parent.style.backgroundColor = '#202020';
  selection.style.color = '#9d1e1b';
  parent.style.borderTop = '2px solid #9d1e1b';
} else if (theme === 'coral') {
  parent.style.backgroundColor = '#2a3642';
  selection.style.color = '#FAD6A5';
  parent.style.borderTop = '2px solid #FAD6A5';
} else {
  parent.style.color = '#121212';
  parent.style.backgroundColor = '#ebebeb';
  parent.style.borderTop = '2px solid #f1c232';
  selection.style.color = '#f1c232';
}

if (path === 'day') {
  parent.style.borderTopLeftRadius = '10px';
} else if (path === 'all') {
  parent.style.borderTopRightRadius = '10px';
}
