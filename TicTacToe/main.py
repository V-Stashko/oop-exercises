from random import choice


class Cell:
    """Класс для ячейки игрового поля."""
    def __init__(self, value: int = 0):
        """Инициализирует ячейку с заданным значением (по умолчанию 0)."""
        self.value = value

    def __bool__(self) -> bool:
        """Возвращает True, если ячейка пуста (value == 0)."""
        return self.value == 0

    def __str__(self) -> str:
        """Возвращает символ для отображения ячейки (⬜, ❌, ⭕)."""
        return {0: '⬜', 1: '❌', 2: '⭕'}[self.value]


class TicTacToe:
    """Класс для игры в крестики-нолики."""
    FREE_CELL = 0
    HUMAN_X = 1
    COMPUTER_O = 2

    def __init__(self):
        """Инициализирует игровое поле."""
        self.init()

    def init(self) -> None:
        """Создает новое пустое игровое поле."""
        self.pole = tuple([tuple([Cell(self.FREE_CELL) for _ in range(3)]) for _ in range(3)])

    def __check_index(self, i: int, j: int) -> bool:
        """Проверяет правильность индексов (от 0 до 2)."""
        if not (0 <= i < 3 and 0 <= j < 3):
            raise IndexError('некорректные индексы')
        return True

    def __getitem__(self, index: tuple[int, int]) -> int:
        """Возвращает значение ячейки по индексам."""
        i, j = index
        if self.__check_index(i, j):
            return self.pole[i][j].value

    def __setitem__(self, index: tuple[int, int], value: int) -> None:
        """Устанавливает значение ячейки по индексам."""
        i, j = index
        if self.__check_index(i, j):
            self.pole[i][j].value = value

    def show(self) -> None:
        """Отображает игровое поле."""
        for row in self.pole:
            print(" ".join(str(col) for col in row))
        print()

    def get_free_cells(self) -> list[tuple[int, int]]:
        """Возвращает список всех пустых клеток."""
        return [(i, j) for i in range(3) for j in range(3) if bool(self.pole[i][j])]

    def human_go(self):
        """Запрос хода игрока."""
        while True:
            i = input('Введите индекс строки (0 - 2): ')
            j = input('Введите индекс столбца (0 - 2): ')
            
            if not (i.isdigit() and j.isdigit()) or not (0 <= int(i) <= 2 and 0 <= int(j) <= 2):
                print('\nИндекс должен быть целым числом от 0 до 2 включительно\n')
                continue

            i = int(i)
            j = int(j)

            if (i, j) not in self.get_free_cells():
                print('\nКлетка занята\n')
                continue

            break
        self.__setitem__((i, j), self.HUMAN_X)

    def computer_go(self) -> None:
        """Ход компьютера (выбор случайной клетки)."""
        self.__setitem__(choice(self.get_free_cells()), self.COMPUTER_O)

    def __check_victory(self, value: int) -> bool:
        """Проверяет наличие победы или ничьей."""
        # Проверка выигрышных комбинаций
        for row in self.pole:
            if all(cell.value == value for cell in row):
                return True
        for col in range(3):
            if all(self.pole[row][col].value == value for row in range(3)):
                return True
        if all(self.pole[i][i].value == value for i in range(3)):
            return True
        if all(self.pole[i][2 - i].value == value for i in range(3)):
            return True
        # Проверка на ничью
        if value == 3 and all(cell.value != self.FREE_CELL for row in self.pole for cell in row):
            return not self.is_human_win and not self.is_computer_win
        return False

    @property
    def is_human_win(self) -> bool:
        """Проверка победы игрока (человека)."""
        return self.__check_victory(self.HUMAN_X)

    @property
    def is_computer_win(self) -> bool:
        """Проверка победы компьютера."""
        return self.__check_victory(self.COMPUTER_O)

    @property
    def is_draw(self) -> bool:
        """Проверка на ничью."""
        return self.__check_victory(3)

    def __bool__(self) -> bool:
        """Проверяет, продолжается ли игра."""
        return not (self.is_human_win or self.is_computer_win or self.is_draw)


# test
cell = Cell()
assert cell.value == 0, "начальное значение атрибута value объекта класса Cell должно быть равно 0"
assert bool(cell), "функция bool для объекта класса Cell вернула неверное значение"
cell.value = 1
assert bool(cell) == False, "функция bool для объекта класса Cell вернула неверное значение"

assert hasattr(TicTacToe, 'show') and hasattr(TicTacToe, 'human_go') and hasattr(TicTacToe, 'computer_go'), "класс TicTacToe должен иметь методы show, human_go, computer_go"

game = TicTacToe()
assert bool(game), "функция bool вернула неверное значения для объекта класса TicTacToe"
assert game[0, 0] == 0 and game[2, 2] == 0, "неверные значения ячеек, взятые по индексам"
game[1, 1] = TicTacToe.HUMAN_X
assert game[1, 1] == TicTacToe.HUMAN_X, "неверно работает оператор присваивания нового значения в ячейку игрового поля"

game[0, 0] = TicTacToe.COMPUTER_O
assert game[0, 0] == TicTacToe.COMPUTER_O, "неверно работает оператор присваивания нового значения в ячейку игрового поля"

game.init()
assert game[0, 0] == TicTacToe.FREE_CELL and game[1, 1] == TicTacToe.FREE_CELL, "при инициализации игрового поля все клетки должны принимать значение из атрибута FREE_CELL"

try:
    game[3, 0] = 4
except IndexError:
    assert True
else:
    assert False, "не сгенерировалось исключение IndexError"

game.init()
assert game.is_human_win == False and game.is_computer_win == False and game.is_draw == False, "при инициализации игры атрибуты is_human_win, is_computer_win, is_draw должны быть равны False, возможно не пересчитывается статус игры при вызове метода init()"

game[0, 0] = TicTacToe.HUMAN_X
game[1, 1] = TicTacToe.HUMAN_X
game[2, 2] = TicTacToe.HUMAN_X
assert game.is_human_win and game.is_computer_win == False and game.is_draw == False, "некорректно пересчитываются атрибуты is_human_win, is_computer_win, is_draw. Возможно не пересчитывается статус игры в момент присвоения новых значения по индексам: game[i, j] = value"

game.init()
game[0, 0] = TicTacToe.COMPUTER_O
game[1, 0] = TicTacToe.COMPUTER_O
game[2, 0] = TicTacToe.COMPUTER_O
assert game.is_human_win == False and game.is_computer_win and game.is_draw == False, "некорректно пересчитываются атрибуты is_human_win, is_computer_win, is_draw. Возможно не пересчитывается статус игры в момент присвоения новых значения по индексам: game[i, j] = value"

# game
game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")