import {switch_dark_mode , change_lightbulb} from "./theme_toggle.js";

document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#slider').addEventListener('click', () => {
        switch_dark_mode();
        change_lightbulb();
    })
})
