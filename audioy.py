import atexit
import ssl
from os import path
from time import time, sleep

import assemblyai as aai
import pandas
import speech_recognition as sr
import vosk
from openai import OpenAI, RateLimitError

atexit.register(breakpoint)
aai.settings.api_key = "Assembly AI API KEY HERE"
client = OpenAI()
transcriber = aai.Transcriber()
# noinspection PyProtectedMember
orig_secure_ssl_context = ssl._create_default_https_context
continue_searching = True
english_accuracy = pandas.read_csv("english_accuracy.csv")
french_accuracy = pandas.read_csv("french_accuracy.csv")
english_time = pandas.read_csv("english_time.csv")
french_time = pandas.read_csv("french_time.csv")
e = None
engines = ['Google', 'Google Cloud', 'Vosk (Small)', 'Vosk', 'Sphinx', 'Whisper', 'Wit', 'Azure', 'Whisper API', "Assembly"]


actual_transcriptions = {
    True: {
        "1.wav": "The playful kitten chased the fluffy ball.",
        "2.wav": "A diligent student always completes assignments on time.",
        "3.wav": "The bright rainbow appeared after the rain shower.",
        "4.wav": "Oliver was excited to explore the mysterious forest.",
        "5.wav": "The bubbly soda fizzed in the glass.",
        "6.wav": "Graceful dolphins leaped through the sparkling waves.",
        "7.wav": "The curious scientist studied the intricate pattern.",
        "8.wav": "Bobby's bicycle has a squeaky wheel.",
        "9.wav": "The friendly librarian recommended a fascinating book.",
        "10.wav": "The adventurous explorer discovered a hidden treasure."
    },
    False: {
        "1.wav": "Le chien joyeux court après le ballon coloré.",
        "2.wav": "Une élève sérieuse finit toujours ses devoirs à temps.",
        "3.wav": "Le jardinier plante de belles fleurs dans le jardin.",
        "4.wav": "La pluie fine crée des flaques sur le trottoir.",
        "5.wav": "Le singe malicieux grimpe rapidement dans l'arbre.",
        "6.wav": "La pizza délicieuse cuit dans le four chaud.",
        "7.wav": "La danseuse gracieuse tourne sur la scène éclairée.",
        "8.wav": "Le chocolat fondant est une délicieuse friandise.",
        "9.wav": "L'oiseau chante une mélodie douce au lever du soleil.",
        "10.wav": "Le professeur explique le problème mathématique clairement."
    }
}

vosk.SetLogLevel(-1)

recognizer = sr.Recognizer()
print("Loading Vosk models. This might take a minute or two. Please wait...")
vosk_small_english = vosk.Model("SmallEnglish")
print("Loaded Small English")
vosk_small_french = vosk.Model("SmallFrench")
print("Loaded Small French")
vosk_english = vosk.Model("English")
print("Loaded English")
vosk_french = vosk.Model("French")
print("Loaded French")
print("Vosk models loaded!")


def record_audio():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    with open("testy.wav", "wb") as f:
        f.write(audio.get_wav_data())
    print("audio captured")
    return audio


def recog_google(audio, english):
    if english:
        start = time()
        text_google = recognizer.recognize_google(audio)
        end = time()
    else:
        start = time()
        text_google = recognizer.recognize_google(audio, language="fr-CA")
        end = time()
    return text_google, end - start


def recog_google_cloud(audio, english):
    if english:
        start = time()
        text_google_cloud = recognizer.recognize_google_cloud(audio,
                                                              credentials_json="JSON Credentials file path HERE")
        end = time()
    else:
        start = time()
        text_google_cloud = recognizer.recognize_google_cloud(audio,
                                                              credentials_json="JSON Credentials file path HERE",
                                                              language="fr-CA")
        end = time()
    return text_google_cloud, end - start


def recog_vosk_small(audio, english):
    if english:
        recognizer.vosk_model = vosk_small_english
        start = time()
        text_vosk = recognizer.recognize_vosk(audio)
        text_vosk = eval(text_vosk)["text"]
        end = time()
    else:
        recognizer.vosk_model = vosk_small_french
        start = time()
        text_vosk = recognizer.recognize_vosk(audio)
        text_vosk = eval(text_vosk)["text"]
        end = time()
    return text_vosk, end - start


def recog_vosk(audio, english):
    if english:
        recognizer.vosk_model = vosk_english
        start = time()
        text_vosk = recognizer.recognize_vosk(audio)
        text_vosk = eval(text_vosk)["text"]
        end = time()
    else:
        recognizer.vosk_model = vosk_french
        start = time()
        text_vosk = recognizer.recognize_vosk(audio)
        text_vosk = eval(text_vosk)["text"]
        end = time()
    return text_vosk, end - start


