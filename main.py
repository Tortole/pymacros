# import time
# from pynput import keyboard, mouse
# from screeninfo import get_monitors  
from actions_track import ActionsTrack  


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

    actions = trck.to_string()
    trck.from_string(actions)

    trck.run()

    #   # Получение данных о разрешении монитора
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
