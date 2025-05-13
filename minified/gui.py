_C=True
_B=None
_A=False
from math import*
from ion import*
from colors import*
from time import sleep
from kandinsky import*
EMULATED=_A
try:import os;EMULATED=_C;print('Emulated')
except:pass
SPACEMENT_X=2
SPACEMENT_Y=4
OUTLINE_SIZE=1
CHAR_HEIGHT=18
MOVES={KEY_UP:(0,-1),KEY_DOWN:(0,1),KEY_RIGHT:(1,0),KEY_LEFT:(-1,0)}
TPS=100
UNHOVERABLE_COLOR=grey
background=white_blue
default_color=light_brown
default_overlay=dark_brown
default_enabled_color=dark_blue
default_hover_overlay=white
layout=[]
class Vector2:
	def __init__(self,x=0,y=0):assert type(x)==int;assert type(y)==int;self.x=x;self.y=y
	def duplicate(self):return Vector2(self.x,self.y)
	def __getitem__(self,idx):
		if idx==0:return self.x
		elif idx==1:return self.y
		return IndexError
	def __add__(self,__o):
		try:return Vector2(self.x+__o[0],self.y+__o[1])
		except Exception as error:raise error
	def __eq__(self,__o):return self.x==__o[0]and self.y==__o[1]
	def __str__(self):return'<'+str(self.x)+', '+str(self.y)+'>'
def txt_len_size(length):return Vector2(length*10,CHAR_HEIGHT)
def txt_size(string):return txt_len_size(len(string))
def add_overlay(size):return size+(2,2)
def wait_released(key):
	while keydown(key):sleep(.05)
class CanvasItem:
	def __init__(self,position=Vector2(10,10),color=_B,overlay=_B,callback=lambda:_B):self.position=position;self.color=color;self.overlay=overlay;self.callback=callback
	def draw(self,pos=_B):'Virtual';raise NotImplementedError('draw() is not implemented on '+repr(self))
	def get_size(self):'Virtual';raise NotImplementedError('get_size() is not implemented on '+repr(self))
	def get_color(self):return self.color or default_color
	def get_overlay(self):return self.overlay or default_overlay
	def handle_input(self):'Virtual';raise NotImplementedError('handle_input() is not implemented on '+repr(self))
class Hoverable(CanvasItem):
	def __init__(self,overlay=_B,hovered=_A,*args,**kwargs):super().__init__(*args,**kwargs);self.hovered=hovered
	def get_overlay(self):return default_hover_overlay if self.hovered else super().get_overlay()
class Label(Hoverable):
	def __init__(self,txt='Lorem Ipsum',*args,**kwargs):super().__init__(*args,**kwargs);self.txt=txt
	def get_size(self):return txt_size(self.txt)
	def draw(self,pos=_B):pos=pos or self.position;size=add_overlay(self.get_size());fill_rect(pos.x-1,pos.y-1,size.x,size.y,UNHOVERABLE_COLOR if self.hovered else self.get_overlay());draw_string(self.txt,pos.x,pos.y,UNHOVERABLE_COLOR if self.hovered else self.get_overlay(),self.get_color())
class Button(Label):
	def __init__(self,*args,enabled=_A,**kwargs):super().__init__(*args,**kwargs);self.enabled=enabled
	def get_size(self):return txt_size(self.txt)
	def draw(self,pos=_B):pos=pos or self.position;size=add_overlay(self.get_size());fill_rect(pos.x-1,pos.y-1,size.x,size.y,default_hover_overlay if self.hovered else self.get_overlay());draw_string(self.txt,pos.x,pos.y,default_hover_overlay if self.hovered else self.get_overlay(),default_enabled_color if self.enabled else self.get_color())
	def toggle(self):self.enabled=not self.enabled
class Focusable(Hoverable):
	def __init__(self,hovered=_A,*args,**kwargs):super().__init__(hovered,*args,**kwargs);self.focused=_A
