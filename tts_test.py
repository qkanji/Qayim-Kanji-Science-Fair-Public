import azure.cognitiveservices.speech as speechsdk

english_azure_voices = ['en-CA-ClaraNeural', 'en-CA-LiamNeural', 'en-US-JennyMultilingualNeural3',
                        'en-US-JennyMultilingualV2Neural3', 'en-US-RyanMultilingualNeural3', 'en-US-JennyNeural',
                        'en-US-GuyNeural', 'en-US-AriaNeural', 'en-US-DavisNeural', 'en-US-AmberNeural',
                        'en-US-AnaNeural', 'en-US-AndrewNeural', 'en-US-AshleyNeural', 'en-US-BrandonNeural',
                        'en-US-BrianNeural', 'en-US-ChristopherNeural', 'en-US-CoraNeural', 'en-US-ElizabethNeural',
                        'en-US-EmmaNeural', 'en-US-EricNeural', 'en-US-JacobNeural', 'en-US-JaneNeural',
                        'en-US-JasonNeural', 'en-US-MichelleNeural', 'en-US-MonicaNeural', 'en-US-NancyNeural',
                        'en-US-RogerNeural', 'en-US-SaraNeural', 'en-US-SteffanNeural', 'en-US-TonyNeural',
                        'en-US-AIGenerate1Neural1', 'en-US-AIGenerate2Neural1', 'en-US-AndrewMultilingualNeural1',
                        'en-US-AvaMultilingualNeural1', 'en-US-AvaNeural1', 'en-US-BlueNeural1',
                        'en-US-BrianMultilingualNeural1', 'en-US-EmmaMultilingualNeural1']
french_azure_voices = ['fr-CA-SylvieNeural', 'fr-CA-JeanNeural', 'fr-CA-AntoineNeural', 'fr-CA-ThierryNeural',
                       'fr-FR-DeniseNeural', 'fr-FR-HenriNeural', 'fr-FR-AlainNeural', 'fr-FR-BrigitteNeural',
                       'fr-FR-CelesteNeural', 'fr-FR-ClaudeNeural', 'fr-FR-CoralieNeural', 'fr-FR-EloiseNeural',
                       'fr-FR-JacquelineNeural', 'fr-FR-JeromeNeural', 'fr-FR-JosephineNeural', 'fr-FR-MauriceNeural',
                       'fr-FR-VivienneNeural', 'fr-FR-YvesNeural', 'fr-FR-YvetteNeural',
                       'fr-FR-RemyMultilingualNeural1', 'fr-FR-VivienneMultilingualNeural1']

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription="AZURE API KEY HERE", region="YOUR REGION")
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.mp3")

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name = 'en-CA-LiamNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Get text from the console and synthesize to the default speaker.
print("Enter some text that you want to speak >")
text = input()

speech_synthesis_result = speech_synthesizer.speak_text(text)
