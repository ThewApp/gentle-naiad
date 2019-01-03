## happy path
* greet
  - line_greet
* mood_great
  - line_happy

## sad path 1
* greet
  - line_greet
* mood_unhappy
  - line_cheer_up
  - line_did_that_help
* mood_affirm
  - line_happy

## sad path 2
* greet
  - line_greet
* mood_unhappy
  - line_cheer_up
  - line_did_that_help
* mood_deny
  - line_goodbye

## say goodbye
* goodbye
  - line_goodbye

## follow
* follow_event
  - line_follow

## unfollow
* unfollow_event
  - action_restart

## add medicine
* add_medicine
  - custom_form_add_medicine
  - form{"name": "custom_form_add_medicine"}
  - form{"name": null}
  - slot{"medicine_list": [{"name": "ยาความดัน", "time": "สามเวลา", "meal": "หลังอาหาร"}]}
  - slot{"new_medicine_name": null}
  - slot{"new_medicine_time": null}
  - slot{"new_medicine_meal": null}

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
* remove_medicine{"remove_medicine_index": 0}
  - custom_remove_medicine
  - slot{"medicine_list": []}

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

## test reminder push
  - custom_medicine_reminder_push
* affirmative
  - line_medicine_reminder_affirmative

## test reminder push
  - custom_medicine_reminder_push
* negative
  - line_medicine_reminder_negative
