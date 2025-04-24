/**
 * Mood Diary - Main JavaScript
 * Contains common functionality for the application
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Fade out alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentLocation.includes(linkPath) && linkPath !== '/') {
            link.classList.add('active');
        } else if (linkPath === '/' && currentLocation === '/') {
            link.classList.add('active');
        }
    });
    
    // Add animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        // Add slight delay to each card for cascade effect
        card.style.animationDelay = `${index * 0.05}s`;
        card.classList.add('fade-in');
    });
    
    // Responsive calendar adjustments
    function adjustCalendar() {
        if (window.innerWidth < 768) {
            // On small screens, shorten day names
            const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            const headings = document.querySelectorAll('.table-light th');
            headings.forEach((heading, index) => {
                if (index < dayNames.length) {
                    heading.textContent = dayNames[index];
                }
            });
        }
    }
    
    // Run on load
    adjustCalendar();
    
    // Run on resize
    window.addEventListener('resize', adjustCalendar);
}); 