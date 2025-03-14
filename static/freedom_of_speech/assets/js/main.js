/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close');

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if(navToggle){
    navToggle.addEventListener('click', (e) =>{
        e.stopPropagation();
        navMenu.classList.add('show-menu');
    });
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if(navClose){
    navClose.addEventListener('click', (e) =>{
        e.stopPropagation();
        navMenu.classList.remove('show-menu');
    });
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav__link');

const linkAction = () =>{
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== SWIPER PROJECTS ===============*/
// const swiperProjects = new Swiper('.projects__container', {
//     loop: true,
//     spaceBetween: 24,
//
//     autoplay: {
//         delay: 3000,
//         disableOnInteraction: false,
//     },
//
//     navigation: {
//         nextEl: ".swiper-button-next",
//         prevEl: ".swiper-button-prev",
//     },
//     pagination: {
//         el: ".swiper-pagination",
//     },
//
//     breakpoints: {
//         1200: {
//             slidesPerView: 2,
//             spaceBetween: -56,
//         },
//     },
// });

/*=============== SWIPER TESTIMONIAL ===============*/
const swiperTestimonial = new Swiper('.testimonial__container', {
    grabCursor: true,
    parallax: true,
    loop: true,

    autoplay: {
        delay: 10000,
        disableOnInteraction: true,
        // pauseOnMouseEnter: true,
    },

    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]');

const scrollActive = () =>{
    const scrollY = window.pageYOffset;

    sections.forEach(current =>{
        const sectionHeight = current.offsetHeight,
            sectionTop = current.offsetTop - 58,
            sectionId = current.getAttribute('id'),
            sectionsClass = document.querySelector('.nav__menu a[href*=' + sectionId + ']');

        if (sectionsClass)
            if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
                sectionsClass.classList.add('active-link');
            }else{
                sectionsClass.classList.remove('active-link');
            }
    })
}
window.addEventListener('scroll', scrollActive);

/*=============== SHOW SCROLL UP ===============*/
const scrollUp = () =>{
    const scrollUp = document.getElementById('scroll-up');
    // When the scroll is higher than 350 viewport height, add the show-scroll class to the tag with the scrollup class
    this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
        : scrollUp.classList.remove('show-scroll');
}
window.addEventListener('scroll', scrollUp);

/*=============== DARK LIGHT THEME ===============*/
const themeButton = document.getElementById('theme-button');

const themes = {'system-theme': 'light-theme', 'light-theme': 'dark-theme', 'dark-theme': 'system-theme'}
// const icons = {'light-theme': 'ri-sun-line', 'system-theme': 'ri-contrast-line', 'dark-theme': 'ri-moon-line'}

themeButton.classList.add(icons["".concat(localStorage.getItem('selected-theme'))]);

// const darkTheme = 'dark-theme'
// const iconTheme = 'ri-sun-line'

//
// // Previously selected topic (if user selected)
// const selectedTheme = selected_theme
// const selectedIcon = selected_icon
//
// window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches

// // We obtain the current theme that the interface has by validating the dark-theme class
// const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
// const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'ri-moon-line' : 'ri-sun-line'

// // We validate if the user previously chose a topic
// if (selectedTheme) {
    // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
    // document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
    // themeButton.classList[selectedIcon === 'ri-moon-line' ? 'add' : 'remove'](iconTheme)
// }

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // System - Light - Dark

    localStorage.setItem('selected-theme', themes[localStorage.getItem('selected-theme')]);
    localStorage.setItem('selected-icon', icons[localStorage.getItem('selected-theme')]);

    const selectedTheme = localStorage.getItem('selected-theme');
    const selectedIcon = localStorage.getItem('selected-icon');

    themeButton.className = `change-theme ${selectedIcon}`;
    document.body.classList.toggle('dark-theme', selectedTheme === 'dark-theme' || (selectedTheme === 'system-theme' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches));
});

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    let selectedTheme = localStorage.getItem('selected-theme')

    if (selectedTheme === 'system-theme') {
        document.body.className = event.matches ? '' : document.body.className;
        document.body.classList.toggle('dark-theme', event.matches);
    }
});

/*=============== CHANGE BACKGROUND HEADER ===============*/
const scrollHeader = () =>{
    const header = document.getElementById('header')
    // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
    this.scrollY > 0 ? header.classList.add('bg-header')
        : header.classList.remove('bg-header')
}
window.addEventListener('scroll', scrollHeader)

/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
    origin: 'bottom',
    distance: '50px',
    duration: 500,
    // delay: 100,
    // interval: 100,
    // reset: true /* Animations repeat */
    // easing: 'cubic-bezier(0.5, 0, 0, 1)',
    // interval: 0,
    // opacity: 1,
    // rotate: {
    //     x: 100,
    //     y: 100,
    //     z: 100,
    // },
    // scale: 1,
    // cleanup: true,
    // container: document.documentElement,
    // desktop: true,
    // mobile: true,
    // useDelay: 'always',
    // viewFactor: 0.0,
    // viewOffset: {
    //     top: 0,
    //     right: 0,
    //     bottom: 0,
    //     left: 0,
    // },
    // afterReset: function (el) {},
    // afterReveal: function (el) {},
    // beforeReset: function (el) {},
    // beforeReveal: function (el) {},
})

// sr.reveal(`.home__data, .constitution__content, .laws__content, .testimonial__container, .profile__data, .entry__content`, {origin: 'top'})
// sr.reveal(`.home__blob, .profile__blob, .entry__form`, {scale: 0})
// sr.reveal(`.constitution__content, .laws__content`, {scale: 0})
// sr.reveal(`.testimonial__container`, {scale: 0})
// sr.reveal(`.home__data, .profile__data`, {origin: 'top'})
sr.reveal(`.footer__container`, {origin: 'top'})
sr.reveal(`.home__info:nth-child(odd) div, .profile__info:nth-child(odd) div`, {origin: 'left'})
sr.reveal(`.home__info:nth-child(even) div, .profile__info:nth-child(even) div`, {origin: 'right'})
sr.reveal(`.contact__content:nth-child(odd)`, {origin: 'left'})
sr.reveal(`.contact__content:nth-child(even)`, {origin: 'right'})
// sr.reveal(`.members__container a:nth-child(odd)`, {origin: 'left', interval: 100, reset: false})
// sr.reveal(`.members__container a:nth-child(even)`, {origin: 'right', interval: 100, delay: 100, reset: false})
// sr.reveal(`.members__container a:nth-child(odd)`, {origin: 'left', opacity: 0})
// sr.reveal(`.members__container a:nth-child(even)`, {origin: 'right', opacity: 0})
// sr.reveal(`.members__container`, {opacity: 0})
sr.reveal(`.government__card`, {interval: 50, scale: 0})

