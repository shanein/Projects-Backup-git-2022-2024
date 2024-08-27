import os
import queue

import pyaudio
import time
import threading
import tkinter as tk
from tkinter import filedialog
from functools import partial

from tqdm import tqdm

from SpeechToTextTo import TextToSpeech
import soundfile as sf
import sounddevice as sd
import wave
from threading import Thread
import pandas as pd
import spacy

from NER.spacy_itinerary_ready_to_use import find_departure_arrival
from Shortpath.shortpath import get_shortpath

nlp = None
graph = {}
stations = None

class TextToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Travel Order")

        # Taille tkinter
        window_width = 700
        window_height = 500
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Centre les boutons verticalement et horizontalement
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True)

        self.vocal_button = tk.Button(self.frame, text="Reconnaissance Vocale", command=partial(self.choisir_audio_mode, "vocal"))
        self.vocal_button.grid(row=0, column=0, pady=10)

        self.timmer = tk.Label(self.frame, text="00:00:00")
        self.timmer.grid(row=1, column=0, pady=0)
        self.recording = False

        self.fichier_button = tk.Button(self.frame, text="Choisir un Fichier", command=partial(self.choisir_audio_mode, "fichier"))
        self.fichier_button.grid(row=2, column=0, pady=20)

        # Affiche le résultat
        self.result_label = tk.Label(master, text="", wraplength=400)
        self.result_label.pack(pady=30)

        self.q = queue.Queue()

    # Fit data into queue
    def callback(self, indata, frames, time, status):
        self.q.put(indata.copy())

    def choisir_audio_mode(self, mode):
        if mode == "vocal":
            # Timmer
            self.timmer.config(text="00:00:00")
            if self.recording:
                self.fichier_button.config(state=tk.NORMAL)  # Enable file selection
                # Mettre à jour le texte du bouton vocal
                self.vocal_button.config(text="Reconnaissance Vocale")

                global recording
                self.recording = False
                self.vocal_button.config(fg="black")
            else:
                self.fichier_button.config(state=tk.DISABLED)  # Disable file selection
                # Mettre à jour le texte du bouton vocal
                self.vocal_button.config(text="Arrêter l'enregistrement ■")

                self.recording = True
                self.vocal_button.config(fg="red")
                # t1 = threading.Thread(target=self.record_audio)
                # t1.start()

                threading.Thread(target=self.record).start()
                # texte_transcrit = TextToSpeech("MySoundFile.wav")
                #
                # if texte_transcrit == None:
                #     self.result_label.config(text="Veuillez parler plus fort ou raprochez vous du micro")
                # else:
                #     self.result_label.config(text="Texte transcrit : " + texte_transcrit)

        elif mode == "fichier":
            fichier_path = filedialog.askopenfilename(title="Choisir un fichier audio", filetypes=[("Fichiers audio", ("*.mp3", "*.wav", "*.ogg", "*.m4a")), ("Tous les fichiers", "*.*")])
            if fichier_path:
                texte_transcrit = TextToSpeech(fichier_path)
                self.result_label.config(text=self.itinerary_locator(texte_transcrit))
            else:
                self.result_label.config(text="Aucun fichier sélectionné")

    def record(self):
        audio = pyaudio.PyAudio()
        # stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=2, frames_per_buffer=1024)
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=512)

        frames = []
        start = time.time()

        print("Enregistrement démarré")


        while self.recording:
            # print(frames)
            data = stream.read(512)
            # data = stream.read(CHUNK)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.timmer.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        # stream.stop_stream()
        stream.close()
        audio.terminate()
        print(f"Enregistrement terminé, {len(frames)} frames enregistrées.")

        try:
            sound_file = wave.open("MySoundFile.wav", "wb")
            sound_file.setnchannels(1)
            sound_file.setsampwidth(2)  # Utiliser une valeur constante (2) pour la largeur de l'échantillon
            sound_file.setframerate(44100)
            sound_file.writeframes(b"".join(frames))
            sound_file.close()
            print("Fichier audio enregistré avec succès")

        except Exception as e:
            print(f"Erreur lors de l'enregistrement du fichier audio : {e}")

        texte_transcrit = TextToSpeech("MySoundFile.wav")
        print(texte_transcrit)
        if texte_transcrit == None:
            self.result_label.config(text="Veuillez parler plus fort ou raprochez vous du micro")
        else:
            self.result_label.config(text=self.itinerary_locator(texte_transcrit))

    def itinerary_locator(self, text):
        try:
            location = find_departure_arrival(text, nlp)
            # location = ([], ['Paris', 'Nantes'])
            print(location)
            print(len(location))
            # print(str(location[0][0]))
            # print(str(location[1][0]))
            # print(location[1][0])
            if  len(location) == 2 and not location[1]:
                print(location)
                print("test")
                if len(location[0]) > 1:
                    location[1].append(location[0].pop())
                    print("Adjusted location:", location)
                print(location)
            elif len(location) == 2 and not location[0]:
                print(location)
                print("test")
                if len(location[1]) > 1:
                    location[0].append(location[1].pop(0))
                    print("Adjusted location:", location)
                print(location)

            if len(location) != 2 or not location[0] or not location[1]:
                print("error location")
                raise ValueError("Veuillez spécifier à la fois une ville de départ et une ville d'arrivée.")
            if location[0][0] == location[1][0]:
                raise ValueError("Vous êtes arrivé !")
            if len(location[0]) > 1 or len(location[1]) > 1:
                print("error location")
                raise ValueError("Veuillez spécifier uniquement une ville de départ et une ville d'arrivée.")
            else:
                try:
                    itinerary = get_shortpath(graph, stations, str(location[0][0]), str(location[1][0]))
                    return itinerary
                except ValueError:
                    return "L'itinéraire n'a pas été trouvé, veuillez réessayer."
                except KeyError:
                    return "L'une des villes de départ ou de destination n'a pas été trouvée dans la base SNCF. Veuillez indiquer un itinéraire de villes pris en charge par les gares SNCF de France."

        except ValueError as e:
            return f"Erreur : {e}"

def loadAppResources():
    global nlp, graph, stations
    try:
        print("\033[92m")

        # Chargement du modèle NLP
        with tqdm(total=33, desc="\033[92mChargement du modèle NLP", unit="%", ncols=100, bar_format="{desc}: {percentage:3.0f}%{bar} {n_fmt}/{total_fmt}") as pbar:
            nlp = spacy.load("./NER/disktosave/model1")
            pbar.update(33)

        # Chargement des données SNCF
        with tqdm(total=67, desc="\033[92mChargement des données SNCF", unit="%", ncols=100) as pbar:
            df = pd.read_csv('./Shortpath/data_sncf_shortpath/timetable.csv')
            for _, row in df.iterrows():
                graph.setdefault(row['from'], []).append((row['to'], row['duration']))
                graph.setdefault(row['to'], []).append((row['from'], row['duration']))
            stations = pd.read_json('./Shortpath/data_sncf_shortpath/stations.json', convert_axes=False)
            pbar.update(67)

    except Exception as e:
        print("\033[0m")
        # Gestion des erreurs lors du chargement
        print("Erreur lors du chargement des ressources:", e)

    finally:
        print("\033[0m")

# Créez une instance de la classe et lancez la boucle principale
try:
    loadAppResources()
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
except Exception as e:
    print("Error:", e)

