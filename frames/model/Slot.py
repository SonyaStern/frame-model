class Slot:
    def __init__(self, name, class_, type_, value):
        self._name = name
        self._class = class_
        self._type = type_
        self._value = value

    def eq(self, other):
        if not isinstance(other, Slot):
            return NotImplemented

        return self.name == other.name and \
               self.class_ == other.class_ and \
               self.type == other.type and \
               self.value == other.value


    @property
    def name(self):
        return self._name

    @property
    def class_(self):
        return self._class

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def print(self, depth):
        if self._value is not None:
            print(" " * depth + self._name + ": " + str(self._value))
