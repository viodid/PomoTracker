document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname.split('/').pop();

    document.querySelector(`#${path}-leaderboard`).style.color = '#f1c232';

})