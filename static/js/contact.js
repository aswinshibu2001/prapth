
document.querySelectorAll('.see_content').forEach(button => {
    button.addEventListener('click', () => {
        var container = button.parentElement;
        var contact_details = container.querySelector('.contact_details');
        
        if (container.style.maxHeight) {
            container.style.maxHeight = null;
            contact_details.classList.remove('active');
        } else {
            container.style.maxHeight = container.scrollHeight + "px";
            contact_details.classList.add('active');
        }
    });
});
