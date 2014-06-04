from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader


class Novel(FloatLayout):

    characters = {}
    music = {}
    backgrounds = {}
    sounds = {}

    current_background = StringProperty()
    left_character_image = StringProperty()
    right_character_image = StringProperty()

    text_box_image = StringProperty()

    textbox_text = StringProperty()

    centertext = StringProperty()

    current_song = ObjectProperty()

    finished = False

    # adding some defaults
    characters['blank'] = "./data/blank.png"

    def __init__(self, path, callback_when_finished, **kwargs):
        super(Novel, self).__init__(**kwargs)

        self.callback_when_finished = callback_when_finished
        self.file = open(path, 'r')

        self.left = 1    # kivy object property
        self.right = 2   # kivy object property

        self.text_box_image = './data/textbox_background.png'
        self.left_character_image = self.characters['blank']
        self.right_character_image = self.characters['blank']

        self.on_touch_down(None)

    def on_touch_down(self, touch):
        if not self.finished:
            while not(self.process_next_line()):
                pass

    def process_next_line(self):
        """
        Processes the next line of the novel file

        return True -> all finished, wait for user input
        return False -> this task is finished, but read next line before user input is required
        """
        line = self.file.readline().strip()
        print(line)
        #Test if the line is a comment.
        if line == '':
            print('empty Line')
            return False
        elif line[0] == '#':
            print(line[0])

            return False

        line = line.split()

        if line[0] == 'character':
            self.characters[line[1]] = line[2]
            print('Character ' + line[1] + ' created.')
            return False

        elif line[0] == 'music':
            self.music[line[1]] = line[2]
            print('Music ' + line[1] + ' created.')
            return False

        elif line[0] == 'background':
            self.backgrounds[line[1]] = line[2]
            print('Background ' + line[1] + ' created.')
            return False

        elif line[0] == 'sound':
            self.sounds[line[1]] = line[2]
            print('Sound ' + line[1] + ' created.')
            return False

        elif line[0] == 'character_left':
            if line[1] in self.characters:
                self.left_character_image = self.characters[line[1]]
            print('Set ' + line[1] + ' tor the left.')
            return False

        elif line[0] == 'character_right':
            if line[1] in self.characters:
                self.right_character_image = self.characters[line[1]]
            print('Set ' + line[1] + ' tor the right.')
            return False

        elif line[0] == 'remove':
            if line[1] == 'left':
                self.left_character_image = self.characters['blank']
            elif line[1] == 'right':
                self.right_character_image = self.characters['blank']
            else:
                print('Error')
            return False

        elif line[0] == 'text':
            text = ' '.join(line[1:])
            self.textbox_text = text
            print('Set text to ' + text)
            return True

        elif line[0] == 'centertext':
            text = ' '.join(line[1:])
            self.centertext = text
            print('centertext to ' + text)
            return True

        elif line[0] == 'set_background':
            if line[1] in self.backgrounds:
                self.current_background = self.backgrounds[line[1]]
            print('Set ' + line[1] + ' as background.')
            return False

        elif line[0] == 'play_music':
            if self.current_song:
                self.current_song.stop()

            sound = SoundLoader.load(self.music[line[1]])
            if sound:
                sound.loop = True
                self.current_song = sound
                self.current_song.play()
            print('Playing song ' + line[1])
            return False

        elif line[0] == 'play_sound':
            sound = SoundLoader.load(self.sounds[line[1]])
            if sound:
                sound.play()
            print('Playing sound effect ' + line[1])
            return False

        elif line[0] in self.characters:
            text = ' '.join(line[1:])
            self.textbox_text = text
            print(line[1] + ' said: ' + text)
            return True

        elif line[0] == 'end':
            self.finished = True
            self.textbox_text = ''
            self.left_character_image = self.characters['blank']
            self.right_character_image = self.characters['blank']
            if self.current_song:
                self.current_song.stop()

            self.callback_when_finished()

            print('The END')
            return True

        else:
            print("Error!")
            return True


class Character():
    # Image is a string to an image
    # name is the name of the character
    def __init__(self, name, image):
        self.name = name
        self.images = image    # dict with all the images