"""
STT + Wake Word detection.
Wake words: configurables en .env (default: "hola mark", "mark tres", "mark 3")
STT: faster-whisper (local, sin internet necesario)
Fallback: SpeechRecognition con Google si faster-whisper no está disponible
"""
import asyncio
import queue
import threading
import tempfile
import os
import numpy as np
import sounddevice as sd
import soundfile as sf
from config.settings import settings
from core import events

_transcriber = None
_listening = False
_callback = None


def _get_transcriber():
    global _transcriber
    if _transcriber is None:
        try:
            from faster_whisper import WhisperModel
            _transcriber = WhisperModel(settings.WHISPER_MODEL, device="cpu", compute_type="int8")
            print(f"[Voice] faster-whisper cargado: {settings.WHISPER_MODEL}")
        except Exception as e:
            print(f"[Voice] faster-whisper no disponible ({e}). Usando SpeechRecognition.")
            _transcriber = "sr_fallback"
    return _transcriber


def _transcribe_audio(audio_data: np.ndarray, sample_rate: int = 16000) -> str:
    model = _get_transcriber()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
    sf.write(tmp_path, audio_data, sample_rate)

    try:
        if model == "sr_fallback":
            return _transcribe_sr(tmp_path)

        segments, _ = model.transcribe(tmp_path, language="es", beam_size=3)
        text = " ".join(seg.text for seg in segments).strip()
        return text
    finally:
        os.unlink(tmp_path)


def _transcribe_sr(wav_path: str) -> str:
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="es-PA")
    except Exception:
        return ""


def _contains_wake_word(text: str) -> bool:
    lowered = text.lower()
    return any(w in lowered for w in settings.WAKE_WORDS)


def _remove_wake_word(text: str) -> str:
    lowered = text.lower()
    for w in settings.WAKE_WORDS:
        lowered = lowered.replace(w, "").strip()
    return lowered.strip(" ,.")


class VoiceListener:
    def __init__(self, on_command):
        self.on_command = on_command
        self.running = False
        self.sample_rate = 16000
        self.chunk_duration = 0.5
        self.silence_threshold = 0.01
        self.max_record_seconds = 15
        self.silence_after_speech = 1.5

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()
        print(f"[Voice] Escuchando wake words: {settings.WAKE_WORDS}")

    def stop(self):
        self.running = False

    def _listen_loop(self):
        chunk_samples = int(self.sample_rate * self.chunk_duration)

        while self.running:
            try:
                audio_buffer = []
                recording = False
                silence_chunks = 0
                max_chunks = int(self.max_record_seconds / self.chunk_duration)

                with sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype="float32",
                    blocksize=chunk_samples,
                ) as stream:
                    for _ in range(max_chunks * 2):
                        if not self.running:
                            break

                        chunk, _ = stream.read(chunk_samples)
                        chunk = chunk.flatten()
                        rms = float(np.sqrt(np.mean(chunk**2)))

                        if not recording:
                            audio_buffer.append(chunk)
                            if len(audio_buffer) > 10:
                                audio_buffer.pop(0)

                            if rms > self.silence_threshold:
                                recording = True
                                silence_chunks = 0
                        else:
                            audio_buffer.append(chunk)
                            if rms < self.silence_threshold:
                                silence_chunks += 1
                                if silence_chunks >= int(self.silence_after_speech / self.chunk_duration):
                                    break
                            else:
                                silence_chunks = 0

                if len(audio_buffer) < 3:
                    continue

                audio = np.concatenate(audio_buffer)
                text = _transcribe_audio(audio, self.sample_rate)

                if not text:
                    continue

                if _contains_wake_word(text):
                    command = _remove_wake_word(text)
                    asyncio.run(events.publish("state_change", {"state": "listening"}))
                    print(f"[Voice] Wake word detectada → '{command}'")
                    if command:
                        asyncio.run(self.on_command(command))
                    else:
                        asyncio.run(events.publish("state_change", {"state": "idle"}))

            except Exception as e:
                print(f"[Voice] Error: {e}")
                import time
                time.sleep(1)
