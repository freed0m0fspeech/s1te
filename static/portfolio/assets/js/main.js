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
    // loop: true,
    // spaceBetween: 24,
    grabCursor: true,

    autoplay: {
        delay: 10000,
        disableOnInteraction: true,
        // pauseOnMouseEnter: true,
    },

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
            // spaceBetween: -56,
        },
    },
});

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

/*=============== EMAIL JS ===============*/
const contactForm = document.getElementById('contact-form'),
    contactName = document.getElementById('contact-name'),
    contactEmail = document.getElementById('contact-email'),
    contactProject = document.getElementById('contact-project'),
    contactMessage = document.getElementById('contact-message')

const sendEmail = (e) =>{
    e.preventDefault()

    // Check if the field has a value
    if(contactName.value === '' || contactEmail.value === '' || contactProject.value === ''){
        // Add or remove color
        contactMessage.classList.remove('color-green')
        contactMessage.classList.add('color-red')

        // Show message
        contactMessage.textContent = 'Write information in all input fields'
    }else {
        // serviceID - templateID - #form - publicKey
        emailjs.sendForm('service_y4ztgpp', 'template_fdxe4ze', '#contact-form', 'tqRfNDsa-d1up1Yus').then(() => {
            // Show message and add color
            contactMessage.classList.add('color-green')
            contactMessage.textContent = 'Message was sent successfully'

            // Remove message after five seconds
            setTimeout(() => {
                contactMessage.textContent = ''
            }, 5000)
        }, (error) => {
            alert("Something went wrong ".concat(error))
        })

        // To clear the input fields
        contactName.value = ''
        contactEmail.value = ''
        contactProject.value = ''
    }
}
// contactForm.addEventListener('submit', sendEmail)

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

const themes = {'system-theme': 'light-theme', 'light-theme': 'dark-theme', 'dark-theme': 'system-theme'}
// const icons = {'light-theme': 'ri-sun-line', 'system-theme': 'ri-contrast-line', 'dark-theme': 'ri-moon-line'}

themeButton.classList.add(icons["".concat(localStorage.getItem('selected-theme'))])

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

const header = document.getElementById('header');

/*=============== CHANGE BACKGROUND HEADER ===============*/
const scrollHeader = () => {
    // const header = document.getElementById('header');

    // When the scroll is greater than 0, add the bg-header class to the header tag
    window.scrollY > 0 ? header.classList.add('bg-header') : header.classList.remove('bg-header');
};

window.addEventListener('scroll', scrollHeader);

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]')
const headerHeight = parseFloat(window.getComputedStyle(header).getPropertyValue('height'))

const scrollActive = () =>{
    const scrollY = window.pageYOffset

    sections.forEach(current =>{
        const sectionHeight = current.offsetHeight,
            sectionTop = current.offsetTop - headerHeight * 2,
            sectionId = current.getAttribute('id'),
            sectionsClass = document.querySelector('.nav__menu a[href*=' + sectionId + ']')

        if(scrollY > sectionTop && scrollY <= sectionTop + sectionHeight){
            sectionsClass.classList.add('active-link')
        }else{
            sectionsClass.classList.remove('active-link')
        }
    })
}
window.addEventListener('scroll', scrollActive)

/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
    origin: 'bottom',
    distance: '50px',
    duration: 500,
    // delay: 400,
    // interval: 100,
    // reset: true /* Animations repeat */
})

// sr.reveal(`.home__data, .projects__container, .testimonial__container`, {origin: 'top'})
// sr.reveal(`.projects__container, .testimonial__container`, {scale: 0})
// sr.reveal(`.home__blob`, {scale: 0})
sr.reveal(`.footer__container`, {origin: 'top'})
sr.reveal(`.home__info:nth-child(odd) div`, {origin: 'left'})
sr.reveal(`.home__info:nth-child(even) div`, {origin: 'right'})
sr.reveal(`.skills__content:nth-child(odd), .contact__content:nth-child(odd)`, {origin: 'left'})
sr.reveal(`.skills__content:nth-child(even), .contact__content:nth-child(even)`, {origin: 'right'})
sr.reveal(`.skills__data`, {interval: 50, scale: 5})
sr.reveal(`.qualification__content:nth-child(odd)`, {origin: 'left'})
sr.reveal(`.qualification__content:nth-child(even)`, {origin: 'right'})
sr.reveal(`.services__card`, {interval: 50, scale: 0})

