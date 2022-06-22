document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('copyright-date').textContent = new Date().getFullYear();
    
    if (window.location.href.split('/').includes('signup')) {
        const inputs = document.getElementsByTagName('input');
        
        for (const input of inputs) {
            input.classList.add('form-control');
        }
    }
    
    if (window.location.href.split('/').includes('login')) {
        const inputs = document.getElementsByTagName('input');
        
        for (const input of inputs) {
            if (input.type === 'checkbox') {
                input.classList.add('form-check-input');
            } else {
                input.classList.add('form-control');
            }
        }
    }
    
    document.getElementById('btn-company-continue').addEventListener('click', () => {
        window.location.replace('projects');
    })
});