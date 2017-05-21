from typing import List
from Stanford.Sudoku import utilities
import copy

ALL_NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9]


class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display_coordinate(self):
        print("{x}, {y}".format(x=self.x, y=self.y))


class Grid(Unit):
    def __init__(self, x, y, data):
        super().__init__(x, y)
        self.data = data

    def is_empty(self):
        if len(self.data) == 1 and self.data[0] == 0:
            return True
        return False

    def is_confirmed(self):
        if len(self.data) == 1 and self.data[0] != 0:
            return True
        return False

    def __repr__(self):
        return "{data}".format(data=self.data)


class SmallGrid(Unit):
    def __init__(self, x, y, length=3):
        super().__init__(x, y)
        self.length = length
        self.grid = []
        for i in range(0, 9):
            self.grid.append(Grid(i // 3, i % 3, []))

    def get_small_row(self, row_num: int):
        row_small_square = []
        for i in range(row_num * self.length, row_num * self.length + self.length):
            row_small_square.append(self.grid[i])
        return row_small_square

    def get_small_col(self, col_num: int):
        col_small_square = []
        for i in [x for x in range(0, self.length ** 2) if x % self.length == col_num]:
            col_small_square.append(self.grid[i])
        return col_small_square


class BigGrid:
    def __init__(self, length=3):
        self.length = length
        self.board = []

        for rowX in range(0, length):
            for colY in range(0, length):
                self.board.append(SmallGrid(rowX, colY))

    def get_row(self, row_num: int):
        row = []
        required_small_rows_grids = self.board[row_num // 3 * 3:row_num // 3 * 3 + 3]
        for small_grid in required_small_rows_grids:
            row.extend(small_grid.get_small_row(row_num % 3))
        return row

    def get_col(self, col_num: int):
        col = []
        required_small_cols_grids = self.board[col_num // 3:: self.length]
        for small_grid in required_small_cols_grids:
            col.extend(small_grid.get_small_col(col_num % 3))
        return col

    def get_all_rows(self):
        all_rows = []
        for i in range(0, 9):
            all_rows.extend(self.get_row(i))
        return all_rows

    def fill_in_data(self, filename):
        all_grids = self.get_all_rows()
        with open(filename) as file:
            data_str = file.read()
            data_str = data_str.replace("\n", "")
            data = data_str.split(",")
            for index, grid in enumerate(all_grids):
                grid.data = [int(data[index])]

    def display_board(self):
        all_data = self.get_all_rows()
        for i, grid in enumerate(all_data):
            if i % 9 == 0:
                print("\n")
            print(utilities.get_fixed_length_str(str(grid.data), 22), end=' ')


# class Snapshot:
#     def __init__(self, current_list_index=0):
#         self.operatingSquareIndex = 0
#         self.operatingPossibilityIndex = -1
#         self.failCountOnThisSnapshot = 0
#         self.snapshot_list = []
#         self.current_list_index = current_list_index
#         self.current_list = []
#         self.bigGrid = BigGrid()
#
#     def set_big_grid(self, big_grid):
#         self.bigGrid = big_grid
#
#     def list_copy(self):
#         self.current_list = copy.deepcopy(self.bigGrid.board)
#         self.snapshot_list.append(self.current_list)
#         print(self.snapshot_list)


class Solver:
    def __init__(self, length=3):
        self.length = length
        self.bigGrid = BigGrid()
        self.snapshot_list = []
        self.current_list = []

    def set_big_grid(self, big_grid):
        self.bigGrid = big_grid

    def list_copy(self):
        self.current_list = copy.deepcopy(self.bigGrid.board)
        self.snapshot_list.append(self.current_list)
        print(self.snapshot_list)

    def fill_in_possibilities(self, small_grid):
        current_numbers = []
        for index in range(0, self.length**2):
            for small in small_grid.grid:
                if not small.is_empty():
                    current_numbers.extend(small.data)
        possibilities = [x for x in ALL_NUMS if x not in current_numbers]
        for small in small_grid.grid:
            if small.is_empty():
                small.data = possibilities

    def calculate_possibility(self):
        for small_grid in self.bigGrid.board:
            self.fill_in_possibilities(small_grid)
        return self.bigGrid.board

    def filter_nine_grids(self, list: List[Grid]):
        if len(list) != 9:
            raise Exception("Unexpected Number of Elements")
        confirmed_num = []
        updated_flag = False
        for grid in list:
            if grid.is_confirmed():
                confirmed_num.extend(grid.data)
        for grid in list:
            if grid.is_confirmed():
                continue
            update_num = [x for x in grid.data if x not in confirmed_num]
            if update_num != grid.data:
                grid.data = update_num
                updated_flag = True
        return updated_flag

    def execute_filter(self):
        while True:
            break_flag = False
            for i in range(0, 9):
                row_flag = self.filter_nine_grids(self.bigGrid.get_row(i))
                col_flag = self.filter_nine_grids(self.bigGrid.get_col(i))
                small_grid_flag = self.filter_nine_grids(self.bigGrid.board[i].grid)
                if not any([row_flag, col_flag, small_grid_flag]):
                    break_flag = True
            if break_flag:
                break

    def max_two_elements_possibility(self):
        max_two_elements = 0
        max_two_elements_grid = 0
        for i in range(0, self.length ** 2):
            count = 0
            for j in range(0, self.length ** 2):
                if len(self.bigGrid.board[i].grid[j].data) == 2:
                    count += 1
            if count > max_two_elements:
                max_two_elements = count
                max_two_elements_grid = i
        return max_two_elements_grid

    def locate_grid_data(self):
        max_two_elements_grid = self.max_two_elements_possibility()
        count = []
        for i in range(0, self.length ** 2):
            if len(self.bigGrid.board[max_two_elements_grid].grid[i].data) == 2:
                count.append(i)
        return count

    def guess_possibilities(self):
        grid_number = self.max_two_elements_possibility()
        count = self.locate_grid_data()
        # self.list_copy()
        for i in range(len(count)):
            item = count[i]
            self.bigGrid.board[grid_number].grid[item].data = [self.bigGrid.board[grid_number].grid[item].data[0]]
            # print("hello")
            self.execute_filter()

    def is_all_die(self):
        all_data = self.bigGrid.get_all_rows()
        for i in range(self.length**2**2):
            if len(all_data[i].data) == 0:
                return True
        return False

    def is_all_success(self):
        all_data = self.bigGrid.get_all_rows()
        for i in range(self.length**2**2):
            if len(all_data[i].data) == 1 and all_data[i].data != 0:
                return True
        return False

    def cont_filter(self):
        while True:
            self.list_copy()
            count = 0
            self.guess_possibilities()
            if self.is_all_die():
                # print("die")
                count += 1
                self.bigGrid.board = self.snapshot_list[count-1]

            if self.is_all_success():
                break



if __name__ == '__main__':
    bigGrid = BigGrid()
    bigGrid.fill_in_data("data.txt")
    solver = Solver()
    solver.set_big_grid(bigGrid)
    solver.calculate_possibility()
    solver.execute_filter()

    solver.max_two_elements_possibility()
    solver.guess_possibilities()
    solver.cont_filter()

    # snapshot = Snapshot()
    bigGrid.display_board()
    print("\n")

    # snapshot.set_big_grid(bigGrid)
    # snapshot.list_copy()
    # snapshot.deepcopy()
    # solver.snapshot()
    # solver.grid_possibilities()
    # solver.execute_filter()
    # solver = Solver()
    # solver.check()

    print("\n")
    print("Done")
