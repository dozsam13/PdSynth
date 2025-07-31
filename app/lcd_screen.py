#Try RPLCD Liberary
# from RPLCD-master import *
# from RPLCD import RPLCD
from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD, BaseCharLCD


class LCDScreen:
  def __init__(self):
    self.screen = CharLCD('PCF8574', 0x27)

  def write_lines(self, lines):
    for i, line in enumerate(lines):
      self.screen.cursor_pos = (i, 0)
      self.screen.write_string(line[:20])

  def write_param_value(self, row, column, value):
    self.screen.cursor_pos = (row*2, column*4)
    self.screen.write_string(value)

  def cleanup(self):
    self.screen.clear()
    return
