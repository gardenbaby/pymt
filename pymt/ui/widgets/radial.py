from __future__ import with_statement
from __future__ import division

from pyglet import *
from pyglet.gl import *
from math import *
from pymt.ui.factory import MTWidgetFactory
from pymt.ui.widgets.widget import MTWidget
from pymt.graphx import *
from pymt.vector import Vector
__all__ = ['MTVectorSlider']

### HELP NEEDED IN THE COLORING DEPARTMENT ###

def _get_distance(Pos1, Pos2):
    '''Get the linear distance between two points'''
    return sqrt((Pos2[0] - Pos1[0])**2 + (Pos2[1] - Pos1[1])**2)

class MTVectorSlider(MTWidget):
    '''
    This is a slider that provides an arrow, and allows you to manipulate
    it just like any other vector, adjusting its angle and amplitude.

    :Parameters:
        'bgcolor' : tuple, default to (.2, .4, .9)
	    The background color of the widget
        'vcolor' : tuple, default to (1, .28, 0)
	    The color for the vector
        'radius': int, default to 200
	    The radius of the whole widget
    '''

    def __init__(self, **kwargs):
        super(MTVectorSlider, self).__init__(**kwargs)

        kwargs.setdefault('radius', 200)
        kwargs.setdefault('vcolor', (1, .28, 0))
        kwargs.setdefault('bgcolor', (.2, .4, .9))

        self.radius = kwargs.get('radius')
        self.vcolor = kwargs.get('vcolor')
        self.bgcolor = kwargs.get('bgcolor')

        #The vector hand
        self.vector = Vector(0, 0)

        #Vector Stuff, for the callback
        self.amplitude = 0
        self.angle = 0

        self.register_event_type('on_amplitude_change')
        self.register_event_type('on_angle_change')
        #This is just a combination of the last two
        self.register_event_type('on_vector_change')

    def collide_point(self, x, y):
        '''Because this widget is a circle, and this method as
        defined in MTWidget is for a square, we have to override
        it.'''
        return _get_distance(self.pos, (x, y)) <= self.radius

    def _calc_stuff(self):
        '''Recalculated the args for the callbacks'''
        self.amplitude = self.vector.distance(self.pos)
	self.angle = self.vector.angle(0, 0)

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            #The blob is in the widget, do stuff
            self.vector[0], self.vector[1] = x, y
            self._calc_stuff()

            self.dispatch_event('on_aplitude_change', self.amplitude)
            self.dispatch_event('on_angle_change', self.angle)
            self.dispatch_event('on_vector_change', self.amplitude, self.angle)

    def on_touch_move(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            #The blob is in the widget, do stuff
            self.vector[0], self.vector[1] = x, y
            self._calc_stuff()

            self.dispatch_event('on_aplitude_change', self.amplitude)
            self.dispatch_event('on_angle_change', self.angle)
            self.dispatch_event('on_vector_change', self.amplitude, self.angle)

    def draw(self):
        #Draw Background
        set_color(*self.bgcolor)
        drawCircle(self.pos, self.radius)

        #A good size for the hand, proportional to the size of the widget
        hd = self.radius / 10
        #Draw center of the hand
        set_color(*self.vcolor)
        drawCircle(self.pos, hd)
        #Rotate the triangle so its not skewed
        l = prot((self.pos[0] - hd, self.pos[1]), self.angle-90, self.pos)
        h = prot((self.pos[0] + hd, self.pos[1]), self.angle-90, self.pos)
        #Draw triable of the hand
        with gx_begin(GL_POLYGON):
            glVertex2f(*l)
            glVertex2f(*h)
            glVertex2f(self.vector[0], self.vector[1])

MTWidgetFactory.register('MTVectorSlider', MTVectorSlider)

if __name__ == '__main__':
    def on_vector_change(amp, ang):
        print amp, ang

    from pymt import *
    w = MTWindow(fullscreen=False)
    mms = MTVectorSlider(pos=(200,200))
    mms.push_handlers('on_vector_change', on_vector_change)
    w.add_widget(mms)
    runTouchApp()