class TextBox(Focusable):
	def __init__(self,hovered=_A,size=10,*args,**kwargs):super().__init__(hovered,*args,**kwargs);self.txt='';self.size=size;self.txt_pos=0
	def handle_input(self):
		for key in range(KEY_EXP,KEY_PLUS+1):
			if keydown(key):self.txt+=chr(key-KEY_EXP+ord('a'));self.txt_pos+=1;self.draw();wait_released(key);return
		if keydown(KEY_LEFT):self.txt_pos=max(0,self.txt_pos-1);self.draw();wait_released(KEY_LEFT);return
		if keydown(KEY_RIGHT):self.txt_pos=min(len(self.txt),self.txt_pos+1);self.draw();wait_released(KEY_RIGHT);return
		if keydown(KEY_UP):self.txt_pos=0;self.draw();wait_released(KEY_UP);return
		if keydown(KEY_DOWN):self.txt_pos=len(self.txt);self.draw();wait_released(KEY_DOWN);return
		if keydown(KEY_BACKSPACE)and self.txt and self.txt_pos!=0:self.txt=self.txt[:self.txt_pos-1]+self.txt[self.txt_pos:];self.txt_pos-=1;self.draw();wait_released(KEY_BACKSPACE);return
	def get_size(self):return txt_len_size(self.size)
	def draw(self,pos=_B):
		pos=pos or self.position;size=self.get_size();size_with_overlay=add_overlay(size);offset=0
		if self.txt_pos>self.size:offset=self.txt_pos-self.size
		fill_rect(pos.x-1,pos.y-1,size_with_overlay.x,size_with_overlay.y,default_hover_overlay if self.hovered else self.get_overlay());fill_rect(pos.x,pos.y,size.x,size.y,self.get_color());draw_string(self.txt[offset:min(offset+self.size,len(self.txt))],pos.x,pos.y,black,self.get_color())
		if self.focused:fill_rect(pos.x+txt_len_size(self.txt_pos-offset).x,pos.y,1,size.y,black)
	def get_color(self):return self.color or white
class Slider(Focusable):
	SLIDER_HEIGHT:int=4;CURSOR_SIZE:int=8
	def __init__(self,min,max,step=1,initial_value=_B,size=100,*args,**kwargs):super().__init__(*args,**kwargs);self.focusable=_C;self.focused=_A;self.min=min;self.max=max;self.step=step;self.value=round((min+max)/2/step)*step if initial_value==_B else initial_value;self.size=size
	def handle_input(self):
		old_val=self.value
		if keydown(KEY_LEFT):self.value=max(self.value-self.step*(10 if keydown(KEY_SHIFT)else 1),self.min);wait_released(KEY_LEFT)
		elif keydown(KEY_RIGHT):self.value=min(self.value+self.step*(10 if keydown(KEY_SHIFT)else 1),self.max);wait_released(KEY_RIGHT)
		if old_val!=self.value:self.callback();self.draw()
	def get_size(self):return Vector2(self.size,self.SLIDER_HEIGHT)
	def get_color(self):return default_enabled_color if self.focused else super().get_color()
	def draw(self,pos=_B):pos=(pos or self.position).duplicate();size=self.get_size();fill_rect(pos.x-1,pos.y,size.x+1,canvas_items_height(1)+1,background);cursor_pos=pos+Vector2(int((self.value-self.min)/(self.max-self.min)*(size.x-self.CURSOR_SIZE)),int((canvas_items_height(1)-self.CURSOR_SIZE)/2));pos.y+=int((canvas_items_height(1)-size.y)/2);fill_rect(pos.x-1,pos.y-1,size.x+2,size.y+2,self.get_overlay());fill_rect(pos.x,pos.y,size.x,size.y,self.get_color());fill_rect(cursor_pos.x-1,cursor_pos.y-1,self.CURSOR_SIZE+2,self.CURSOR_SIZE+2,self.get_overlay());fill_rect(cursor_pos.x,cursor_pos.y,self.CURSOR_SIZE,self.CURSOR_SIZE,self.get_color())
