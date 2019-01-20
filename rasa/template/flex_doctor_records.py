from rasa.constants import COLOR_SECONDARY

def get_flex_doctor_records():
    return {
        "type": "bubble",
        "styles": {
            "header": {
                "backgroundColor": COLOR_SECONDARY
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
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมอ A",
                            "size": "lg",
                            "align": "center"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "พบครั้งต่อไป",
                                    "weight": "bold",
                                    "align": "end"
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
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "เวลา",
                                    "weight": "bold",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": "บ่ายโมง"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมอ B",
                            "size": "lg",
                            "align": "center"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "พบครั้งต่อไป",
                                    "weight": "bold",
                                    "align": "end"
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
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "เวลา",
                                    "weight": "bold",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": "8 โมง"
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
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมอ A",
                            "size": "lg",
                            "align": "center"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "พบเมื่อ",
                                    "weight": "bold",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": "จันทร์ที่แล้ว"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "หมอ B",
                            "size": "lg",
                            "align": "center"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "พบเมื่อ",
                                    "weight": "bold",
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": "พุธที่แล้ว"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
