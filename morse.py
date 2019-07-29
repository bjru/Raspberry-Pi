#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
# Use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

from time import sleep
symbols = {' ':'/','A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', 'Å':'.--.-', 'Ä':'.-.-', 'Ö':'---.', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----',
           ',':'--..--', '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', '(':'-.--.', ')':'-.--.-',
           '!':'-.-.--'}
morse_port = 17
morse_start = 4
# Returns "Hey all ." as: ".... . -.--/ .- .-.. .-../ .-.-.-"
# So letters spacing: " "
# Word spacing: " / "
def text_to_morse(text):
    if not isinstance(text, str): TypeError("Must be string")

    text = text.upper()
    morse = symbols[text[0]]
    for letter in text[1:]:
        if letter == " ":
            morse += symbols[letter]
        else:
            morse += " "+symbols[letter]

    return morse

def flash(on, port):
    if not isinstance(on, bool): TypeError("Must be boolean")
    if not isinstance(port, int): TypeError("Must be integer")
    if on:
        # GPIO.output(port, GPIO.HIGH)
        print("ON!", end="-----------")
    else:
        # GPIO.output(port, GPIO.LOW)
        print("off!")

def flash_on(port):
    if not isinstance(port, int): TypeError("Must be integer")
    flash(True, port)
def flash_off(port):
    if not isinstance(port, int): TypeError("Must be integer")
    flash(False, port)

# Controls the flashes of light
def send_signal(light,morse_letter=None):
    if not isinstance(light, str): TypeError("Must be string")
    if not isinstance(morse_letter, str): TypeError("Must be string")
    unit = 0.5
    if light == "signal":

        for signal in morse_letter:
            if signal == ".":
                flash_on(morse_port)
                sleep(unit)
                flash_off(morse_port)
            elif signal == "-":
                flash_on(morse_port)
                sleep(unit*3)
                flash_off(morse_port)
            elif signal == " " or signal == "/": #New words get 8 instead of 7 units
                flash_off(morse_port)
                sleep(unit*3)
            sleep(unit)

    elif light == "start":
        print("start End")
        for i in range(10):
            flash_on(morse_start)
            sleep(0.1)
            flash_off(morse_start)
        print("start End")

def translator(text):
    text = text.upper()
    morse = text_to_morse(text)


    send_signal("start")
    for signal in morse:
        send_signal("signal", signal)

def translator_loop(text):
    text = text.upper()
    morse = text_to_morse(text)

    while True:
        send_signal("start")
        for signal in morse:
            send_signal("signal", signal)


def go(text):
    translator_loop(text)
if __name__ == '__main__':
    texten = "Hej alla scouter!"
    go(texten)