// let number = 69;

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max) + 1;
    return Math.floor(Math.random() * (max - min) + min); // The maximum is exclusive and the minimum is inclusive
}

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    let textContent = null
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);

        textContent = obj.textContent.replace(/[0-9]/g, '');

        obj.textContent = Math.floor(progress * (end - start) + start) + textContent;

        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function getMinutesBetweenDates(startDate, endDate) {
    var diff = endDate.getTime() - startDate.getTime();
    return (diff / 60000);
}

window.onload = function() {
    // Resize text areas onlaod

    if (document.getElementById('constitution_text')) {
        text_area_auto_change(document.getElementById('constitution_text'))
    }

    if (document.getElementById('laws_text')) {
        text_area_auto_change(document.getElementById('laws_text'))
    }

    // if (document.getElementsByClassName('members__container')[0]) {
    //     text_area_auto_change(document.getElementsByClassName('members__container')[0])
    // }

    // Month Day, Year Hour:Minute:Second, id-of-element-container
    if (document.getElementById('home__date_counter')) {
        date = document.getElementById('home__info__years_value').getAttribute('data');
        document.getElementById('home__info__years_value').textContent = ''.concat(new Date(document.getElementById('home__info__years_value').getAttribute('data').replace(/-/g, "/")).toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric'}))
        // countUpFromTime(date, 'home__date_counter'); // ****** Change this line!
        // date = new Date('2023-06-01 23:23:12')
        // var today = new Date();
        // var date = new Date(today.getFullYear(), today.getMonth()+1, 0);
        countDownFromTime(date, 'home__date_counter');
    }

    if (document.getElementById('date__updated')){
        document.getElementById('date__updated').textContent = 'Обновлено '.concat(new Date(document.getElementById('date__updated').getAttribute('data').replace(/-/g, "/")).toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'}))
    }

    if (document.getElementById('date__updated_admin')){
        document.getElementById('date__updated_admin').textContent = 'Обновлено '.concat(new Date(document.getElementById('date__updated_admin').getAttribute('data').replace(/-/g, "/")).toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'}))
    }

    if (document.getElementById('profile__date_counter')) {
        date = document.getElementById('profile__info__years_value').getAttribute('data');
        countUpFromTime(date, 'profile__date_counter');
    }

    function isValidDate(d) {
        return d instanceof Date && !isNaN(d);
    }

    if (document.getElementById('profile__info__years_value')) {
        date = new Date(document.getElementById('profile__info__years_value').getAttribute('data').replace(/-/g, "/"));

        if (isValidDate(date)) {
            document.getElementById('profile__info__years_value').textContent = date.toLocaleString('ru', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
        }
        //.concat(' - ', new Date().toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric'}))
    }

    //if (document.getElementById('home__info__years_value'))
    //    document.getElementById('home__info__years_value').textContent = new Date(document.getElementById('home__info__years_value').textContent).toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric'}).concat(' - ', new Date().toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric'}));

    if (document.getElementById('footer__copy__years_value')) {
        footer__copy__years_value = document.getElementById('footer__copy__years_value');
        footer__copy__years_value.textContent = ''.concat('© Copyright ', footer__copy__years_value.textContent, '-', new Date().getFullYear(), ', @. All rights reserved');
    }

    fun_value = document.getElementById("fun_value");
    // members_value = document.getElementById("members_value");

    if (fun_value) {
        const fun_value_int = parseInt(fun_value.textContent);

        // Run with interval
        setInterval(function () {
            animateValue(fun_value, parseInt(fun_value.textContent), getRandomInt(1, fun_value_int), 1500);
        }, 5000);
        // Run once when page loaded
        setTimeout(function () {
            animateValue(fun_value, parseInt(fun_value.textContent), getRandomInt(1, fun_value_int), 1500);
        });
    }

    // if (members_value) {
    //     const members_value_int = parseInt(members_value.textContent);
    //
    //     setInterval(function () {
    //         animateValue(members_value, parseInt(members_value.textContent), getRandomInt(2000, members_value_int), 10000);
    //     }, 10000)
    //     setTimeout(function () {
    //         animateValue(members_value, parseInt(members_value.textContent), getRandomInt(2000, members_value_int), 10000);
    //     })
    // }
};
function countUpFromTime(countFrom, id) {
    var tcountFrom = new Date(countFrom.replace(/-/g, "/")).getTime();

    if (isNaN(tcountFrom))
        return

    var now = new Date().getTime(),
        // countFrom = new Date(countFrom),
        timeDifference = (now - tcountFrom);

    var secondsInADay = 60 * 60 * 1000 * 24,
        secondsInAHour = 60 * 60 * 1000;

    days = Math.floor(timeDifference / (secondsInADay) * 1);
    years = Math.floor(days / 365);
    if (years > 0){ days = days - (years * 365) }
    hours = Math.floor((timeDifference % (secondsInADay)) / (secondsInAHour) * 1);
    mins = Math.floor(((timeDifference % (secondsInADay)) % (secondsInAHour)) / (60 * 1000) * 1);
    secs = Math.floor((((timeDifference % (secondsInADay)) % (secondsInAHour)) % (60 * 1000)) / 1000 * 1);

    var idEl = document.getElementById(id);
    // idEl.getElementsByClassName('years')[0].innerHTML = years;
    // idEl.getElementsByClassName('days')[0].innerHTML = days;
    // idEl.getElementsByClassName('hours')[0].innerHTML = hours;
    // idEl.getElementsByClassName('minutes')[0].innerHTML = mins;
    // idEl.getElementsByClassName('seconds')[0].innerHTML = secs;
    idEl.textContent = ''.concat(years.toString(), 'г ', days.toString(), 'д ', hours.toString(), 'ч:', mins.toString(), 'м:', secs.toString(), 'с');

    clearTimeout(countUpFromTime.interval);
    countUpFromTime.interval = setTimeout(function(){ countUpFromTime(countFrom, id); }, 1000);
}

function parseDate(str) {
    var parts = str.split(" ");
    var dateparts = parts[0].split("-");
    var timeparts = (parts[1] || "").split(":");
    var year = +dateparts[0];
    var month = +dateparts[1];
    var day = +dateparts[2];
    var hours = timeparts[0] ? +timeparts[0] : 0;
    var minutes = timeparts[1] ? +timeparts[1] : 0;
    var seconds = timeparts[2] ? +timeparts[2] : 0;
    // Treats the string as UTC, but you can remove the `Date.UTC` part and use
    // `new Date` directly to treat the string as local time
    return new Date(Date.UTC(year, month - 1, day, hours, minutes, seconds));
}

function countDownFromTime(countTo, id, date) {
    var tcountTo = new Date(countTo.replace(/-/g, "/")).getTime();

    // var tcountTo = parseDate(countTo).getTime();

    if (isNaN(tcountTo))
        return

    var now = new Date().getTime(),
        // countTo = new Date(countTo),
        timeDifference = (tcountTo - now);

    var secondsInADay = 60 * 60 * 1000 * 24,
        secondsInAHour = 60 * 60 * 1000;

    days = Math.floor(timeDifference / (secondsInADay) * 1);
    // years = Math.floor(days / 365);
    // if (years > 0){ days = days - (years * 365) }
    hours = Math.floor((timeDifference % (secondsInADay)) / (secondsInAHour) * 1);
    mins = Math.floor(((timeDifference % (secondsInADay)) % (secondsInAHour)) / (60 * 1000) * 1);
    secs = Math.floor((((timeDifference % (secondsInADay)) % (secondsInAHour)) % (60 * 1000)) / 1000 * 1);

    var idEl = document.getElementById(id);
    // idEl.getElementsByClassName('years')[0].innerHTML = years;
    // idEl.getElementsByClassName('days')[0].innerHTML = days;
    // idEl.getElementsByClassName('hours')[0].innerHTML = hours;
    // idEl.getElementsByClassName('minutes')[0].innerHTML = mins;
    // idEl.getElementsByClassName('seconds')[0].innerHTML = secs;
    idEl.textContent = ''.concat(days.toString(), 'д ', hours.toString(), 'ч:', mins.toString(), 'м:', secs.toString(), 'с');

    clearTimeout(countDownFromTime.interval);
    countDownFromTime.interval = setTimeout(function(){ countDownFromTime(countTo, id); }, 1000);
}

const genPercent = () => {
    document.querySelector('.animated_percent').style.setProperty("--percent", Math.random());
};

const genNumber = () => {
    // number += Math.random()
    document.querySelector('.animated_number').style.setProperty("--number", Math.random());
};

function text_area_auto_change(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight) + "px";
}

$('#constitution_button').on('click', function(e) {
    e.preventDefault();
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    const constitution = $('#constitution_text');
    const constitutionMessage = $('#constitution-message')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/edit/constitution/',
        data: {
            constitution: constitution.val()
        },
        success: function(data, status, jqXHR) {
            // location.reload();
            constitution.val(data);

            constitutionMessage.removeClass('color-red')
            constitutionMessage.addClass('color-green')

            constitutionMessage.text('Изменения в конституции успешно сохранены')
            setTimeout(() => {
                constitutionMessage.text('')
            }, 5000);
            // console.log(data);
        },
        error(xhr,status,error){
            constitutionMessage.removeClass('color-green')
            constitutionMessage.addClass('color-red')

            constitutionMessage.text('Возникли проблемы с вашим запросом')
            setTimeout(() => {
                constitutionMessage.text('')
            }, 5000);
            // Some error
        },
    });
});

$('#laws_button').on('click', function(e) {
    e.preventDefault();
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    const laws = $('#laws_text');
    const lawsMessage = $('#laws-message')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/edit/laws/',
        data: {
            laws: laws.val()
        },
        success: function(data, status, jqXHR) {
            // location.reload();
            laws.val(data);

            lawsMessage.removeClass('color-red')
            lawsMessage.addClass('color-green')

            lawsMessage.text('Изменения в законах успешно сохранены')
            setTimeout(() => {
                lawsMessage.text('')
            }, 5000);

            // console.log(data);
        },
        error(xhr,status,error){
            // Some Error
            lawsMessage.removeClass('color-green')
            lawsMessage.addClass('color-red')

            lawsMessage.text('Возникли проблемы с вашим запросом')
            setTimeout(() => {
                lawsMessage.text('')
            }, 5000);
        },
    });
});

