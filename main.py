import atexit
import ssl
from os import path, listdir
from time import time

import assemblyai as aai
import openai
import pandas
import speech_recognition as sr
import vosk
from openai import OpenAI

from MarkTranscription import mark

atexit.register(breakpoint)
aai.settings.api_key = "Assembly AI API KEY HERE"
openai.api_key = "OpenAI API KEY HERE"
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

all_engines = ['Google', 'Google Cloud', 'Vosk (Small)', 'Vosk', 'Sphinx', 'Whisper', 'Wit', 'Azure', 'Whisper API', "Assembly"]
engines = []
inputted_start = input("Where would you like to start? Enter the name of the student folder: ")
inputted_engines = input("Which engines would you like to test or not test? Provide a list separated by commas with no spaces between items: ")
include_or_exclude = input('Type "+" if you would like to test these or "-" if you would like to test all but these: ')
if include_or_exclude == "+":
    for engine in inputted_engines.split(","):
        if engine in all_engines:
            engines.append(engine)
elif include_or_exclude == "-":
    engines = all_engines.copy()
    for engine in inputted_engines.split(","):
        engines.remove(engine)

print(f"List of engines received: {engines}")


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
if "Vosk (Small)" in engines:
    vosk_small_english = vosk.Model("SmallEnglish")
    print("Loaded Small English")
    vosk_small_french = vosk.Model("SmallFrench")
    print("Loaded Small French")
if "Vosk" in engines:
    vosk_english = vosk.Model("English")
    print("Loaded English")
    vosk_french = vosk.Model("French")
    print("Loaded French")
print("Vosk models loaded!")


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
    results = {}
    times = {}
    if "Google" in engines:
        try:
            results["Google"], times["Google"] = recog_google(audio, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Google"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Google"] = ""
    if "Google Cloud" in engines:
        try:
            results["Google Cloud"], times["Google Cloud"] = recog_google_cloud(audio, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Google Cloud"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Google Cloud"] = ""
    if "Vosk (Small)" in engines:
        try:
            results["Vosk (Small)"], times["Vosk (Small)"] = recog_vosk_small(audio, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Vosk (Small)"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Vosk (Small)"] = ""
    if "Vosk" in engines:
        try:
            results["Vosk"], times["Vosk"] = recog_vosk(audio, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Vosk"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Vosk"] = ""
    if "Sphinx" in engines:
        try:
            results["Sphinx"], times["Sphinx"] = recog_sphinx(audio, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Sphinx"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Sphinx"] = ""
    if "Whisper" in engines:
        try:
            results["Whisper"], times["Whisper"] = recog_whisper(audio, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Whisper"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Whisper"] = ""
    if "Wit" in engines:
        try:
            results["Wit"], times["Wit"] = recog_wit(audio, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Wit"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Wit"] = ""
    if "Azure" in engines:
        try:
            results["Azure"], times["Azure"] = recog_azure(audio, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Azure"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Azure"] = ""
    if "Assembly" in engines:
        try:
            results["Assembly"], times["Assembly"] = recog_assembly(audio_path, english)
        except sr.UnknownValueError as e:
            print("Sorry, I couldn't understand that: " + str(e))
            results["Assembly"] = ""
        except sr.RequestError as e:
            print("Sorry, there was an error processing your request: " + str(e))
            results["Assembly"] = ""
    return results, times


if __name__ == "__main__":
    with sr.AudioFile("C:/Users/qayim/Documents/Science-Fair-2023-4/test.wav") as source:
        audio = recognizer.record(source)
    # noinspection PyArgumentEqualDefault
    results = recognize_speech(audio, "C:/Users/qayim/Documents/Science-Fair-2023-4/test.wav", True)[0]
    print(f"English Test Completed: {results}")
    with sr.AudioFile("C:/Users/qayim/Documents/Science-Fair-2023-4/test2.wav") as source:
        audio = recognizer.record(source)
    results = recognize_speech(audio, "C:/Users/qayim/Documents/Science-Fair-2023-4/test2.wav", False)[0]
    print(f"French Test Completed: {results}")
    always_path = path.join(path.dirname(path.realpath(__file__)), "Audio Files")
    for student_folder in listdir("Audio Files"):
        if continue_searching:
            if student_folder == inputted_start:
                continue_searching = False
            else:
                continue
        scores = {x: 0 for x in engines}
        current_folder = path.join(always_path, student_folder)
        recordings = listdir(current_folder)
        if len(recordings) > 10:
            recordings.remove(student_folder + ".aup3")
        recordings.append(recordings.pop(1))
        if "EN" in student_folder:
            english = True
        else:
            english = False
        student_times = {x: [] for x in engines}
        for recording in recordings:
            full_path_recording = path.join(current_folder, recording)
            with sr.AudioFile(full_path_recording) as source:
                audio = recognizer.record(source)
            results, times = recognize_speech(audio, full_path_recording, english)
            print(f"{recording}: Audio Transcribed. Marking... ")
            print(f"Results: {results}")
            for ky, val in times.items():
                student_times[ky].append(val)
            for key, value in results.items():
                # noinspection PyBroadException
                try:
                    scores[key] += mark(actual_transcriptions[english][recording], value.strip())
                except:
                    print("mark failed")
                    breakpoint()
            print(f"{recording}: Marked")
        for k, v in student_times.items():
            # noinspection PyBroadException
            try:
                student_times[k] = sum(v) / len(v)
            except:
                breakpoint()
        print("Student + Language Code: " + student_folder)
        print(f"Accuracy: {scores}")
        print(f"Average Times for One Request: {student_times}")
        scores["Student + Language Code"] = student_folder
        student_times["Student + Language Code"] = student_folder
        if english:
            # noinspection PyProtectedMember
            english_accuracy = english_accuracy._append(scores, ignore_index=True)
            # noinspection PyProtectedMember
            english_time = english_time._append(student_times, ignore_index=True)
        else:
            # noinspection PyProtectedMember
            french_accuracy = french_accuracy._append(scores, ignore_index=True)
            # noinspection PyProtectedMember
            french_time = french_time._append(student_times, ignore_index=True)
    english_accuracy.to_csv("english_accuracy.csv")
    english_time.to_csv("english_time.csv")
    french_accuracy.to_csv("french_accuracy.csv")
    french_time.to_csv("french_time.csv")
