import time
from tracemalloc import is_tracing
from pynput import keyboard, mouse
from screeninfo import get_monitors

class ActionsTrack:
    mouse_buttom_to_string = {
        mouse.Button.left: 'l',
        mouse.Button.right: 'r',
        mouse.Button.middle: 'm'
    }
    string_to_mouse_button = {v: k for k, v in mouse_buttom_to_string.items()}
    
    _space_key_code = '000'

    def __init__(self):
        # Запущена ли прослушка клавиатуры и мыши
        self.is_listening = False
        self.is_tracking = False
        # Прослушка клавиатуры
        self.keyboard_listener = None
        # Прослушка мыши
        self.mouse_listener = None
        # Клавиша для запуска или остановки макроса
        self.hotkey_macros_write = keyboard.Key.shift_r
        # Значения разрешения главного экрана
        self.primary_monitor_resolution = {}
        # Получение данных о разрешении монитора
        for m in get_monitors():
            if m.is_primary:
                primary_monitor_resolution['width'] = m.width
                primary_monitor_resolution['height'] = m.height
                break
        # Последовательность действий клавиатуры и мыши
        self.track = []

    def _add_action(self, device, action, **kwargs):
        if action not in ['press', 'release', 'move', 'scroll']:
            raise ValueError('Wrong action name.')

        if device == 'keyboard':
            self.track.append({
                'device': device,
                'action': action,
                'key': kwargs['key']
            })
        elif device == 'mouse':
            action_dict = {
                'device': device,
                'action': action,
                'x': kwargs['x'],
                'y': kwargs['y']
            }

            if action == 'press' or action == 'release':
                action_dict['key'] = kwargs['key']
            if action == 'scroll':
                action_dict['dx'] = kwargs['dx']
                action_dict['dy'] = kwargs['dy']

            self.track.append(action_dict)
        else:
            raise ValueError('Wrong device name.')

    # vvvv mouse vvvv

    # def coord_to_string(x, y):
    #     return f'{x / primary_monitor_resolution["width"]:.2f}{y / primary_monitor_resolution["height"]:.2f}'


    # def string_to_coord(str_coord):
    #     return round(float(str_coord[:4]) * primary_monitor_resolution['width']), \
    #         round(float(str_coord[4:]) * primary_monitor_resolution['height'])

    def on_move_mouse_track(self, x, y):
        if self.is_tracking:
            pass

    def on_click_mouse_track(self, x, y, button, is_pressed):
        # global is_listen_run
        # if is_listen_run:
        #     track_actions.append(
        #         f'm'
        #         f'{coord_to_string(x, y)}'
        #         f'{"p" if is_pressed else "r"}'
        #         f'{mouse_buttom_to_string[button]}'
        #     )
        if self.is_tracking:
            self._add_action(
                'mouse',
                'press' if is_pressed else 'release',
                x=x,
                y=y,
                key=button
            )


    def on_scroll_mouse_track(self, x, y, dx, dy):
        # global is_listen_run
        # if is_listen_run:
        #     track_actions.append(f'm{coord_to_string(x, y)}s{dx:+}{dy:+}')
        if self.is_tracking:
            self._add_action(
                'mouse',
                'scroll',
                x=x,
                y=y,
                dx=dx,
                dy=dy
            )


    # ^^^^ mouse ^^^^
    # vvvv keyboard vvvv

    # def key_to_string(key):
    #     try:
    #         return key.char
    #     except AttributeError:
    #         if key == keyboard.Key.space:
    #             return space_key_code
    #         return f'{str(key.value)[1:-1]:0>3}'

    # def string_to_key(string):
    #     if len(string) > 1:
    #         if string == space_key_code:
    #             return keyboard.Key.space
    #         else:
    #             return keyboard.KeyCode.from_vk(int(string))
    #     else:
    #         return string


    pressed_keys = set()

    def on_press_keyboard_track(self, key):
        # global is_listen_run
        # if is_listen_run:
        #     key_pressed = key_to_string(key)
        #     if key_pressed not in pressed_keys:
        #         pressed_keys.add(key_pressed)
        #         track_actions.append(f'kp{key_pressed}')
        if key == self.hotkey_macros_write:
            # nothing
            pass
        elif self.is_tracking and key not in pressed_keys:
            self._add_action(
                'keyboard',
                'press',
                key=key
            )
            pressed_keys.add(key)

    def on_release_keyboard_track(self, key):
        # global is_listen_run
        # if key == hotkey_macros_write:
        #     is_listen_run = not is_listen_run
        # elif is_listen_run:
        #     key_released = key_to_string(key)
        #     pressed_keys.discard(key_released)
        #     track_actions.append(f'kr{key_released}')
        if key == self.hotkey_macros_write:
            self.is_tracking = not self.is_tracking
        elif self.is_tracking:
            self._add_action(
                'keyboard',
                'release',
                key=key
            )
            pressed_keys.discard(key)


    # ^^^^ keyboard ^^^^

    def start(self):
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press_keyboard_track,
            on_release=self.on_release_keyboard_track
        )
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move_mouse_track,
            on_click=self.on_click_mouse_track,
            on_scroll=self.on_scroll_mouse_track
        )

        self.is_listening = True # !!!
        self.is_tracking = True
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def pause(self):
        self.is_tracking = False

    def unpause(self):
        self.is_tracking = True

    def stop(self):
        self.is_listening = False # !!!
        self.is_tracking = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def run(self):
        # !!!
        print(self.track)
        keyboard_controller = keyboard.Controller()
        mouse_controller = mouse.Controller()

        for t in self.track:
            time.sleep(0.2)
            # Действия клавиатуры
            if t['device'] == 'keyboard':
                # Нажатие клавиши клавиатуры
                if t['action'] == 'press':
                    keyboard_controller.press(t['key'])
                # Отпуск клавиши клавиатуры
                elif t['action'] == 'release':
                    keyboard_controller.release(t['key'])

            # Действия мыши
            if t['device'] == 'mouse':
                # Движение мыши
                mouse_controller.move(
                    t['x'] - mouse_controller.position[0],
                    t['y'] - mouse_controller.position[1]
                )                
                # Прокручивание колёсика
                if t['action'] == 'scroll':
                    mouse_controller.scroll(t['dx'], t['dy'])
                # Нажатие клавиши мыши
                elif t['action'] == 'press':
                    mouse_controller.press(t['key'])
                # Отпуск клавиши мыши
                elif t['action'] == 'release':
                    mouse_controller.release(t['key'])

    def to_string(self):
        pass

    def from_string(self, track_str):
        pass

    def get_action(self, index):
        pass
    


