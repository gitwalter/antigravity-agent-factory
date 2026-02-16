---
description: Speech-to-text (Whisper, cloud APIs), text-to-speech synthesis, real-time
  transcription, and audio analysis
name: processing-speech
type: skill
---
# Speech Processing

Speech-to-text (Whisper, cloud APIs), text-to-speech synthesis, real-time transcription, and audio analysis

Convert speech to text, synthesize text to speech, perform real-time transcription, and analyze audio content.

## Process

1. Review the task requirements.
2. Apply the skill's methodology.
3. Validate the output against the defined criteria.
### Step 1: Speech-to-Text with Whisper

```python
import whisper
import torch

def transcribe_whisper(audio_path: str, model_size: str = "base", language: str = None) -> dict:
    """Transcribe audio using OpenAI Whisper.

    Args:
        audio_path: Path to audio file
        model_size: tiny, base, small, medium, large
        language: Language code (e.g., 'en', 'es') or None for auto-detect
    """
    # Load model
    model = whisper.load_model(model_size)

    # Transcribe
    result = model.transcribe(
        audio_path,
        language=language,
        task="transcribe",  # or "translate" for translation
        verbose=False
    )

    return {
        "text": result["text"],
        "segments": result["segments"],
        "language": result["language"]
    }

# With word-level timestamps
def transcribe_with_timestamps(audio_path: str) -> list:
    """Get transcription with word-level timestamps."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)

    words = []
    for segment in result["segments"]:
        for word_info in segment.get("words", []):
            words.append({
                "word": word_info["word"],
                "start": word_info["start"],
                "end": word_info["end"],
                "confidence": word_info.get("probability", 0)
            })

    return words

# Batch processing
def transcribe_batch(audio_paths: list[str], model_size: str = "base") -> list:
    """Transcribe multiple audio files."""
    model = whisper.load_model(model_size)
    results = []

    for audio_path in audio_paths:
        result = model.transcribe(audio_path)
        results.append({
            "file": audio_path,
            "text": result["text"],
            "language": result["language"]
        })

    return results
```

### Step 2: Real-Time Transcription

```python
import pyaudio
import wave
import numpy as np
from collections import deque
import threading

class RealTimeTranscriber:
    """Real-time audio transcription using Whisper."""

    def __init__(self, model_size: str = "base", chunk_duration: float = 5.0):
        self.model = whisper.load_model(model_size)
        self.chunk_duration = chunk_duration
        self.audio_queue = deque()
        self.is_recording = False

    def start_recording(self, sample_rate: int = 16000, channels: int = 1):
        """Start recording audio."""
        self.is_recording = True
        self.sample_rate = sample_rate

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=1024
        )

        # Start transcription thread
        transcription_thread = threading.Thread(target=self._transcribe_loop)
        transcription_thread.start()

        # Record audio
        while self.is_recording:
            data = stream.read(1024)
            self.audio_queue.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def _transcribe_loop(self):
        """Continuously transcribe audio chunks."""
        chunk_samples = int(self.sample_rate * self.chunk_duration)
        audio_buffer = []

        while self.is_recording:
            if len(self.audio_queue) > 0:
                audio_buffer.extend(self.audio_queue.popleft())

                if len(audio_buffer) >= chunk_samples:
                    # Convert to numpy array
                    audio_np = np.frombuffer(
                        b''.join(audio_buffer[:chunk_samples]),
                        dtype=np.int16
                    ).astype(np.float32) / 32768.0

                    # Transcribe
                    result = self.model.transcribe(audio_np, language="en")
                    print(f"Transcription: {result['text']}")

                    # Clear buffer
                    audio_buffer = audio_buffer[chunk_samples:]

    def stop_recording(self):
        """Stop recording."""
        self.is_recording = False
```

### Step 3: Voice Activity Detection

