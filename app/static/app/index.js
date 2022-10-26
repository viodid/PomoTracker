import {switch_dark_mode, change_lightbulb} from "./theme_toggle.js";

document.addEventListener('DOMContentLoaded', function () {

    const overlay = document.querySelector('#overlay');
    overlay.style.visibility = 'hidden';
    const timer = new Timer();

    document.querySelector('#start').addEventListener('click', () => {
        display_overlay(overlay, timer);
    })

    document.querySelector('#cancel').addEventListener('click', () => {
        display_overlay(overlay, timer)
    })

    document.addEventListener('keydown', event => {

        if (event.code === 'Space' && overlay.style.visibility === 'hidden') {
            display_overlay(overlay, timer);

        } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
            display_overlay(overlay, timer);
            play_sound(document.querySelector('#whoosh'));
        }
    })

    document.querySelector('#slider').addEventListener('click', () => {
        switch_dark_mode();
        change_lightbulb();
    })
})

function display_overlay(overlay, timer, hide=false) {

    // Reset timer to 25 minutes in the background
    if (hide === true) {
        //overlay.style.visibility = 'hidden';
        //overlay.style.opacity = 0;
        //stop_animation();
        reset_timer(timer)
        //document.querySelector('.focus').innerHTML = 'Focus';
        //timer.phase = 'focus';
        location.reload();
    }
    else if (overlay.style.visibility === 'hidden') {
        render_timer(25, '#f1c232');
        overlay.style.visibility = 'visible';
        overlay.style.opacity = 0.97;
        start_timer(timer);

    } else {
        if (confirm('Sure?')) {
            //play_sound(document.querySelector('#whoosh'))
            //overlay.style.visibility = 'hidden';
            //overlay.style.opacity = 0;
            //stop_animation();
            reset_timer(timer);
            //document.querySelector('.focus').innerHTML = 'Focus';
            //timer.phase = 'focus';
            location.reload();
        }
    }
}

function render_timer(time, color) {

    const minutes = document.querySelector('#minute');
    const seconds = document.querySelector('#second');

    minutes.innerHTML = time.toString();
    seconds.innerHTML = '01';

    const time_to_seconds = time * 60 + 1

    const sheet = window.document.styleSheets[0];
    sheet.insertRule('svg circle.meter {' +
        `filter: drop-shadow(0 0 3px ${color});` +
        `stroke: ${color};` +
        `animation: prog ${time_to_seconds}s linear forwards` +
        '}', sheet.cssRules.length);
}

function start_timer(timer) {

    // Execute function if clicking timer is turned on
    // play_sound('clicking')

    const minutes = document.querySelector('#minute');
    const seconds = document.querySelector('#second');

    // Change clock when finished
    if (minutes.innerHTML === '00' && seconds.innerHTML === '00') {
        clearTimeout(timer.timeout)
        play_sound(document.querySelector('#ding'));
        timer.phase === 'focus' ? timer.phase = 'break' : timer.phase = 'focus'
        change_timer(minutes, timer)
    } else {
        [minutes.innerHTML, seconds.innerHTML]  = format_time(minutes.innerHTML, seconds.innerHTML);
        timer.timeout = setTimeout(start_timer, 1000, timer);

    }
}

function change_timer(minutes, timer) {

    if (timer.phase === 'break') {
        document.querySelector('.focus').innerHTML = 'Break';
        stop_animation();
        // Check if user is logged in to save the pomodoro
        const user_logged = document.querySelector('#user-logged');
        if (user_logged.innerHTML === 'Sign Out') {
            save_pomodoro(timer);
        } else {
            display_social();
        }
    } else {
        location.reload();
    }
}

function save_pomodoro(timer) {
    // Show tag input form
    change_labels(true)
    // Save pomodoro to the API
    const token = document.querySelector('#token').value;

    document.addEventListener('keydown', event => {
        if (event.code === 'Enter' && document.querySelector('#save').style.display === 'block') {
            post_pomodoro(token, timer)
        }
    })

    document.querySelector('#save').addEventListener('click', () => {
        post_pomodoro(token, timer)
    })
}

