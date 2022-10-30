import {switch_dark_mode , change_lightbulb} from "./theme_toggle.js";

document.addEventListener('DOMContentLoaded', function () {

    // Denote element by changing its color
    const path = window.location.pathname.split('/').pop();
    document.querySelector(`#${path}-leaderboard`).style.color = '#f1c232';

    document.querySelector('#slider').addEventListener('click', () => {
        switch_dark_mode();
        change_lightbulb();
    })
})
