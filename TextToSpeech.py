import os
import time
import openai
from openai import OpenAI
from pathlib import Path
from gtts import gTTS
from google.cloud import texttospeech
from google.oauth2 import service_account
import azure.cognitiveservices.speech as speechsdk

continue_searching = True
inputted_start = input("Where would you like to start? Enter the name of the student folder: ")
inputted_sentence = int(input("What sentence would you like to start from? Enter a number from 1 to 10: "))
inputted_time_to_wait = float(input("How long to wait before starting script in seconds: "))
time.sleep(inputted_time_to_wait)
credentials = service_account.Credentials.from_service_account_file("JSON Credentials file path HERE")
google_client = texttospeech.TextToSpeechClient(credentials=credentials)
client = OpenAI(api_key="OpenAI API KEY HERE")
speech_config = speechsdk.SpeechConfig(subscription="AZURE API KEY HERE", region="YOUR REGION")
openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
google_english_voices = ['en-US-Journey-D', 'en-US-Journey-F', 'en-US-Neural2-A', 'en-US-Neural2-C', 'en-US-Neural2-D', 'en-US-Neural2-E', 'en-US-Neural2-F', 'en-US-Neural2-G', 'en-US-Neural2-H', 'en-US-Neural2-I', 'en-US-Neural2-J', 'en-US-News-K', 'en-US-News-L', 'en-US-News-N', 'en-US-Polyglot-1', 'en-US-Standard-A', 'en-US-Standard-B', 'en-US-Standard-C', 'en-US-Standard-D', 'en-US-Standard-E', 'en-US-Standard-F', 'en-US-Standard-G', 'en-US-Standard-H', 'en-US-Standard-I', 'en-US-Standard-J', 'en-US-Studio-O', 'en-US-Studio-Q', 'en-US-Wavenet-A', 'en-US-Wavenet-B', 'en-US-Wavenet-C', 'en-US-Wavenet-D', 'en-US-Wavenet-E', 'en-US-Wavenet-F', 'en-US-Wavenet-G', 'en-US-Wavenet-H', 'en-US-Wavenet-I', 'en-US-Wavenet-J']
google_french_voices = ['fr-CA-Neural2-A', 'fr-CA-Neural2-B', 'fr-CA-Neural2-C', 'fr-CA-Neural2-D', 'fr-CA-Standard-A', 'fr-CA-Standard-B', 'fr-CA-Standard-C', 'fr-CA-Standard-D', 'fr-CA-Wavenet-A', 'fr-CA-Wavenet-B', 'fr-CA-Wavenet-C', 'fr-CA-Wavenet-D', 'fr-FR-Neural2-A', 'fr-FR-Neural2-B', 'fr-FR-Neural2-C', 'fr-FR-Neural2-D', 'fr-FR-Neural2-E', 'fr-FR-Polyglot-1', 'fr-FR-Standard-A', 'fr-FR-Standard-B', 'fr-FR-Standard-C', 'fr-FR-Standard-D', 'fr-FR-Standard-E', 'fr-FR-Studio-A', 'fr-FR-Studio-D', 'fr-FR-Wavenet-A', 'fr-FR-Wavenet-B', 'fr-FR-Wavenet-C', 'fr-FR-Wavenet-D', 'fr-FR-Wavenet-E']
english_sentences = ['the playful kitten chased the fluffy ball', 'a diligent student always completes assignments on time', 'the bright rainbow appeared after the rain shower', 'oliver was excited to explore the mysterious forest', 'the bubbly soda fizzed in the glass', 'graceful dolphins leaped through the sparkling waves', 'the curious scientist studied the intricate pattern', 'bobbys bicycle has a squeaky wheel', 'the friendly librarian recommended a fascinating book', 'the adventurous explorer discovered a hidden treasure']
french_sentences = ['le chien joyeux court après le ballon coloré', 'une élève sérieuse finit toujours ses devoirs à temps', 'le jardinier plante de belles fleurs dans le jardin', 'la pluie fine crée des flaques sur le trottoir', 'le singe malicieux grimpe rapidement dans larbre', 'la pizza délicieuse cuit dans le four chaud', 'la danseuse gracieuse tourne sur la scène éclairée', 'le chocolat fondant est une délicieuse friandise', 'loiseau chante une mélodie douce au lever du soleil', 'le professeur explique le problème mathématique clairement']
english_azure_voices = ['en-CA-ClaraNeural', 'en-CA-LiamNeural', 'en-US-JennyNeural', 'en-US-GuyNeural', 'en-US-AriaNeural', 'en-US-DavisNeural', 'en-US-AmberNeural', 'en-US-AnaNeural', 'en-US-AndrewNeural', 'en-US-AshleyNeural', 'en-US-BrandonNeural', 'en-US-BrianNeural', 'en-US-ChristopherNeural', 'en-US-CoraNeural', 'en-US-ElizabethNeural', 'en-US-EmmaNeural', 'en-US-EricNeural', 'en-US-JacobNeural', 'en-US-JaneNeural', 'en-US-JasonNeural', 'en-US-MichelleNeural', 'en-US-MonicaNeural', 'en-US-NancyNeural', 'en-US-RogerNeural', 'en-US-SaraNeural', 'en-US-SteffanNeural', 'en-US-TonyNeural']
french_azure_voices = ['fr-CA-SylvieNeural', 'fr-CA-JeanNeural', 'fr-CA-AntoineNeural', 'fr-FR-DeniseNeural', 'fr-FR-HenriNeural', 'fr-FR-AlainNeural', 'fr-FR-BrigitteNeural', 'fr-FR-CelesteNeural', 'fr-FR-ClaudeNeural', 'fr-FR-CoralieNeural', 'fr-FR-EloiseNeural', 'fr-FR-JacquelineNeural', 'fr-FR-JeromeNeural', 'fr-FR-JosephineNeural', 'fr-FR-MauriceNeural', 'fr-FR-YvesNeural', 'fr-FR-YvetteNeural']


