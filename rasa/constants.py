from datetime import time

COLOR_PRIMARY = "#2de898"
COLOR_SECONDARY = "#23D8F5"
COLOR_1 = "#389ae5"
COLOR_2 = "#ffa731"
COLOR_3 = "#ff6c31"

DEFAULT_REMINDER = {
    ("morning", "before_meal"): {
        "time_text": "เช้า",
        "meal_text": "ก่อนอาหาร",
        "time": time(0, 0),
        "job_id": None
    },
    ("morning", "after_meal"): {
        "time_text": "เช้า",
        "meal_text": "หลังอาหาร",
        "time": time(1, 0),
        "job_id": None
    },
    ("noon", "before_meal"): {
        "time_text": "กลางวัน",
        "meal_text": "ก่อนอาหาร",
        "time": time(4, 0),
        "job_id": None
    },
    ("noon", "after_meal"): {
        "time_text": "กลางวัน",
        "meal_text": "หลังอาหาร",
        "time": time(5, 30),
        "job_id": None
    },
    ("evening", "before_meal"): {
        "time_text": "เย็น",
        "meal_text": "ก่อนอาหาร",
        "time": time(11, 0),
        "job_id": None
    },
    ("evening", "after_meal"): {
        "time_text": "เย็น",
        "meal_text": "หลังอาหาร",
        "time": time(12, 0),
        "job_id": None
    },
    ("night", None): {
        "time_text": "ก่อนนอน",
        "meal_text": None,
        "time": time(13, 30),
        "job_id": None
    }
}
