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

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll('section[id]')

const scrollActive = () =>{
    const scrollY = window.pageYOffset

    sections.forEach(current =>{
        const sectionHeight = current.offsetHeight,
            sectionTop = current.offsetTop - 58,
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

    localStorage.setItem('selected-theme', themes["".concat(localStorage.getItem('selected-theme'))])
    localStorage.setItem('selected-icon', icons["".concat(localStorage.getItem('selected-theme'))])

    let selected_theme = localStorage.getItem('selected-theme')
    let selected_icon = localStorage.getItem('selected-icon')

    themeButton.className = ''
    themeButton.classList.add('change-theme')
    themeButton.classList.add(selected_icon)

    if (selected_theme === 'dark-theme'){
        document.body.className = ''
        document.body.classList.add('dark-theme')
    } else if (selected_theme === 'system-theme'){
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches){
            document.body.className = ''
            document.body.classList.add('dark-theme')
        } else{
            document.body.className = ''
        }
    } else {
        document.body.className = ''
    }
})

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    let selected_theme = localStorage.getItem('selected-theme')

    if (selected_theme === 'system-theme') {
        if ((event.matches ? "dark" : "light") === "light") {
            // Changed to light
            document.body.className = ''
        } else {
            // Changed to dark
            document.body.className = ''
            document.body.classList.add('dark-theme')
        }
    }
});

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
    origin: 'bottom',
    distance: '50px',
    duration: 500,
    // delay: 400,
    // interval: 100,
    // reset: true /* Animations repeat */
})

// sr.reveal(`.home__data, .projects__container, .testimonial__container`, {origin: 'top'})
sr.reveal(`.home__data`, {origin: 'top'})
sr.reveal(`.footer__container`, {origin: 'top', reset: true})
sr.reveal(`.home__info:nth-child(odd) div`, {origin: 'left', reset: true})
sr.reveal(`.home__info:nth-child(even) div`, {origin: 'right', reset: true})
sr.reveal(`.skills__content:nth-child(odd), .contact__content:nth-child(odd)`, {origin: 'left'})
sr.reveal(`.skills__content:nth-child(even), .contact__content:nth-child(even)`, {origin: 'right'})
// sr.reveal(`.qualification__content`, {interval: 50})
sr.reveal(`.services__card`, {interval: 50})

window.onload = function() {
    // Month Day, Year Hour:Minute:Second, id-of-element-container
    countUpFromTime("Sep 1, 2017 12:00:00", 'home__date_counter'); // ****** Change this line!
    document.getElementById('home__info__years_value').textContent = ''.concat('2017-', new Date().getFullYear());
    document.getElementById('footer__copy__years_value').textContent = ''.concat('© Copyright 2017-', new Date().getFullYear(), ', @. All rights reserved');
};

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

$(document).on('click', function (e){
    // Close all popup menus

    $('#nav-menu').removeClass('show-menu')
});

document.addEventListener('dblclick', function(event) {
    event.preventDefault();
}, { passive: false });
