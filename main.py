from frames.model.Frame import Frame
from frames.model.Slot import Slot


def main():
    Frame.load_from_db()
    data = {'name': 'frame1', 'slots':
        [{'name': 'slot1', 'class': 'class1', 'type': 'type1', 'value': 'value1'}
         ]
            }
    slot1 = Slot('slot1', 'class1', 'type1', 'value1')
    slot2 = Slot('slot2', 'class2', 'type2', 'value2')
    slot3 = Slot('slot33', 'class2', 'type2', 'value2')
    slots = [slot1, slot2]
    slots1 = [slot3]
    child_data = {'name': 'frame1.1', 'slots':
        [{'name': 'slot1', 'class': 'class1', 'type': 'type1', 'value': 'value1'},
         {'name': 'slot2', 'class': 'class2', 'type': 'type2', 'value': 'value2'}
         ]
                  }
    data2 = {'name': 'frame2', 'slots':
        [{'name': 'slot1', 'class': 'class1', 'type': 'type1', 'value': 'value1'},
         {'name': 'slot2', 'class': 'class2', 'type': 'type2', 'value': 'value2'}
         ],
             'children':
                 [
                     {'name': 'frame2.1', 'slots':
                         [{'name': 'slot1', 'class': 'class1', 'type': 'type1', 'value': 'value1'},
                          {'name': 'slot2', 'class': 'class2', 'type': 'type2', 'value': 'value2'}
                          ]
                      }
                 ]
             }
    Frame.create_or_update_frame(data)
    # Frame.create_or_update_frame(data2)
    # Frame.delete(frame1)
    # Frame.add_child(data, child_data)
    print(Frame.search(slots, 'strict'))
    print(Frame.search(slots1, 'wide'))

    Frame.save_to_db()


if __name__ == '__main__':
    main()