def tts_openai(sentence, voice, model, file_destination):
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=sentence
    )

    response.stream_to_file(file_destination)


def tts_google(sentence, voice, file_destination, lang_code):
    # Instantiates a client
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=sentence)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code, name=voice
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = google_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(file_destination, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)


def tts_azure(sentence, voice, file_destination):
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_destination)
    speech_config.speech_synthesis_voice_name = voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text(sentence)


for g_voice in google_english_voices:
    for sentence in english_sentences:
        person_code = f"GAP{google_english_voices.index(g_voice) + 1}EN"
        if continue_searching:
            if (person_code == inputted_start) and ((english_sentences.index(sentence) + 1) == inputted_sentence):
                continue_searching = False
            else:
                continue
        time.sleep(1)
        if not(person_code in os.listdir("Audio Files")):
            os.mkdir("Audio Files/" + person_code)
        speech_file_path = Path(__file__).parent / "Audio Files" / person_code / (str(english_sentences.index(sentence) + 1) + ".mp3")
        tts_google(sentence, g_voice, speech_file_path, "en-US")
        print(speech_file_path)
for g_voice in google_french_voices:
    for sentence in french_sentences:
        person_code = f"GAP{google_french_voices.index(g_voice) + 1 + len(google_english_voices)}FR"
        if continue_searching:
            if (person_code == inputted_start) and ((french_sentences.index(sentence) + 1) == inputted_sentence):
                continue_searching = False
            else:
                continue
        time.sleep(1)
        if not(person_code in os.listdir("Audio Files")):
            os.mkdir("Audio Files/" + person_code)
        speech_file_path = Path(__file__).parent / "Audio Files" / person_code / (str(french_sentences.index(sentence) + 1) + ".mp3")
        tts_google(sentence, g_voice, speech_file_path, g_voice[:5])
        print(speech_file_path)

breakpoint()


