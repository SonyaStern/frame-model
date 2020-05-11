import json
import os
from copy import deepcopy

import settings
from frames.model.Slot import Slot

frames = dict()


class Frame:

    def __init__(self, name, parent):
        self._name = name
        self._slots = {}
        self._children = {}
        self._parent = parent

    @property
    def name(self):
        return self._name

    @property
    def slots(self):
        return self._slots

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    @staticmethod
    def save_to_db():
        """
        Сохранение в базу данных (файл формата JSON)
        """
        data = []
        file_path = settings.DB_FILE_PATH

        for element in frames.values():
            data.append(element.serialize())
            print('Схема "{}" сохранена в {}\n'.format(element, file_path))

        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=1, ensure_ascii=False)

    @staticmethod
    def create_or_update_frame(data, parent=None):
        """
        Сохранение/обновление фрейма и его полей
        """
        frame = Frame(data['name'], parent)
        for element in data['slots']:
            slot_name = element.pop('name')
            slot_class = element.pop('class')
            slot_type = element.pop('type')
            slot_value = element.pop('value')
            slot = Slot(slot_name, slot_class, slot_type, slot_value)
            frame.slots[slot_name] = slot

        if "children" in data:
            for element in data['children']:
                child = Frame.create_or_update_frame(element, frame)
                frame.children[child.name] = child

        frames.update({frame.name: frame})
        return frame

    @staticmethod
    def add_child(parent, child_frame):
        """
        Добавление дочернего фрейма
        """
        parent = frames.get(parent['name'])
        child_frame = Frame.create_or_update_frame(child_frame)
        parent.children[child_frame.name] = child_frame
        frames.update({parent.name: parent})

    @staticmethod
    def delete(frame):
        """
        Удаоение фрейма
        """
        if frames.keys().__contains__(frame.name):
            frames.__delitem__(frame.name)
            print('{} was deleted\n'.format(frame.name))

    @staticmethod
    def strict_search(slots_prototype):
        """
        Строгий поиск
        """
        found = []
        for db_frame in frames.values():
            db_slots = db_frame.slots
            copy = deepcopy(db_slots)
            for slot_proto in slots_prototype:
                for db_element in db_slots.values():
                    if db_element.eq(slot_proto):
                        copy.pop(db_element.name)
            if copy.__len__() == 0:
                found.append(db_frame)
        return found

    @staticmethod
    def wide_search(slots_prototype):
        """
        Широкий поиск
        """
        found = []
        for db_frame in frames.values():
            db_slots = db_frame.slots
            copy = deepcopy(db_slots)
            for slot_proto in slots_prototype:
                for db_element in db_slots.values():
                    if db_element.eq(slot_proto):
                        copy.pop(db_element.name)
            if copy.__len__() < db_slots.__len__():
                found.append(db_frame)
        return found

    @staticmethod
    def search(slots, type_):
        if type_.__eq__('strict'):
            return Frame.strict_search(slots)
        else:
            return Frame.wide_search(slots)

    def serialize(self):
        data = {
            attr: getattr(self, attr).value
            for attr in dir(self)
            if isinstance(getattr(self, attr), Slot)
        }
        data['name'] = self.name
        data['slots'] = []
        for slot in self.slots.values():
            slot_data = {
                'name': slot.name,
                'class': slot.class_,
                'type': slot.type,
                'value': slot.value
            }
            data['slots'].append(slot_data)
        data['children'] = []
        for child in self.children.values():
            data['children'].append(child.serialize())

        return data

    @classmethod
    def deserialize(cls, data):
        """
        :type data: dict
        """
        frame = Frame(cls)

        for key, value in data.items():
            getattr(frame, key).value = value

        return frame

    @classmethod
    def load_from_db(cls):
        """
        Загрузка фрейма из базы данных (файл формата JSON)
        """
        file_path = settings.DB_FILE_PATH

        if os.stat(file_path).st_size != 0:
            with open(file_path, 'r') as infile:
                data = json.load(infile)
                for element in data:
                    scheme = Frame.create_or_update_frame(element)
                    print('Схема "{}" загружена из {}\n'.format(scheme, file_path))

            return scheme
        else:
            print('DB is empty')
