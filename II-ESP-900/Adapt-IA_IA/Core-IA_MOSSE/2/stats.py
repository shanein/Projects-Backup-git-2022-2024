from datetime import datetime
import json
import statistics
import numpy as np

def convert_to_python_types(data):
    if isinstance(data, np.float32):  # Ajout de cette ligne pour gérer np.float32
        return float(data)
    elif isinstance(data, np.int64):
        return int(data)
    elif isinstance(data, dict):
        return {k: convert_to_python_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_python_types(v) for v in data]
    return data


class Stats:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Stats, cls).__new__(cls)

            cls.face_trackers= {}
            cls.unique_people_counter = 0
            cls.people_info= {}
            cls.frame_count = 0

            cls.start_counter = None
            cls.speed_stats = []
            cls.start_analyse = None
        return cls._instance

    @classmethod
    def updateStat(cls, nom_variable, nouvelle_valeur):
        if hasattr(cls, nom_variable):
            setattr(cls, nom_variable, nouvelle_valeur)
        else:
            raise AttributeError(f"La variable '{nom_variable}' n'existe pas.")

    @classmethod
    def add_new_face_tracker(cls, tracker_data):
        new_id = cls.unique_people_counter + 1
        if new_id in cls.face_trackers:
            raise ValueError(f"Un tracker avec l'ID '{new_id}' existe déjà.")
        cls.face_trackers[cls.unique_people_counter + 1] = tracker_data
        cls.unique_people_counter += 1
        cls.add_data_to_people_info(new_id, {})

        return new_id

    @classmethod
    def updatefaceTrackerById(cls, tracker_id, tracker_data):
        # Vérifier si le tracker_id existe
        if tracker_id in cls.face_trackers:
            # Mettre à jour les données du tracker
            cls.face_trackers[tracker_id] = tracker_data
            cls.update_people_info_by_id(tracker_id, tracker_data['predicts'])
        else:
            raise ValueError(f"Aucun tracker trouvé avec l'ID '{tracker_id}'.")

    @classmethod
    def updatefaceTrackerPredictsById(cls, tracker_id, predicts_data):
        # Vérifier si le tracker_id existe
        if tracker_id in cls.face_trackers:
            # Mettre à jour les données du tracker
            cls.face_trackers[tracker_id]['predicts'] = predicts_data
            cls.update_people_info_by_id(tracker_id, predicts_data)
        else:
            raise ValueError(f"Aucun tracker trouvé avec l'ID '{tracker_id}'.")

    @classmethod
    def delete_face_tracker(cls, tracker_id):
        if tracker_id in cls.face_trackers:
            del cls.face_trackers[tracker_id]
        # delete tracker_id from face_trackers which is a dictionary
            # cls.face_trackers.pop(tracker_id)


            print(f'tracker {tracker_id} deleted')
        else :
            print(f'tracker {tracker_id} not found for deletion')


    @classmethod
    def increment_unique_people_counter(cls):
        cls.unique_people_counter += 1

    @classmethod
    def increment_frame_count(cls):
        cls.frame_count += 1


    @classmethod
    def add_data_to_people_info(cls, id, data):
        cls.people_info[id] = data

    @classmethod
    def update_people_info_by_id(cls, id, new_data):
        if id in cls.people_info:
            cls.people_info[id].update(new_data)
        else:
            raise ValueError(f"Aucune donnée trouvée avec l'ID '{id}'.")

    @classmethod
    def log_people_infos(cls):
        final_log = []
        for person_id, data in cls.face_trackers.items():
            if data is not None and 'predicts' in data and 'bbox' in data:
                # print(f"Tracker ID: {person_id}, Predicts: {data['predicts']}, BBox: {data['bbox']}")
                info = DataPrinter(person_id, data['predicts'], data['bbox'])
                final_log.append(info.data)
            else:
                print(f"Missing data for tracker ID: {person_id}")

        print(final_log)
        return final_log


    @classmethod
    def start_start_analyse(cls):
        cls.start_analyse = datetime.now()

    @classmethod
    def start_counter_speed(cls):
        cls.start_counter = datetime.now()

    @classmethod
    def end_counter_speed(cls):
        if cls.start_counter:
            time_diff = datetime.now() - cls.start_counter
            cls.speed_stats.append(time_diff.total_seconds())
            # print(f'end counter speed, duration: {time_diff.total_seconds()} seconds')
        else:
            print('Start counter not initialized !!!!!!!!!!!!!!!!')


    @classmethod
    def get_session_stats(cls):
        if cls.speed_stats:
            moy = statistics.mean(cls.speed_stats)
            med = statistics.median(cls.speed_stats)
            eq_type = statistics.stdev(cls.speed_stats)
        else:
            moy = med = eq_type = None

        return {'moy': moy, 'med': med, 'eq_type': eq_type}


    def get_session_configuration(cls, self):
        return {
            "detection_interval": self.ia.detection_interval,
            "prediction_interval": self.ia.prediction_interval,
            "inactive_threshold": self.ia.inactive_threshold,
            "inactive_detection": self.ia.inactive_detection,
        }

    @classmethod
    def _save_to_file(cls, config):
        start_time = cls.start_analyse.strftime("%Y%m%d%H%M%S") if cls.start_counter else "unknown"
        now = datetime.now()
        end_time = now.strftime("%Y%m%d%H%M%S") if now else "unknown"
        session_stats = cls.get_session_stats()

        data = convert_to_python_types({
            # "face_trackers": cls.face_trackers,
            "unique_people_counter": cls.unique_people_counter,
            "people_info": cls.people_info,
            "frame_count": cls.frame_count,
            "speed_stats": cls.speed_stats,
            "speed_stats_statistics": session_stats,
            'config': config
        })
        filename = f"Stats_{start_time}-{end_time}.json"
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")



class Predictions:

    def __init__(self, gender, gender_index, age, age_index, gender_confidence_score, age_confidence_score ):
        self.data = {
            'gender' : gender,
            'gender_index' : gender_index,
            'age' : age,
            'age_index' : age_index,
            'gender_confidence_score' : gender_confidence_score,
            'age_confidence_score' : age_confidence_score,
        }



class DataPrinter:

    def __init__(self, id, predicts, bbox ):
        self.data = {
            'id' : id,
            'age' : {
                "pred": predicts['age'] or 'unknown',
                "conf": predicts['age_confidence_score'] or 'unknown',
            },
            'gender' : {
                "pred": predicts['gender'] or 'unknown',
                "conf": predicts['gender_confidence_score'] or 'unknown',
            },
            "position" : {
                "start_x": bbox[0],
                "start_y": bbox[1],
                "len_x": bbox[2],
                "len_y": bbox[3],
            }
        }
