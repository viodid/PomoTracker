document.addEventListener('DOMContentLoaded', function () {

    const overlay = document.querySelector('#overlay');
    overlay.style.visibility = 'hidden';
    const timer = new Timer();

    document.querySelector('#start').addEventListener('click', () => {
        display_overlay(overlay, timer);
    })

    document.querySelector('#cancel').addEventListener('click', () => {
        display_overlay(overlay, timer)
        play_sound(document.querySelector('#whoosh'))
    })

    document.addEventListener('keydown', event => {

        if (event.code === 'Space' && overlay.style.visibility === 'hidden') {
            display_overlay(overlay, timer);

        } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
            display_overlay(overlay, timer);
            play_sound(document.querySelector('#whoosh'))
        }
    })
})

function display_overlay(overlay, timer, hide=false) {

    // Reset timer to 25 minutes in the background
    if (hide === true) {
        overlay.style.visibility = 'hidden';
        overlay.style.opacity = 0;
        stop_animation();
        reset_timer(timer)
    }
    else if (overlay.style.visibility === 'hidden') {
        render_timer(0, '#f1c232');
        overlay.style.visibility = 'visible';
        overlay.style.opacity = 0.97;
        start_timer(timer)

    } else {
        alert('Sure?');
        play_sound(document.querySelector('#whoosh'))
        overlay.style.visibility = 'hidden';
        overlay.style.opacity = 0;
        stop_animation();
        reset_timer(timer);
    }
}

function render_timer(time, color) {

    const minutes = document.querySelector('#minute');
    const seconds = document.querySelector('#second');

    minutes.innerHTML = time.toString();
    seconds.innerHTML = '04';

    const time_to_seconds = time * 60 + 1

    const sheet = window.document.styleSheets[0];
    sheet.insertRule('svg circle.meter {' +
        `filter: drop-shadow(0 0 3px ${color});` +
        `stroke: ${color};` +
        `animation: prog ${time_to_seconds}s linear forwards, glow 1s ${time_to_seconds - 1}s ease-in-out forwards;` +
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

    console.log(timer.timeout)

    if (timer.phase === 'break') {
        document.querySelector('.focus').innerHTML = 'Break';
        // Check if user is logged in to save the pomodoro
        const user_logged = document.querySelector('#user-logged')
        if (user_logged.innerHTML === 'Sign Out') {
            save_pomodoro();
        } else {
            display_social();
        }
    } else {
        display_overlay(document.querySelector('#overlay'), timer, hide=true)
    }
}

function save_pomodoro() {
    // Show tag input form
    change_labels(true)
    // Save pomodoro to the API
    const token = document.querySelector('#token').value;

    // add enter button eventlistener
    document.querySelector('#save').addEventListener('click', () => {
        fetch(`/api/${token}/create`, {
            method: 'POST',
            body: JSON.stringify({
                'tag': document.querySelector('#text-input').value
            })
        })
            .then(() => {
                // Hide tag input form
                change_labels(false)
                // Render timer and set time
                const cycle = document.querySelector('#today').innerHTML
                if (parseInt(cycle) % 4 === 0 && parseInt(cycle) !== 0) {
                    render_timer(15, 'greenyellow')
                } else render_timer(5, 'greenyellow')

                // append pomodoro to the index: count and today's

            })
    })
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
    return [minutes, seconds]
}

function check_format(time) {

    if (time < 10) {
        return ('0' + time.toString())
    }

    return time.toString()
}


function stop_animation() {
    return true
}


function reset_timer(timer) {
    clearTimeout(timer.timeout)
    console.log(timer)
}


class Timer {
    constructor() {
        this.timeout = null;
        this.phase= 'focus';
    }
}