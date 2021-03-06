from pymt import *
import pyglet
from mutagen.id3 import ID3
from cStringIO import StringIO
import glob

class fileList(MTKineticScrollText):
    def __init__(self, **kwargs):
        kwargs.setdefault('pos', (0,0))
        kwargs.setdefault('size', (200,400))
        kwargs.setdefault('font_size', 10)
        super(fileList, self).__init__(**kwargs)
        self.player = pyglet.media.Player()


    def on_item_select(self,file):
        print file
        self.player.seek(0)
        source = pyglet.media.load(file,streaming=True)
        self.player.queue(source)
        if self.player.playing == True:            
            self.player.next()
        else:
            self.player.play()
       
class MusicPlayer(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        super(MusicPlayer, self).__init__(**kwargs)
        self.dir = kwargs.get('dir')
        self.file_list = glob.glob(self.dir) 
        self.list = []
        for self.file in self.file_list:
            sublist = []
            self.f=ID3(self.file)
            sublist.append(self.f["TIT2"])
            sublist.append(self.file)
            self.list.append(sublist)        
            
        mms = fileList(pos=(10,10),items=self.list)
        self.add_widget(mms,side='back')
        self.coverart = CoverArt(pos=(10,10),frame=self.f)
        self.add_widget(self.coverart,side='front')
        self.width =  300
        self.height = 300
        mms.height = self.coverart.height
        mms.width = self.coverart.width
        self.fbut = FlipButton(pos=(self.width-25,0))
        self.add_widget(self.fbut,side='front')
        self.add_widget(self.fbut,side='back')
        self.playpause = PlayPauseButton(player=mms.player)
        self.add_widget(self.playpause,side='back')

        
class FlipButton(MTButton):
    def __init__(self, **kwargs):
        kwargs.setdefault('label', '~')
        kwargs.setdefault('size', (25,25))
        kwargs.setdefault('pos', (0,0))
        kwargs.setdefault('color', (0.5,0.5,0.5,1))
        super(FlipButton, self).__init__(**kwargs) 
    
    def on_press(self,touchID, x, y):
        self.parent.flip()
        
class CoverArt(MTWidget):
    def __init__(self, **kwargs):
        #kwargs.setdefault('scale', 0.5)
        super(CoverArt, self).__init__(**kwargs)
        self.f = kwargs.get('frame')
        for self.frame in self.f.getall("APIC"):
            self.img                 = pyglet.image.load('Default.jpg', file=StringIO(self.frame.data))
        try:
            self.image          = pyglet.sprite.Sprite(self.img)
        except AttributeError:
            self.img                 = pyglet.image.load('Default.jpg')
            self.image          = pyglet.sprite.Sprite(self.img)
        self.image.x        = self.x
        self.image.y        = self.y
        self.scale          = 280.0/float(self.img.width)
        self.image.scale    = self.scale
        self.size           = (280, 280)

    def draw(self):
        self.image.x        = self.x
        self.image.y        = self.y
        self.image.scale    = self.scale
        self.size           = (self.img.width, self.img.height)
        self.image.draw()        


class PlayPauseButton(MTImageButton):
    '''MTVideoPlayPause is a dynamic play/pause button of the video widget'''
    def __init__(self, **kwargs):
        kwargs.setdefault('filename', 'play.png')
        kwargs.setdefault('filename_pause','pause.png')
        kwargs.setdefault('player', None)
        super(PlayPauseButton, self).__init__(**kwargs)
        self.vid        = kwargs.get('player')
        self.playState  = 'Play'

        self.images = {} #crate a python dictionary..like a hash map
        self.images['Play']  = pyglet.sprite.Sprite(pyglet.image.load('play.png'))
        self.images['Pause'] = pyglet.sprite.Sprite(pyglet.image.load('pause.png'))

        self.scale    = 0.75        
        
    def on_draw(self):
        if self.vid.playing == True:            
            self.image = self.images['Pause']
        else:
            self.image = self.images['Play']
        self.draw()

    def on_touch_down(self, touches, touchID, x,y):
        if self.collide_point(x,y):
            self.state = ('down', touchID)
            if self.playState == 'Pause':
                self.vid.play()
                self.playState = 'Play'
            elif self.playState == 'Play':
                self.vid.pause()
                self.playState = 'Pause'

            #set the correct image
            self.image = self.images[self.playState]  #playState is one of the two strings that are used as keys/lookups in the dictionary        
        
if __name__ == '__main__':
    w = MTWindow(color=(0,0,0,1.0), fullscreen=True)
    w.add_widget(MusicPlayer(pos=(210,410),dir='F:\\Final Fantasy\\*.mp3')) #change directory here
    w.add_widget(MusicPlayer(pos=(500,600),dir='F:\\rock on\\*.mp3')) #change directory here
    runTouchApp()
