"""
Recognizer:
    Creates a new Recognizer instance, which represents a collection of speech recognition functionality.

AudioFile:
    Creates a new AudioFile instance given a WAV/AIFF/FLAC audio file filename_or_fileobject. Subclass of AudioSource.
    If filename_or_fileobject is a string, then it is interpreted as a path to an audio file on the filesystem. Otherwise, filename_or_fileobject should be a file-like object such as io.BytesIO or similar.
    Note that functions that read from the audio (such as recognizer_instance.record or recognizer_instance.listen) will move ahead in the stream. For example, if you execute recognizer_instance.record(audiofile_instance, duration=10) twice, the first time it will return the first 10 seconds of audio, and the second time it will return the 10 seconds of audio right after that. This is always reset to the beginning when entering an AudioFile context.
    WAV files must be in PCM/LPCM format; WAVE_FORMAT_EXTENSIBLE and compressed WAV are not supported and may result in undefined behaviour.
    Both AIFF and AIFF-C (compressed AIFF) formats are supported.
    FLAC files must be in native FLAC format; OGG-FLAC is not supported and may result in undefined behaviour.

adjust_for_ambient_noise:
    Adjusts the energy threshold dynamically using audio from source (an AudioSource instance) to account for ambient noise.
    Intended to calibrate the energy threshold with the ambient energy level. Should be used on periods of audio without speech - will stop early if any speech is detected.
    The duration parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning. This value should be at least 0.5 in order to get a representative sample of the ambient noise.

record:
    Records up to duration seconds of audio from source (an AudioSource instance) starting at offset (or at the beginning if not specified) into an AudioData instance, which it returns.
    If duration is not specified, then it will record until there is no more audio input.      

recognize_google:
    Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition API.
    The Google Speech Recognition API key is specified by key. If not specified, it uses a generic key that works out of the box. This should generally be used for personal or testing purposes only, as it **may be revoked by Google at any time**.
    The recognition language is determined by language, an RFC5646 language tag like "en-US" (US English) or "fr-FR" (International French), defaulting to US English. A list of supported language tags can be found in this `StackOverflow answer <http://stackoverflow.com/a/14302134>`__.
    The profanity filter level can be adjusted with pfilter: 0 - No filter, 1 - Only shows the first character and replaces the rest with asterisks. The default is level 0.
    Returns the most likely transcription if show_all is false (the default). Otherwise, returns the raw API response as a JSON dictionary.
    Raises a speech_recognition.UnknownValueError exception if the speech is unintelligible. Raises a speech_recognition.RequestError exception if the speech recognition operation failed, if the key isn't valid, or if there is no internet connection.
"""
from speech_recognition import AudioFile, Recognizer, RequestError, UnknownValueError


def speech_to_text(filename: str, language: str) -> str:
    """
    fuction to convert Audio file into text
    args : 
        ``filename`` : path and name of the audio file in (WAV/AIFF/FLAC) format
        ``language`` : language of the audio file
    return:
        ``text`` : output text

    """
    r = Recognizer()
    with AudioFile(filename) as source:
        r.adjust_for_ambient_noise(source)
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language=language)
        except UnknownValueError:
            print("could not understand audio")
        except RequestError:
            print('Request Failed')

    return text


if __name__ == "__main__":

    filename = r"C:\Users\m.aghili\Desktop\uni_project\speech_to_text\a.wav"
    language = "en-US"
    text = speech_to_text(filename, language)
    print(text)
