#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
# # Use GPIO numbers not pin numbers
#
chiffer_start = 9
chiffer_pins = [17,18,27,22,23,24,25,4,8,7]
GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.OUT)
GPIO.output(9, GPIO.LOW)
for pin in chiffer_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

pins_left = [17,18,27]
pins_right = [22,23,24]
pins_up = [17,25,22]
pins_down = [27,4,24]
pins_type1 = [8]
pins_type2 = [7]

pins_locations = [pins_left, pins_right, pins_up, pins_down, pins_type1, pins_type2]


from time import sleep

default_key = "abcdefghi jklmnoprs tuvxyzåäö"


#   0   1   2
#   #   #   #
#                  0               1                2
#   _|_|_       0  1  2        9  10  11       18  19  20
#   _|_|_       3  4  5       12  13  14       21  22  23
#    | |        6  7  8       15  16  17       24  25  26

# nr    1   2   3   4   5   6   7   8   9
# Left  0   1   1   0   1   1   0   1   1
# Right 1   1   0   1   1   0   1   1   0
# Up    0   0   0   1   1   1   1   1   1
# Down  1   1   1   1   1   1   0   0   0
# Type

# # Numbered Square
# for i in range(27):
#     print(i, end="\t")
print()
# # # Left
# # for i in range(27):
# #     print(min(i%3,1), end="\t")
# # print()
# # # Right
# # for i in range(27):
# #     print(min((i+1)%3,1), end="\t")
# # print()
# # # Up
# # for i in range(27):
# #     print(min(max((i%9)-2,0),1), end="\t")
# # print()
# # # Down
# # for i in range(27):
# #     print(min(max(((i+3)%9)-2,0),1), end="\t")
# # print()
# # # Type of pagode 1
# for i in range(27):
#     print(min(max(int(i/9),0),1), end="\t")
# print()
# for i in range(27):
#     print(min(max(int(i/9)-1,0),1), end="\t")
# print()
def create_locations():
    locations = []
    for i in range(27):
        location = []

        location.append(i)                          # Numbered Square
        location.append(min(i%3,1))                 # Left
        location.append(min((i+1)%3,1))             # Right
        location.append(min(max((i%9)-2,0),1))      # Up
        location.append(min(max(((i+3)%9)-2,0),1))  # Down
        location.append(min(max(int(i/9),0),1))    # Type of pagode 1:st lamp
        location.append(min(max(int(i/9)-1,0),1))  # Type of pagode 2:nd lamp

        locations.append(location)
    return locations

def key_OK(text,key):
    sections = key.split()
    if len(key) != 27+2: #27 letters + 2 spaces (check default key)
        return False
    if len(sections)!=3:
        return False
    for section in sections:
        if len(section) != 9:
            return False
    for letter in text:
        if letter not in key: # space caught by the spaces in the key format
            return False
    return True

def create_key(key):
    locations = create_locations()
    symbols = {" ": " "}

    key_index = 0
    for display in locations:
        if key[key_index] == " ": key_index += 1
        symbols[key[key_index]] = display
        key_index += 1
    return symbols


def text_to_chiffer(text,key=None):
    if not (isinstance(text, str) or isinstance(key, str) or key == None): TypeError("Must be string or None")
    if key == None or key == "": key = default_key
    text = text.upper()
    key = key.upper()
    if not key_OK(text,key): raise ValueError("Key must have format: "+ "abcde fghij klmno prstu vyåäö")

    symbols = create_key(key)
    chiffer = []
    for letter in text:
        chiffer.append(symbols[letter])
    return chiffer

# ==========================================================

def flash(on, port):
    # if not isinstance(on, bool): TypeError("Must be boolean")
    # if not isinstance(port, int): TypeError("Must be integer")
    if on:
        GPIO.output(port, GPIO.HIGH)
        # print("ON!", end="-----------")
    else:
        GPIO.output(port, GPIO.LOW)
        # print("off!")

def flash_on(port):
    # if not isinstance(port, int): TypeError("Must be integer")
    flash(True, port)
def flash_on_multiple(ports):
    # if not isinstance(port, int): TypeError("Must be integer")
    for pin in ports:
        flash(True, pin)
def flash_off(port):
    # if not isinstance(port, int): TypeError("Must be integer")
    flash(False, port)
def flash_off_all():
    # if not isinstance(port, int): TypeError("Must be integer")
    for pin in chiffer_pins:
        flash(False, pin)

# Controls the flashes of light
def send_signal(start,chiffer=None):
    # if not isinstance(start, str): TypeError("Must be string")
    # if not isinstance(morse_letter, str): TypeError("Must be string")
    unit = 0.5
    if not start:

        for sign in chiffer:
            if isinstance(sign, str) and sign == " ":
                sleep(3 * unit)
            else:
                for i in range(1,len(sign)):
                    if bool(sign[i]): flash_on(pins_locations[i-1])
            sleep(4*unit)
            flash_off_all()
            # sleep(1 * unit)

    else:
        for i in range(10):
            flash_on(chiffer_start)
            sleep(0.1)
            flash_off(chiffer_start)
            sleep(0.1)


# ==========================================================




def translator_loop(text, key=None):
    # if not isinstance(key, str): TypeError("Must be string")
    text = text.upper()
    chiffer = text_to_chiffer(text,key)

    while True:
        send_signal(True)
        # for signal in morse:
        send_signal(False, chiffer)

def go(text, key=None):
    translator_loop(text, key)


if __name__ == '__main__':
    go("Hej alla")
    # text = input("Give text to translate to brädgårdschiffer:\n")
    # custom_key = input("Give key (optional) on format:"+default_key+"\n")

    # go(text,custom_key)