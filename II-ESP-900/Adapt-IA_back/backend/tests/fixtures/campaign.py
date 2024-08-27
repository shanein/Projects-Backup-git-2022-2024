from fastapi import Form
import pytest


@pytest.fixture(scope="module")
def get_campaign_sample():
    def _get_campaign_sample(valid=True):
        sample_campaign = {
            "name": "Good campaign",
            "description": "My good test campaign",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "budget": 500,
            "is_smart": True,
            "address": "1 Rue de Rivoli",
            "postal_code": "75000",
            "cibles_json": (
                [
                    {
                        "age": 18,
                        "genre": "Female",
                    },
                    {
                        "age": 15,
                        "genre": "Male",
                    },
                ]
            ),
            "video_file": 0,
            "terminals": [""],
        }
        return sample_campaign

    return _get_campaign_sample
