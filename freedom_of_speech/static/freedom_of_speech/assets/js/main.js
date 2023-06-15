/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close')

/*===== MENU SHOW =====*/
/* Validate if constant exists */
if(navToggle){
    navToggle.addEventListener('click', (e) =>{
        e.stopPropagation()
        navMenu.classList.add('show-menu')
    })
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if(navClose){
    navClose.addEventListener('click', (e) =>{
        e.stopPropagation()
        navMenu.classList.remove('show-menu')
    })
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav__link')

const linkAction = () =>{
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== SWIPER PROJECTS ===============*/
const swiperProjects = new Swiper('.projects__container', {
    loop: true,
    spaceBetween: 24,

    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    pagination: {
        el: ".swiper-pagination",
    },

    breakpoints: {
        1200: {
            slidesPerView: 2,
            spaceBetween: -56,
        },
    },
});

/*=============== SWIPER TESTIMONIAL ===============*/
const swiperTestimonial = new Swiper('.testimonial__container', {
    grabCursor: true,

    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]')

const scrollActive = () =>{
    const scrollY = window.pageYOffset

    sections.forEach(current =>{
        const sectionHeight = current.offsetHeight,
            sectionTop = current.offsetTop - 58,
            sectionId = current.getAttribute('id'),
            sectionsClass = document.querySelector('.nav__menu a[href*=' + sectionId + ']')

        if (sectionsClass)
            if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
                sectionsClass.classList.add('active-link')
            }else{
                sectionsClass.classList.remove('active-link')
            }
    })
}
window.addEventListener('scroll', scrollActive)

/*=============== SHOW SCROLL UP ===============*/
const scrollUp = () =>{
    const scrollUp = document.getElementById('scroll-up')
    // When the scroll is higher than 350 viewport height, add the show-scroll class to the tag with the scrollup class
    this.scrollY >= 350 ? scrollUp.classList.add('show-scroll')
        : scrollUp.classList.remove('show-scroll')
}
window.addEventListener('scroll', scrollUp)

/*=============== DARK LIGHT THEME ===============*/
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'ri-sun-line'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'ri-moon-line' : 'ri-sun-line'

// We validate if the user previously chose a topic
if (selectedTheme) {
    // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
    document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
    themeButton.classList[selectedIcon === 'ri-moon-line' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})

/*=============== CHANGE BACKGROUND HEADER ===============*/
const scrollHeader = () =>{
    const header = document.getElementById('header')
    // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
    this.scrollY >= 50 ? header.classList.add('bg-header')
        : header.classList.remove('bg-header')
}
window.addEventListener('scroll', scrollHeader)

/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '50px',
    duration: 500,
    // delay: 0,
    // interval: 100,
    // reset: true /* Animations repeat */
})

sr.reveal(`.home__data, .constitution__container, .laws__container, .testimonial__container, .footer__container, .profile__data, .entry__container`)
sr.reveal(`.home__info:nth-child(odd) div, .profile__info:nth-child(odd) div`, {origin: 'left'})
sr.reveal(`.home__info:nth-child(even) div, .profile__info:nth-child(even) div`, {origin: 'right'})
sr.reveal(`.contact__content:nth-child(odd)`, {origin: 'left'})
sr.reveal(`.contact__content:nth-child(even)`, {origin: 'right'})
sr.reveal(`.government__card`, {interval: 50})

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
    // Month Day, Year Hour:Minute:Second, id-of-element-container
    if (document.getElementById('home__date_counter')) {
        date = document.getElementById('home__info__years_value').textContent;
        document.getElementById('home__info__years_value').textContent = ''.concat(new Date(document.getElementById('home__info__years_value').textContent.replace(/-/g, "/")).toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric'}))
        // countUpFromTime(date, 'home__date_counter'); // ****** Change this line!
        // date = new Date('2023-06-01 23:23:12')
        // var today = new Date();
        // var date = new Date(today.getFullYear(), today.getMonth()+1, 0);
        countDownFromTime(date, 'home__date_counter');
    }

    if (document.getElementById('date__updated')){
        document.getElementById('date__updated').textContent = 'Обновлено '.concat(new Date(document.getElementById('date__updated').textContent.replace(/-/g, "/")).toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'}))
    }

    if (document.getElementById('profile__date_counter')) {
        date = document.getElementById('profile__info__years_value').textContent;
        countUpFromTime(date, 'profile__date_counter');
    }

    if (document.getElementById('profile__info__years_value'))
        document.getElementById('profile__info__years_value').textContent = new Date(document.getElementById('profile__info__years_value').textContent.replace(/-/g, "/")).toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric'}).concat(' - ', new Date().toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric'}))

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

        setInterval(function () {
            animateValue(fun_value, parseInt(fun_value.textContent), getRandomInt(1, fun_value_int), 1500);
        }, 5000);
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
    idEl.textContent = ''.concat(years.toString(), ' г ', days.toString(), ' д ', hours.toString(), 'ч:', mins.toString(), 'м:', secs.toString(), 'с');

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
    idEl.textContent = ''.concat(days.toString(), ' д ', hours.toString(), 'ч:', mins.toString(), 'м:', secs.toString(), 'с');

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
            constitution: constitution.text()
        },
        success: function(data, status, jqXHR) {
            // location.reload();
            $('#constitution_text_span').text(data);

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
            laws: laws.text()
        },
        success: function(data, status, jqXHR) {
            // location.reload();
            $('#laws_text_span').text(data);

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
            }, 3000);
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
            }, 3000);

            username.val('')
            password.val('')
            repeat_password.val('')
        },
        error(xhr,status,error){
            entryMessage.removeClass('color-green')
            entryMessage.addClass('color-red')

            if (xhr.status === 409)
                entryMessage.text('Такой пользователь уже зарегистрирован')

            if (xhr.status === 500)
                entryMessage.text('Возникли проблемы во время регистрации')

            if (xhr.status === 422)
                entryMessage.text('Возникли проблемы с вашим запросом')

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
    const password = $('#username-change_password')

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
        url: '/freedom_of_speech/edit/username/',
        data: {
            username: username.val(),
            password: password.val(),
        },
        success: function (data, status, jqXHR) {
            entryMessage.removeClass('color-red')
            entryMessage.addClass('color-green')

            entryMessage.text('Никнейм успешно изменено')

            new_username = username.val()

            setTimeout(() => {
                window.location.replace(`/freedom_of_speech/profile/${new_username}`)
            }, 3000);

            username.val('')
            password.val('')
        },
        error(xhr,status,error){
            entryMessage.removeClass('color-green')
            entryMessage.addClass('color-red')

            if (xhr.status === 401)
                entryMessage.text('Неверные данные')

            if (xhr.status === 409)
                entryMessage.text('Такой пользователь уже зарегистрирован')

            if (xhr.status === 422)
                entryMessage.text('Возникли проблемы с вашим запросом')

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
    const old_password = $('#password-change_old_password')
    const new_password = $('#password-change_new_password')

    if(old_password.val() === '' || new_password.val() === ''){
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
            old_password: old_password.val(),
            new_password: new_password.val(),
        },
        success: function (data, status, jqXHR) {
            entryMessage.removeClass('color-red')
            entryMessage.addClass('color-green')
            entryMessage.text('Пароль успешно изменен')

            old_password.val('')
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

            if (xhr.status === 422)
                entryMessage.text('Возникли проблемы с вашим запросом')

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
            }, 1000);
        },
        error(xhr,status,error){
            // Some error
        }
    });
});