function redirect(href) {
    window.location.replace(href)

    return 0
}

$('#signin-button').on('click', function(e) {
    e.preventDefault();
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    const entryMessage = $('#entry-message')
    const username = $('#signin-username')
    const password = $('#signin-password')

    if(username.val() === '' || password.val() === ''){
        entryMessage.removeClass('color-green')
        entryMessage.addClass('color-red')

        // Show message
        entryMessage.text('Заполните все поля');

        setTimeout(() => {
            entryMessage.text('')
        }, 5000);

        return 1
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/signin/',
        data: {
            username: username.val(),
            password: password.val(),
        },
        success: function (data, status, jqXHR) {
            entryMessage.removeClass('color-red')
            entryMessage.addClass('color-green')
            entryMessage.text('Авторизация успешна')

            setTimeout(() => {
                // window.location.replace(`/freedom_of_speech/profile/${username.val()}`)
                window.location.replace("/freedom_of_speech/")
            }, 0);
            // setTimeout(redirect('/freedom_of_speech/'), 5000)
            // redirect('/freedom_of_speech/')

            // username.val('')
            // password.val('')
            //
            // setTimeout(() => {
            //     entryMessage.text('')
            // }, 5000);
        },
        error(xhr,status,error){
            entryMessage.removeClass('color-green')
            entryMessage.addClass('color-red')
            if (xhr.status === 401)
                entryMessage.text('Неверные данные')
            else
                entryMessage.text(error)

            setTimeout(() => {
                entryMessage.text('')
            }, 5000);
        }
    });
});

