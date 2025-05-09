from math import *
from ion import *
from colors import *
from time import sleep

from kandinsky import *
EMULATED = False
try: import os; EMULATED = True; print("Emulated")
except: pass


SPACEMENT_X = 2
SPACEMENT_Y = 4
OUTLINE_SIZE = 1
CHAR_HEIGHT = 18
MOVES = {
  KEY_UP: (0, -1),
  KEY_DOWN: (0, 1),
  KEY_RIGHT: (1, 0),
  KEY_LEFT: (-1, 0)
}

UNHOVERABLE_COLOR = grey

background = white_blue
default_color = light_brown
default_overlay = dark_brown
default_enabled_color = dark_blue
default_hover_overlay = white
layout: list[list["CanvasItem"]] = []
# focused_text_box = None

class Vector2():
  def __init__(self, x: int = 0, y: int = 0):
    assert type(x) == int
    assert type(y) == int
    self.x: int = x
    self.y: int = y

  def duplicate(self) -> "Vector2":
    return Vector2(self.x, self.y)

  def __getitem__(self, idx):
    if idx == 0:
      return self.x
    elif idx == 1:
      return self.y

    return IndexError

  def __add__(self, __o):
    try:
      return Vector2(self.x + __o[0], self.y + __o [1])
    except Exception as error:
      raise error

  def __eq__(self, __o: object) -> bool:
    return self.x == __o[0] and self.y == __o[1]

  def __str__(self) -> str:
    return "<" + str(self.x) + ", " + str(self.y) + ">"


def txt_size(string: str) -> Vector2:
  return Vector2(len(string)*10, CHAR_HEIGHT)
def txt_overlay(string: str) -> Vector2:
  return txt_size(string) + (2, 2)


def wait_released(key) -> None:
  while keydown(key):
    sleep(0.05)

class CanvasItem():
  def __init__(self, position: Vector2 = Vector2(10, 10), color = None, overlay = None, callback = lambda: None) -> None:
    self.position = position
    self.color = color
    self.overlay = overlay
    self.callback = callback
  
  def draw(self, pos: Vector2 = None) -> None:
    """Virtual"""
    raise NotImplementedError("draw() is not implemented on " + repr(self))
  
  def get_size(self) -> Vector2:
    """Virtual"""
    raise NotImplementedError("get_size() is not implemented on " + repr(self))
  
  def get_color(self):
    return self.color or default_color
  def get_overlay(self):
    return self.overlay or default_overlay
  
  def handle_input(self) -> None:
    """Virtual"""
    raise NotImplementedError("handle_input() is not implemented on " + repr(self))


