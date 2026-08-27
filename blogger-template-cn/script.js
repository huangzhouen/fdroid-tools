// 博客模板 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    const yearSpan = document.getElementById('currentYear');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
    
    window.addEventListener('scroll', function() {
        const header = document.querySelector('.site-header');
        if (window.scrollY > 10) {
            header.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        } else {
            header.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
        }
    });
});
