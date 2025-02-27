const icons = {
  'light-theme': 'ri-sun-line',
  'system-theme': 'ri-contrast-line',
  'dark-theme': 'ri-moon-line'
};

let selected_theme = localStorage.getItem('selected-theme') || 'system-theme';
let selected_icon = icons[selected_theme] || icons['system-theme'];

if (!localStorage.getItem('selected-theme')) {
  localStorage.setItem('selected-theme', selected_theme);
  localStorage.setItem('selected-icon', selected_icon);
}

if (selected_theme === 'dark-theme' || (selected_theme === 'system-theme' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  document.body.classList.add('dark-theme');
}