import PySimpleGUI as sg

# help(sg.Column)

test_list = list(range(20))

def up_elem(button_key):
    pass

column1 = [
    [sg.Button(f'up', key=f'up-{i}'), sg.Text(f'Scrollable {v}')] for i, v in enumerate(test_list) 
]

# column2 = [
#     [sg.Text(f'Static{i}')] for i in range(10) 
# ]

layout = [
    [
        sg.Column(column1, scrollable=True,  vertical_scroll_only=True, size=(1500, 600)),
        # sg.Column(column2)
    ]
]

window = sg.Window(
    'Scrollable',
    layout,
    # size=(2000, 1200)
)

while True:
    event, values = window.read()
    print(event)
    print(values)
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

window.close()




# import PySimpleGUI as sg

# sg.theme('DarkAmber')   # Add a touch of color
# # All the stuff inside your window.
# layout = [  [sg.Text('Some text on Row 1')],
#             [sg.Text('Enter something on Row 2'), sg.InputText()],
#             [sg.Button('Ok'), sg.Button('Cancel')] ]

# # Create the Window
# window = sg.Window('Window Title', layout)
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
#         break
#     print('You entered ', values[0])

# window.close()