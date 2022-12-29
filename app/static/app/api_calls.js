export function deletePomodoro(token, id) {
  fetch(`/api/${token}/${id}`, {
    method: 'DELETE',
  }).then((response) => {
    console.log(response);
    });
}
