import cv2
import numpy as np
from video import Video
from tracker import Tracker
from stats import Stats

GENDER_MODEL = 'weights/deploy_gender.prototxt'
GENDER_PROTO = 'weights/gender_net.caffemodel'
# Each Caffe Model impose the shape of the input image also image preprocessing is required like mean
# substraction to eliminate the effect of illunination changes
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
GENDER_LIST = ['Male', 'Female']
FACE_PROTO = "weights/deploy.prototxt.txt"
FACE_MODEL = "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"
AGE_MODEL = 'weights/deploy_age.prototxt'
AGE_PROTO = 'weights/age_net.caffemodel'
AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                 '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']


class IA :

    def __init__(self, dectect_int=10, pred_int=20, inactive_threshold=10):
        # load face Caffe model
        self.face_net = cv2.dnn.readNetFromCaffe(FACE_PROTO, FACE_MODEL)
        # Load age prediction model
        self.age_net = cv2.dnn.readNetFromCaffe(AGE_MODEL, AGE_PROTO)
        # Load gender prediction model
        self.gender_net = cv2.dnn.readNetFromCaffe(GENDER_MODEL, GENDER_PROTO)

        self.inactive_threshold = inactive_threshold

        # self.people_info = {}
        # self.unique_people_counter = 0  # Initialisation du compteur de personnes uniques
        # self.face_trackers = {}
        # self.frame_count = 0


        # global people_info
        # people_info= {}
        # global unique_people_counter
        # unique_people_counter = 0  # Initialisation du compteur de personnes uniques
        # global face_trackers
        # face_trackers= {}
        # global frame_count
        # frame_count = 0
        self.stats = Stats()
        self.detection_interval = dectect_int
        self.prediction_interval = pred_int



    def get_faces(self, frame, confidence_threshold=0.5):
        # convert the frame into a blob to be ready for NN input
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177.0, 123.0))
        # set the image as input to the NN
        self.face_net.setInput(blob)
        # perform inference and get predictions
        output = np.squeeze(self.face_net.forward())
        # initialize the result list
        faces = []
        # Loop over the faces detected
        for i in range(output.shape[0]):
            # print(f'shape {i}')
            confidence = output[i, 2]
            if confidence > confidence_threshold:
                box = output[i, 3:7] * \
                    np.array([frame.shape[1], frame.shape[0],
                            frame.shape[1], frame.shape[0]])
                # convert to integers
                start_x, start_y, end_x, end_y = box.astype(int)
                # widen the box a little
                start_x, start_y, end_x, end_y = start_x - \
                    10, start_y - 10, end_x + 10, end_y + 10
                start_x = 0 if start_x < 0 else start_x
                start_y = 0 if start_y < 0 else start_y
                end_x = 0 if end_x < 0 else end_x
                end_y = 0 if end_y < 0 else end_y
                # append to our list
                faces.append((start_x, start_y, end_x, end_y))
        return faces

    def get_gender_predictions(self, face_img):
        blob = cv2.dnn.blobFromImage(
            image=face_img, scalefactor=1.0, size=(227, 227),
            mean=MODEL_MEAN_VALUES, swapRB=False, crop=False
        )
        self.gender_net.setInput(blob)
        return self.gender_net.forward()

    def get_age_predictions(self, face_img):
        blob = cv2.dnn.blobFromImage(
            image=face_img, scalefactor=1.0, size=(227, 227),
            mean=MODEL_MEAN_VALUES, swapRB=False
        )
        self.age_net.setInput(blob)
        return self.age_net.forward()

    def make_predictions(self, faces, frame):
        print('make prediction ')

        for person_id, data in face_trackers.items():
            tracker = data['tracker']

            bbox = data['bbox']

            # Assurez-vous que les valeurs de bbox sont des entiers valides
            x, y, w, h = map(int, bbox)
            # Vérifiez que les valeurs de bbox sont à l'intérieur de l'image
            x, y, w, h = max(0, x), max(0, y), min(w, frame.shape[1] - x), min(h, frame.shape[0] - y)
            # Vérifiez que la région découpée n'est pas vide
            if w > 0 and h > 0:
                face_img = frame[y:y+h, x:x+w]

                # Exécutez la prédiction si face_img est valide
                if face_img.size > 0 and face_img.shape[0] > 0 and face_img.shape[1] > 0:
                    age_preds = self.get_age_predictions(face_img)
                    gender_preds = self.get_gender_predictions(face_img)
                    gender_index = gender_preds[0].argmax()
                    age_index = age_preds[0].argmax()
                    gender = GENDER_LIST[gender_index]
                    age = AGE_INTERVALS[age_index]
                    gender_confidence_score = gender_preds[0][gender_index]
                    age_confidence_score = age_preds[0][age_index]

                    box_color = (255, 0, 0) if gender == "Male" else (147, 20, 255)

                    # Verifier si ['predicts'] existe
                    if not 'predicts' in data:
                        data['predicts'] = {
                            'gender': GENDER_LIST[gender_index],
                            'gender_index': gender_index,
                            'age': AGE_INTERVALS[age_index],
                            'age_index': age_index,
                            'gender_confidence_score': gender_confidence_score,
                            'age_confidence_score': age_confidence_score
                        }

                    # Étiquetage et dessin de la boîte englobante
                    label = f"{gender}-{gender_confidence_score*100:.1f}%, {age}-{age_confidence_score*100:.1f}%"

                    yPos = y - 15
                    while yPos < 15:
                        yPos += 15

                    cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
                    cv2.putText(frame, label, (x, yPos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

                else :
                    print(f"Image du visage vide pour le tracker {person_id}")
                    data['inactive_frames'] += 1

            else:
                print(f"Boîte vide pour le tracker {person_id}")
                data['inactive_frames'] += 1




    def eval_boxes_evol(self, bbox, data):
        # calculer evolution de la taille de la boite englobante
        boxNew = bbox[2] * bbox[3]
        boxOld = data['bbox'][2] * data['bbox'][3]
        evolSizes = (boxNew - boxOld) / boxOld

        # calculer le ratio de la boite englobante
        ratioNewBox = bbox[2] / bbox[3]
        ratioOldBox = data['bbox'][2] / data['bbox'][3]
        evolRatio = (ratioNewBox - ratioOldBox) / ratioOldBox

        return evolSizes, evolRatio


    def centers_close_ratio(self, centerNew, centerTracker, boxWidth, boxHeight):
        # Calculer la différence en x et y entre les centres
        x_diff = centerNew[0] - centerTracker[0]
        y_diff = centerNew[1] - centerTracker[1]

        # Calculer la distance euclidienne entre les deux centres
        distance = np.sqrt(x_diff**2 + y_diff**2)

        # Calculer 80% et 120% de la plus grande dimension de la boîte englobante
        max_dimension = max(boxWidth, boxHeight)
        lower_threshold = 0.70 * max_dimension
        upper_threshold = 1.30 * max_dimension

        print(f"distance : {distance}")
        print(f"lower_threshold : {lower_threshold}")
        print(f"upper_threshold : {upper_threshold}")

        # Vérifier si la distance est comprise entre 80% et 120% de la plus grande dimension de la boîte
        return lower_threshold <= distance <= upper_threshold


    def initialize_trackers(self, frame, faces):
        global unique_people_counter
        print(f"\n\nInitialize_trackers : {len(faces)} face(s) sent")

        for (start_x, start_y, end_x, end_y) in faces:
            bbox = (start_x, start_y, end_x - start_x, end_y - start_y)
            center_new_face = ((start_x + end_x) // 2, (start_y + end_y) // 2)
            new_tracker_needed = True

            # Vérifiez si le centre du nouveau visage est proche d'un tracker existant
            # for data in trackers.values():
            for person_id, data in face_trackers.items():

                print(f"person_id : {person_id}")
                print(f"data :  {data}")

                center_tracked_face = ((data['bbox'][0] + data['bbox'][2]) // 2,
                                    (data['bbox'][1] + data['bbox'][3]) // 2)

                # Detecter si c est le meme visage, ou un nouveau donc il faut set un tracker
                    # Si c est le meme visage on update le tracker
                    # Si c est un nouveau visage on set un nouveau tracker

                # if centers_close(center_new_face, center_tracked_face, 700):
                # if self.centers_close_ratio(center_new_face, center_tracked_face, data['bbox'][2], data['bbox'][3]):
                if self.centers_close_ratio(center_new_face, center_tracked_face, data['bbox'][2], data['bbox'][3]):

                    print(f"centers_close entre le tracker : {person_id} et un nouveau" )
                    evolSizes, evolRatio = self.eval_boxes_evol(bbox, data)

                    if  -0.80 <= evolSizes <= 1.20 and -0.80 <= evolRatio <= 1.20:
                        # print(f'On update le tracker {person_id} : {evolSizes} | {evolRatio}')
                        predicts_data = data.get('predicts', {'gender': None, 'age': None}) # Ajoutez une valeur par défaut
                        tracker = cv2.legacy.TrackerMOSSE_create()
                        tracker.init(frame, bbox)
                        face_trackers[person_id] = {'tracker': tracker, 'bbox': bbox, 'predicts': predicts_data, 'inactive_frames': data['inactive_frames']}
                        new_tracker_needed = False
                        break



            # Créez un nouveau tracker si nécessaire
            if new_tracker_needed:
                print(f'creating new tracker {unique_people_counter}')
                tracker = cv2.legacy.TrackerMOSSE_create()
                tracker.init(frame, bbox)
                face_trackers[unique_people_counter] = {'tracker': tracker, 'bbox': bbox, 'inactive_frames': 0}
                unique_people_counter += 1




    def initialize_trackers_V2(self, frame, faces):
        # global unique_people_counter
        print('initialise-trackers-v2')

        for (start_x, start_y, end_x, end_y) in faces:
            bbox = (start_x, start_y, end_x - start_x, end_y - start_y)
            center_new_face = ((start_x + end_x) // 2, (start_y + end_y) // 2)

            #print(f'creating new tracker {unique_people_counter}')
            tracker = cv2.legacy.TrackerMOSSE_create()
            tracker.init(frame, bbox)
            self.stats.face_trackers[unique_people_counter] = {'tracker': tracker, 'bbox': bbox, 'inactive_frames': 0}
            self.stats.unique_people_counter += 1


    def update_trackers(self, trackers, frame):
        # print(f"update_trackers")
        new_trackers = {}
        for person_id, data in trackers.items():
            tracker = data['tracker']
            ok, bbox = tracker.update(frame)
            x, y, w, h = bbox
            # Vérifiez que le tracker est dans les limites de l'image
            in_bounds = (0 <= x < frame.shape[1]) and (0 <= y < frame.shape[0])

            if ok and in_bounds:
                # print(f"Le tracker {person_id} est dans les limites")
                # print(f"data['inactive_frames'] : {data['inactive_frames']}")
                data['inactive_frames'] = 0
                new_trackers[person_id] = data

            elif ok and not in_bounds:
                print(f"Le tracker {person_id} est hors limites")
                # new_trackers[person_id] = data
                data['inactive_frames'] += 3
                print(f"data['inactive_frames'] : {data['inactive_frames']}")
                if data['inactive_frames'] < self.inactive_threshold:
                    new_trackers[person_id] = data

            elif not ok and in_bounds:
                print(f"Le tracker {person_id} a perdu sa target")
                data['inactive_frames'] += 5
                print(f"data['inactive_frames'] : {data['inactive_frames']}")
                if data['inactive_frames'] < self.inactive_threshold:
                    new_trackers[person_id] = data
            else:
                data['inactive_frames'] += 10
                print(f"data['inactive_frames'] : {data['inactive_frames']}")

                # if data['inactive_frames'] < self.inactive_threshold:
                #     new_trackers[person_id] = data


            if data['inactive_frames'] >= self.inactive_threshold:
                print(f"Le tracker {person_id} a été supprimé")
                # Vérifier si on voit un visage dans la zone du tracker
                faces = self.get_faces(frame[y:y+h, x:x+w])
                if len(faces) > 0:
                    print(f"Un visage a été détecté dans la zone du tracker {person_id}")
                    # Créer un nouveau tracker pour le visage détecté
                    bbox = faces[0]
                    tracker = cv2.legacy.TrackerMOSSE_create()
                    tracker.init(frame, bbox)
                    new_trackers[person_id] = {'tracker': tracker, 'bbox': bbox, 'inactive_frames': 0}
                else:
                    print(f"Aucun visage détecté dans la zone du tracker {person_id}")


        # boucle sur

        return new_trackers


    def refresh_trackers(self, frame):
        # print(f"update_trackers")
        new_trackers = {}
        for person_id, data in face_trackers.items():
            tracker = data['tracker']
            ok, bbox = tracker.update(frame)
            x, y, w, h = bbox
            # Vérifiez que le tracker est dans les limites de l'image
            in_bounds = (0 <= x < frame.shape[1]) and (0 <= y < frame.shape[0])

            if ok and in_bounds:
                # print(f"Le tracker {person_id} est dans les limites")
                # print(f"data['inactive_frames'] : {data['inactive_frames']}")
                data['inactive_frames'] = 0
                new_trackers[person_id] = data

            elif ok and not in_bounds:
                print(f"Le tracker {person_id} est hors limites")
                # new_trackers[person_id] = data
                data['inactive_frames'] += 3
                print(f"data['inactive_frames'] : {data['inactive_frames']}")
                if data['inactive_frames'] < self.inactive_threshold:
                    new_trackers[person_id] = data

            elif not ok and in_bounds:
                print(f"Le tracker {person_id} a perdu sa target")
                data['inactive_frames'] += 5
                print(f"data['inactive_frames'] : {data['inactive_frames']}")
                if data['inactive_frames'] < self.inactive_threshold:
                    new_trackers[person_id] = data
            else:
                data['inactive_frames'] += 10
                print(f"data['inactive_frames'] : {data['inactive_frames']}")

                # if data['inactive_frames'] < self.inactive_threshold:
                #     new_trackers[person_id] = data


            if data['inactive_frames'] >= self.inactive_threshold:
                print(f"Le tracker {person_id} a été supprimé")
                # Vérifier si on voit un visage dans la zone du tracker
                faces = self.get_faces(frame[y:y+h, x:x+w])
                if len(faces) > 0:
                    print(f"Un visage a été détecté dans la zone du tracker {person_id}")
                    # Créer un nouveau tracker pour le visage détecté
                    bbox = faces[0]
                    tracker = cv2.legacy.TrackerMOSSE_create()
                    tracker.init(frame, bbox)
                    new_trackers[person_id] = {'tracker': tracker, 'bbox': bbox, 'inactive_frames': 0}
                else:
                    print(f"Aucun visage détecté dans la zone du tracker {person_id}")

        self.face_trackers = new_trackers


    def refresh_faces(self, frame):
        print('refresh_faces start')

        faces = self.get_faces(frame)

        for (start_x, start_y, end_x, end_y) in faces:
            bbox = (start_x, start_y, end_x - start_x, end_y - start_y)
            center_new_face = ((start_x + end_x) // 2, (start_y + end_y) // 2)
            new_tracker_needed = True

            # Vérifiez si le centre du nouveau visage est proche d'un tracker existant
            # for data in trackers.values():
            for person_id, data in self.stats.face_trackers.items():

                center_tracked_face = ((data['bbox'][0] + data['bbox'][2]) // 2,
                                    (data['bbox'][1] + data['bbox'][3]) // 2)

                # Detecter si c est le meme visage, ou un nouveau donc il faut set un tracker
                    # Si c est le meme visage on update le tracker
                    # Si c est un nouveau visage on set un nouveau tracker

                # if centers_close(center_new_face, center_tracked_face, 700):
                if self.centers_close_ratio(center_new_face, center_tracked_face, data['bbox'][2], data['bbox'][3]):
                    print(f"centers_close entre le tracker : {person_id} et un nouveau" )
                    evolSizes, evolRatio = self.eval_boxes_evol(bbox, data)
                    if  -0.80 <= evolSizes <= 1.20 and -0.80 <= evolRatio <= 1.20:
                        print(f'On update le tracker {person_id} : evolSizes={evolSizes} | evolRatio={evolRatio}')
                        print(f'Updating tracker {person_id} : {evolSizes} | {evolRatio}')
                        tracker = cv2.legacy.TrackerMOSSE_create()
                        tracker.init(frame, bbox)
                        self.stats.face_trackers[person_id] = {'tracker': tracker, 'bbox': bbox, 'predicts': data['predicts'], 'inactive_frames': data['inactive_frames']}
                        new_tracker_needed = False
                        break



            # Créez un nouveau tracker si nécessaire
            if new_tracker_needed:
                print(f'creating new tracker {self.stats.unique_people_counter}')
                tracker = cv2.legacy.TrackerMOSSE_create()
                tracker.init(frame, bbox)
                self.stats.face_trackers[self.stats.unique_people_counter] = {'tracker': tracker, 'bbox': bbox, 'inactive_frames': 0}
                self.stats.unique_people_counter += 1



    def update_trackersV2(self, frame):
        print('REFRESH TRACKERS V2')

        new_trackers = {}
        for person_id, data in face_trackers.items():
            tracker = data['tracker']
            ok, bbox = tracker.update(frame)
            if ok:
                # Assurez-vous que les valeurs de bbox sont des entiers valides
                x, y, w, h = map(int, bbox)
                # Vérifiez que les valeurs de bbox sont à l'intérieur de l'image
                x, y, w, h = max(0, x), max(0, y), min(w, frame.shape[1] - x), min(h, frame.shape[0] - y)
                # Vérifiez que la région découpée n'est pas vide
                if w > 0 and h > 0:
                    face_img = frame[y:y+h, x:x+w]
                    box_color = (255, 0, 0)

                    if frame_count % self.prediction_interval == 0:
                        # On refait les predictions sur les visages deja validées
                        print('on refresh les predictions des visages')

                        age_preds = self.get_age_predictions(face_img)
                        gender_preds = self.get_gender_predictions(face_img)
                        gender_index = gender_preds[0].argmax()
                        age_index = age_preds[0].argmax()
                        gender = GENDER_LIST[gender_index]
                        age = AGE_INTERVALS[age_index]
                        gender_confidence_score = gender_preds[0][gender_index]
                        age_confidence_score = age_preds[0][age_index]



                         # Verifier si ['predicts'] existe
                        if not 'predicts' in data:
                            data['predicts'] = {
                                'gender': GENDER_LIST[gender_index],
                                'gender_index': gender_index,
                                'age': AGE_INTERVALS[age_index],
                                'age_index': age_index,
                                'gender_confidence_score': gender_confidence_score,
                                'age_confidence_score': age_confidence_score
                            }

                        #  if else gender_confidence_score > ['predicts']['gender_confidence_score']
                        elif not gender == data['predicts']['gender'] and (gender_confidence_score > data['predicts']['gender_confidence_score'] or gender_confidence_score > 0.90 ):
                            data['predicts']['gender'] = gender
                            data['predicts']['gender_confidence_score'] = gender_confidence_score

                        #  if else age_confidence_score > ['predicts']['age_confidence_score']
                        elif not age == data['predicts']['age'] and (age_confidence_score > data['predicts']['age_confidence_score'] or age_confidence_score > 0.90):
                            data['predicts']['age'] = age
                            data['predicts']['age_confidence_score'] = age_confidence_score

                        else:
                            # print(f"Prédiction de l'âge et du genre pour le tracker {person_id} déjà effectuée")
                            # print(f"L'ancienne certitude est: sexe : {data['predicts']['gender_confidence_score']*100:.1f} |  age : {data['predicts']['age_confidence_score']*100:.1f}")
                            box_color = (255, 0, 0) if data['predicts']['gender'] == "Male" else (147, 20, 255)

                        # Étiquetage et dessin de la boîte englobante
                        label = f"{gender}-{gender_confidence_score*100:.1f}%, {age}-{age_confidence_score*100:.1f}%"

                    elif 'predicts' in data:
                        label = f"{data['predicts']['gender']}-{data['predicts']['gender_confidence_score']*100:.1f}%, {data['predicts']['age']}-{data['predicts']['age_confidence_score']*100:.1f}%"
                        box_color = (255, 0, 0) if data['predicts']['gender'] == "Male" else (147, 20, 255)

                    yPos = y - 15
                    while yPos < 15:
                        yPos += 15

                    cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
                    cv2.putText(frame, label, (x, yPos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
                    # print(person_id)
                else:
                    print(f"Image du visage vide pour le tracker {person_id}")
                    data['inactive_frames'] += 3
            else:
                print(f"Boîte englobante invalide pour le tracker {person_id}")
                data['inactive_frames'] += 3


    def initializeIADetection(self, frame):
        print('IA Detection Starting')

        faces = self.get_faces(frame)
        print(f'inizialized faces length : {len(faces)}')
        if len(faces) != 0 :
            # Creation des trackers sur les faces detected
            # self.initialize_trackers(frame, faces)
            self.initialize_trackers_V2(frame, faces)

            # faire la prediction sur les faces ou trackers ?
            self.make_predictions(faces, frame)

            # dessiner les trackers avec les predictions dessus


class RunSmartDooh :

    def __init__(self):
        self.stats = Stats()


    def changer_variable_stats(self, nom_variable, nouvelle_valeur):
        self.stats.updateStat(nom_variable, nouvelle_valeur)




def main():
    # global frame_count, unique_people_counter, face_trackers
    stats = Stats()
    video = Video()  # Initialiser la vidéo
    video.startCapture()  # Commencer la capture vidéo
    ia = IA()  # Initialiser l'IA
    initialisez = False

    while True:
        #v1 : on update les trackers each frame et declanche IA tout les X frames pour detection
        ret, img = video.cap.read()
        if not ret:
            print('video access troubles')
            break

        frame = cv2.resize(img, (video.camera_Xlength, video.camera_Ylength))

        if initialisez is False :
            ia.initializeIADetection(frame)  # Initialiser la détection IA

            print(f'face_trackers : {stats.face_trackers}')
            print(f'len(face_trackers) : {len(stats.face_trackers)}')
            if len(stats.face_trackers) != 0 :
                initialisez = True

        else :
            # update des trackers
            ia.update_trackersV2(frame)

            if stats.frame_count % ia.detection_interval == 0:
                # On refait la detection des faces sur la nouvelle frame
                print('on refresh la detection des visages')
                ia.refresh_faces(frame)

            # if frame_count % ia.prediction_interval == 0:
            #     # On refait les predictions sur les visages deja validées
            #     print('on refresh les predictions des visages')

            else :
                # boucle pour continuer prediction des visages pas sures
                for person_id, data in stats.face_trackers.items() :
                    print(f'person_id :  {person_id}')
                    print(f'person_data :  {data}')


            stats.frame_count.updateStat() += 1

            # FIN -----------------


        people_count_label = f"Nombre total de personnes uniques : {stats.unique_people_counter}"
        cv2.putText(frame, people_count_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("SmartDisplay IA System", frame)

        # print du detail des visages actuellement présents pour COM to C#
        print(f'FINAL PRINT viewers actifs : {len(stats.face_trackers)}')

        # Exit loop when 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            print(f"Nombre total de personnes uniques : {stats.unique_people_counter}")
            print(f'Details des viewers :')
            print(stats.people_info)
            break


    video.cap.release()
    cv2.destroyAllWindows()





# # Exécuter le programme
if __name__ == "__main__":
    main()





