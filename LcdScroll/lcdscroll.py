# -*- coding: utf-8 -*-
"""LcdScroll module -- A wrapper for Adafruit_CharLCD that deals with HD44780's line scrolling problems.

The HD44780 compatible LCD is wonderful except that the lines do not 'roll over' to the next line.

The 16 x 2 waits until the 40 character line buffer is full the it rolls the 41st character on to the second line.

The 20 x 4 display the full 40 characters but uses line three as the over flow for line one, and line four for line two.

Examples:

16 x 2:

+--------+----------------+------------------------+
| Line # | Display Area   | Over flow buffer       |
+========+================+========================+
|Line 1: |aaaaaaaaaaaaaaaa|aaaaaaaaaaaaaaaaaaaaaaaa|
+--------+----------------+------------------------+
|Line 2: |aaaaaaaaaaaaaaaa|aaaaaaaaaaaaaaaaaaaaaaaa|
+--------+----------------+------------------------+


20 x 4:

+--------+--------------------+
| Line # | Display Area       |
+========+====================+
|Line 1: |AAAAAAAAAAAAAAAAAAAA|
+--------+--------------------+
|Line 2: |BBBBBBBBBBBBBBBBBBBB|
+--------+--------------------+
|Line 3: |AAAAAAAAAAAAAAAAAAAA|
+--------+--------------------+
|Line 4: |BBBBBBBBBBBBBBBBBBBB|
+--------+--------------------+

Depending on the font used to display these tables, the lines may not be equal. Don't worry they are.

:program: LcdScroll
:file: lcdscroll
:platform: Cross-Platform, Primarily Raspberry Pi.
:synopsis: This module extends the Adafruit_CharLCD class, adds interfaces to automatically scroll from line to line.

.. moduleauthor:: James L. Key <james@bluepenguinslutions.com>

"""

import Adafruit_CharLCD  # pylint: disable=F0401


LCDSCROLL_DOWN = 0
LCDSCROLL_UP = 1