window.onload = function() {
    // if (document.getElementById('project_pushed-at')) {
    //     console.log(document.getElementById('project_pushed-at').textContent.replace(/-/g, "/").replace('T', ' ').replace('Z', ''))
    //     document.getElementById('project_pushed-at').textContent = 'Обновлено '.concat(new Date(document.getElementById('project_pushed-at').textContent.replace(/-/g, "/").replace('T', ' ').replace('Z', '')).toLocaleString('ru', {month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'}))
    // }

    // Month Day, Year Hour:Minute:Second, id-of-element-container
    countUpFromTime("Sep 1, 2017 12:00:00", 'home__date_counter'); // ****** Change this line!
    document.getElementById('home__info__years_value').textContent = ''.concat('2017-', new Date().getFullYear());
    document.getElementById('footer__copy__years_value').textContent = ''.concat('© Copyright 2017-', new Date().getFullYear(), ', @. All rights reserved');
};

$(document).ready(function () {
    $('.projects_pushed-at').each(function () {
        let pushed_at = $(this)[0]
        pushed_at.textContent = 'pushed at '.concat(new Date(pushed_at.textContent.replace(/-/g, "/").replace('T', ' ').replace('Z', '')).toLocaleString('en', {month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'}).concat(' (UTC)'))
    })
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

function countUpFromTime(countFrom, id) {
    var tcountFrom = new Date(countFrom.replace(/-/g, "/")).getTime();

    if (isNaN(tcountFrom))
        return


    var now = new Date(),
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
    idEl.textContent = ''.concat(years.toString(), ' year(s) ', days.toString(), ' day(s) ', hours.toString(), 'h:', mins.toString(), 'm:', secs.toString(), 's');

    clearTimeout(countUpFromTime.interval);
    countUpFromTime.interval = setTimeout(function(){ countUpFromTime(countFrom, id); }, 1000);
}

$('#contact_button').on('click', function(e) {
    e.preventDefault();

    const contactMessage = $('#contact-message')
    const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    // const name = $('#contact-name').val();
    // const role = $('#contact-role').val();
    const testimonial = $('#contact-testimonial');
    // const name = $('#contact-name');
    // const role = $('#contact-role')

    // Check if the field has a value

    // if (name.val() === ''){
    //     // Add or remove color
    //     contactMessage.removeClass('color-green')
    //     contactMessage.addClass('color-red')
    //
    //     // Show message
    //     contactMessage.text('Write your name');
    //
    //     setTimeout(() => {
    //         contactMessage.text('')
    //     }, 5000);
    //
    //     return
    // }
    //
    // if (role.val() === ''){
    //     // Add or remove color
    //     contactMessage.removeClass('color-green')
    //     contactMessage.addClass('color-red')
    //
    //     // Show message
    //     contactMessage.text('Write your role');
    //
    //     setTimeout(() => {
    //         contactMessage.text('')
    //     }, 5000);
    //
    //     return
    // }

    if(testimonial.val() === ''){
        // Add or remove color
        contactMessage.removeClass('color-green')
        contactMessage.addClass('color-red')

        // Show message
        contactMessage.text('Write your testimonial');

        setTimeout(() => {
            contactMessage.text('')
        }, 5000);

        return
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', csrf_token);
        }
    });

    $.ajax({
        type: 'post',
        url: '/portfolio/add/testimonial/',
        data: {
            // name: name.val(),
            // role: role.val(),
            testimonial: testimonial.val(),
        },
        success: function(data, status, jqXHR) {
            // Show message and add color
            contactMessage.removeClass('color-red')
            contactMessage.addClass('color-green')
            contactMessage.text('Testimonial was sent successfully')
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
                contactMessage.text('Something went wrong')

            setTimeout(() => {
                contactMessage.text('')
            }, 5000);
        },
    });

    // To clear the input fields
    testimonial.val('')
});

// Prevent menu from closing by clicking inside of it
$('#nav-menu').on('click', function (e){
    e.stopPropagation()
});

$(document).on('click', function (e){
    // Close all popup menus

    $('#nav-menu').removeClass('show-menu')
});

document.addEventListener('dblclick', function(event) {
    event.preventDefault();
}, { passive: false });
