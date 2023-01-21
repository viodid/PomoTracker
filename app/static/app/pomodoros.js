import { deletePomodoro, editPomodoro } from './api_calls.js';
import { token } from './user_settings.js';

const pomos = document.querySelectorAll('#pomo');
pomos.forEach((pomo) => {
  const id = pomo.querySelector('#pomodoro-id').value;
  pomo.querySelector('#delete-pomo').addEventListener('click', () => {
    if (confirm('Are you sure you want to delete this pomodoro?')) {
      deletePomodoro(token, id);
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
    let tag = pomo.querySelector('#text-input').value;
    if (tag.length > 0) {
      editPomodoro(token, id, tag);
      tag = tag.toUpperCase();
      tag = tag.replace(' ', '_');
      pomo.querySelector('#tag').textContent = tag;
    }
    pomo.querySelector('#edit-pomo').style.display = 'initial';
    pomo.querySelector('#save-pomo').style.display = 'none';
    pomo.querySelector('#tag').style.display = 'initial';
    pomo.querySelector('#text-input').style.display = 'none';
    });
})

