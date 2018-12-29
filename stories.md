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

## add medicine
* add_medicine
  - line_ask_medicine_name
* enter_medicine_name
  - line_add_medicine_success