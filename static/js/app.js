/**
 * Global App JS
 * Handles navigation highlighting and theme toggling.
 */

document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initNavigation();
});

/**
 * Initialize and manage dark/light themes
 */
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;

    const currentTheme = localStorage.getItem('theme') || 'dark';
    
    // Set initial theme
    if (currentTheme === 'light') {
        document.body.classList.remove('theme-dark');
        document.body.classList.add('theme-light');
        themeToggle.checked = true;
    } else {
        document.body.classList.remove('theme-light');
        document.body.classList.add('theme-dark');
        themeToggle.checked = false;
    }

    // Listen for toggle changes
    themeToggle.addEventListener('change', function() {
        if (themeToggle.checked) {
            document.body.classList.remove('theme-dark');
            document.body.classList.add('theme-light');
            localStorage.setItem('theme', 'light');
        } else {
            document.body.classList.remove('theme-light');
            document.body.classList.add('theme-dark');
            localStorage.setItem('theme', 'dark');
        }
        
        // Notify any components that theme changed (e.g., charts need re-rendering)
        window.dispatchEvent(new Event('themeChanged'));
    });
}

/**
 * Highlight active page in sidebar
 */
function initNavigation() {
    const navLinks = document.getElementById('navLinks');
    if (!navLinks) return;

    const path = window.location.pathname;
    const links = navLinks.getElementsByTagName('a');

    for (let link of links) {
        const navType = link.getAttribute('data-nav');
        if (path.includes(navType)) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    }
}
