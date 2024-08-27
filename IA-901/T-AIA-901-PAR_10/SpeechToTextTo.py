from pydub import AudioSegment
import speech_recognition as sr
import io

def TextToSpeech(audio_path):
    # Récupère l'extension du fichier audio
    extension = audio_path.split(".")[-1]

    # Convertir le fichier audio en objet AudioSegment
    audio = AudioSegment.from_file(audio_path, format=extension)
    audio = audio.set_frame_rate(16000).set_channels(1)

    # Exporter l'audio converti en objet bytes, donc pas de fichier physique créé
    byte_io = io.BytesIO()
    audio.export(byte_io, format="wav")
    byte_io.seek(0)  # retourner au début du fichier

    # Initialiser le recognizer
    r = sr.Recognizer()

    # Utiliser l'objet bytes comme source pour la reconnaissance
    with sr.AudioFile(byte_io) as source:
        audio_data = r.record(source)

        try:
            # Transcription par Google Web Speech API
            text_google = r.recognize_google(audio_data, language="fr-FR")

            return text_google

        except sr.UnknownValueError:
            print("Google Web Speech API n'a pas pu comprendre l'audio")
        except sr.RequestError as e:
            print(f"Impossible d'obtenir les résultats de Google Web Speech API; {e}")

# Exemple d'utilisation de la fonction avec un fichier M4a
# fichier_mp4 = "test.m4a"
# texte_transcrit = TextToSpeech(fichier_mp4)
# print("Texte transcrit : ", texte_transcrit)