class LcdScroller:
    # pylint: disable=R0902
    r"""
    Parsing Control for Adafruit_CharLCD in CERMMorse

    This class implements a set of methods to scroll messages upward on a LCD display.
    The limits are adjustable to different lengths and rows depending on hardware, It parses
    the message into words and check if there is enough space left on the screen and if not
    pushes the display up then prints the word.
    Also a method to move the cursor from letter to letter like follow the bouncing ball
    in a sing along.

    .. todo:: remove this fake assignment of Lcd.Adafruit...

    Args:

        cols: (int, optional): Number of columns on display
        lines: (int, optional): Number of line on display
        cursor: (bool, optional): True or False, enable bouncing ball style cursor
        direction:


    """

    def __init__(self, cols: int=16, lines: int=2, direction: int=LCDSCROLL_DOWN, cursor: bool=False):
        """

        Args:
            cols:
            lines:
            direction:
            cursor:
        """
        self._display_size = [cols, lines]
        #: Internal Message to send
        self._message_text = ''
        #: Internal dictionary of special characters
        self._special_characters = {' ': None}
        if not isinstance(self.special_characters, dict):
            raise LcdScrollEx('special_characters need to be a dictionary object')
        self._screen_buffer = []
        for line in range(0, lines - 1):
            self._screen_buffer.append('')
        self._line_buffer = ''
        self._word_buffer = ''
        self._remaining_line_buffer, _ = self.display_size
        #: Internal "bouncing ball" cursor switch
        self._cursor_enabled = cursor
        #: current position of cursor
        self._cursor_position = [0, 0]
        self.direction = direction
        self._word = ''

    @property
    def message_text(self) -> str:
        return self._message_text

    @message_text.setter
    def message_text(self, message_text: str):
        r"""
        Property: Message buffer to be processed and sent

        :getter: Get LcdScroll.message property
        :setter (String): Set LcdScroll.message property

        Examples::

        my_message = LcdScroll.message()

        LcdScroll.message_text('This is a message')

        """
        self._message_text = message_text

    @property
    def special_characters(self) -> dict:
        return self._special_characters

    @special_characters.setter
    def special_characters(self, special_characters: dict):
        r"""
        Property: List of special characters that need special handling

        :getter: Get LcdScroll.special_characters property
        :setter (Dictionary): Set LcdScroll.special_characters property

        Example::

            spec_char = LcdScroll.special_characters()

            LcdScroll.special_characters({'\u00B': '\x00', }


        Returns:

        """
        self._special_characters = special_characters

    @property
    def display_size(self) -> tuple:

        return self._display_size[0], self._display_size[1]

    @property
    def columns(self) -> int:
        return self._display_size[0]

    @columns.setter
    def columns(self, columns: int = 16):
        r"""
        Sets number of columns for display size

        Args:
            columns (int): Number of lines in display

        """
        if columns <= 0:
            raise LcdScrollEx('Error display_size must be positive integers greater than zero')
        self._display_size[0] = columns

    @property
    def lines(self) -> int:
        return self._display_size[1]

    @lines.setter
    def lines(self, lines: int = 1):
        r"""
        Sets number of lines for display size

        Args:
            lines (int): Number of lines in display

        """
        if lines <= 0:
            raise LcdScrollEx('Error display_size must be positive integers greater than zero')
        for line in range(0, lines - 1):
            self._screen_buffer.append('')
        self._display_size[1] = lines

    @property
    def display_cursor(self) -> bool:
        return self._cursor_enabled

    @display_cursor.setter
    def display_cursor(self, enabled: bool = True):
        r"""
        Property: Set to enable of disable "Bouncing Ball" cursor during display

        :getter: Get ScrollLCD.display_cursor property
        :setter (Bool): Set the ScrollLcd.display_size property

        Returns:
           Bool: Option state

        Examples::

            if(LcdScroll.display_cursor()):
                do_something()

            LcdScroll.display_cursor(True)

        """
        if not(enabled | (not enabled)):
            raise LcdScrollEx('Error display_size must be positive integers greater than zero')
        self._cursor_enabled = enabled

    def trigger_cursor(self, position: tuple=(None, None)):
        """
        Trigger the cursor movement or set to custom location.
        Second line.

        Args:
             position:

        """
        local_position = list(position)
        if (local_position[0] is None) and (local_position[1] is None):
            local_position[0] = self._cursor_position[0]
            local_position[1] = self._cursor_position[1]

        if ((local_position[0] < 0) | (local_position[0] >= self._display_size[0]) | (local_position[1] < 0) |
                (local_position[1] >= self._display_size[1])):
            raise LcdScrollEx('Error cursor position is not within the display area')

        if position[0] == 0:
            self._cursor_position = local_position
        else:
            self._cursor_position[0] += 1

        if self._cursor_position[0] == self.display_size[0]:
            self._cursor_position[0] = 0
        self.set_cursor(self._cursor_position[0], self._cursor_position[1])

    def send_character(self, char: str, position: tuple=(None, None)):
        """
        Sends one character to the display. Primarily used by bouncing ball option.
        To be overridden by derived classes to add functionality.

        Args:
            char:
            position:


        """
        if len(char) > 1:
            raise LcdScrollEx('More than one character sent to send_character()')
        local_position = list(position)
        if (local_position[0] is None) and (local_position[1] is None):
            self.message(char)
        else:
            self.set_cursor(local_position[0], local_position[1])
            self.message(char)

    def send_word(self, word: str):
        """
        Sends one word to the display.
        To be overridden by derived classes to add functionality.

        Args:
            word:


        """
        self.message(word)

    def _scroll(self):
        screen_buffer = []

        def scroll_down():
            nonlocal screen_buffer
            for line in range(0, self.lines - 2):
                screen_buffer[line] = self._screen_buffer[line + 1]

        def scroll_up():
            nonlocal screen_buffer
            for line in range(1, self.lines - 1):
                screen_buffer[line - 1] = self._screen_buffer[line]

        if self.lines > 0:
            if LCDSCROLL_DOWN:
                scroll_down()
            else:
                scroll_up()
            for row in range(0, self.lines - 1):
                self.set_cursor(0, row)
                self.message(self._screen_buffer[row])
            self._screen_buffer = screen_buffer

    def _send_message_with_cursor(self):
        while True:

            # iterate number of letters?
            # cursor 0 - col-1
            # calc word length
            self.send_word(self._word)  # display word
            # set cursor pos to current - word length
            # make cursor visible?
            # iterate letters of word
            # play char
            # move cursor
            # if iteration var = word length: break | or try: except:?

    def _send_message_without_cursor(self, string):
        string_buffer = list(string)
        while len(string_buffer) > 0:
            # while there are letters
            # display letter
            self.send_character(string_buffer.pop(0))

    def _set_init_cursor_pos(self):
        if len(str(self._line_buffer)) is 0:  # Move cursor to Bottom line
            if LCDSCROLL_DOWN:
                self.set_cursor(0, 0)
            else:  # LCDSCROLL_UP
                self.set_cursor(0, self.lines - 1)

    def send_message(self):
        """
        Method to initiate sending

        .. todo:: Not end of string in message?

        """
        # set initial state
        columns, rows = self.display_size
        self.clear()
        self.show_cursor(False)
        self._line_buffer = 0
        self._cursor_position = 0
        for line in range(0, self.lines - 1):
            self._screen_buffer[line] = ''

        # break into words
        local_message_temp = self.message_text
        local_message = []
        while len(local_message_temp) > 0:
            word_buffer = local_message_temp.partition(" ")
            local_message.append(word_buffer[0])
            local_message[-1] += word_buffer[1]
            local_message_temp = word_buffer[2]


        while True:
            try:
                self._set_init_cursor_pos()
                for word in local_message:  # feed one at a time to display
                    # calculate if there is room on the line if not move text up
                    if len(word) > self._remaining_line_buffer:
                        self.clear()
                        self._scroll()
                        self._remaining_line_buffer = columns

                    if self.display_cursor:
                        self._send_message_with_cursor()
                        self._remaining_line_buffer -= len(word)
                    else:
                        self._send_message_without_cursor(word)
                        self._remaining_line_buffer -= len(word)
                return
            except IndexError:
                break