$(document).ready(function () {
    // const signup_password = $('#signup-password')
    // const entry_message = $('#entry-message')
    //
    // signup_password.keyup(function () {
    //     entry_message.html(checkStrength(signup_password.val()))
    // })
    // function checkStrength(password) {
    //     var strength = 0
    //     if (password.length < 6) {
    //         entry_message.removeClass()
    //         entry_message.addClass('short__password')
    //         return 'Too short'
    //     }
    //     if (password.length > 7) strength += 1
    //     // If password contains both lower and uppercase characters, increase strength value.
    //     if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1
    //     // If it has numbers and characters, increase strength value.
    //     if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1
    //     // If it has one special character, increase strength value.
    //     if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
    //     // If it has two special characters, increase strength value.
    //     if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
    //     // Calculated strength value, we can return messages
    //     // If value is less than 2
    //     if (strength < 2) {
    //         entry_message.removeClass()
    //         entry_message.addClass('weak__password')
    //         return 'Weak'
    //     } else if (strength == 2) {
    //         entry_message.removeClass()
    //         entry_message.addClass('good__password')
    //         return 'Good'
    //     } else {
    //         entry_message.removeClass()
    //         entry_message.addClass('strong__password')
    //         return 'Strong'
    //     }
    // }
    return 1
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
                }, 1000);
                // location.reload();
                // $('#constitution_text_span').text(data);
                // console.log(data);
            },
            error(xhr,status,error){
                contactMessage.removeClass('color-green')
                contactMessage.addClass('color-red')

                if (xhr.status === 422)
                    contactMessage.text('Возникли проблемы с вашим запросом')

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

    auth_telegram_button = $('#auth-telegram_button')

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
                }, 1000);
            },
            error(xhr,status,error){
                if (xhr.status === 409)
                    alert('Твоя роль не позволяет отвязать Telegram')
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

    if(confirm('Проголосовать за кандидата '.concat(candidate, '?'))){
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

                $('#government__vote_president').off('click')
                $('#government__vote_president-selected').prop('href', "/freedom_of_speech/profile/".concat(candidate, '/')).text(candidate)
                $('#government__votes_president').removeClass('government__votes-open')
            },
            error(xhr,status,error){
                $('#government__votes_president').removeClass('government__votes-open')

                if (xhr.status === 403)
                    console.log(403)
                if (xhr.status === 422)
                    alert('Только авторизованные пользователи могут голосовать')
                if (xhr.status === 404)
                    alert('Только пользователи которые привязали Telegram могут голосовать')
                if (xhr.status === 409)
                    alert('Только пользователи свобода которых больше 30 дней могут голосовать')
                if(xhr.status === 401)
                    alert('Только участники Telegram группы "Freedom of speech" могут голосовать')
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

    if(confirm('Проголосовать за кандидата '.concat(candidate, '?'))){
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

                $('#government__vote_parliament').off('click')
                $('#government__vote_parliament-selected').prop("href", "/freedom_of_speech/profile/".concat(candidate, '/')).text(candidate)
                $('#government__votes_parliament').removeClass('government__votes-open')
            },
            error(xhr,status,error){
                $('#government__votes_parliament').removeClass('government__votes-open')

                if (xhr.status === 403)
                    console.log(403)
                if (xhr.status === 422)
                    alert('Только авторизованные пользователи могут голосовать')
                if (xhr.status === 404)
                    alert('Только пользователи которые привязали Telegram могут голосовать')
                if (xhr.status === 409)
                    alert('Только пользователи свобода которых больше 30 дней могут голосовать')
                if(xhr.status === 401)
                    alert('Только участники Telegram группы "Freedom of speech" могут голосовать')
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

    if (candidate === '—')
        confirm_text = 'Снять кандидата?'
    else
        confirm_text = 'Проголосовать за кандидата '.concat(candidate, '?')

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

                // $('#government__vote_judge').off('click')
                $('#government__vote_judge-selected').prop("href", "/freedom_of_speech/profile/".concat(candidate, '/')).text(candidate)
                $('#government__votes_judge').removeClass('government__votes-open')
            },
            error(xhr,status,error){
                $('#government__votes_judge').removeClass('government__votes-open')

                if (xhr.status === 422)
                    console.log('422')
                if (xhr.status === 404)
                    if (candidate === '')
                        alert('Судьи в данный момент нет')
                    else
                        alert('Этот пользователь не может быть судьей')
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

    confirm_text = opinion.concat('?');

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
            },
            error(xhr,status,error){
                $('#government__votes').removeClass('government__votes-open')

                if (xhr.status === 422)
                    console.log('422')
                if (xhr.status === 409)
                    alert('В данный момент Вы не можете голосовать за референдум')
            },
        });
    }else {
        console.log('Cancel vote')
    }
});

$('.government__card').on('click', function (e){
    // if (e.target.tagName.toLowerCase() in {'a': '', 'ul': '', 'li': ''})
    //     return
    e.stopPropagation()

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
        confirm_text = 'Баллотироваться на '.concat(role, '?')

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
                if (xhr.status === 422)
                    console.log('422')
                if (xhr.status === 409)
                    alert('В данный момент Вы не можете баллотироваться')
            },
        });
    }else {
        console.log('Cancel vote')
    }
});

$(document).on('click', function (e){
    // Close all popup menus
    $('#government__votes_president').removeClass('government__votes-open')
    $('#government__votes_parliament').removeClass('government__votes-open')
    $('#government__votes_judge').removeClass('government__votes-open')
    $('#government__votes').removeClass('government__votes-open')

    $('#nav-menu').removeClass('show-menu')
});

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
