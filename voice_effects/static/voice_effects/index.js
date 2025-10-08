let iframe;
let currentObjectUrl = null; // keep track of the last blob URL

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
        document.getElementById("message").textContent = `Uploading. Please wait`;
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
        document.getElementById("message").textContent = `${data["status"].charAt(0).toUpperCase()+data["status"].slice(1)}. ${data["message"]} You can choose another file`;
    } catch (e) {
        console.error("Could not parse JSON:", e);
    }
}

function apply_effect(effectUrl) {
    fetch(effectUrl)
        .then(async (response) => {
            const contentType = response.headers.get("Content-Type");

            if (contentType && contentType.includes("application/json")) {
                // Error response
                const data = await response.json();
                document.getElementById("modal-description").textContent =
                    `Error: ${data.error || data.message}`.substring(0, 200) + "..."; // truncate if too long
                return;
            }

            if (contentType && contentType.includes("audio/")) {
                // Audio response
                const blob = await response.blob();

                // Clean up old object URL if one exists
                if (currentObjectUrl) {
                    URL.revokeObjectURL(currentObjectUrl);
                }

                const url = URL.createObjectURL(blob);
                currentObjectUrl = url; // save reference for next time

                const player = document.querySelector("#modal-player");
                player.src = url;
                player.play()
                document.getElementById("modal-title").textContent = new URL(effectUrl, window.location.origin).searchParams.get("effect_name");
                return;
            }

            console.error("Unexpected response type:", contentType);
        })
        .catch((error) => {
            console.error("Error applying effect:", error);
        });
}
