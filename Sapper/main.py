from random import randint

class Validator:
    """
    Класс-дескриптор для валидации значений атрибутов объекта Cell.
    Поддерживает атрибуты:
    - is_mine: bool
    - number: int (от 0 до 8)
    - is_open: bool
    """

    def __set_name__(self, owner: type, name: str) -> None:
        """Устанавливает имя атрибута для внутреннего использования."""
        self.name = f"_{owner.__name__}__{name}"

    def __get__(self, instance: object, owner: type):
        """Возвращает значение атрибута."""
        if instance is None: 
            return property()
        return getattr(instance, self.name)

    def veification(self, value: object) -> bool:
        """Проверяет значение атрибута на корректность."""
        if self.name.endswith(('is_mine', 'is_open')):
            return isinstance(value, bool)
        elif self.name.endswith('number'):
            return isinstance(value, int) and 0 <= value <= 8
        raise TypeError("Недопустимый тип значения")

    def __set__(self, instance: object, value: object) -> None:
        """Устанавливает значение атрибута, если оно корректно."""
        if not self.veification(value):
            raise ValueError("Недопустимое значение атрибута")
        setattr(instance, self.name, value)


class Cell:
    """
    Класс для представления клетки на игровом поле.
    Атрибуты:
    - is_mine (bool): Содержит ли клетка мину.
    - number (int): Количество мин вокруг клетки (от 0 до 8).
    - is_open (bool): Открыта ли клетка.
    """
    is_mine = Validator()
    number = Validator()
    is_open = Validator()

    def __init__(self) -> None:
        self.is_mine = False
        self.number = 0
        self.is_open = False

    def __bool__(self) -> bool:
        """Возвращает True, если клетка закрыта."""
        return not self.is_open


class GamePole:
    """
    Класс для представления игрового поля "Сапера".
    Атрибуты:
    - M (int): Количество строк на игровом поле.
    - N (int): Количество столбцов на игровом поле.
    - total_mines (int): Общее количество мин на поле.
    """
    __instance = None
    __is_exist = False

    def __new__(cls, *args, **kwargs):
        """Реализация паттерна Singleton для создания только одного экземпляра игрового поля."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, M: int, N: int, total_mines: int) -> None:
        if not self.__is_exist:
            self.M = M
            self.N = N
            self.total_mines = total_mines
            self.__pole_cells = [[Cell() for _ in range(self.N)] for _ in range(self.M)]
            GamePole.__is_exist = True

    @property
    def pole(self) -> list[list[Cell]]:
        """Возвращает текущее состояние игрового поля."""
        return self.__pole_cells

    def __create_mines(self) -> set[tuple[int, int]]:
        """Создает случайное размещение мин на поле."""
        mines = set()
        while len(mines) != self.total_mines:
            mines.add((randint(0, self.M - 1), randint(0, self.N - 1)))
        return mines

    def __add_around_mines(self, i: int, j: int) -> None:
        """Увеличивает счетчики number у клеток вокруг мины."""
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.M and 0 <= nj < self.N:
                self.pole[ni][nj].number += 1

    def init_pole(self) -> None:
        """Инициализирует игровое поле минами и счетчиками."""
        mines = self.__create_mines()
        for i, j in mines:
            self.pole[i][j].is_mine = True
            self.__add_around_mines(i, j)

    def open_cell(self, i: int, j: int) -> None:
        """Открывает клетку по указанным координатам."""
        if not (0 <= i < self.M and 0 <= j < self.N):
            raise IndexError('Некорректные индексы i, j клетки игрового поля')
        self.pole[i][j].is_open = True

    def show_pole(self) -> None:
        """Выводит текущее состояние игрового поля в консоль."""
        bomb = "💣"
        blue_square = "🔶"
        numbers = {
            0: "0️⃣", 1: "1️⃣", 2: "2️⃣", 
            3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 
            6: "6️⃣", 7: "7️⃣", 8: "8️⃣"
        }

        for row in self.pole:
            row_display = []
            for cell in row:
                if cell.is_open:
                    if cell.is_mine:
                        row_display.append(bomb)
                    else:
                        row_display.append(numbers[cell.number])
                else:
                    row_display.append(blue_square)
            print("".join(row_display))


# Тестирование
pole = GamePole(10, 20, 10)  # создается поле размерами 10x20 с общим числом мин 10
pole.init_pole()
if pole.pole[0][1]:
    pole.open_cell(0, 1)
if pole.pole[3][5]:
    pole.open_cell(3, 5)

try:
    pole.open_cell(30, 100)  # генерируется исключение IndexError
except IndexError as e:
    print(e)

pole.show_pole()