function post_pomodoro(token, timer) {

    const tag = document.querySelector('#text-input').value

    fetch(`/api/${token}/create`, {
        method: 'POST',
        body: JSON.stringify({
            'tag': tag
        })
    })
        .then(response => {
            // append pomodoro to the index: count and today's
            if (response.status === 201) {
                // Hide tag input form
                change_labels(false);
                // Render timer and set time
                let cycle = document.querySelector('#today').innerHTML;
                cycle = parseInt(cycle) + 1;
                document.querySelector('.focus').innerHTML = 'Break';

                if (parseInt(cycle) % 4 === 0) {
                    render_timer(15, 'greenyellow');
                } else render_timer(5, 'greenyellow')
                start_timer(timer);
                append_pomodoro(tag);
            } else if (response.status === 422) {
                alert('Must not overlap saved pomodoros, please wait 24 minutes and 59 seconds.')
            }
        })
}

function append_pomodoro(tag) {

    tag = tag.toUpperCase();

    const hour = format_hour();

    const parent = document.querySelector('.todays-pomodoros');
    const node = parent.lastElementChild.cloneNode(true)
    parent.lastElementChild.classList.remove('last');
    node.lastElementChild.innerHTML = tag;
    node.firstElementChild.innerHTML = hour;
    parent.appendChild(node)

    sum_count_pomodoros(['.today', '.week', '.month', '.year'])
}


function sum_count_pomodoros(classes) {
    classes.forEach(c => {
        const node = document.querySelector(c);
        const child = node.querySelector('.right')
        child.innerHTML = (parseInt(child.innerHTML) + 1).toString();
    })
}


function format_hour() {
    const date = new Date();
    let hour = date.getHours();
    let minute = date.getMinutes();

    // Format hours to 12 time format
    if (hour > 12) {
        hour = hour - 12;

        if (hour < 10) {
            hour = '0' + hour.toString()
        } else if (minute < 10) minute = '0' + minute.toString();

        hour = `${hour.toString()}:${minute.toString()} PM`;

    } else hour = `${hour.toString()}:${minute.toString()} AM`;

    return hour.toString()
}


function change_labels(change) {
    const parent = document.querySelector('.fill-data');
    if (change) {
        parent.querySelector('#cancel').style.display = 'none';
        parent.querySelector('#save').style.display = 'block';
        parent.querySelector('.last-text').innerHTML = 'or press enter'
        parent.querySelector('.focus').style.display = 'none';
        parent.querySelector('.text-input').style.display = 'block';
        parent.querySelector('.text-input').focus();
    } else {
        parent.querySelector('#cancel').style.display = 'block';
        parent.querySelector('#save').style.display = 'none';
        parent.querySelector('.last-text').innerHTML = 'or press ESC'
        parent.querySelector('.focus').style.display = 'block';
        parent.querySelector('.text-input').style.display = 'none';
    }
}

function play_sound(sound) {
    sound.play()
}

function format_time(minutes, seconds) {


    minutes = parseInt(minutes);
    seconds = parseInt(seconds);

    if (seconds === 0) {
        minutes -= 1
        seconds = 60
    }

    seconds -= 1
    minutes = check_format(minutes);
    seconds = check_format(seconds);

    // Change title dynamically
    const title = document.title;
    document.title = `${minutes}:${seconds} | ` + title.slice(title.length - 11, title.length);

    return [minutes, seconds]
}

function check_format(time) {

    if (time < 10) {
        return ('0' + time.toString())
    }

    return time.toString()
}


function stop_animation() {
    const sheet = window.document.styleSheets[0];
    sheet.deleteRule(sheet.cssRules.length - 1);
}


function reset_timer(timer) {
    clearTimeout(timer.timeout)
}


class Timer {
    constructor() {
        this.timeout = null;
        this.phase= 'focus';
    }
}
