#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import RPi.GPIO as GPIO
# Use GPIO numbers not pin numbers
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(4, GPIO.OUT)
# GPIO.setup(17, GPIO.OUT)
import morse

default_key = "abcde fghij klmno prstu vyåäö"


def key_OK(text,key):
        sections = key.split()
        if len(key) != 25+4: #25 letters + 4 spaces (check default key)
            return False
        if len(sections)!=5:
            return False
        for section in sections:
            if len(section) != 5:
                return False
        for letter in text:
            if letter not in key: # space caught by the spaces in the key format
                return False
        return True
def create_key(key):
    key_symbols = ['s','c','o','u','t']
    key_symbols_upper = [x.upper() for x in key_symbols]
    symbols = {" ": " "}
    key_index = 0
    for rad in key_symbols:
        for kol in key_symbols_upper:
            if key[key_index] == " ": key_index += 1
            symbols[key[key_index]] = kol + rad
            key_index += 1
    return symbols

def text_to_chiffer(text,key=None):
    if not (isinstance(text, str) or isinstance(key, str) or key == None): TypeError("Must be string or None")
    if key == None or key == "": key = default_key
    text = text.upper()
    key = key.upper()
    if not key_OK(text,key): raise ValueError("Key must have format: "+ "abcde fghij klmno prstu vyåäö")

    symbols = create_key(key)
    chiffer = ""
    for letter in text:
        chiffer += symbols[letter]
    return chiffer



def translator_loop(text, key=None):
    # if not isinstance(key, str): TypeError("Must be string")
    text = text.upper()
    chiffer = text_to_chiffer(text,key)
    morse.translator_loop(chiffer)

def go(text, key=None):
    translator_loop(text, key)


if __name__ == '__main__':
    text = input("Give text to translate to scoutchiffer, then to morse:\n")
    custom_key = input("Give key (optional) on format:"+default_key+"\n")

    go(text,custom_key)