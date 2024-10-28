import pyaudio
import wave

# Function to list available audio devices
def list_audio_devices(audio):
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    print("Available audio devices:")
    for i in range(0, numdevices):
        if audio.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels') > 0:
            print(f"Output Device id {i} - {audio.get_device_info_by_host_api_device_index(0, i).get('name')}")

# Parameters
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1              # Mono
RATE = 44100              # 44.1kHz sampling rate
CHUNK = 1024              # 2^10 samples for buffer
RECORD_SECONDS = 5        # Record duration
WAVE_OUTPUT_FILENAME = "test.wav"

# Create an interface to PortAudio
audio = pyaudio.PyAudio()

# List available audio devices
list_audio_devices(audio)

# Setup the microphone stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Record the audio data
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording complete")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded data to a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Reinitialize PyAudio for playback
audio = pyaudio.PyAudio()

# List available output devices again (optional)
list_audio_devices(audio)

# Open the audio stream for playback
try:
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=0)  # Adjust the device index as needed

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Playback complete")
except Exception as e:
    print(f"An error occurred: {e}")
