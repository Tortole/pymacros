# from kivy.uix.button import Button
# from kivy.app import App
# from functools import partial
#
#
# class KivyButton(App):
#     def disable(self, instance, *args):
#         instance.disabled = True
#
#     def update(self, instance, *args):
#         instance.text = "I am Disabled!"
#
#     def build(self):
#         mybtn = Button(text="Click me to disable")
#         mybtn.bind(on_press=partial(self.disable, mybtn))
#         mybtn.bind(on_press=partial(self.update, mybtn))
#         return mybtn
#
#
# KivyButton().run()


from kivy.app import App
from kivy.lang import Builder

kv = '''
FloatLayout:
    # Define the root widget
    ScatterLayout:
        size_hint: 1.0, 0.2
        do_translation_x: False
        # do_translation_y: False
        Label:
            size_hint: 1.0, 1
            text: 'Drag me'
            canvas.before:
                Color:
                    rgb: .6, .6, .6
                Rectangle:
                    pos: self.pos
                    size: self.size
'''

class RectangleApp(App):
    def build(self):
        object = Builder.load_string(kv)
        return object

if __name__ == '__main__':
    RectangleApp().run()



# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.uix.label import Label
#
# class MyWidget(Widget):
#     def draw(self):
#         for i in range(6):
#             print('I draw label')
#             self.add_widget(Label(text='hello', pos=(100, i*100)))
#
# class MyApp(App):
#     def build(self):
#         game = MyWidget()
#         game.draw()
#         return game
#
# if __name__ == '__main__':
#     MyApp().run()
