from rasa.constants import COLOR_PRIMARY, COLOR_3, DEFAULT_MEDICINE_TEXT


def get_flex_medicine_list(medicine_list):
    return {
        "type": "flex",
        "altText": "รายการยา",
        "contents": {
            "type": "bubble",
            "styles": {
                "header": {
                    "backgroundColor": COLOR_PRIMARY
                }
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "รายการยา",
                        "weight": "bold",
                        "color": "#1F1F1F",
                        "size": "xl"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": get_body_contents(medicine_list)
            }
        }
    }


def get_body_contents(medicine_list):
    contents = []
    length = len(medicine_list)
    for index, medicine in enumerate(medicine_list):
        delete_data = "/remove_medicine{\"remove_medicine_uuid\": \"%s\"}" % (
            medicine.get("uuid"))
        medicine_time = medicine.get("time")
        medicine_info = [
            {
                "type": "text",
                "text": medicine["name"],
                "size": "xl"
            },
            {
                "type": "text",
                "text": "ทานตอน" + DEFAULT_MEDICINE_TEXT.get(medicine_time, medicine_time)
            }
        ]
        medicine_meal = medicine.get("meal")
        if medicine_meal:
            medicine_info.append({
                "type": "text",
                "text": DEFAULT_MEDICINE_TEXT.get(medicine_meal)
            })
        contents.append({
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": medicine_info
                        },
                        {
                            "type": "button",
                            "flex": 0,
                            "style": "primary",
                            "color": COLOR_3,
                            "gravity": "center",
                            "action": {
                                "type": "postback",
                                "label": "ลบ",
                                "data": delete_data,
                                "displayText": "ลบ" + medicine["name"]
                            }
                        }
                    ]
                }
            ]})
        if index + 1 < length:
            contents.append({
                "type": "separator"
            })
    return contents
