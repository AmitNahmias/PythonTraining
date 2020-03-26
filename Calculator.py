class math_funcs(object):
    """This class include special math funcs"""

    @staticmethod
    def factorial(num: str):
        """Doing factorial math function"""
        fact = 1
        for n in range(1, int(num) + 1):
            fact = fact * n
        return fact

    @staticmethod
    def average(num1: int, num2: int):
        """"Doing average between two numbers"""
        avg = (num1 + num2) / 2
        return avg


class Calculator(object):
    """The class defines calculator with operations order"""

    def __init__(self, list_of_exercise: list):
        """
        Defines five different dictionaries according specific math orders,
        also getting a list that contains split string that represents math exercise.
        """
        self.list_of_exercise = list_of_exercise
        self.dict_of_operations_volume_5 = {"&": lambda num1, num2: min(num1, num2),
                                            "$": lambda num1, num2: max(num1, num2),
                                            "@": lambda num1, num2: math_funcs.average(num1, num2)}
        self.dict_of_operations_volume_4 = {"!": lambda num: math_funcs.factorial(num),
                                            "%": lambda num1, num2: num1 % num2}
        self.dict_of_operations_volume_3 = {"^": lambda num1, num2: num1 ** num2}
        self.dict_of_operations_volume_2 = {"*": lambda num1, num2: num1 * num2,
                                            "/": lambda num1, num2: num1 / num2}
        self.dict_of_operations_volume_1 = {"+": lambda num1, num2: num1 + num2,
                                            "-": lambda num1, num2: num1 - num2}
        self.list_of_dicts = [self.dict_of_operations_volume_5, self.dict_of_operations_volume_4,
                              self.dict_of_operations_volume_3, self.dict_of_operations_volume_2,
                              self.dict_of_operations_volume_1]

    def change_list(self, result, index: int):
        """The function changing list values after calculate"""
        self.list_of_exercise[index] = result
        self.list_of_exercise.pop(index + 1)
        self.list_of_exercise.pop(index - 1)

    def scan_and_calculate(self):
        """The function scan the exercise and calculating him according math order"""
        for dictionary in self.list_of_dicts:
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
    exercise = input("Write a exercise:")
    lst_from_exercise = exercise.split()
    my_instance = Calculator(lst_from_exercise)
    while len(lst_from_exercise) > 1:
        my_instance.scan_and_calculate()
    print(lst_from_exercise[0])


if __name__ == '__main__':
    main()