```python
import webrtcvad
import numpy as np

class VoiceActivityDetector:
    """Detect speech segments in audio."""

    def __init__(self, aggressiveness: int = 2):
        """
        Args:
            aggressiveness: 0-3, higher = more aggressive filtering
        """
        self.vad = webrtcvad.Vad(aggressiveness)
        self.sample_rate = 16000  # VAD requires 8k, 16k, 32k, or 48k
        self.frame_duration_ms = 30
        self.frame_size = int(self.sample_rate * self.frame_duration_ms / 1000)

    def detect_speech_segments(self, audio_path: str) -> list:
        """Detect segments containing speech."""
        import wave

        with wave.open(audio_path, 'rb') as wf:
            sample_rate = wf.getframerate()
            if sample_rate != self.sample_rate:
                raise ValueError(f"Sample rate must be {self.sample_rate}")

            audio_data = wf.readframes(wf.getnframes())

        # Process in frames
        speech_segments = []
        current_segment_start = None

        for i in range(0, len(audio_data), self.frame_size * 2):  # *2 for 16-bit
            frame = audio_data[i:i + self.frame_size * 2]

            if len(frame) < self.frame_size * 2:
                break

            is_speech = self.vad.is_speech(frame, self.sample_rate)
            timestamp = i / (self.sample_rate * 2)

            if is_speech:
                if current_segment_start is None:
                    current_segment_start = timestamp
            else:
                if current_segment_start is not None:
                    speech_segments.append({
                        "start": current_segment_start,
                        "end": timestamp
                    })
                    current_segment_start = None

        # Close final segment
        if current_segment_start is not None:
            speech_segments.append({
                "start": current_segment_start,
                "end": len(audio_data) / (self.sample_rate * 2)
            })

        return speech_segments
```

### Step 4: Text-to-Speech Synthesis

```python
from gtts import gTTS
import pyttsx3
import io

def synthesize_gtts(text: str, lang: str = "en", slow: bool = False) -> bytes:
    """Synthesize speech using Google Text-to-Speech (free, requires internet)."""
    tts = gTTS(text=text, lang=lang, slow=slow)

    # Save to bytes buffer
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    return mp3_fp.read()

def synthesize_pyttsx3(text: str, voice_id: int = None, rate: int = 150) -> None:
    """Synthesize speech using pyttsx3 (offline, system voices)."""
    engine = pyttsx3.init()

    # Set properties
    engine.setProperty("rate", rate)

    # Set voice
    voices = engine.getProperty("voices")
    if voice_id is not None and voice_id < len(voices):
        engine.setProperty("voice", voices[voice_id].id)

    # Speak
    engine.say(text)
    engine.runAndWait()

# Save to file
def synthesize_to_file(text: str, output_path: str, lang: str = "en"):
    """Synthesize speech and save to file."""
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)

# Using cloud APIs
def synthesize_azure_speech(text: str, output_path: str, subscription_key: str, region: str):
    """Synthesize using Azure Cognitive Services Speech."""
    import azure.cognitiveservices.speech as speechsdk

    speech_config = speechsdk.SpeechConfig(
        subscription=subscription_key,
        region=region
    )

    # Set voice
    speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=speechsdk.audio.AudioOutputConfig(filename=output_path)
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return True
    return False
```

### Step 5: Audio Analysis and Segmentation