def canvas_items_width(canvas_items):
	result=len(canvas_items)*(OUTLINE_SIZE+SPACEMENT_X)-SPACEMENT_X
	for canvas_item in canvas_items:result+=canvas_item.get_size().x
	return result
def canvas_items_height(canvas_items):
	if type(canvas_items)==list:canvas_items=len(canvas_items)
	return canvas_items*(CHAR_HEIGHT+OUTLINE_SIZE+SPACEMENT_Y)-SPACEMENT_Y
def layout_get(position):return layout[position[1]][position[0]]
def clamp(value,minimum,maximum):return max(min(value,maximum),minimum)
def layout_clamp(position):y=clamp(position[1],0,len(layout)-1);x=clamp(position[0],0,len(layout[y])-1);return Vector2(x,y)
def example():
	global layout;slider=Slider(0,91,1);label=Label('XX')
	def slider_callback():label.txt='{0:2d}'.format(slider.value);label.draw()
	slider.callback=slider_callback;slider_callback();layout=[[Button('Az'),Button('By'),Button('Cx')],[slider,label],[Button('Truc'),Button('Machin')],[TextBox()]];print(start())
def parse_result():
	result=[]
	for row in layout:
		row_result=[];result.append(row_result)
		for canvas_item in row:
			if isinstance(canvas_item,Button):
				if canvas_item.enabled:row_result.append(canvas_item.txt)
			elif isinstance(canvas_item,Slider):row_result.append(canvas_item.value)
			elif isinstance(canvas_item,TextBox):row_result.append(canvas_item.txt)
	return result
def start():
	fill_rect(0,0,320,222,background)
	for row in layout:
		for canvas_item in row:
			if isinstance(canvas_item,Button):canvas_item.enabled=_A
			canvas_item.hovered=_A
		row[0].enabled=_C
	layout_get((0,0)).hovered=_C;y=111-canvas_items_height(layout)//2
	for row in layout:
		x=160-canvas_items_width(row)//2
		for canvas_item in row:canvas_item.position=Vector2(x,y);canvas_item.draw();x+=canvas_items_width([canvas_item])+SPACEMENT_X
		y+=canvas_items_height(1)+SPACEMENT_Y
	hovering_pos=Vector2(0,0);hovering_canvas_item=layout_get(hovering_pos);focused=_A
	while not keydown(KEY_OK):
		sleep(1/TPS);old_hovering_pos=_B
		if focused:hovering_canvas_item.handle_input()
		else:
			for key in MOVES:
				if keydown(key):
					if not old_hovering_pos:old_hovering_pos=hovering_pos
					hovering_pos=layout_clamp(hovering_pos+MOVES[key]);hovering_canvas_item=layout_get(hovering_pos)
			if old_hovering_pos and old_hovering_pos!=hovering_pos:button=layout_get(old_hovering_pos);button.hovered=_A;button.draw();hovering_canvas_item.hovered=_C;hovering_canvas_item.draw()
		if keydown(KEY_EXE):
			if isinstance(hovering_canvas_item,Focusable):focused=not focused;hovering_canvas_item.focused=focused;hovering_canvas_item.draw()
			else:
				for(i,canvas_item)in enumerate(layout[hovering_pos.y]):
					if isinstance(canvas_item,Button):
						if i==hovering_pos.x:
							if not canvas_item.enabled:canvas_item.enabled=_C;canvas_item.draw()
						elif canvas_item.enabled:canvas_item.enabled=_A;canvas_item.draw()
			wait_released(KEY_EXE)
		if EMULATED:
			try:display(_C)
			except:pass
		while old_hovering_pos:
			old_hovering_pos=_A
			for key in MOVES:
				if keydown(key):old_hovering_pos=_C
	wait_released(KEY_OK);return parse_result()
if EMULATED and __name__=='__main__':example()