for model in ["tts-1", "tts-1-hd"]:
    for open_voice in openai_voices:
        for sentence in english_sentences:
            if model == "tts-1":
                person_code = f"OAP{openai_voices.index(open_voice) + 1}ENS"
            else:
                person_code = f"OAP{openai_voices.index(open_voice) + 1}ENH"
            if continue_searching:
                if (person_code == inputted_start) and ((english_sentences.index(sentence) + 1) == inputted_sentence):
                    continue_searching = False
                else:
                    continue
            time.sleep(21)
            if not(person_code in os.listdir("Audio Files")):
                os.mkdir("Audio Files/" + person_code)
            speech_file_path = Path(__file__).parent / "Audio Files" / person_code / (str(english_sentences.index(sentence) + 1) + ".mp3")
            try:
                tts_openai(sentence, open_voice, model, speech_file_path)
                print(speech_file_path)
            except openai.RateLimitError:
                while True:
                    try:
                        tts_openai(sentence, open_voice, model, speech_file_path)
                        print(speech_file_path)
                        break
                    except openai.RateLimitError:
                        print("Waiting because of rate limit")
                        time.sleep(61)
        for sentence in french_sentences:
            if model == "tts-1":
                person_code = f"OAP{openai_voices.index(open_voice) + 1}FRS"
            else:
                person_code = f"OAP{openai_voices.index(open_voice) + 1}FRH"
            if continue_searching:
                if (person_code == inputted_start) and ((french_sentences.index(sentence) + 1) == inputted_sentence):
                    continue_searching = False
                else:
                    continue
            time.sleep(21)
            if not(person_code in os.listdir("Audio Files")):
                os.mkdir("Audio Files/" + person_code)
            speech_file_path = Path(__file__).parent / "Audio Files" / person_code / (str(french_sentences.index(sentence) + 1) + ".mp3")
            try:
                tts_openai(sentence, open_voice, model, speech_file_path)
                print(speech_file_path)
            except openai.RateLimitError:
                while True:
                    try:
                        tts_openai(sentence, open_voice, model, speech_file_path)
                        print(speech_file_path)
                        break
                    except openai.RateLimitError:
                        print("Waiting because of rate limit")
                        time.sleep(61)

for sentence in english_sentences:
    person_code = "GTP1EN"
    if continue_searching:
        if (person_code == inputted_start) and ((english_sentences.index(sentence) + 1) == inputted_sentence):
            continue_searching = False
        else:
            continue
    if not(person_code in os.listdir("Audio Files")):
        os.mkdir("Audio Files/" + person_code)
    speech_file_path = Path(__file__).parent / "Audio Files" / person_code / (str(english_sentences.index(sentence) + 1) + ".mp3")
    response = gTTS(sentence)
    response.save(speech_file_path)
    print(speech_file_path)

for sentence in french_sentences:
    person_code = "GTP1FR"
    if continue_searching:
        if (person_code == inputted_start) and ((french_sentences.index(sentence) + 1) == inputted_sentence):
            continue_searching = False
        else:
            continue
    if not(person_code in os.listdir("Audio Files")):
        os.mkdir("Audio Files/" + person_code)
    speech_file_path = Path(__file__).parent / "Audio Files" / person_code / (str(french_sentences.index(sentence) + 1) + ".mp3")
    response = gTTS(sentence)
    response.save(speech_file_path)
    print(speech_file_path)


for a_voice in english_azure_voices:
    for sentence in english_sentences:
        person_code = f"AAP{english_azure_voices.index(a_voice) + 1}EN"
        if continue_searching:
            if (person_code == inputted_start) and ((english_sentences.index(sentence) + 1) == inputted_sentence):
                continue_searching = False
            else:
                continue
        if not(person_code in os.listdir("Audio Files")):
            os.mkdir("Audio Files/" + person_code)
        speech_file_path = Path(__file__).parent / "Audio Files" / person_code / (str(english_sentences.index(sentence) + 1) + ".mp3")
        tts_azure(sentence, a_voice, str(speech_file_path))
        print(speech_file_path)
for a_voice in french_azure_voices:
    for sentence in french_sentences:
        person_code = f"AAP{french_azure_voices.index(a_voice) + 1 + len(english_azure_voices)}FR"
        if continue_searching:
            if (person_code == inputted_start) and ((french_sentences.index(sentence) + 1) == inputted_sentence):
                continue_searching = False
            else:
                continue
        if not(person_code in os.listdir("Audio Files")):
            os.mkdir("Audio Files/" + person_code)
        speech_file_path = Path(__file__).parent / "Audio Files" / person_code / (str(french_sentences.index(sentence) + 1) + ".mp3")
        tts_azure(sentence, a_voice, str(speech_file_path))
        print(speech_file_path)
