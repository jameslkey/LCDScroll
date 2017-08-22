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
from LcdScroll import LcdScroll_CharLCDPlate
from unittest import skip
from LcdScroll import LcdScrollEx
import pytest
import time


class TestLcdScroll(TestCase):
    def setUp(self):
        self.columns = 20
        self.lines = 4
        self.display = LcdScroll_CharLCDPlate(cols=self.columns, lines=self.lines)
        self.display.clear()
        self.display.set_backlight(0)

    def test_message_set(self):
        r"""
        Simple test of message set method

        """
        self.display.message = 'Test message that should be longer than 16 characters'
        self.assertIsInstance(self.display.message, str)

    def test_message(self):
        r"""
        Simple test of message get method

        """
        self.display.message = 'Test message that should be longer than 16 characters'
        self.assertIsInstance(self.display.message, str)

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
        self.display.columns = 20
        self.display.lines = 4
        self.assertIsInstance(self.display.display_size, tuple, 'display_size() Did not return tuple')
        self.assertEqual(self.display.display_size, (20, 4), 'Unable to set display size')
        self.display.columns = 16
        self.display.lines = 2
        self.assertEqual(self.display.display_size, (16, 2), 'Unable to change display size')

        def set_col():
            self.display.columns = 0

        def set_line():
            self.display.lines = -3

        self.assertRaises(LcdScrollEx, set_col)
        self.assertRaises(LcdScrollEx, set_line)

    def test_display_size(self):
        r"""
        Simple test of display_size get method

        """
        self.assertIsInstance(self.display.display_size, tuple, 'display_size() Did not return tuple')

    def test_display_cursor_set(self):
        r"""
        Simple test of display_size set method

        """
        self.display.display_cursor = True
        self.assertIsInstance(self.display.display_cursor, bool, 'display_cursor() Did not return bool')
        self.assertEqual(self.display.display_cursor, True, 'Unable to set cursor')
        self.display.display_cursor = False
        self.assertEqual(self.display.display_cursor, False, 'Unable to change cursor')

    def test_display_cursor(self):
        r"""
        Simple test of display_cursor get method

        """
        self.assertIsInstance(self.display.display_cursor, bool, 'display_cursor() Did not return Bool')

    def test_trigger_cursor_set(self):
        self.display.columns = self.columns
        self.display.lines = self.lines
        self.display.set_backlight(1)
        self.display.show_cursor(True)
        self.display.blink(True)
        self.display.trigger_cursor()
        time.sleep(.1)
        self.display.trigger_cursor((4, 1))
        time.sleep(.1)
        with pytest.raises(LcdScrollEx):
            self.display.trigger_cursor((22, 5))
        with pytest.raises(LcdScrollEx):
            self.display.trigger_cursor((-12, 32))
        self.display.trigger_cursor((0, 0))
        cols = self.display.display_size[0]
        for x in range(0, cols):
            self.display.message(chr(ord('A') + x))
        for x in range(0, cols):
            self.display.trigger_cursor()
            time.sleep(.5)

        self.display.set_backlight(0)
        self.display.blink(False)
        self.display.show_cursor(False)

    def test_send_character(self):
        r"""
        Stupid Test

        """
        self.display.send_character('a')
        self.display.send_character('b')
        with pytest.raises(LcdScrollEx):
            self.display.send_character('asdasdasd')

    @skip
    def test_send_word(self):
        self.fail()

    @skip
    def test_send_message(self):
        self.fail()