$('#signup-button').on('click', function(e) {
    e.preventDefault();
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    const entryMessage = $('#entry-message')
    const username = $('#signup-username')
    const password = $('#signup-password')
    const repeat_password = $('#signup-password_repeat')

    if(password.val() !== repeat_password.val()){
        entryMessage.removeClass('color-green')
        entryMessage.addClass('color-red')

        // Show message
        entryMessage.text('Пароли не совпадают');

        setTimeout(() => {
            entryMessage.text('')
        }, 5000);

        return 1
    }

    if(username.val() === '' || password.val() === '' || repeat_password.val() === ''){
        entryMessage.removeClass('color-green')
        entryMessage.addClass('color-red')

        // Show message
        entryMessage.text('Заполните все поля');

        setTimeout(() => {
            entryMessage.text('')
        }, 5000);

        return 1
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/signup/',
        data: {
            username: username.val(),
            password: password.val(),
            repeat_password: repeat_password.val(),
        },
        success: function (data, status, jqXHR) {
            entryMessage.removeClass('color-red')
            entryMessage.addClass('color-green')
            entryMessage.text('Регистрация успешна')

            setTimeout(() => {
                window.location.replace(`/freedom_of_speech/profile/${username.val()}`)
            }, 0);

            username.val('')
            password.val('')
            repeat_password.val('')
        },
        error(xhr,status,error){
            entryMessage.removeClass('color-green')
            entryMessage.addClass('color-red')

            if (xhr.status === 409)
                entryMessage.text('Такой пользователь уже зарегистрирован')
            else if (xhr.status === 500)
                entryMessage.text('Возникли проблемы во время регистрации')
            else if (xhr.status === 422)
                entryMessage.text('Возникли проблемы с вашим запросом')
            else
                entryMessage.text(error)

            setTimeout(() => {
                entryMessage.text('')
            }, 5000);
        }
    });
});

$('#username-change_button').on('click', function(e) {
    e.preventDefault();
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    const entryMessage = $('#entry-message-username')
    const username = $('#username-change_username')
    // const password = $('#username-change_password')

    if(username.val() === ''){
        entryMessage.removeClass('color-green')
        entryMessage.addClass('color-red')

        // Show message
        entryMessage.text('Заполните все поля');

        setTimeout(() => {
            entryMessage.text('')
        }, 5000);

        return 1
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/edit/username/',
        data: {
            username: username.val(),
            // password: password.val(),
        },
        success: function (data, status, jqXHR) {
            entryMessage.removeClass('color-red')
            entryMessage.addClass('color-green')

            entryMessage.text('Никнейм успешно изменено')

            new_username = username.val()

            setTimeout(() => {
                window.location.replace(`/freedom_of_speech/profile/${new_username}`)
            }, 0);

            username.val('')
            // password.val('')
        },
        error(xhr,status,error){
            entryMessage.removeClass('color-green')
            entryMessage.addClass('color-red')

            if (xhr.status === 401)
                entryMessage.text('Неверные данные')
            else if (xhr.status === 409)
                entryMessage.text('Такой пользователь уже зарегистрирован')
            else if (xhr.status === 422)
                entryMessage.text('Возникли проблемы с вашим запросом')
            else
                entryMessage.text(error)

            setTimeout(() => {
                entryMessage.text('')
            }, 5000);
        }
    });
});

$('#password-change_button').on('click', function(e) {
    e.preventDefault();
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    const entryMessage = $('#entry-message-password')
    // const old_password = $('#password-change_old_password')
    const new_password = $('#password-change_new_password')

    if(new_password.val() === ''){
        entryMessage.removeClass('color-green')
        entryMessage.addClass('color-red')

        // Show message
        entryMessage.text('Заполните все поля');

        setTimeout(() => {
            entryMessage.text('')
        }, 5000);

        return 1
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/edit/password/',
        data: {
            // old_password: old_password.val(),
            new_password: new_password.val(),
        },
        success: function (data, status, jqXHR) {
            entryMessage.removeClass('color-red')
            entryMessage.addClass('color-green')
            entryMessage.text('Пароль успешно изменен')

            // old_password.val('')
            new_password.val('')

            setTimeout(() => {
                entryMessage.text('')
            }, 5000);
        },
        error(xhr,status,error){
            entryMessage.removeClass('color-green')
            entryMessage.addClass('color-red')
            // if (xhr.status === 409)
            //     entryMessage.text('Username already registered')
            if (xhr.status === 401)
                entryMessage.text('Неверные данные')
            else if (xhr.status === 422)
                entryMessage.text('Возникли проблемы с вашим запросом')
            else
                entryMessage.text(error)

            setTimeout(() => {
                entryMessage.text('')
            }, 5000);
        }
    });
});

$('#signout-button').on('click', function(e) {
    e.preventDefault();
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/signout/',
        data: {

        },
        success: function (data, status, jqXHR) {
            setTimeout(() => {
                window.location.replace('/freedom_of_speech/')
            }, 0);
        },
        error(xhr,status,error){
            if (error)
                alert(error)
            else
                alert("status=".concat(xhr.status))
        }
    });
});

$('#logout-button').on('click', function(e) {
    e.preventDefault();
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token)
        }
    });

    $.ajax({
        type: 'post',
        url: '/freedom_of_speech/logout/',
        data: {

        },
        success: function (data, status, jqXHR) {
            alert('Вы успешно завершили все другие сеансы')

            // setTimeout(() => {
            //     window.location.replace('/freedom_of_speech/profile/')
            // }, 0);
        },
        error(xhr,status,error){
            if (error)
                alert(error)
            else
                alert("status=".concat(xhr.status))
        }
    });
});

$(document).ready(function () {
// Add smooth scrolling to all links
//     $("a").on('click', function(event) {
//         // Make sure this.hash has a value before overriding default behavior
//         if (this.hash !== "") {
//             // Prevent default anchor click behavior
//             event.preventDefault();
//
//             // Store hash
//             var hash = this.hash;
//
//             // Using jQuery's animate() method to add smooth page scroll
//             // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
//             $('html, body').animate({
//                 scrollTop: $(hash).offset().top
//             }, 500, function(){
//                 // Add hash (#) to URL when done scrolling (default click behavior)
//                 window.location.hash = hash;
//             });
//         } // End if
//     });
});