```python
from pydub import AudioSegment
import numpy as np

def analyze_audio(audio_path: str) -> dict:
    """Analyze audio file properties."""
    audio = AudioSegment.from_file(audio_path)

    return {
        "duration_seconds": len(audio) / 1000.0,
        "sample_rate": audio.frame_rate,
        "channels": audio.channels,
        "frame_width": audio.frame_width,
        "max_possible_amplitude": audio.max_possible_amplitude,
        "rms": audio.rms,  # Root mean square (loudness)
        "dBFS": audio.dBFS  # Decibels relative to full scale
    }

def detect_silence_segments(audio_path: str, silence_thresh: int = -50, min_silence_len: int = 1000) -> list:
    """Detect silent segments in audio."""
    audio = AudioSegment.from_file(audio_path)

    # Split on silence
    chunks = pydub.silence.split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=True
    )

    # Calculate timestamps
    segments = []
    current_time = 0

    for chunk in chunks:
        duration = len(chunk) / 1000.0
        segments.append({
            "start": current_time,
            "end": current_time + duration,
            "is_silence": chunk.rms < abs(silence_thresh)
        })
        current_time += duration

    return segments

def segment_by_duration(audio_path: str, segment_duration_seconds: float) -> list:
    """Split audio into fixed-duration segments."""
    audio = AudioSegment.from_file(audio_path)
    segment_duration_ms = segment_duration_seconds * 1000

    segments = []
    for i in range(0, len(audio), segment_duration_ms):
        segment = audio[i:i + segment_duration_ms]
        segments.append({
            "start": i / 1000.0,
            "end": (i + len(segment)) / 1000.0,
            "audio": segment
        })

    return segments

def normalize_audio(audio_path: str, output_path: str, target_dBFS: float = -20.0):
    """Normalize audio to target loudness."""
    audio = AudioSegment.from_file(audio_path)

    # Calculate change needed
    change_in_dBFS = target_dBFS - audio.dBFS

    # Apply normalization
    normalized = audio.apply_gain(change_in_dBFS)

    # Export
    normalized.export(output_path, format="wav")
```

### Step 6: Cloud Speech APIs

```python
from google.cloud import speech_v1
import io

def transcribe_google_cloud(audio_path: str, credentials_path: str, language_code: str = "en-US") -> dict:
    """Transcribe using Google Cloud Speech-to-Text."""
    client = speech_v1.SpeechClient.from_service_account_file(credentials_path)

    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech_v1.RecognitionAudio(content=content)
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)

    results = []
    for result in response.results:
        alternative = result.alternatives[0]
        results.append({
            "text": alternative.transcript,
            "confidence": alternative.confidence,
            "words": [
                {
                    "word": word.word,
                    "start_time": word.start_time.total_seconds(),
                    "end_time": word.end_time.total_seconds()
                }
                for word in alternative.words
            ]
        })

    return {"results": results}

def transcribe_azure_speech(audio_path: str, subscription_key: str, region: str, language: str = "en-US") -> str:
    """Transcribe using Azure Speech Services."""
    import azure.cognitiveservices.speech as speechsdk

    speech_config = speechsdk.SpeechConfig(
        subscription=subscription_key,
        region=region
    )
    speech_config.speech_recognition_language = language

    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return f"No speech could be recognized: {result.no_match_details}"
    elif result.reason == speechsdk.ResultReason.Canceled:
        return f"Speech Recognition canceled: {result.cancellation_details.reason}"

    return ""
```

## Speech Processing Tools Comparison

| Tool | Type | Accuracy | Languages | Cost | Offline |
|------|------|----------|-----------|------|---------|
| Whisper | STT | Very High | 99+ | Free | Yes |
| Google Cloud Speech | STT | Very High | 50+ | Paid | No |
| Azure Speech | STT/TTS | Very High | 50+ | Paid | No |
| gTTS | TTS | High | 100+ | Free | No |
| pyttsx3 | TTS | Medium | System | Free | Yes |

## Best Practices

- Use Whisper for offline, high-accuracy transcription
- Preprocess audio (normalize, remove noise) before transcription
- Use voice activity detection to skip silent segments
- Choose appropriate model size based on accuracy vs. speed needs
- Cache transcriptions for repeated audio files
- Use word-level timestamps for precise alignment
- Normalize audio levels before processing
- Handle multiple speakers with speaker diarization when needed

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No audio preprocessing | Normalize, denoise before transcription |
| Wrong sample rate | Convert to model's required rate (16kHz for Whisper) |
| Processing entire file | Use VAD to segment speech regions |
| Ignoring confidence scores | Filter low-confidence transcriptions |
| No language specification | Detect or specify language for better accuracy |
| Large model for simple tasks | Use smaller models (base/tiny) when speed matters |
| No error handling | Handle API failures and audio format errors |

## Related

- Skill: `vision-agents`
- Skill: `rag-patterns`
- Skill: `ocr-processing`

## When to Use
This skill should be used when strict adherence to the defined process is required.

## Prerequisites
- Basic understanding of the agent factory context.
- Access to the necessary tools and resources.