class Hoverable(CanvasItem):
  def __init__(self, overlay = None, hovered: bool = False, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.hovered: bool = hovered
  
  def get_overlay(self):
    return default_hover_overlay if self.hovered else super().get_overlay()


class Label(Hoverable):
  def __init__(self, txt: str = "Lorem Ipsum", *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.txt: str = txt
    # self.hovered: bool = hovered

  def get_size(self) -> Vector2:
    return txt_size(self.txt)

  def draw(self, pos: Vector2 = None):
    pos = pos or self.position
    size = txt_overlay(self.txt)
    fill_rect(pos.x-1, pos.y-1, size.x, size.y, UNHOVERABLE_COLOR if self.hovered else self.get_overlay())
    draw_string(self.txt,pos.x,pos.y, UNHOVERABLE_COLOR if self.hovered else self.get_overlay(), self.get_color())


class Button(Label):
  def __init__(self, *args, enabled: bool = False, **kwargs):
    super().__init__(*args, **kwargs)
    self.enabled: bool = enabled
    # self.hovered: bool = hovered

  def get_size(self) -> Vector2:
    return txt_size(self.txt)

  def draw(self, pos: Vector2 = None):
    pos = pos or self.position
    size = txt_overlay(self.txt)
    fill_rect(pos.x-1, pos.y-1, size.x, size.y, default_hover_overlay if self.hovered else self.get_overlay())
    draw_string(self.txt,pos.x,pos.y, default_hover_overlay if self.hovered else self.get_overlay(), default_enabled_color if self.enabled else self.get_color())

  def toggle(self):
    self.enabled = not self.enabled


class Focusable(Hoverable):
  def __init__(self, hovered: bool = False, *args, **kwargs) -> None:
    super().__init__(hovered, *args, **kwargs)
    self.focused = False


class TextBox(Focusable):
  def __init__(self, type_hint, *args, **kwargs):
    super().__init__(self, *args, **kwargs)
    # self.focusable = True
    self.type_hint = type_hint

  def handle_input(self):
    pass
    
  def toggle(self):
    super().toggle()
    if self.enabled:
      pass
      # focused_text_box = self
    else:
      pass
      # focused_text_box = None    


class Slider(Focusable):
  SLIDER_HEIGHT: int = 4
  CURSOR_SIZE: int = 8
  
  def __init__(self, min: float, max: float, step: float = 1, initial_value: float = None, size: int = 100, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.focusable = True
    self.focused = False
    self.min: float = min
    self.max: float = max
    self.step: float = step
    self.value: float = round((min + max) / 2 / step) * step if initial_value == None else initial_value
    self.size: int = size
  
  def handle_input(self) -> None:
    old_val = self.value
    if keydown(KEY_LEFT):
      self.value = max(self.value - (self.step * (10 if keydown(KEY_SHIFT) else 1)), self.min)
      wait_released(KEY_LEFT)
    elif keydown(KEY_RIGHT):
      self.value = min(self.value + (self.step * (10 if keydown(KEY_SHIFT) else 1)), self.max)
      wait_released(KEY_RIGHT)
    if old_val != self.value:
      self.callback()
      self.draw()
  
  def get_size(self) -> Vector2:
    return Vector2(self.size, self.SLIDER_HEIGHT)
  
  def get_color(self):
    return default_enabled_color if self.focused else super().get_color()
  
  def draw(self, pos: Vector2 = None) -> None:
    pos = (pos or self.position).duplicate()
    size = self.get_size()
    fill_rect(pos.x-1, pos.y, size.x+1, canvas_items_height(1) + 1, background)
    cursor_pos = pos + Vector2(int((self.value - self.min) / (self.max - self.min) * (size.x - self.CURSOR_SIZE)), int((canvas_items_height(1) - self.CURSOR_SIZE) / 2))
    pos.y += int((canvas_items_height(1) - size.y) / 2)
    fill_rect(pos.x-1, pos.y-1, size.x+2, size.y+2, self.get_overlay())
    fill_rect(pos.x, pos.y, size.x, size.y, self.get_color())
    fill_rect(cursor_pos.x-1, cursor_pos.y-1, self.CURSOR_SIZE+2, self.CURSOR_SIZE+2, self.get_overlay())
    fill_rect(cursor_pos.x, cursor_pos.y, self.CURSOR_SIZE, self.CURSOR_SIZE, self.get_color())
    # draw_string(self.txt,pos.x,pos.y, default_hover_overlay if self.hovered else self.get_overlay(), default_enabled_color if self.enabled else self.get_color())


def canvas_items_width(canvas_items: list[CanvasItem]) -> int:
  result: int = len(canvas_items) * (OUTLINE_SIZE + SPACEMENT_X) - SPACEMENT_X
  for canvas_item in canvas_items:
    result += canvas_item.get_size().x
  return result

def canvas_items_height(canvas_items: int|list) -> int:
  if type(canvas_items) == list:
    canvas_items = len(canvas_items)

  return canvas_items * (CHAR_HEIGHT + OUTLINE_SIZE + SPACEMENT_Y) - SPACEMENT_Y

def layout_get(position: Vector2) -> CanvasItem:
  return layout[position[1]][position[0]]

def clamp(value, minimum, maximum) -> int:
  return max(min(value, maximum), minimum)
def layout_clamp(position: Vector2) -> Vector2:
  y = clamp(position[1], 0, len(layout) - 1)
  x = clamp(position[0], 0, len(layout[y]) - 1)
  return Vector2(x, y)

def example() -> None:
  global layout
  
  slider = Slider(0, 91, 1)
  label = Label("XX")
  def slider_callback():
    label.txt = "{0:2d}".format(slider.value)
    label.draw()
  
  slider.callback = slider_callback
  slider_callback()
  
  layout = [
    [Button("Az"), Button("By"), Button("Cx")],
    [slider, label],
    [Button("Truc"), Button("Machin")]#,
    # [TextBox()]
  ]
  print(start())


def parse_result() -> list[list]:
  result = []
  for row in layout:
    row_result = []
    result.append(row_result)
    for canvas_item in row:
      if isinstance(canvas_item, Button):
        if canvas_item.enabled:
          row_result.append(canvas_item.txt)
      elif isinstance(canvas_item, Slider):
        row_result.append(canvas_item.value)

  return result


def start():
  fill_rect(0, 0, 320, 222, background)

  for row in layout:
    for canvas_item in row:
      if isinstance(canvas_item, Button):
        canvas_item.enabled = False
      canvas_item.hovered = False
    row[0].enabled = True
  layout_get((0, 0)).hovered = True

  y: int = 111 - canvas_items_height(layout)//2
  for row in layout:
    x: int = 160 - canvas_items_width(row)//2
    for canvas_item in row:
      canvas_item.position = Vector2(x, y)
      canvas_item.draw()
      x += canvas_items_width([canvas_item])  + SPACEMENT_X

    y += canvas_items_height(1) + SPACEMENT_Y


  hovering_pos = Vector2(0, 0)
  hovering_canvas_item = layout_get(hovering_pos)
  focused: bool = False

  while not keydown(KEY_OK):
    old_hovering_pos = None
    
    if focused:
      hovering_canvas_item.handle_input()
    else:
      for key in MOVES:
        if keydown(key):
          if not old_hovering_pos:
            old_hovering_pos = hovering_pos
          hovering_pos = layout_clamp(hovering_pos + MOVES[key])
          hovering_canvas_item = layout_get(hovering_pos)

      if old_hovering_pos and old_hovering_pos != hovering_pos:
        button = layout_get(old_hovering_pos)
        button.hovered = False
        button.draw()

        hovering_canvas_item.hovered = True
        hovering_canvas_item.draw()

    if keydown(KEY_EXE):
      if isinstance(hovering_canvas_item, Focusable):
        focused = not focused
        hovering_canvas_item.focused = focused
        hovering_canvas_item.draw()
      else:
        for i, canvas_item in enumerate(layout[hovering_pos.y]):
          if isinstance(canvas_item, Button):
            if i == hovering_pos.x:
              if not canvas_item.enabled:
                canvas_item.enabled = True
                canvas_item.draw()
            elif canvas_item.enabled:
              canvas_item.enabled = False
              canvas_item.draw()
      wait_released(KEY_EXE)
      

    if EMULATED:
      try:
        display(True) # type: ignore
      except:
        pass

    while old_hovering_pos:
      old_hovering_pos = False
      for key in MOVES:
        if keydown(key):
          old_hovering_pos = True

  wait_released(KEY_OK)

  return parse_result()


if EMULATED and __name__ == "__main__":
  example()