import { deletePomodoro } from './api_calls.js';
import * as settings from './user_settings.js';

const pomos = document.querySelectorAll('#pomo');
pomos.forEach((pomo) => {
  pomo.querySelector('#delete-pomo').addEventListener('click', () => {
    confirm('Are you sure you want to delete this pomodoro?');
    const id = pomo.querySelector('#pomodoro-id').value;
    deletePomodoro(settings.token, id);
    pomo.remove();
    });
})

