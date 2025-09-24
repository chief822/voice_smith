document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('modal');
    const openBtn = document.getElementById('openModal');
    const closeBtn = document.getElementById('closeModal');

    // Open modal
    document.querySelectorAll("button[data-url]").forEach(button => {
        button.addEventListener('click', () => {
            modal.classList.add('active');
        });
    });

    // Close modal
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    // Close when clicking outside the box
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
});