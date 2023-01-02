import { deletePomodoro, editPomodoro } from './api_calls.js';
import * as settings from './user_settings.js';

const pomos = document.querySelectorAll('#pomo');
pomos.forEach((pomo) => {
  const id = pomo.querySelector('#pomodoro-id').value;
  pomo.querySelector('#delete-pomo').addEventListener('click', () => {
    if (confirm('Are you sure you want to delete this pomodoro?')) {
      deletePomodoro(settings.token, id);
      pomo.remove();
    }
    });

  pomo.querySelector('#edit-pomo').addEventListener('click', () => {
    pomo.querySelector('#edit-pomo').style.display = 'none';
    pomo.querySelector('#save-pomo').style.display = 'initial';
    pomo.querySelector('#tag').style.display = 'none';
    pomo.querySelector('#text-input').style.display = 'initial';
  });

  pomo.querySelector('#save-pomo').addEventListener('click', () => {
    const tag = pomo.querySelector('#text-input').value;
    if (tag.length > 0) {
      editPomodoro(settings.token, id, tag);
      pomo.querySelector('#tag').textContent = tag.toUpperCase();
    }
    pomo.querySelector('#edit-pomo').style.display = 'initial';
    pomo.querySelector('#save-pomo').style.display = 'none';
    pomo.querySelector('#tag').style.display = 'initial';
    pomo.querySelector('#text-input').style.display = 'none';
    });
})

