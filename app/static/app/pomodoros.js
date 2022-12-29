import { deletePomodoro } from './api_calls.js';
import * as settings from './user_settings.js';

const pomos = document.querySelectorAll('#delete-pomo');
pomos.forEach((pomo) => {
  pomo.addEventListener('click', () => {
    const id = pomo.querySelector('#pomodoro-id').value;
    deletePomodoro(settings.token, id);
    });
})

