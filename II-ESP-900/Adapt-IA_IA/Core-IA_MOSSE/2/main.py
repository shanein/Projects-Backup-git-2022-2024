import cv2
import numpy as np
from video import Video
from tracker import Tracker
from stats import Stats
from ia import IA

class RunSmartDooh :

    def __init__(self):
        self.stats = Stats()
        self.main()


    def main (self):
        print(f'cv2 : {cv2.getVersionString()}')
        print(f'cv2 : {cv2.__version__}')
        print(f'numpy : {np.version.version}')

        video = Video()
        video.startCapture()

        # Define 4K resolution
        video.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        video.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)


        current_width = int(video.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        current_height = int(video.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if current_width != 3840 or current_height != 2160:
            # if not 4k
            video.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            video.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            # video.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 128)
            # video.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 128)

        ia = IA()
        initialisez = False
        self.stats.start_start_analyse()

        while True:

            self.stats.start_counter_speed()

            #v1 : on update les trackers each frame et declanche IA tout les X frames pour detection
            ret, img = video.cap.read()
            if not ret:
                print('video access troubles')
                break

            frame = img.copy()
            # if frame.shape[1] > ia.frame_width:
            #     frame = ia.image_resize(frame, ia.frame_width)
            # else :
            #     frame = cv2.resize(img, (video.camera_Xlength, video.camera_Ylength))

            frame = cv2.resize(img, (video.camera_Xlength, video.camera_Ylength))

            # # Test zoom
            # scale_factor = 2
            # height, width = frame.shape[:2]
            # frame = cv2.resize(frame, (width * scale_factor, height * scale_factor))

            # print(video.camera_Xlength)
            # Print video resolution
            current_width = int(video.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            current_height = int(video.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # print(current_width, current_height)

            if current_width != 3840 or current_height != 2160:
                print("La résolution de la caméra n'est pas en 4K.", )



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
                    # print('on refresh la detection des visages')
                    ia.refresh_faces(frame)

                # else :
                    # boucle pour continuer prediction des visages pas sures
                    # for person_id, data in self.stats.face_trackers.items() :
                        # print(f'person_id :  {person_id}')
                        # print(f'person_data :  {data}')

                # boucle pour détruire les trackers des visages non détectés



            # FIN ------------------------------
            people_count_label = f"Nombre total de personnes uniques : {self.stats.unique_people_counter}"
            cv2.putText(frame, people_count_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("SmartDisplay IA System", frame)

            self.stats.increment_frame_count()
            self.stats.end_counter_speed()

            # print(f"\n")
            stats_printed = self.stats.log_people_infos()
            # print(stats_printed)
            # print(f"-------------------------------------- \n")

            if cv2.waitKey(1) == ord('q'):
                print(f"Nombre total de personnes uniques : {self.stats.unique_people_counter}")
                break



        config = ia.get_config()
        self.stats._save_to_file(config)
        video.cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    RunSmartDooh()