# # Запущена ли прослушка клавиатуры и мыши
# is_listen_run = True
# # Клавиша для запуска или остановки макроса
# hotkey_macros_write = keyboard.Key.shift_r
# # 
# primary_monitor_resolution = {}
# track_actions = []


# # vvvv mouse vvvv 


# def coord_to_string(x, y):
#     return f'{x / primary_monitor_resolution["width"]:.2f}{y / primary_monitor_resolution["height"]:.2f}'


# def string_to_coord(str_coord):
#     return round(float(str_coord[:4]) * primary_monitor_resolution['width']), \
#            round(float(str_coord[4:]) * primary_monitor_resolution['height'])


# mouse_buttom_to_string = {
#     mouse.Button.left: 'l',
#     mouse.Button.right: 'r',
#     mouse.Button.middle: 'm'
# }
# string_to_mouse_button = {v: k for k, v in mouse_buttom_to_string.items()}


# def on_move_mouse_track(x, y):
#     # global is_listen_run
#     # if is_listen_run:
#         # track_actions.append(f'm{coord_to_string(x, y)}m')
#     pass


# def on_click_mouse_track(x, y, button, is_pressed):
#     global is_listen_run
#     if is_listen_run:
#         track_actions.append(
#             f'm'
#             f'{coord_to_string(x, y)}'
#             f'{"p" if is_pressed else "r"}'
#             f'{mouse_buttom_to_string[button]}'
#         )