class LcdScroll_CharLCD(Adafruit_CharLCD.Adafruit_CharLCD, LcdScroller):
    r"""

    """
    def __init__(self, cols: int, lines: int, cursor: bool=False, direction: int=LCDSCROLL_DOWN, *args, **kwargs):
        r"""

        Args:
            rs:
            en:
            d4:
            d5:
            d6:
            d7:
            cols:
            lines:
            backlight:
            invert_polarity:
            enable_pwm:
            gpio:
            pwm:
            initial_backlight:
            cursor:
        """
        super().__init__(self, *args, **kwargs)
        LcdScroller.__init__(self, cols=cols, lines=lines, direction=direction, cursor=cursor)


class LcdScroll_CharLCDPlate(Adafruit_CharLCD.Adafruit_CharLCDPlate, LcdScroller):
    r"""

    """
    def __init__(self, cols: int =16, lines: int=2, cursor: bool=False, direction: int=LCDSCROLL_DOWN, *args, **kwargs):
        r"""

        Args:
            address:
            busnum:
            cols:
            lines:
            cursor:
        """

        super().__init__(*args, **kwargs)

        LcdScroller.__init__(self, cols=cols, lines=lines, direction=direction, cursor=cursor)


class LcdScroll_RGBCharLCD(Adafruit_CharLCD.Adafruit_RGBCharLCD, LcdScroller):
    r"""

    """
    def __init__(self, cols: int, lines: int, cursor: bool=False, direction: int=LCDSCROLL_DOWN, *args, **kwargs):
        r"""

        Args:
            rs:
            en:
            d4:
            d5:
            d6:
            d7:
            cols:
            lines:
            red:
            green:
            blue:
            gpio:
            invert_polarity:
            enable_pwm:
            pwm:
            initial_color:
            cursor:
        """

        super().__init__(*args, **kwargs)

        LcdScroller.__init__(self, cols=cols, lines=lines, direction=direction, cursor=cursor)


class LcdScrollEx(Exception):
    """
    Internal Exception for Scroll Class
    """
    def __init__(self, message):
        r"""

        Args:
            message:
        """
        Exception.__init__(self)
        self.message = message
