document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('modal');
    const openBtn = document.getElementById('openModal');
    const closeBtn = document.getElementById('closeModal');

    // Open modal
    document.querySelectorAll("button[data-url]").forEach(button => {
        button.addEventListener('click', () => {
            document.getElementById("demo_audio").pause(); // Pause demo audio if playing
            document.getElementById("modal-title").textContent = "Processing..."
            modal.classList.add('active');
        });
    });

    function closeModal() {
        modal.classList.remove('active');
        const player = document.querySelector("#modal-player");
        player.pause();
    }
    // Close modal
    closeBtn.addEventListener('click', () => {
        closeModal();
    });

    // Close when clicking outside the box
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });
});