# import PySimpleGUI as sg
#
# # help(sg.Column)
#
# test_list = list(range(20))
#
# def up_elem(button_key):
#     pass
#
# column1 = [
#     [sg.Button(f'up', key=f'up-{i}'), sg.Text(f'Scrollable {v}')] for i, v in enumerate(test_list)
# ]
#
# # column2 = [
# #     [sg.Text(f'Static{i}')] for i in range(10)
# # ]
#
# layout = [
#     [
#         sg.Column(column1, scrollable=True,  vertical_scroll_only=True, size=(1500, 600)),
#         # sg.Column(column2)
#     ]
# ]
#
# window = sg.Window(
#     'Scrollable',
#     layout,
#     # size=(2000, 1200)
# )
#
# while True:
#     event, values = window.read()
#     print(event)
#     print(values)
#     if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
#         break
#
# window.close()




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




# https://github.com/PySimpleGUI/PySimpleGUI/issues/3441
import PySimpleGUI as sg


def hide_header(tree):
    tree.Widget.configure(show='tree')

def key_to_id(key):
    for k, v in tree.IdToKey.items():
        if v == key:
            return k
    return None

def select(key=''):
    iid = key_to_id(key)
    if iid:
        tree.Widget.see(iid)
        tree.Widget.selection_set(iid)

def where():
    item = tree.Widget.selection()
    return '' if len(item) == 0 else tree.IdToKey[item[0]]

def move_up():
    key =  where()
    if key == '':
        return
    node = treedata.tree_dict[key]
    parent_node = treedata.tree_dict[node.parent]
    index = parent_node.children.index(node)
    if index != 0:
        parent_node.children[index-1], parent_node.children[index] = (
            parent_node.children[index], parent_node.children[index-1])
    tree.update(values=treedata)
    select(key)

def move_down():
    key = where()
    if key == '':
        return
    node = treedata.tree_dict[key]
    parent_node = treedata.tree_dict[node.parent]
    index = parent_node.children.index(node)
    if index != len(parent_node.children)-1:
        parent_node.children[index+1], parent_node.children[index] = (
            parent_node.children[index], parent_node.children[index+1])
    tree.update(values=treedata)
    select(key)

fruits = [
    "Apple", "Banana", "Cherry", "Durian", "Elderberry", "Guava", "Jackfruit",
    "Kiwi", "Lemon", "Mango", "Orange", "Papaya", "Strawberry", "Tomato",
    "Watermelon",
]

treedata = sg.TreeData()
for i, fruit in enumerate(fruits):
    treedata.Insert('', i, fruit, values=[f'Fruit {i:0>2d}'])

layout = [
    [sg.Button('Move Up'), sg.Button('Move Down')],
    [sg.Tree(data=treedata, key='TREE', headings=['Nothing'],
        select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
]

window = sg.Window('Tree', layout, finalize=True)
tree = window['TREE']
hide_header(tree)

while True:

    event, values = window.read()
    print(event, values)
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Move Up':
        move_up()
    elif event == 'Move Down':
        move_down()

window.close()