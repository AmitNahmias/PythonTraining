class Calculator(object):
    """ The class defines calculator with operations order according to specific instructions """

    def __init__(self, list_of_exercise: list):
        """
        Defines five different dictionaries according specific math orders,
        also getting a list that contains split string that represents math exercise.
        @param list_of_exercise: list that contains exercise :list
        """
        self.list_of_exercise = list_of_exercise
        self.dict_of_operations_prioritize_5 = {"&": lambda num1, num2: min(num1, num2),
                                                "$": lambda num1, num2: max(num1, num2),
                                                "@": lambda num1, num2: (num1 + num2) / 2}
        self.dict_of_operations_prioritize_4 = {"!": lambda fact, num: num * fact(fact, num - 1) if num > 0 else 1,
                                                "%": lambda num1, num2: num1 % num2}
        self.dict_of_operations_prioritize_3 = {"^": lambda num1, num2: num1 ** num2}
        self.dict_of_operations_prioritize_2 = {"*": lambda num1, num2: num1 * num2,
                                                "/": lambda num1, num2: num1 / num2}
        self.dict_of_operations_prioritize_1 = {"+": lambda num1, num2: num1 + num2,
                                                "-": lambda num1, num2: num1 - num2}
        self.list_of_prioritize = [self.dict_of_operations_prioritize_5, self.dict_of_operations_prioritize_4,
                                   self.dict_of_operations_prioritize_3, self.dict_of_operations_prioritize_2,
                                   self.dict_of_operations_prioritize_1]

    def change_list(self, result, index: int):
        """
        Changing list values after calculate
        @param result: the result of the calculate
        @param index: the index of the result should be in the list
        """
        self.list_of_exercise[index] = result
        self.list_of_exercise.pop(index + 1)
        self.list_of_exercise.pop(index - 1)

    def exercise_handler(self):
        """ This function handle in use of [ ] in the exercise and using calculate method"""
        while "[" in self.list_of_exercise:
            temp_list = []
            opening = len(self.list_of_exercise) - self.list_of_exercise[::-1].index("[") - 1
            closing = self.list_of_exercise.index("]")
            index = closing
            while index >= opening:
                temp_list.insert(0, self.list_of_exercise.pop(index))
                index -= 1
            temp_list.pop(0)
            temp_list.pop(len(temp_list) - 1)
            temp_instance_of_calc = Calculator(temp_list)
            result = temp_instance_of_calc.calculate()
            self.list_of_exercise.insert(opening, result)
        else:
            self.calculate()

    def calculate(self):
        """The function calculating exercise according specific math order"""
        for dictionary in self.list_of_prioritize:
            i = 0
            while i < len(self.list_of_exercise):
                sign = self.list_of_exercise[i]
                if sign == "!":
                    result = dictionary[sign](int(self.list_of_exercise[self.list_of_exercise.index(sign) - 1]))
                    self.change_list(result, self.list_of_exercise.index(sign))
                    i -= 1
                elif sign in dictionary.keys():
                    result = dictionary[sign](int(self.list_of_exercise[self.list_of_exercise.index(sign) - 1]),
                                              int(self.list_of_exercise[self.list_of_exercise.index(sign) + 1]))
                    self.change_list(result, self.list_of_exercise.index(sign))
                    i -= 2
                i += 1
        return self.list_of_exercise[0]


def sorting_exercise_to_list(exercise: str):
    """
    Sorting string that contains exercise to new list
    @param exercise: contains exercise :str
    @return: list that contains the exercise
    """
    lst_from_exercise = []
    for p in exercise:
        if p != " ":
            lst_from_exercise.append(p)
    lst_from_exercise_after_sort = [""]
    temp = ""
    for pos in lst_from_exercise:
        if pos.isnumeric():
            temp = temp + pos
        else:
            if pos in ["[", "]"]:
                if pos == "]":
                    lst_from_exercise_after_sort.append(temp)
                    temp = ""
                    lst_from_exercise_after_sort.append(pos)
                else:
                    lst_from_exercise_after_sort.append(pos)
            else:
                if lst_from_exercise_after_sort[-1] == "]":
                    lst_from_exercise_after_sort.append(pos)
                else:
                    lst_from_exercise_after_sort.append(temp)
                    temp = ""
                    lst_from_exercise_after_sort.append(pos)
    lst_from_exercise_after_sort.append(temp)
    lst_from_exercise_after_sort.pop(0)
    lst_from_exercise_after_sort.pop(len(lst_from_exercise_after_sort) - 1)
    return lst_from_exercise_after_sort


def main():
    """
    main() -> NoneType
    Control the flow of the program
    """
    exercise = input("Write an exercise:")
    my_lst = sorting_exercise_to_list(exercise)
    my_instance = Calculator(my_lst)
    while len(my_lst) > 1:
        my_instance.exercise_handler()
    print(my_lst[0])


if __name__ == '__main__':
    main()
