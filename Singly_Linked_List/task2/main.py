class StackObj:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None
        self.__len = 0


    def push_back(self, obj):
        if self.top is None:
            self.top = obj
        else:
            current = self.top
            while current.next:
                current = current.next
            current.next = obj

        self.__len += 1


    def push_front(self, obj):
        current = self.top
        self.top = obj
        self.top.next = current
        
        self.__len += 1


    def _check_index(self, index):
        if not (0 <= index < self.__len):
            raise IndexError('неверный индекс')
        return True
    

    def _get_obj(self, index):
        if self._check_index(index):
            current_index = 0
            current_obj = self.top
            while current_index < index:
                current_obj = current_obj.next
                current_index += 1

            return current_obj
    
    
    def __getitem__(self, index):
        return self._get_obj(index).data
    

    def __setitem__(self, index, value):
        self._get_obj(index).data = value


    def __iter__(self):
        index = 0

        while index < self.__len:
            yield self._get_obj(index)
            index += 1

    

st = Stack()
st.push_back(StackObj("1"))
st.push_front(StackObj("2"))

assert st[0] == "2" and st[1] == "1", "неверные значения данных из объектов стека, при обращении к ним по индексу"

st[0] = "0"
assert st[0] == "0", "получено неверное значение из объекта стека, возможно, некорректно работает присваивание нового значения объекту стека"

for obj in st:
    assert isinstance(obj, StackObj), "при переборе стека через цикл должны возвращаться объекты класса StackObj"

try:
    a = st[3]
except IndexError:
    assert True
else:
    assert False, "не сгенерировалось исключение IndexError"