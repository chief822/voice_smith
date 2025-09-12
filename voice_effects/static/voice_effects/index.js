let iframe;

document.addEventListener("DOMContentLoaded", function() {
    iframe = document.getElementById("hidden_iframe");
    document.querySelector("#audio").addEventListener('change', upload_audio);
    iframe.onload = handle_audio;
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
    console.log("Raw response:", text);

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
    gh
}
