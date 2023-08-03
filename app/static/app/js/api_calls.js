export function deletePomodoro(token, id) {
  fetch(`/api/${token}/${id}`, {
    method: 'DELETE',
  }).then((response) => {
    console.log(response);
    });
}

export function editPomodoro(token, id, tag) {
  fetch(`/api/${token}/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      tag: tag,
    }),
  }).then((response) => {
    console.log(response);
    });
}

export function getAllPomodoros(username) {
  fetch(`/api/${username}/get/pomodoros`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    });
}

export function editTag(token, id, tag) {
  fetch(`/api/${token}/updateTag/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({
      tag: tag,
    }),
  }).then((response) => {
    console.log(response);
    });
}
