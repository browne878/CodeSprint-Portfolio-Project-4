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

    if (window.location.href.split('/').includes('create-company')) {
        document.getElementById('btn-company-continue').addEventListener('click', () => {
            window.location.replace('projects');
        })
    }

    if (window.location.href.split('/').includes('projects')) {
        const closeButtons = document.getElementsByClassName('toggle-new-project');

        for (const button of closeButtons) {
            button.addEventListener('click', () => {
                $('#new-project').modal('toggle');
            });
        }
    }

    if (window.location.href.split('/').includes('sprints')) {
        const closeButtons = document.getElementsByClassName('toggle-new-sprint');

        for (const button of closeButtons) {
            button.addEventListener('click', () => {
                $('#new-sprint').modal('toggle');
            });
        }
    }
});