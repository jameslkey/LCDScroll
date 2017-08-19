# -*- coding: utf-8 -*-
"""
Comments go here!!!

:program: CERMMorse2.0
:file: test_lcdScroll
:platform: Cross-Platform
:synopsis: Change this text.

.. moduleauthor:: James L. Key <james@bluepenguinslutions.com>

"""
from unittest import TestCase
from LcdScroll import LcdScroll
from unittest import skip
from LcdScroll import LcdScrollEx
import pytest
import time

import os
if os.name == 'nt':
    from Waxfruit_CharLCD import Adafruit_CharLCDPlate
else:
    from Adafruit_CharLCD import Adafruit_CharLCDPlate  # pylint: disable=F0401


class TestLcdScroll(TestCase):
    def setUp(self):
        self.columns = 20
        self.lines = 4
        self.display = Adafruit_CharLCDPlate(cols=self.columns, lines=self.lines)
        self.display.clear()
        self.display.set_backlight(0)
        self.lcd = LcdScroll(self.display)

    def test_message_set(self):
        """
        Simple test of message set method

        """
        self.lcd.message = 'Test message that should be longer than 16 characters'
        self.assertIsInstance(self.lcd.message, str)

    def test_message(self):
        """
        Simple test of message get method

        """
        self.lcd.message = 'Test message that should be longer than 16 characters'
        self.assertIsInstance(self.lcd.message, str)

    @skip
    def test_special_characters_set(self):
        self.fail()

    @skip
    def test_special_characters(self):
        self.fail()

    def test_display_size_set(self):
        r"""
        Simple test of display_size set method

        """
        self.lcd.columns = 20
        self.lcd.lines = 4
        self.assertIsInstance(self.lcd.display_size, tuple, 'display_size() Did not return tuple')
        self.assertEqual(self.lcd.display_size, (20, 4), 'Unable to set display size')
        self.lcd.columns = 16
        self.lcd.lines = 2
        self.assertEqual(self.lcd.display_size, (16, 2), 'Unable to change display size')

        def set_col():
            self.lcd.columns = 0

        def set_line():
            self.lcd.lines = -3

        self.assertRaises(LcdScrollEx, set_col)
        self.assertRaises(LcdScrollEx, set_line)

    def test_display_size(self):
        r"""
        Simple test of display_size get method

        """
        self.assertIsInstance(self.lcd.display_size, tuple, 'display_size() Did not return tuple')

    def test_display_cursor_set(self):
        r"""
        Simple test of display_size set method

        """
        self.lcd.display_cursor = True
        self.assertIsInstance(self.lcd.display_cursor, bool, 'display_cursor() Did not return bool')
        self.assertEqual(self.lcd.display_cursor, True, 'Unable to set cursor')
        self.lcd.display_cursor = False
        self.assertEqual(self.lcd.display_cursor, False, 'Unable to change cursor')

    def test_display_cursor(self):
        r"""
        Simple test of display_cursor get method

        """
        self.assertIsInstance(self.lcd.display_cursor, bool, 'display_cursor() Did not return Bool')

    def test_trigger_cursor_set(self):
        self.lcd.columns = self.columns
        self.lcd.lines = self.lines
        self.display.set_backlight(1)
        self.display.show_cursor(True)
        self.display.blink(True)
        self.lcd.trigger_cursor()
        time.sleep(.1)
        self.lcd.trigger_cursor((4, 1))
        time.sleep(.1)
        with pytest.raises(LcdScrollEx):
            self.lcd.trigger_cursor((22, 5))
        with pytest.raises(LcdScrollEx):
            self.lcd.trigger_cursor((-12, 32))
        self.lcd.trigger_cursor((0, 0))
        cols = self.lcd.display_size[0]
        for x in range(0, cols):
            self.display.message(chr(ord('A') + x))
        for x in range(0, cols):
            self.lcd.trigger_cursor()
            time.sleep(.5)

        self.display.set_backlight(0)
        self.display.blink(False)
        self.display.show_cursor(False)

    def test_send_character(self):
        r"""
        Stupid Test

        """
        self.lcd.send_character('a')
        self.lcd.send_character('b')
        with pytest.raises(LcdScrollEx):
            self.lcd.send_character('asdasdasd')


    @skip
    def test_send_word(self):
        self.fail()

    @skip
    def test_send_message(self):
        self.fail()

