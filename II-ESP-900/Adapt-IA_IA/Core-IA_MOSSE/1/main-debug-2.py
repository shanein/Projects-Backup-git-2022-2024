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

        self.stats = Stats()
        self.inactive_threshold = inactive_threshold
        self.detection_interval = dectect_int
        self.prediction_interval = pred_int

    def changer_variable_stats(self, nom_variable, nouvelle_valeur):
        self.stats.updateStat(nom_variable, nouvelle_valeur)

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

        for person_id, data in self.stats.face_trackers.items():
            tracker = data['tracker']
            bbox = data['bbox']
            new_tracker_data = {}

            # Assurez-vous que les valeurs de bbox sont des entiers valides
            x, y, w, h = map(int, bbox)
            # Vérifiez que les valeurs de bbox sont à l'intérieur de l'image
            x, y, w, h = max(0, x), max(0, y), min(w, frame.shape[1] - x), min(h, frame.shape[0] - y)
            # Vérifiez que la région découpée n'est pas vide
            if w > 0 and h > 0:
                face_img = frame[y:y+h, x:x+w]
                new_tracker_data = data

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
                        new_tracker_data['predicts'] =  {
                                'gender': GENDER_LIST[gender_index],
                                'gender_index': gender_index,
                                'age': AGE_INTERVALS[age_index],
                                'age_index': age_index,
                                'gender_confidence_score': gender_confidence_score,
                                'age_confidence_score': age_confidence_score
                            }

                        self.stats.updatefaceTrackerById(person_id, new_tracker_data)

                    # Étiquetage et dessin de la boîte englobante
                    label = f"{gender}-{gender_confidence_score*100:.1f}%, {age}-{age_confidence_score*100:.1f}%"

                    yPos = y - 15
                    while yPos < 15:
                        yPos += 15

                    cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
                    cv2.putText(frame, label, (x, yPos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

                else :
                    print(f"Image du visage vide pour le tracker {person_id}")
                    new_tracker_data['inactive_frames'] += 1
                    self.stats.updatefaceTrackerById(person_id, new_tracker_data)

            else:
                print(f"Boîte vide pour le tracker {person_id}")
                new_tracker_data['inactive_frames'] += 1
                self.stats.updatefaceTrackerById(person_id, new_tracker_data)



    def make_one_prediction(self, new_tracker_id, bbox, frame):
        print('one prediction')
        new_tracker_data = {}
        # bbox = face_tracker['bbox']

        # Assurez-vous que les valeurs de bbox sont des entiers valides
        x, y, w, h = map(int, bbox)
        # Vérifiez que les valeurs de bbox sont à l'intérieur de l'image
        x, y, w, h = max(0, x), max(0, y), min(w, frame.shape[1] - x), min(h, frame.shape[0] - y)
        # Vérifiez que la région découpée n'est pas vide
        if w > 0 and h > 0:
            face_img = frame[y:y+h, x:x+w]
            # new_tracker_data = face_tracker

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
                if not 'predicts' in new_tracker_data:
                    new_tracker_data['predicts'] =  {
                            'gender': GENDER_LIST[gender_index],
                            'gender_index': gender_index,
                            'age': AGE_INTERVALS[age_index],
                            'age_index': age_index,
                            'gender_confidence_score': gender_confidence_score,
                            'age_confidence_score': age_confidence_score
                        }

                    # self.stats.updatefaceTrackerPredictsById(new_tracker_id, new_tracker_data)
                    self.stats.updatefaceTrackerPredictsById(new_tracker_id, {
                            'gender': GENDER_LIST[gender_index],
                            'gender_index': gender_index,
                            'age': AGE_INTERVALS[age_index],
                            'age_index': age_index,
                            'gender_confidence_score': gender_confidence_score,
                            'age_confidence_score': age_confidence_score
                        })

                # Étiquetage et dessin de la boîte englobante
                label = f"{gender}-{gender_confidence_score*100:.1f}%, {age}-{age_confidence_score*100:.1f}%"

                yPos = y - 15
                while yPos < 15:
                    yPos += 15

                cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
                cv2.putText(frame, label, (x, yPos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

            else :
                print(f"Image du visage vide pour le tracker {new_tracker_id}")
                new_tracker_data['inactive_frames'] += 1
                self.stats.updatefaceTrackerById(new_tracker_id, new_tracker_data)

        else:
            print(f"Boîte vide pour le tracker {new_tracker_id}")
            new_tracker_data['inactive_frames'] += 1
            self.stats.updatefaceTrackerById(new_tracker_id, new_tracker_data)


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




    def centers_close_ratioV2(self, centerNew, centerTracker, boxWidth, boxHeight):
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

        # width_min = boxWidth * 0.7
        # width_max = boxWidth * 1.3
        # height_min = boxWidth * 0.7
        # heigth_max = boxWidth * 1.3
        # print(f"width_min : {width_min}")
        # print(f"width_max : {width_max}")
        # print(f"height_min : {height_min}")
        # print(f"heigth_max : {heigth_max}")


        # if (distance >= width_min and distance <= width_max) and (distance >= height_min and distance <= heigth_max) :
        #     return True
        # else :
        #     return False

        # Vérifier si la distance est comprise entre 80% et 120% de la plus grande dimension de la boîte
        # return lower_threshold <= distance <= upper_threshold

        return lower_threshold >= distance <= upper_threshold


    def initialize_trackers_V2(self, frame, faces):
        # print('initialise-trackers-v2')
        for (start_x, start_y, end_x, end_y) in faces:
            bbox = (start_x, start_y, end_x - start_x, end_y - start_y)
            center_new_face = ((start_x + end_x) // 2, (start_y + end_y) // 2)
            tracker = cv2.legacy.TrackerMOSSE_create()
            tracker.init(frame, bbox)
            new_tracker_id = self.stats.add_new_face_tracker({'tracker': tracker, 'bbox': bbox, 'inactive_frames': 0})




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
                if self.centers_close_ratioV2(center_new_face, center_tracked_face, (data['bbox'][0] + data['bbox'][2]), (data['bbox'][1] + data['bbox'][3])) == True:
                    print(f"centers_close entre le tracker : {person_id} et un nouveau" )
                    evolSizes, evolRatio = self.eval_boxes_evol(bbox, data)
                    if  -0.80 <= evolSizes <= 1.20 and -0.80 <= evolRatio <= 1.20:
                        print(f'On update le tracker {person_id} : evolSizes={evolSizes} | evolRatio={evolRatio}')
                        print(f'Updating tracker {person_id} : {evolSizes} | {evolRatio}')
                        tracker = cv2.legacy.TrackerMOSSE_create()
                        tracker.init(frame, bbox)
                        self.stats.updatefaceTrackerById(person_id, {'tracker': tracker, 'bbox': bbox, 'predicts': data['predicts'], 'inactive_frames': data['inactive_frames']})
                        new_tracker_needed = False
                        break



            # Créez un nouveau tracker si nécessaire
            if new_tracker_needed:
                print(f'creating new tracker {self.stats.unique_people_counter}')
                tracker = cv2.legacy.TrackerMOSSE_create()
                tracker.init(frame, bbox)
                new_tracker_id = self.stats.add_new_face_tracker({'tracker': tracker, 'bbox': bbox, 'inactive_frames': 0})
                # --> faire predictions sur ce nouveau tracker
                self.make_one_prediction(new_tracker_id, bbox, frame)



    def update_trackersV2(self, frame):
        print('update_trackersV2')

        for person_id, data in self.stats.face_trackers.items():
            tracker = data['tracker']
            new_tracker_data = {**data, 'tracker': tracker}
            ok, bbox = tracker.update(frame)
            if ok:
                # Assurez-vous que les valeurs de bbox sont des entiers valides
                x, y, w, h = map(int, bbox)
                # Vérifiez que les valeurs de bbox sont à l'intérieur de l'image
                x, y, w, h = max(0, x), max(0, y), min(w, frame.shape[1] - x), min(h, frame.shape[0] - y)
                # Vérifiez que la région découpée n'est pas vide
                if w > 0 and h > 0:
                    face_img = frame[y:y+h, x:x+w]
                    box_color = (0, 0, 0)
                    new_tracker_data = {**data, 'tracker': tracker}
                    label = ""


                    if self.stats.frame_count % self.prediction_interval == 0:
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
                            new_tracker_data['predicts'] =  {
                                'gender': GENDER_LIST[gender_index],
                                'gender_index': gender_index,
                                'age': AGE_INTERVALS[age_index],
                                'age_index': age_index,
                                'gender_confidence_score': gender_confidence_score,
                                'age_confidence_score': age_confidence_score
                            }

                        #  if else gender_confidence_score > ['predicts']['gender_confidence_score']
                        elif 'gender' in data['predicts'] and not gender == data['predicts']['gender'] and (gender_confidence_score > data['predicts']['gender_confidence_score'] or gender_confidence_score > 0.90 ):
                            new_tracker_data['predicts']['gender'] = gender
                            new_tracker_data['predicts']['gender_confidence_score'] = gender_confidence_score

                        #  if else age_confidence_score > ['predicts']['age_confidence_score']
                        elif 'age' in data['predicts'] and not age == data['predicts']['age'] and (age_confidence_score > data['predicts']['age_confidence_score'] or age_confidence_score > 0.90):
                            # data['predicts']['age'] = age
                            new_tracker_data['predicts']['age'] = age

                            # data['predicts']['age_confidence_score'] = age_confidence_score
                            new_tracker_data['predicts']['age_confidence_score'] = age_confidence_score

                        else:
                            # print(f"Prédiction de l'âge et du genre pour le tracker {person_id} déjà effectuée")
                            # print(f"L'ancienne certitude est: sexe : {data['predicts']['gender_confidence_score']*100:.1f} |  age : {data['predicts']['age_confidence_score']*100:.1f}")
                            box_color = (255, 0, 0) if 'gender' in data['predicts'] and data['predicts']['gender'] == "Male" else (147, 20, 255)

                        # Étiquetage et dessin de la boîte englobante
                        label = f"{gender}-{gender_confidence_score*100:.1f}%, {age}-{age_confidence_score*100:.1f}%"
                        self.stats.updatefaceTrackerById(person_id, new_tracker_data)

                    elif 'predicts' in new_tracker_data:
                        # print(f'predicts : {new_tracker_data['predicts']}')
                        # label = f"{new_tracker_data['predicts']['gender']}-{new_tracker_data['predicts']['gender_confidence_score']*100:.1f}%, {new_tracker_data['predicts']['age']}-{new_tracker_data['predicts']['age_confidence_score']*100:.1f}%"
                        # box_color = (255, 0, 0) if new_tracker_data['predicts']['gender'] == "Male" else (147, 20, 255)
                        if 'gender' and 'gender_confidence_score' in new_tracker_data['predicts']:
                            label = f"{new_tracker_data['predicts']['gender']}-{new_tracker_data['predicts']['gender_confidence_score']*100:.1f}%%"
                            box_color = (255, 0, 0) if new_tracker_data['predicts']['gender'] == "Male" else (147, 20, 255)
                        else :
                            label = f"unknown"

                        if 'age' and 'age_confidence_score' in new_tracker_data['predicts']:
                            label += f", {new_tracker_data['predicts']['age']}-{new_tracker_data['predicts']['age_confidence_score']*100:.1f}%"
                        else :
                            label += f", unknown"
                    yPos = y - 15
                    while yPos < 15:
                        yPos += 15

                    cv2.rectangle(frame, (x, y), (x+w, y+h), box_color, 2)
                    cv2.putText(frame, label, (x, yPos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
                    # print(person_id)
                else:
                    print(f"Image du visage vide pour le tracker {person_id}")
                    new_tracker_data['inactive_frames'] += 3
                    self.stats.updatefaceTrackerById(person_id, new_tracker_data)
            else:
                print(f"Boîte englobante invalide pour le tracker {person_id}")
                if new_tracker_data['inactive_frames'] == 40 :
                    #delete the tracker from face_trackers
                    self.stats.delete_face_tracker(person_id)

                else :
                    new_tracker_data['inactive_frames'] += 3

                self.stats.updatefaceTrackerById(person_id, new_tracker_data)



    def initializeIADetection(self, frame):
        print('IA Detection Starting')

        faces = self.get_faces(frame)
        print(f'inizialized faces length : {len(faces)}')
        if len(faces) != 0 :
            # Creation des trackers sur les faces detected
            # self.initialize_trackers(frame, faces)
            self.initialize_trackers_V2(frame, faces)

            # # faire la prediction sur les faces ou trackers ?
            self.make_predictions(faces, frame)

            # dessiner les trackers avec les predictions dessus


class RunSmartDooh :

    def __init__(self):
        self.stats = Stats()
        self.main()


    def main (self):
        video = Video()  # Initialiser la vidéo
        video.startCapture()  # Commencer la capture vidéo
        ia = IA()  # Initialiser l'IA
        initialisez = False
        self.stats.start_start_analyse()

        while True:

            self.stats.start_counter_speed()

            #v1 : on update les trackers each frame et declanche IA tout les X frames pour detection
            ret, img = video.cap.read()
            if not ret:
                print('video access troubles')
                break

            frame = cv2.resize(img, (video.camera_Xlength, video.camera_Ylength))

            if initialisez is False :
                ia.initializeIADetection(frame)  # Initialiser la détection IA

                # print(f'face_trackers : {self.stats.face_trackers}')
                # print(f'len(face_trackers) : {len(self.stats.face_trackers)}')
                if len(self.stats.face_trackers) != 0 :
                    initialisez = True

            else :
                # update des trackers
                ia.update_trackersV2(frame)

                if self.stats.frame_count % ia.detection_interval == 0:
                    # On refait la detection des faces sur la nouvelle frame
                    print('on refresh la detection des visages')
                    ia.refresh_faces(frame)

                # else :
                    # boucle pour continuer prediction des visages pas sures
                    # for person_id, data in self.stats.face_trackers.items() :
                        # print(f'person_id :  {person_id}')
                        # print(f'person_data :  {data}')



                # FIN -----------------




            people_count_label = f"Nombre total de personnes uniques : {self.stats.unique_people_counter}"
            cv2.putText(frame, people_count_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("SmartDisplay IA System", frame)

            self.stats.increment_frame_count()
            self.stats.end_counter_speed()

            # print du detail des visages actuellement présents pour COM to C#
            print(f"\n")
            stats_printed = self.stats.log_people_infos()
            print(stats_printed)
            # print(f"\n")
            print(f"-------------------------------------- \n")

            # Exit loop when 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                print(f"Nombre total de personnes uniques : {self.stats.unique_people_counter}")
                # print(f'Details des viewers :')
                # print(self.stats.people_info)
                break




        self.stats._save_to_file()
        video.cap.release()
        cv2.destroyAllWindows()



# # Exécuter le programme
if __name__ == "__main__":
    # main()
    RunSmartDooh()