$('#contact_button').on('click', function(e) {
    e.preventDefault();

    const contactMessage = $('#contact-message')
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    // const name = $('#contact-name').val();
    // const role = $('#contact-role').val();
    const testimonial = $('#contact-testimonial');

    // Check if the field has a value
    if(testimonial.val() === ''){
        // Add or remove color
        contactMessage.removeClass('color-green')
        contactMessage.addClass('color-red')

        // Show message
        contactMessage.text('Введите текст в поле ввода');

        setTimeout(() => {
            contactMessage.text('')
        }, 5000);
    }else {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        });

        $.ajax({
            type: 'post',
            url: '/freedom_of_speech/add/testimonial/',
            data: {
                // name: name,
                // role: role,
                testimonial: testimonial.val(),
            },
            success: function(data, status, jqXHR) {
                // Show message and add color
                contactMessage.removeClass('color-red')
                contactMessage.addClass('color-green')
                contactMessage.text('Отзыв успешно отправлен')
                // contactMessage.classList.add('color-blue');
                // contactMessage.textContent = 'Testimonial was sent successfully';

                // Remove message after five seconds
                setTimeout(() => {
                    // contactMessage.text('')

                    // window.location.replace("/freedom_of_speech/")
                    window.location.reload()
                }, 0);
                // location.reload();
                // $('#constitution_text_span').text(data);
                // console.log(data);
            },
            error(xhr,status,error){
                contactMessage.removeClass('color-green')
                contactMessage.addClass('color-red')

                if (xhr.status === 422)
                    contactMessage.text('Возникли проблемы с вашим запросом')
                else
                    if (error)
                        contactMessage.text(status)
                    else
                        contactMessage.text("status=".concat(xhr.status))

                setTimeout(() => {
                    contactMessage.text('')
                }, 5000);
            },
        });

        // To clear the input fields
        testimonial.val('')
    }
});

$('#auth-telegram_button').on('click', function(e) {
    e.preventDefault();

    let link_status = false

    if ($(this).hasClass('profile__community-link__True'))
        link_status = true

    // TODO get bot id

    window.Telegram.Login.auth(
        { bot_id: '2037332308', request_access: true },
        (data) => {
            if (!data) {
                // authorization failed
                // console.log('telegram authorization failed')
                // auth_telegram_button.removeClass('profile__community-link__True')
                // auth_telegram_button.addClass('profile__community-link__False')
            }else {
                // Here you would want to validate data like described there https://core.telegram.org/widgets/login#checking-authorization
                // console.log(data)
                sendAuthDataToServer(data)
            }
        }
    );

    function sendAuthDataToServer (data){
        const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        const request_data = data
        // const type = 'telegram'

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token)
            }
        });

        $.ajax({
            type: 'post',
            url: '/freedom_of_speech/auth/telegram/',
            data: request_data,
            success: function(data, status, jqXHR) {
                // location.reload();
                // $('#constitution_text_span').text(data);
                // console.log('authorized');
                // auth_telegram_button.removeClass('profile__community-link__False')
                // auth_telegram_button.addClass('profile__community-link__True')

                setTimeout(() => {
                    window.location.replace("/freedom_of_speech/profile/")
                }, 0);
            },
            error(xhr,status,error){
                if (xhr.status === 409)
                    if (!link_status)
                        alert('Этот Telegram аккаунт уже привязан к другому персональному профилю')
                    else
                        alert('Тебе запрещено отвязывать Telegram в данный момент по одной из причин:\n\n 1. У твоего аккаунта не установлен пароль\n 2. Ты текущее правительство\n 3. Твой никнейм автоматически сгенерирован и его необходимо сменить')
                else
                    if (error)
                        alert(error)
                    else
                        alert("status=".concat(xhr.status))
                // Some error
            },
        });
    }
    // window.open("https://oauth.telegram.org/auth?bot_id=2037332308&origin=http://127.0.0.1/freedom_of_speech/auth&embed=1&request_access=write&return_to=http://127.0.0.1/freedom_of_speech/auth")

    // const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    // const name = $('#contact-name').val();
    // const role = $('#contact-role').val();
    // const testimonial = $('#contact-testimonial').val();
    // const type = 'testimonial';


    // $.ajax({
    //     type: 'get',
    //     url: '',
    //     data: {
    //         type: type,
    //         name: name,
    //         role: role,
    //         testimonial: testimonial,
    //     },
    //     success: function(data, status, jqXHR) {
    //         print(data)
    //     }
    // });
});

$('#sign-telegram_button').on('click', function(e) {
    e.preventDefault();

    window.Telegram.Login.auth(
        { bot_id: '2037332308', request_access: true },
        (data) => {
            if (!data) {
            }else {
                sendAuthDataToServer(data)
            }
        }
    );

    function sendAuthDataToServer (data){
        const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        const request_data = data
        // const type = 'telegram'

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token)
            }
        });

        $.ajax({
            type: 'post',
            url: '/freedom_of_speech/sign/telegram/',
            data: request_data,
            success: function(data, status, jqXHR) {

                setTimeout(() => {
                    window.location.replace("/freedom_of_speech/profile/")
                }, 0);
            },
            error(xhr,status,error){
                if (error)
                    alert(error)
                else
                    alert("status=".concat(xhr.status))
                // Some error
            },
        });
    }
});

$('#sign-discord_button').on('click', function(e) {
    e.preventDefault();

    let params = 'scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no'
    let url = "https://discord.com/api/oauth2/authorize?client_id=805497711264661565&redirect_uri=https%3A%2F%2Fs1te.fly.dev%2Ffreedom_of_speech%2Fsign%2Fdiscord%2F&response_type=code&scope=identify"
    // let url = "https://discord.com/api/oauth2/authorize?client_id=805497711264661565&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Ffreedom_of_speech%2Fsign%2Fdiscord%2F&response_type=code&scope=identify"
    // const url = `https://discord.com/api/oauth2/authorize?client_id=${clientId}&redirect_uri=${redirectUrl}&response_type=code&scope=${scopes}`
    const popup = createPopupWindow(url, 'AuthDiscord', 486, 802, params)

    // Set the state to localStorage when popup opens
    localStorage.setItem('auth-discord', 'false')

    // Keep track of changes to the popup state while the popup is open
    window.addEventListener('storage', function auth_discord_storage(e){
        if (e.key === 'auth-discord') {
            // reload location
            // popupData = JSON.parse(e.newValue);
            if (e.newValue === 'true') {
                // Reload this location
                setTimeout(() => {
                    window.location.replace("/freedom_of_speech/profile/")
                }, 0);
                // Delete this event listener
                // window.removeEventListener('storage', auth_discord_storage)
            }
        }
    })

});

