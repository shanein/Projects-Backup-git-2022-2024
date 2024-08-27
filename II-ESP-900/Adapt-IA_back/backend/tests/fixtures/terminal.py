import pytest


@pytest.fixture(scope="module")
def get_terminal_sample():
    def _get_terminal_sample():
        sample_terminal = {
            "place_type": "Café",
            "name": "Good terminal",
            "description": "My good test terminal",
            "localisation": "14 Rue Voltaire",
            "lat": 46,
            "long": 2,
            "week_schedule": (
                {
                    "lundi": {"opening": "08:00", "closing": "18:00"},
                    "mardi": {"opening": "08:00", "closing": "18:00"},
                    "mercredi": {"opening": "08:00", "closing": "18:00"},
                    "jeudi": {"opening": "08:00", "closing": "18:00"},
                    "vendredi": {"opening": "08:00", "closing": "18:00"},
                    "samedi": {"opening": "08:00", "closing": "18:00"},
                    "dimanche": {"opening": "08:00", "closing": "18:00"},
                }
            ),
            "start_date": "01-01-2024",
            "unavailable_dates": [],
        }
        return sample_terminal

    return _get_terminal_sample
