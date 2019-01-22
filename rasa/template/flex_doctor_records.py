from rasa.constants import COLOR_SECONDARY


def get_flex_doctor_records():
    return {
        "type": "flex",
        "altText": "🏥 ตารางพบแพทย์",
        "contents": get_flex_doctor_contents()
    }


def get_flex_doctor_contents():
    return {
        "type": "bubble",
        "styles": {
            "header": {
                "backgroundColor": "#23D8F5"
            }
        },
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏥 ตารางพบแพทย์",
                    "weight": "bold",
                    "color": "#1F1F1F",
                    "size": "xxl"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "นัดหมายล่วงหน้า",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมอ A",
                            "size": "lg",
                            "align": "center",
                            "flex": 1,
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 3,
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "พบ",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "text": "จันทร์หน้า"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "เวลา",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "text": "บ่ายโมง"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "เพิ่มเติม",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "wrap": True,
                                            "text": "- ไม่มี -"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมอ B",
                            "size": "lg",
                            "align": "center",
                            "flex": 1,
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 3,
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "พบ",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "text": "พุธหน้า"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "เวลา",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "text": "8 โมง"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "เพิ่มเติม",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "wrap": True,
                                            "text": "❌งดน้ำ ก่อนมาตรวจ 4 ชั่วโมง"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "separator"
                },
                {
                    "type": "text",
                    "text": "ประวัติการพบ",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมอ A",
                            "size": "lg",
                            "align": "center",
                            "flex": 1,
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 3,
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "พบ",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "text": "พุธที่แล้ว"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "เพิ่มเติม",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "wrap": True,
                                            "text": "❌งดน้ำอัดลม"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมอ B",
                            "size": "lg",
                            "align": "center",
                            "flex": 1,
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 3,
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "พบ",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "text": "พุธที่แล้ว"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "เพิ่มเติม",
                                            "weight": "bold",
                                            "align": "center"
                                        },
                                        {
                                            "type": "text",
                                            "wrap": True,
                                            "text": "- ไม่มี -"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