function createPopupWindow(pageURL, pageTitle,
                        popupWinWidth, popupWinHeight, features) {
    var left = (screen.width - popupWinWidth) / 2;
    var top = (screen.height - popupWinHeight) / 2;

    return window.open(pageURL, pageTitle,
        'resizable=yes, width=' + popupWinWidth
        + ', height=' + popupWinHeight + ', top='
        + top + ', left=' + left + features);
}

$('#auth-discord_button').on('click', function(e) {
    e.preventDefault();

    let params = 'scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no'
    let url = "https://discord.com/api/oauth2/authorize?client_id=805497711264661565&redirect_uri=https%3A%2F%2Fs1te.fly.dev%2Ffreedom_of_speech%2Fauth%2Fdiscord%2F&response_type=code&scope=identify"

    // const url = `https://discord.com/api/oauth2/authorize?client_id=${clientId}&redirect_uri=${redirectUrl}&response_type=code&scope=${scopes}`
    const popup = createPopupWindow(url, 'AuthDiscord', 486, 802, params)


    // Set the state to localStorage when popup opens
    localStorage.setItem('auth-discord', 'false')

    // Keep track of changes to the popup state while the popup is open
    window.addEventListener('storage', function auth_discord_storage(e){
        if (e.key === 'auth-discord') {
            // reload location
            // popupData = JSON.parse(e.newValue);
            if (e.newValue === 'true') {
                // Reload this location
                setTimeout(() => {
                    window.location.reload()
                }, 0);
                // Delete this event listener
                // window.removeEventListener('storage', auth_discord_storage)
            }
        }
    })

});

// $('#members_value').on('click', function (e){
//     let members_value = $('#members_value')
//
//     let change = members_value.text()
//     let new_change = members_value.attr('change')
//     members_value.attr('change', change)
//     members_value.text(new_change)
//
//     let members_value_name = $('#members_value_name')
//     let name = members_value_name.text()
//     let new_name = members_value_name.attr('change')
//     members_value_name.attr('change', name)
//     members_value_name.text(new_name)
//
// })

$('.change').on('click', function (e){
    let temp = $(this)
    let parent = temp.parent().parent('div').children('h3')

    let change = temp.text()
    let new_change = temp.attr('change')
    let parent_change = parent.text()
    let new_parent_change = parent.attr('change')

    if (new_change) {
        // temp.removeClass('change')
        temp.css('animation', 'None')
        void temp[0].offsetWidth

        temp.attr('change', change)
        temp.text(new_change)

        // temp.addClass('change')
        temp.css('animation', 'fly .5s')
    }

    if (new_parent_change){
        // parent.removeClass('change')
        parent.css('animation', 'None')
        void parent[0].offsetWidth

        parent.attr('change', parent_change)
        parent.text(new_parent_change)

        // parent.addClass('change')
        parent.css('animation', 'fly .5s')
    }
})

$('.imgchange').on('click', function (e){
    let temp = $(this)

    // temp.css('transition','None')
    // temp.css('transform','None')
    // temp.css('display', 'None')
    // temp.css('animation', 'None')

    let change = temp.attr('src')
    let new_change = temp.attr('change')

    if (new_change) {
        temp.css('animation', 'None')
        temp.removeClass('imgchange')
        void temp[0].offsetWidth

        temp.attr('change', change)
        temp.attr('src', new_change)

        temp.addClass('imgchange')
    }

    // temp.css('transition','.5s')
    // temp.css('transform','rotateY(360deg)')
    // temp.css('display', 'inline-block')
    // temp.css('animation', 'popup infinite 1s')
})

$('#government__vote').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();

    $('#government__votes').toggleClass('government__votes-open')
});
$('#government__vote_president').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();

    $('#government__votes_president').toggleClass('government__votes-open')
});

$('#government__vote_parliament').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();

    $('#government__votes_parliament').toggleClass('government__votes-open')
});

$('#government__vote_judge').on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();

    $('#government__votes_judge').toggleClass('government__votes-open')
});

$('#government__votes_president').on('click', function (e){
    e.stopPropagation();

    if (e.target.tagName.toLowerCase() === 'ul')
        return

    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let candidate = $(e.target).text();

    if(confirm('Проголосовать за кандидата "'.concat(candidate, '"?'))){
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        });

        $.ajax({
            type: 'post',
            url: '/freedom_of_speech/vote/president/',
            data: {
                candidate: candidate,
            },
            success: function(data, status, jqXHR) {
                candidate = data

                $('#government__vote_president').off('click').addClass('government__vote-default').removeClass('government__vote-animation')
                $('#government__vote_president-selected').html(`<a href="/freedom_of_speech/profile/${candidate}/">${candidate}</a>`)
                $('#government__votes_president').removeClass('government__votes-open')
            },
            error(xhr,status,error){
                $('#government__votes_president').removeClass('government__votes-open')

                if (xhr.status === 422)
                    alert('Только авторизованные пользователи могут голосовать')
                else if (xhr.status === 404)
                    alert('Только пользователи которые привязали Telegram могут голосовать')
                else if (xhr.status === 409)
                    alert('Только пользователи свобода которых больше 30 дней могут голосовать')
                else if(xhr.status === 401)
                    alert('Только участники Telegram группы "Freedom of speech" могут голосовать')
                else
                    if (error)
                        alert(error)
                    else
                        alert("status=".concat(xhr.status))
            },
        });
    }else {
        console.log('Cancel vote')
    }
});

