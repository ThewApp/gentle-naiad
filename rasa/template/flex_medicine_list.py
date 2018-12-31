from rasa.constants import COLOR_PRIMARY, COLOR_3

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
                        "color": "#444444",
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
                            "contents": [
                                {
                                    "type": "text",
                                    "text": medicine["name"],
                                    "size": "xl"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "ทาน" + medicine["time"]
                                        },
                                        {
                                            "type": "text",
                                            "text": medicine["meal"]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "button",
                            "flex": 0,
                            "style": "primary",
                            "color": COLOR_3,
                            "action": {
                                "type": "postback",
                                "label": "ลบ",
                                "data": "delete[%i]" % index,
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