# def on_scroll_mouse_track(x, y, dx, dy):
#     global is_listen_run
#     if is_listen_run:
#         track_actions.append(f'm{coord_to_string(x, y)}s{dx:+}{dy:+}')


# # ^^^^ mouse ^^^^
# # vvvv keyboard vvvv

# space_key_code = '000'

# # class KeyCode(enum):
# #     space_key_code = '000'

# #     @classmethod
# #     def __missing__(self, value):


# def key_to_string(key):
#     try:
#         return key.char
#     except AttributeError:
#         if key == keyboard.Key.space:
#             return space_key_code
#         return f'{str(key.value)[1:-1]:0>3}'

# def string_to_key(string):
#     if len(string) > 1:
#         if string == space_key_code:
#             return keyboard.Key.space
#         else:
#             return keyboard.KeyCode.from_vk(int(string))
#     else:
#         return string


# pressed_keys = set([key_to_string(hotkey_macros_write)])


# def on_press_keyboard_track(key):
#     global is_listen_run
#     if is_listen_run:
#         key_pressed = key_to_string(key)
#         if key_pressed not in pressed_keys:
#             pressed_keys.add(key_pressed)
#             track_actions.append(f'kp{key_pressed}')


# def on_release_keyboard_track(key):
#     global is_listen_run
#     if key == hotkey_macros_write:
#         is_listen_run = not is_listen_run
#     elif is_listen_run:
#         key_released = key_to_string(key)
#         pressed_keys.discard(key_released)
#         track_actions.append(f'kr{key_released}')


# # ^^^^ keyboard ^^^^


# # 
# def macros_run(track_actions):
#     keyboard_controller = keyboard.Controller()
#     mouse_controller = mouse.Controller()

#     for t_a in track_actions:
#         time.sleep(0.2)
#         # Действия клавиатуры
#         if t_a[0] == 'k':
#             key = string_to_key(t_a[2:])

#             # Нажатие клавиши клавиатуры
#             if t_a[1] == 'p':
#                 keyboard_controller.press(key)
#             # Отпуск клавиши клавиатуры
#             elif t_a[1] == 'r':
#                 keyboard_controller.release(key)

#         # Действия мыши
#         elif t_a[0] == 'm':
#             position_dx, position_dy = string_to_coord(t_a[1:9])
#             position_dx -= mouse_controller.position[0]
#             position_dy -= mouse_controller.position[1]
#             mouse_controller.move(position_dx, position_dy)

#             # Прокручивание колёсика
#             if t_a[9] == 's':
#                 dx = int(t_a[10:12])
#                 dy = int(t_a[12:14])
#                 mouse_controller.scroll(dx, dy)
#             # Нажатие клавиши мыши
#             elif t_a[9] == 'p':
#                 mouse_controller.press(string_to_mouse_button[t_a[10]])
#             # Отпуск клавиши мыши
#             elif t_a[9] == 'r':
#                 mouse_controller.release(string_to_mouse_button[t_a[10]])


if __name__ == '__main__':
    '''
    

    '''

    trck = ActionsTrack()

    trck.start()

    while trck.is_tracking:
        pass

    trck.stop()
    trck.run()

    # # Получение данных о разрешении монитора
    # for m in get_monitors():
    #     if m.is_primary:
    #         primary_monitor_resolution['width'] = m.width
    #         primary_monitor_resolution['height'] = m.height
    #         break

    # # Прослушка клавиатуры
    # keyboard_listener = keyboard.Listener(
    #     on_press=on_press_keyboard_track,
    #     on_release=on_release_keyboard_track
    # )
    # keyboard_listener.start()

    # # Прослушка мыши
    # mouse_listener = mouse.Listener(
    #     on_move=on_move_mouse_track,
    #     on_click=on_click_mouse_track,
    #     on_scroll=on_scroll_mouse_track
    # )
    # mouse_listener.start()

    # # is_listen_run = True

    # while is_listen_run:
    #     pass

    # # with open("key_pressed_history.txt", "w") as file_out:
    # #     file_out.write(''.join(track_actions))

    # mouse_listener.stop()
    # keyboard_listener.stop()
    # macros_run(track_actions)