$('#government__votes_parliament').on('click', function (e){
    e.stopPropagation();

    if (e.target.tagName.toLowerCase() === 'ul')
        return

    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let candidate = $(e.target).text();

    if(confirm('Проголосовать за кандидата "'.concat(candidate, '"?'))){
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        });

        $.ajax({
            type: 'post',
            url: '/freedom_of_speech/vote/parliament/',
            data: {
                candidate: candidate,
            },
            success: function(data, status, jqXHR) {
                candidate = data

                $('#government__vote_parliament').off('click').addClass('government__vote-default').removeClass('government__vote-animation')
                $('#government__vote_parliament-selected').html(`<a href="/freedom_of_speech/profile/${candidate}/">${candidate}</a>`)
                $('#government__votes_parliament').removeClass('government__votes-open')
            },
            error(xhr,status,error){
                $('#government__votes_parliament').removeClass('government__votes-open')

                if (xhr.status === 422)
                    alert('Только авторизованные пользователи могут голосовать')
                else if (xhr.status === 404)
                    alert('Только пользователи которые привязали Telegram могут голосовать')
                else if (xhr.status === 409)
                    alert('Только пользователи свобода которых больше 30 дней могут голосовать')
                else if(xhr.status === 401)
                    alert('Только участники Telegram группы "Freedom of speech" могут голосовать')
                else
                    if (error)
                        alert(error)
                    else
                        alert("status=".concat(xhr.status))
            },
        });
    }else {
        console.log('Cancel vote')
    }
});

$('#government__votes_judge').on('click', function (e){
    e.stopPropagation();

    if (e.target.tagName.toLowerCase() === 'ul')
        return

    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let candidate = $(e.target).text();

    let confirm_text

    if (candidate === '—') {
        confirm_text = 'Снять кандидата?'
        candidate = ''
    }
    else
        confirm_text = 'Проголосовать за кандидата "'.concat(candidate, '"?')

    if(confirm(confirm_text)){
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        });

        $.ajax({
            type: 'post',
            url: '/freedom_of_speech/vote/judge/',
            data: {
                candidate: candidate,
            },
            success: function(data, status, jqXHR) {
                candidate = data

                if (candidate === ''){
                    $('#government__vote_judge-selected').html('Выбери <i class="ri-arrow-down-circle-line"></i>')
                    $('#government__vote_judge').addClass('government__vote-animation').removeClass('government__vote-default')
                }else {
                    $('#government__vote_judge-selected').html(`${candidate} <i class="ri-arrow-down-circle-line"></i>`)
                    $('#government__vote_judge').addClass('government__vote-default').removeClass('government__vote-animation')
                }

                $('#government__votes_judge').removeClass('government__votes-open')
            },
            error(xhr,status,error){
                $('#government__votes_judge').removeClass('government__votes-open')

                if (xhr.status === 404)
                    if (candidate === '')
                        alert('Судьи в данный момент нет')
                    else
                        alert('Этот пользователь не может быть Судьей')
                else if (xhr.status === 409)
                    alert('Этот пользователь не может быть Судьей')
                else if(xhr.status === 401)
                    alert('Только участники Telegram группы "Freedom of speech" могут выбирать Судью')
                else
                    if (error)
                        alert(error)
                    else
                        alert("status=".concat(xhr.status))
                // contactMessage.text('Возникли проблемы с вашим запросом')
            },
        });
    }else {
        console.log('Cancel vote')
    }
});

$('#government__votes').on('click', function (e){
    e.stopPropagation()

    if (e.target.tagName.toLowerCase() === 'ul')
        return

    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let opinion = $(e.target).text();

    let confirm_text;
    let government__votes = e.target;

    confirm_text = 'Проголосовать "'.concat(opinion.concat('"?'));

    opinion = opinion === 'Поддерживаю';

    if(confirm(confirm_text)){
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        });

        $.ajax({
            type: 'post',
            url: '/freedom_of_speech/vote/referendum/',
            data: {
                opinion: opinion,
            },
            success: function(data, status, jqXHR) {
                $('#government__votes').removeClass('government__votes-open')
                $('#government__votes .government__votes-active').removeClass('government__votes-active')
                $(government__votes).addClass('government__votes-active')
                // Get values of referendum
                // referendum_votes_count = Number($('#referendum__percent').attr('referendum_votes_count'))
                // telegram_members_count = Number($('#referendum__percent').attr('telegram_members_count'))

                if (data === 'True') {
                    // Change referendum percent to +1 vote
                    // $('#referendum__percent').attr('referendum_votes_count', referendum_votes_count+1)
                    // referendum_percent = parseInt((referendum_votes_count+1)/telegram_members_count*100)
                    // $('#referendum__percent').text(`Референдум ${referendum_percent}%`)
                    alert('Вы изменили свой голос за Референдум')
                }
                else {
                    // Change referendum percent to -1 vote
                    // $('#referendum__percent').attr('referendum_votes_count', referendum_votes_count-1)
                    // referendum_percent = parseInt((referendum_votes_count-1)/telegram_members_count*100)
                    // $('#referendum__percent').text(`Референдум ${referendum_percent}%`)
                    alert('Вы изменили свой голос против Референдума')
                }
            },
            error(xhr,status,error){
                $('#government__votes').removeClass('government__votes-open')

                if (xhr.status === 409)
                    alert('В данный момент Вы не можете голосовать за референдум по одной из причин:\n\n1. В данный момент проходят выборы')
                else if (xhr.status === 422)
                    alert('Только авторизованные пользователи могут голосовать за референдум')
                else
                    if (error)
                        alert(error)
                    else
                        alert("status=".concat(xhr.status))
            },
        });
    }else {
        console.log('Cancel vote')
    }
});

