from rasa.constants import HELP_LIFF_URI, THINGS_LIFF_URI

RICH_MENU_DEFAULT_OBJECT = {
    "size": {
        "width": 2500,
        "height": 1686
    },
    "selected": True,
    "name": "rich_menu_default",
    "chatBarText": "Menu",
    "areas": [
        {
            "bounds": {
                "x": 0,
                "y": 0,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "uri",
                "label": "วิธีใช้",
                "uri": HELP_LIFF_URI
            }
        },
        {
            "bounds": {
                "x": 834,
                "y": 0,
                "width": 1666,
                "height": 843
            },
            "action": {
                "type": "message",
                "label": "รายการยา",
                "text": "รายการยา"
            }
        },
        {
            "bounds": {
                "x": 0,
                "y": 844,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "message",
                "label": "ประวัติสุขภาพ",
                "text": "ประวัติสุขภาพ"
            }
        },
        {
            "bounds": {
                "x": 834,
                "y": 844,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "message",
                "label": "ตารางนัดพบแพทย์",
                "text": "ตารางนัดพบแพทย์"
            }
        },
        {
            "bounds": {
                "x": 1667,
                "y": 844,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "message",
                "label": "เพิ่มยาใหม่",
                "text": "เพิ่มยาใหม่"
            }
        }
    ]
}

RICH_MENU_THINGS_OBJECT = {
    "size": {
        "width": 2500,
        "height": 1686
    },
    "selected": True,
    "name": "rich_menu_things",
    "chatBarText": "Menu",
    "areas": [
        {
            "bounds": {
                "x": 0,
                "y": 0,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "uri",
                "label": "วิธีใช้",
                "uri": HELP_LIFF_URI
            }
        },
        {
            "bounds": {
                "x": 834,
                "y": 0,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "message",
                "label": "รายการยา",
                "text": "รายการยา"
            }
        },
        {
            "bounds": {
                "x": 1667,
                "y": 0,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "uri",
                "label": "อุปกรณ์แจ้งเตือน",
                "uri": THINGS_LIFF_URI
            }
        },
        {
            "bounds": {
                "x": 0,
                "y": 844,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "message",
                "label": "ประวัติสุขภาพ",
                "text": "ประวัติสุขภาพ"
            }
        },
        {
            "bounds": {
                "x": 834,
                "y": 844,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "message",
                "label": "ตารางนัดพบแพทย์",
                "text": "ตารางนัดพบแพทย์"
            }
        },
        {
            "bounds": {
                "x": 1667,
                "y": 844,
                "width": 833,
                "height": 843
            },
            "action": {
                "type": "message",
                "label": "เพิ่มยาใหม่",
                "text": "เพิ่มยาใหม่"
            }
        }
    ]
}

RICH_MENU_DEFAULT_IMAGE = {
    "path": "assets/rich_menu_default.jpg",
    "type": "image/jpeg"
}

RICH_MENU_THINGS_IMAGE = {
    "path": "assets/rich_menu_things.jpg",
    "type": "image/jpeg"
}
