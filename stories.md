## follow
* follow_event
  - line_follow

## unfollow
* unfollow_event
  - action_restart

## things link
* things_link{"things_deviceId": "t123"}
  - line_things_link

## things unlink
* things_unlink{"things_deviceId": "t123"}
  - line_things_unlink

## add medicine
* add_medicine
  - custom_form_add_medicine
  - form{"name": "custom_form_add_medicine"}
  - form{"name": null}
  - slot{"medicine_list": [{"name": "ยาความดัน", "time": "morning", "meal": "before_meal"}]}
  - slot{"new_medicine_name": null}
  - slot{"new_medicine_time": null}
  - slot{"new_medicine_meal": null}
  - custom_medicine_reminder_update

## add medicine cancel
* add_medicine
  - custom_form_add_medicine
  - form{"name": "custom_form_add_medicine"}
* negative
  - custom_reset_add_new_medicine
  - form{"name": null}
  - slot{"new_medicine_name": null}
  - slot{"new_medicine_time": null}
  - slot{"new_medicine_meal": null}

## delete medicine
* remove_medicine{"remove_medicine_uuid": "uuid"}
  - custom_remove_medicine
  - slot{"medicine_list": []}
  - custom_medicine_reminder_update

## list medicine (empty) affirmative
* medicine_list
  - slot{"medicine_list": null}
  - line_ask_add_new_medicine
* affirmative
  - custom_form_add_medicine
  - form{"name": "custom_form_add_medicine"}

## list medicine (empty) negative
* medicine_list
  - slot{"medicine_list": null}
  - line_ask_add_new_medicine
* negative

## list medicine
* medicine_list
  - slot{"medicine_list": [{"name": "ยาความดัน"}]}
  - custom_flex_medicine_list

## test reminder
* test_reminder
  - custom_test_reminder_setup
  - reminder{"action": "custom_medicine_reminder_push", "date_time": "2019-01-02 11:59:29"}

## reminder push (affirmative)
  - custom_medicine_reminder_push
* affirmative
  - line_medicine_reminder_affirmative

## reminder push (negative)
  - custom_medicine_reminder_push
* negative
  - line_medicine_reminder_negative

## doctor records
* doctor_records
  - custom_flex_doctor_records

## greeting help
* greeting
  - line_greeting_help

## greeting help (negative)
* greeting
  - line_greeting_help
* negative
  - line_greeting_help_negative

## howto
* howto
  - line_howto

## sleep
* sleep
  - line_sleep

## lazy
* lazy
  - line_lazy

## hungry
* hungry
  - line_eat_food

## tired
* tired
  - line_cheer_up