$('.government__card').on('click', function stand(e){
    // if (e.target.tagName.toLowerCase() in {'a': '', 'ul': '', 'li': ''})
    //     return
    e.stopPropagation()

    if ($(this).attr('stand'))
        return

    if (e.target.tagName.toLowerCase() === 'a')
        return

    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let role = $(this).children('h2.government__title').text().replace(/[\n\t\r ]/g, '');
    let confirm_text
    let government__card = this

    // if already candidate
    if ($(this).find('.government__border').hasClass('government__border-selected')) {
        confirm_text = 'Снять свою кандидатуру?'

        role = ''
    } else {
        confirm_text = 'Баллотироваться на "'.concat(role, '"?')

        role_text = role

        if (role === 'Президент')
            role = 'president'
        else if (role === 'Парламент')
            role = 'parliament'
        else if (role === 'Судья')
            role = 'judge'
    }

    if(confirm(confirm_text)){
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        });

        $.ajax({
            type: 'post',
            url: '/freedom_of_speech/vote/candidate/',
            data: {
                role: role,
            },
            success: function(data, status, jqXHR) {
                role = data
                $('.government__border').removeClass('government__border-selected')

                if(role)
                    $(government__card).find('.government__border').addClass('government__border-selected')
            },
            error(xhr,status,error){
                if (xhr.status === 409) {
                    if (role !== 'judge')
                        alert(`В данный момент Вы не можете баллотироваться на "${role_text}" по одной из причин:\n\n1. Только пользователи свобода которых больше 30 дней могут баллотироваться`)
                    else
                        alert(`В данный момент Вы не можете баллотироваться на "${role_text}" по одной из причин:\n\n1. Только пользователи свобода которых больше 30 дней могут баллотироваться\n2. Вы являетесь Президентом или Парламентом и не можете баллотироваться на "${role_text}"`)
                }
                else if(xhr.status === 401)
                    alert(`Только участники Telegram группы "Freedom of speech" могут баллотироваться на "${role_text}"`)
                else if(xhr.status === 422)
                    alert(`Только авторизованные пользователи могут баллотироваться на "${role_text}"`)
                else
                    if (error)
                        alert(error)
                    else
                        alert("status=".concat(xhr.status))
            },
        });
    }else {
        console.log('Cancel vote')
    }
});

$('#date__updated_admin').on('click', function (e){
    e.stopPropagation()

    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let target = ''
    let username = ''
    try {
        username = window.location.href.split('freedom_of_speech/profile/')[1].replace('/', '')
    }catch (e){
        // console.log(e.message)
    }

    if ($(this).parent().parent().hasClass('home__data'))
        target = 'chat'
    else if ($(this).parent().parent().hasClass('profile__data'))
        target = 'member'

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        }
    });

    $.ajax({
        type: 'post',
        url: `/freedom_of_speech/update/${target}/`,
        data: {
            username: username,
        },
        success: function(data, status, jqXHR) {
            setTimeout(() => {
                window.location.reload()
            }, 0);
        },
        error(xhr,status,error){
            // if(xhr.status === 404)
            //     alert('Пользователь не является участником группы')
            if (xhr.status === 422)
                alert('Произошла ошибка во время обновления данных')
            else if(xhr.status === 429)
                alert('Обновлять данные можно только каждые 30 минут')
            else
                if (error)
                    alert(error)
                else
                    alert("status=".concat(xhr.status))
        },
    });
});

function sortMembers(container, sortBy, reverse) {
    var items = container.children('a').sort(function (a, b) {
        var compA = $(a).attr(sortBy);
        var compB = $(b).attr(sortBy);

        return reverse ? compB.localeCompare(compA, undefined, {'numeric': true}) : compA.localeCompare(compB, undefined, {'numeric': true});
    });

    container.append(items);
}

$('#members-sort').on('click', function (event){
    // 'reactions_count', 'reactions_count':
    //  'Реакций', 'Реакций':
    var iter_sort = {'lvl': 'messages_count', 'messages_count': 'voicetime', 'voicetime': 'lvl'};
    var iter_sort_text = {'Уровень': 'Сообщений', 'Сообщений': 'Время', 'Время': 'Уровень'};

    var members = $('.members__container');

    var text = $(this).text().trim();
    var sort = '';
    var reverse = true;

    if (text === 'Уровень'){
        sort = iter_sort['lvl'];
    } else if (text === 'Сообщений'){
        sort = iter_sort['messages_count'];
    // } else if (text === 'Реакций'){
    //     sort = iter_sort['reactions_count'];
    } else if (text === 'Время'){
        sort = iter_sort['voicetime'];
    }

    $(this).html(`<i class="ri-filter-3-line"></i> ${iter_sort_text[text]}`)

    sortMembers(members, sort, reverse);
});

$('#members-search').on('input', function (event){
    let filter = $(this)[0].value.toLowerCase();
    let nodes = $('.members__container').children('a');

    for (let i = 0; i < nodes.length; i++) {
        if (nodes[i].innerText.toLowerCase().includes(filter)) {
            nodes[i].style.display = "flex";
        } else {
            nodes[i].style.display = "none";
        }
    }
})

$('#members-search').on('focusout', function (event) {
    $(this).animate({width: '0vw'}, {easing: 'linear', duration: 100});
})

$('.members__filters #search').on('click', function (event) {
    let search_input = $('#members-search')

    search_input.val('')

    let nodes = $('.members__container').children('a');

    for (let i = 0; i < nodes.length; i++) {
        nodes[i].style.display = "flex";
    }

    search_input.animate({width: '50vw'}, {easing: 'linear', duration: 100}).focus();
})

// Prevent menu from closing by clicking inside of it
$('#nav-menu').on('click', function (e){
    e.stopPropagation()
});

$(document).on('click', function (e){
    // Close all popup menus
    $('#government__votes_president').removeClass('government__votes-open')
    $('#government__votes_parliament').removeClass('government__votes-open')
    $('#government__votes_judge').removeClass('government__votes-open')
    $('#government__votes').removeClass('government__votes-open')

    $('#nav-menu').removeClass('show-menu')
});


document.addEventListener('dblclick', function(event) {
    event.preventDefault();
}, { passive: false });

// $('#vote_button').on('click', function (e){
//     const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
//     let confirm_text
//
//     confirm_text = 'Начать внеочередные выборы?'
//
//     if(confirm(confirm_text)){
//         $.ajaxSetup({
//             beforeSend: function(xhr, settings) {
//                 xhr.setRequestHeader('X-CSRFToken', csrf_token);
//             }
//         });
//
//         $.ajax({
//             type: 'post',
//             url: '/freedom_of_speech/vote/extraordinary/',
//             data: {
//
//             },
//             success: function(data, status, jqXHR) {
//
//             },
//             error(xhr,status,error){
//                 if (xhr.status === 422)
//                     console.log('422')
//             },
//         });
//     }else {
//         console.log('Cancel extraordinary')
//     }
// });
