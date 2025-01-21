class Validator:
    def __set_name__(self, owner, name) -> None:
        self.name = f"_{owner.__name__}__{name}"

    def __get__(self, instance, owner) -> any:
        return getattr(instance, self.name)
    
    def __set__(self, instance, value) -> None:
        setattr(instance, self.name, value)


class StackObj:
    data = Validator()
    next = Validator()

    def __init__(self, data: any) -> None:
        self.data = data
        self.next = None


class Stack:
    def __init__(self) -> None:
        self.top = None

    def push_back(self, obj: object) -> None:
        if not self.top:
            self.top = obj
        else:
            current = self.top
            while current.next:
                current = current.next
            current.next = obj

    def pop_back(self) -> object:
        if self.top is None:
            return None
        if self.top.next is None:
            obj = self.top
            self.top = None
            return obj
        current = self.top
        while current.next and current.next.next:
            current = current.next
        obj = current.next
        current.next = None
        return obj

    def __add__(self, obj: object) -> object:
        self.push_back(obj)
        return self

    def __iadd__(self, obj: object) -> object:
        self.push_back(obj)
        return self

    def __mul__(self, data_list: list) -> object:
        for data in data_list:
            self.push_back(StackObj(data))
        return self

    def __imul__(self, data_list: list) -> object:
        for data in data_list:
            self.push_back(StackObj(data))
        return self
    

if __name__ == "__main__":
    assert hasattr(Stack, 'pop_back'), "класс Stack должен иметь метод pop_back"

    st = Stack()
    top = StackObj("1")
    st.push_back(top)
    assert st.top == top, "неверное значение атрибута top"

    st = st + StackObj("2")
    st = st + StackObj("3")
    obj = StackObj("4")
    st += obj

    st = st * ['data_1', 'data_2']
    st *= ['data_3', 'data_4']
    st += StackObj("225")
    st.pop_back()

    d = ["1", "2", "3", "4", 'data_1', 'data_2', 'data_3', 'data_4']
    h = top
    i = 0
    while h:
        assert h._StackObj__data == d[i], "неверное значение атрибута __data, возможно, некорректно работают операторы + и *"
        h = h._StackObj__next
        i += 1
        
    assert i == len(d), "неверное число объектов в стеке"

    print("Все тесты пройдены успешно!")