let iframe;

document.addEventListener("DOMContentLoaded", function() {
    iframe = document.getElementById("hidden_iframe");
    document.querySelector("#audio").addEventListener('change', upload_audio);
    iframe.onload = handle_audio;

    document.querySelectorAll("button[data-url]").forEach(button => {
        button.addEventListener("click", function() {
            const effect = this.getAttribute("data-url");
            apply_effect(effect);
        });
    });
});

function upload_audio(event) {
    const files = event.target.files; // FileList object

    if (files.length > 0) {
        document.querySelector("#form").submit();
    }
}

function handle_audio() {
    const doc = iframe.contentDocument || iframe.contentWindow.document;
    const text = doc.body.innerText.trim();

    if (!text) {
        // Empty response (likely initial load)
        return;
    }
    try {
        let data = JSON.parse(text);
        document.getElementById("message").textContent = `${data["status"]}, ${data["message"]} You can choose another file`;
    } catch (e) {
        console.error("Could not parse JSON:", e);
    }
}

function apply_effect(effect) {
    fetch(effect)
        .then(response => response.json())
        .then(data => {
            if (data.status === "error") {
                document.getElementById("message").textContent = `Error: ${data.message}`;
                return;
            }
        })
        .catch(error => {
            console.error("Error applying effect:", error);
        });
}
