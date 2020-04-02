class Calculator(object):
    """The class defines calculator with operations order"""

    def __init__(self, list_of_exercise: list):
        """
        Defines five different dictionaries according specific math orders,
        also getting a list that contains split string that represents math exercise.
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
        """The function changing list values after calculate"""
        self.list_of_exercise[index] = result
        self.list_of_exercise.pop(index + 1)
        self.list_of_exercise.pop(index - 1)

    def handle_in_parenthesis(self, some_list: list):
        """ This function handel in use of [ ] in the exercise """
        if "[" in some_list:
            opening = some_list.index("[")
            if some_list[::-1].index("]") == 0:
                closing = len(some_list) - some_list[::-1].index("]") - 1
            else:
                closing = len(some_list) - some_list[::-1].index("]")
            temp_list = some_list[opening + 1:closing - 1]
            self.handle_in_parenthesis(temp_list)
            temp_instance = Calculator(temp_list)
            return temp_instance.calculate()

    def calculate(self):
        """The function calculating exercise according specific math order"""
        if "[" in self.list_of_exercise:
            self.list_of_exercise
            self.handle_in_parenthesis(self.list_of_exercise)
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


def main():
    exercise = input("Write an exercise:")
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
    my_instance = Calculator(lst_from_exercise_after_sort)
    while len(lst_from_exercise_after_sort) > 1:
        my_instance.calculate()
    print(lst_from_exercise_after_sort[0])


if __name__ == '__main__':
    main()
