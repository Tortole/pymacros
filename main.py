from pynput import keyboard, mouse
from screeninfo import get_monitors

# !!!
import time


is_listen_run = False
hotkey_macros_write = keyboard.Key.scroll_lock
is_mouse_button_press = False
primary_monitor_resolution = {}


def coord_to_string(x, y):
    return f'x{x / primary_monitor_resolution["width"]:.2f}y{y / primary_monitor_resolution["height"]:.2f}'


def mouse_buttom_to_string(button):
    if button == mouse.Button.left:
        return 'l'


def on_move_mouse_track(x, y, track_mouse_actions):
    if is_mouse_button_press:
        track_mouse_actions.append(f'mm{coord_to_string(x, y)}')
    # print('Pointer moved to {0}'.format((x, y)))


def on_click_mouse_track(x, y, button, is_pressed, track_mouse_actions):
    if is_pressed:
        track_mouse_actions.append(f'mp{button.value}{coord_to_string(x, y)}')
    else:
        track_mouse_actions.append(f'mr{button.value}{coord_to_string(x, y)}')
    print(track_mouse_actions[-1])
    # print('{0} {1} at {2}'.format('Pressed' if is_pressed else 'Released', button, (x, y)))
    # if not pressed:
    #     # Stop listener
    #     return False


def on_scroll_mouse_track(x, y, dx, dy, track_mouse_actions):
    track_mouse_actions.append(f'ms{dx:+}{dy:+}{coord_to_string(x, y)}')
    print(track_mouse_actions[-1])
    # print('Scrolled {0} {1} at {2}'.format('down' if dy < 0 else 'up', dx, (x, y)))


def key_to_string(key):
    try:
        return f'{key.char}'
    except AttributeError:
        return f'{str(key.value)[1:-1]:0>3}'


def on_press_keyboard_track(key, track_keyboard_actions, pressed_keys):
    key_pressed = key_to_string(key)
    if key_pressed not in key_pressing:
        pressed_keys.add(key_pressed)
        # print('kp' + key_pressed)
        track_keyboard_actions.append('kp' + key_pressed)


def on_release_keyboard_track(key, track_keyboard_actions, pressed_keys):
    key_pressed = key_to_string(key)
    pressed_keys.remove(key_pressed)
    # print('kr' + key_pressed)
    track_keyboard_actions.append('kr' + key_pressed)


def on_stop_listeners(key):
    if key == hotkey_macros_write:
        keyboard_listener.stop()
        mouse_listener.stop()
        global is_listen_run
        is_listen_run = False

    # if key == keyboard.Key.scroll_lock:
    #     # Stop listener
    #     # file_out.close()
    #     return False


def macros_run():
    keyboard_controller = keyboard.Controller()
    # controller.press("<ctrl>")
    for t_a in track_actions:
        if t_a[0] == 'k':
            key = t_a[2:]
            if len(key) > 1:
                key = keyboard.KeyCode.from_vk(int(key))

            if t_a[1] == 'p':
                keyboard_controller.press(key)
            elif t_a[1] == 'r':
                keyboard_controller.release(key)


# def on_activate():
#     print('Global hotkey activated!')
#
#
# def for_canonical(f):
#     print('for_canonical')
#     return lambda k: f(l.canonical(k))


if __name__ == '__main__':
    '''
    
    
    
    '''

    # Получение данных о разрешении монитора
    for m in get_monitors():
        if m.is_primary:
            primary_monitor_resolution['width'] = m.width
            primary_monitor_resolution['height'] = m.height
            break

    key_pressing = set()
    track_actions = []
    is_listen_run = False

    hotkey_listener = keyboard.Listener(
        # on_press=,
        on_release=on_stop_listeners
    )
    hotkey_listener.start()

    # file_out = open("key_pressed_history.txt", "w")

    # Collect events until released
    # with keyboard.Listener(
    #         on_press=on_press,
    #         on_release=on_release
    #     ) as listener:
    #     listener.join()

    # Прослушка клавиатуры
    keyboard_listener = keyboard.Listener(
        on_press=lambda key: on_press_keyboard_track(key, track_actions, key_pressing),
        on_release=lambda key: on_release_keyboard_track(key, track_actions, key_pressing)
    )
    keyboard_listener.start()

    # Прослушка мыши
    mouse_listener = mouse.Listener(
        on_move=lambda x, y: on_move_mouse_track(x, y, track_actions),
        on_click=lambda x, y, b, p: on_click_mouse_track(x, y, b, p, track_actions),
        on_scroll=lambda x, y, dx, dy: on_scroll_mouse_track(x, y, dx, dy, track_actions))
    mouse_listener.start()

    is_listen_run = True

    while is_listen_run:
        pass

    # time.sleep(3)
    # listener.stop()
    macros_run()

    # hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<alt>+h'),
    #                          on_activate)
    # with keyboard.Listener(on_press=for_canonical(hotkey.press),
    #                        on_release=for_canonical(hotkey.release)) as l:
    #     l.join()
