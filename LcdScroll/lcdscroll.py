# -*- coding: utf-8 -*-
"""
Comments go here!!!

:program: LcdScroll
:file: lcdscroll
:platform: Cross-Platform
:synopsis: Change this text.

.. moduleauthor:: James L. Key <james@bluepenguinslutions.com>

"""


import os

import lcdscroller

if os.name == 'nt':
    from Waxfruit_CharLCD import Adafruit_CharLCDPlate
    import Waxfruit_CharLCD as Adafruit_CharLCD
else:
    import Adafruit_CharLCD  # pylint: disable=F0401
    from Adafruit_CharLCD import Adafruit_CharLCDPlate  # pylint: disable=F0401


class LcdScroll_CharLCD(Adafruit_CharLCD.Adafruit_CharLCD, lcdscroller.LCDScroller):
    def __init__(self, rs: int, en: int, d4:int, d5: int, d6: int, d7: int, cols: int, lines: int,
                 backlight: int=None, invert_polarity: bool=True, enable_pwm: bool=False, gpio='', pwm='',
                 initial_backlight: float=1.0, cursor: bool=False):
        Adafruit_CharLCD.Adafruit_CharLCD.__init__(self, rs=rs, en=en, d4=d4, d5=d5, d6=d6, d7=d7,
                                                   cols=cols, lines=lines, backlight=backlight,
                                                   invert_polarity=invert_polarity, enable_pwm=enable_pwm, gpio=gpio,
                                                   pwm=pwm, initial_backlight=initial_backlight)
        lcdscroller.LCDScroller.__init__(self, cols=cols, lines=lines, cursor=cursor)


class LcdScroll_CharLCDPlate(Adafruit_CharLCD.Adafruit_CharLCDPlate, lcdscroller.LCDScroller):
    def __init__(self, address: hex=0x20, busnum='', cols: int =16, lines: int=2, cursor: bool=False):

        Adafruit_CharLCD.Adafruit_CharLCDPlate.__init__(self, address=address, busnum=busnum, cols=cols, lines=lines)

        lcdscroller.LCDScroller.__init__(self, cols=cols, lines=lines, cursor=cursor)


class LcdScroll_RGBCharLCD(Adafruit_CharLCD.Adafruit_RGBCharLCD, lcdscroller.LCDScroller):
    def __init__(self, rs: int, en: int, d4: int, d5: int, d6: int, d7: int, cols: int, lines: int,
                 red: int, green: int, blue: int, gpio='', invert_polarity: bool=True,
                 enable_pwm: bool=False, pwm='', initial_color: tuple=(1.0, 1.0, 1.0), cursor: bool=False):

        Adafruit_CharLCD.Adafruit_RGBCharLCD.__init__(self, rs=rs, en=en, d4=d4, d5=d5, d6=d6, d7=d7, cols=cols,
                                                      lines=lines, red=red, green=green, blue=blue, gpio=gpio,
                                                      invert_polarity=invert_polarity, enable_pwm=enable_pwm,
                                                      pwm=pwm, initial_color=initial_color)

        lcdscroller.LCDScroller.__init__(self, cols=cols, lines=lines, cursor=cursor)


class LcdScrollEx(Exception):
    """
    Internal Exception for Scroll Class
    """
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
