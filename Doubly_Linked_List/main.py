class Validator:
    def __set_name__(self, owner, name) -> None:
        self.name = f"_{owner.__name__}__{name}"

    def __get__(self, instance, owner) -> any:
        return getattr(instance, self.name)
    
    def __set__(self, instance, value) -> None:
        setattr(instance, self.name, value)


class ObjList:
    prev = Validator()
    next = Validator()
    data = Validator()

    def __init__(self, data: any) -> None:
        self.data = data
        self.prev = None
        self.next = None


class LinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def add_obj(self, obj: ObjList) -> None:
        if not self.head:
            self.head = self.tail = obj
        else:
            self.tail.next = obj
            obj.prev = self.tail
            self.tail = obj

    def get_obj_indx(self, indx: int) -> ObjList:
        if indx < 0 or indx >= len(self):
            raise IndexError("Индекс вне допустимого диапазона")

        count = 0
        current = self.head
        
        while count != indx:
            count += 1
            current = current.next

        return current

    def remove_obj(self, indx: int) -> None:
        current = self.get_obj_indx(indx)

        if current == self.head:
            self.head = current.next
            if self.head:
                self.head.prev = None

        elif current == self.tail:
            self.tail = current.prev
            if self.tail:
                self.tail.next = None

        else:
            current.prev.next = current.next
            current.next.prev = current.prev

        if self.head is None:
            self.tail = None

        del current

    def __len__(self) -> int:
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def __call__(self, indx: int) -> any:
        return self.get_obj_indx(indx).data


if __name__ == "__main__":
    ln = LinkedList()
    ln.add_obj(ObjList("Сергей"))
    ln.add_obj(ObjList("Балакирев"))
    ln.add_obj(ObjList("Python ООП"))
    ln.remove_obj(2)

    assert len(ln) == 2, "функция len вернула неверное число объектов в списке, возможно, неверно работает метод remove_obj()"
    ln.add_obj(ObjList("Python"))
    assert ln(2) == "Python", "неверное значение атрибута __data, взятое по индексу"
    assert len(ln) == 3, "функция len вернула неверное число объектов в списке"
    assert ln(1) == "Балакирев", "неверное значение атрибута __data, взятое по индексу"

    n = 0
    h = ln.head
    while h:
        assert isinstance(h, ObjList)
        h = h._ObjList__next
        n += 1

    assert n == 3, "при перемещении по списку через __next не все объекты перебрались"

    n = 0
    h = ln.tail
    while h:
        assert isinstance(h, ObjList)
        h = h._ObjList__prev
        n += 1

    assert n == 3, "при перемещении по списку через __prev не все объекты перебрались"

    print("Все тесты пройдены успешно!")
