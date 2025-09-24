from django.shortcuts import render
from .forms import AudioInput
from django.http import FileResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Effects

import os
import tempfile
import subprocess


def index(request):
    effects = Effects.objects.all()
    form = AudioInput(auto_id=True)
    return render(request, 'voice_effects/index.html', {
        "effects": effects,
        "form": form
    })


def audio_effect(request):
    if request.method == "POST":
        audio_form = AudioInput(request.POST, request.FILES)
        if not audio_form.is_valid():
            # Collect all errors into a dict
            errors = {field: error.get_json_data() for field, error in audio_form.errors.items()}
            return JsonResponse(
                {
                    "status": "error",
                    "message": "There was a problem with your upload.",
                    "errors": errors,
                },
                status=400
            )

        audio = audio_form.cleaned_data["audio"]

        # Ensure session exists
        session_key = request.session.session_key

        # Paths
        upload_name = f"tmp/{session_key}_upload"
        upload_path = default_storage.save(upload_name, ContentFile(audio.read()))

        # Convert to normalized wav (overwrite per session)
        normalized_name = f"tmp/{session_key}.wav"
        normalized_path = os.path.join(settings.MEDIA_ROOT, normalized_name)

        # Ensure old normalized file is removed
        if os.path.exists(normalized_path):
            os.remove(normalized_path)

        input_file = os.path.join(settings.MEDIA_ROOT, upload_path)

        # ffprobe command to check for audio streams
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=index",
            "-of", "csv=p=0", input_file
        ]

        try:
            audio_streams = subprocess.check_output(probe_cmd).decode().strip().splitlines()
        except subprocess.CalledProcessError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid media file."
            }, status=400)

        if not audio_streams:
            return JsonResponse({
                "status": "error",
                "message": "File does not contain audio."
            }, status=400)

        # Run ffmpeg for normalizing audio
        command = [
            "ffmpeg", "-y",
            "-i", input_file,
            "-ar", "48000",   # 48kHz sample rate
            "-ac", "1",       # mono
            normalized_path
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            return JsonResponse({
                "status": "error",
                "message": "Failed to process audio file."
            }, status=500)

        # Delete raw uploaded file (only keep normalized one)
        default_storage.delete(upload_path)

        # Save path in session
        request.session['audio_path'] = normalized_name

        return JsonResponse({
            "status": "success",
            "message": "Audio uploaded successfully.",
            "file": normalized_name
        })

    elif request.method == "GET":
        # Ensure session exists
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse(
                {"status": "error", "message": "No active session. Please upload an audio file first."},
                status=400
            )

        filename = f"tmp/{session_key}.wav"
        input_file = os.path.join(settings.MEDIA_ROOT, filename)

        if not os.path.exists(input_file):
            # Fallback: use demo.wav from static
            input_file = os.path.join(
                settings.BASE_DIR,
                "voice_effects/static/voice_effects/audio/demo.wav"
            )

        # Create a temporary output file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_out:
            output_file = tmp_out.name

        effect = request.GET.get("effect_name", "none").strip().lower()
        effects = Effects.objects.filter(name__iexact=effect)
        if not effects.exists():
            return JsonResponse({"status": "error", "message": "Effect not found."}, status=404)
        effect = effects.first()

        command = effect.command(input=input_file, output=output_file)

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            os.remove(output_file)
            return JsonResponse(
                {"status": "error", "message": f"Audio processing failed: {e.stderr or e.stdout}"},
                status=500
            )

        # Return processed file for download
        response = FileResponse(
            open(output_file, "rb"),
            as_attachment=True,
            filename="processed.wav",
            content_type="audio/wav"
        )

        # Ensure cleanup after response is finished
        def cleanup(file_path):
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass

        response.close = lambda *args, **kwargs: cleanup(output_file)
        return response

    else:
        return JsonResponse(
            {"status": "error", "message": "Method not allowed. Use GET to process or POST to upload."},
            status=405
        )
