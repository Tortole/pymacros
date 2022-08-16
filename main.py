import time
from pynput import keyboard, mouse
from screeninfo import get_monitors


is_listen_run = False
hotkey_macros_write = keyboard.Key.scroll_lock
primary_monitor_resolution = {}


def coord_to_string(x, y):
    return f'{x / primary_monitor_resolution["width"]:.2f}{y / primary_monitor_resolution["height"]:.2f}'


def string_to_coord(str_coord):
    return round(float(str_coord[:4]) * primary_monitor_resolution['width']), \
           round(float(str_coord[4:]) * primary_monitor_resolution['height'])


mouse_buttom_to_string = {
    mouse.Button.left: 'l',
    mouse.Button.right: 'r',
    mouse.Button.middle: 'm'
}
string_to_mouse_button = {v: k for k, v in mouse_buttom_to_string.items()}


def on_move_mouse_track(x, y, track_mouse_actions):
    # track_mouse_actions.append(f'm{coord_to_string(x, y)}m')
    pass


def on_click_mouse_track(x, y, button, is_pressed, track_mouse_actions):
    track_mouse_actions.append(
        f'm'
        f'{coord_to_string(x, y)}'
        f'{"p" if is_pressed else "r"}'
        f'{mouse_buttom_to_string[button]}'
    )


def on_scroll_mouse_track(x, y, dx, dy, track_mouse_actions):
    track_mouse_actions.append(f'm{coord_to_string(x, y)}s{dx:+}{dy:+}')


def key_to_string(key):
    try:
        return key.char
    except AttributeError:
        return f'{str(key.value)[1:-1]:0>3}'


def on_press_keyboard_track(key, track_keyboard_actions, pressed_keys):
    key_pressed = key_to_string(key)
    if key_pressed not in key_pressing:
        pressed_keys.add(key_pressed)
        track_keyboard_actions.append(f'kp{key_pressed}')


def on_release_keyboard_track(key, track_keyboard_actions, pressed_keys):
    key_released = key_to_string(key)
    pressed_keys.discard(key_released)
    track_keyboard_actions.append(f'kp{key_released}')


def on_stop_listeners(key):
    if key == hotkey_macros_write:
        keyboard_listener.stop()
        mouse_listener.stop()
        global is_listen_run
        is_listen_run = False


def macros_run():
    keyboard_controller = keyboard.Controller()
    mouse_controller = mouse.Controller()

    for t_a in track_actions:
        time.sleep(0.2)
        # Действия клавиатуры
        if t_a[0] == 'k':
            key = t_a[2:]
            if len(key) > 1:
                key = keyboard.KeyCode.from_vk(int(key))

            # Нажатие клавиши клавиатуры
            if t_a[1] == 'p':
                keyboard_controller.press(key)
            # Отпуск клавиши клавиатуры
            elif t_a[1] == 'r':
                keyboard_controller.release(key)

        # Действия мыши
        elif t_a[0] == 'm':
            position_dx, position_dy = string_to_coord(t_a[1:9])
            position_dx -= mouse_controller.position[0]
            position_dy -= mouse_controller.position[1]
            mouse_controller.move(position_dx, position_dy)

            # Прокручивание колёсика
            if t_a[9] == 's':
                dx = int(t_a[10:12])
                dy = int(t_a[12:14])
                mouse_controller.scroll(dx, dy)
            # Нажатие клавиши мыши
            elif t_a[9] == 'p':
                mouse_controller.press(string_to_mouse_button[t_a[10]])
            # Отпуск клавиши мыши
            elif t_a[9] == 'r':
                mouse_controller.release(string_to_mouse_button[t_a[10]])


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
        on_release=on_stop_listeners
    )
    hotkey_listener.start()

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

    # file_out = open("key_pressed_history.txt", "w")

    macros_run()
