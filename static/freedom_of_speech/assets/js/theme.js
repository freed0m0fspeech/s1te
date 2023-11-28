const icons = {'light-theme': 'ri-sun-line', 'system-theme': 'ri-contrast-line', 'dark-theme': 'ri-moon-line'}

let selected_theme = localStorage.getItem('selected-theme')
let selected_icon = icons["".concat(localStorage.getItem('selected-theme'))]

if (!selected_theme || !selected_icon) {
    localStorage.setItem('selected-theme', 'system-theme')
    localStorage.setItem('selected-icon', icons["".concat(localStorage.getItem('selected-theme'))])

    selected_theme = 'system-theme'
    selected_icon = 'ri-contrast-line'
}

if (selected_theme === 'dark-theme')
    document.body.classList.add('dark-theme')
else if (selected_theme === 'system-theme')
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
        document.body.classList.add('dark-theme')