def recog_sphinx(audio, english):
    if english:
        start = time()
        text_sphinx = recognizer.recognize_sphinx(audio)
        end = time()
    else:
        start = time()
        text_sphinx = recognizer.recognize_sphinx(audio, language="fr-FR")
        end = time()
    return text_sphinx, end - start


def recog_whisper(audio, english):
    if english:
        start = time()
        text_whisper = recognizer.recognize_whisper(audio, language="english")
        end = time()
    else:
        start = time()
        text_whisper = recognizer.recognize_whisper(audio, language="french")
        end = time()
    return text_whisper, end - start


def recog_wit(audio, english):
    if english:
        start = time()
        text_wit = recognizer.recognize_wit(audio, key="WIT.AI API KEY HERE")
        end = time()
    else:
        start = time()
        text_wit = recognizer.recognize_wit(audio, key="WIT.AI API KEY HERE")
        end = time()
    return text_wit, end - start


def recog_whisper_api(audio_path, english):
    global e
    if english:
        audio_file = open(audio_path, "rb")
        try:
            start = time()
            text_whisper_api = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                language="en"
            )
            end = time()
        except RateLimitError as e:
            while True:
                try:
                    start = time()
                    text_whisper_api = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text",
                        language="en"
                    )
                    end = time()
                    break
                except RateLimitError as e:
                    e = str(e)
                    if e[e.index("Please try again in ") + 20:][:3] == "20s":
                        print("Waiting 21s")
                        sleep(21)
                    else:
                        print("Waiting 7m13s")
                        sleep(433)
    else:
        audio_file = open(audio_path, "rb")
        try:
            start = time()
            text_whisper_api = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                language="fr"
            )
            end = time()
        except RateLimitError:
            while True:
                try:
                    start = time()
                    text_whisper_api = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text",
                        language="fr"
                    )
                    end = time()
                    break
                except RateLimitError as e:
                    e = str(e)
                    if e[e.index("Please try again in ") + 20:][:3] == "20s":
                        print("Waiting 21s")
                        sleep(21)
                    else:
                        print("Waiting 7m13s")
                        sleep(433)
    return text_whisper_api.strip(), end - start


def recog_assembly(path, english):
    if english:
        start = time()
        config = aai.TranscriptionConfig(language_code="en")
        text_assembly = transcriber.transcribe(path, config).text
        end = time()
    else:
        start = time()
        config = aai.TranscriptionConfig(language_code="fr")
        text_assembly = transcriber.transcribe(path, config).text
        end = time()
    return text_assembly, end - start


# noinspection PyProtectedMember
def recog_azure(audio, english):
    if english:
        ssl._create_default_https_context = ssl._create_unverified_context
        start = time()
        # noinspection PyArgumentEqualDefault
        text_micro = recognizer.recognize_azure(audio, key="AZURE API KEY HERE", location="YOUR REGION", language="en-US", profanity="raw")
        end = time()
        ssl._create_default_https_context = orig_secure_ssl_context
    else:
        ssl._create_default_https_context = ssl._create_unverified_context
        start = time()
        text_micro = recognizer.recognize_azure(audio, key="AZURE API KEY HERE", location="YOUR REGION", language="fr-FR", profanity="raw")
        end = time()
        ssl._create_default_https_context = orig_secure_ssl_context
    return text_micro[0], end - start


def recognize_speech(audio, audio_path, english=True):
    global engines
    global e
    if "Azure" in engines:
        try:
            print(f"Azure: {recog_azure(audio, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
    if "Assembly" in engines:
        try:
            print(f"Assembly: {recog_assembly(audio_path, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
    if "Whisper" in engines:
        try:
            print(f"Whisper: {recog_whisper(audio, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
    if "Wit" in engines:
        try:
            print(f"Wit.ai: {recog_wit(audio, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
    if "Google" in engines:
        try:
            print(f"Google: {recog_google(audio, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
    if "Vosk" in engines:
        try:
            print(f"Vosk: {recog_vosk(audio, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
    if "Google Cloud" in engines:
        try:
            print(f"Google Cloud: {recog_google_cloud(audio, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
    if "Vosk (Small)" in engines:
        try:
            print(f"Vosk (Small): {recog_vosk_small(audio, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
    if "Sphinx" in engines:
        try:
            print(f"Sphinx: {recog_sphinx(audio, english)[0]}")
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))


if __name__ == "__main__":
    while True:
        if input("Press enter to continue or type anything else to exit: ") != "":
            if input("Are you sure (y/n)? ").lower() == "y":
                quit()
        audio = record_audio()
        print("\n\n\n\n\n\n\n\n\n\n\n\n")
        recognize_speech(audio, path.join(path.dirname(path.realpath(__file__)), "testy.wav"))
