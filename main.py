from kivy.app import App
from factory import Novel
from kivy.lang import Builder
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
from kivy.core.window import Window


class VisualNovel(App):

    current_widget = ''

    def build(self):
        self.title = 'KiViNo'
        Builder.load_file('novel.kv')
        novel = Novel('talk1', self.finished)
        self.current_widget = novel
        return novel

    def finished(self):
        Window.remove_widget(self.current_widget)
        novel = Novel('talk2', self.finished)
        Window.add_widget(novel)
        self.current_widget = novel

if __name__ == '__main__':
    VisualNovel().run()