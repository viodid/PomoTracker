document.addEventListener('DOMContentLoaded', function () {

    const overlay = document.querySelector('#overlay');
    overlay.style.visibility = 'hidden';
    const timer = new Timer(25, 4)

    document.querySelector('#start').addEventListener('click', () => {
        display_overlay(overlay);
        render_timer(timer);
    })

    document.querySelector('#cancel').addEventListener('click', () => {
        display_overlay(overlay)
        clearInterval(timer.interval)
    })

    document.addEventListener('keydown', event => {
        if (event.code === 'Space' && overlay.style.visibility === 'hidden') {
            display_overlay(overlay);
            render_timer(timer);
        } else if (event.code === 'Escape' && overlay.style.visibility === 'visible') {
            display_overlay(overlay);
            clearInterval(timer.interval)
        }
    })
})

function display_overlay(element) {
    if (element.style.visibility === 'hidden') {
        element.style.visibility = 'visible';
        element.style.opacity = 0.97;
    } else {
        alert('Sure?');
        element.style.visibility = 'hidden';
        element.style.opacity = 0;
    }
}

function render_timer(timer) {
    const minutes = document.querySelector('#minute');
    const seconds = document.querySelector('#second');
    if (minutes.innerHTML === '00' && seconds.innerHTML === '00') {
        clearTimeout(timer.interval);
        minutes.innerHTML = '05';
        //save_pomodoro()
        return
    }
    [minutes.innerHTML, seconds.innerHTML]  = format_time(minutes.innerHTML, seconds.innerHTML);
    timer.interval = setTimeout(render_timer, 1000, timer);
}

function format_time(minutes, seconds) {
    console.log(minutes, seconds)
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


class Timer {
    constructor(clock, cycle) {
        this.clock = clock;
        this.cycle = cycle;
        this.interval = null;
    }
}