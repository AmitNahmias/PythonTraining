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
    """The class defines special calculator """

    def __init__(self, list_of_exercise: str):
        self.list_of_exercise = list_of_exercise

    def scanner(self):
        """The method scan for the most powerful sign"""
        if "&" in self.list_of_exercise:
            index = self.list_of_exercise.index('&')
            result = min(self.list_of_exercise[index - 1], self.list_of_exercise[index + 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)
        elif "$" in self.list_of_exercise:
            index = self.list_of_exercise.index('$')
            result = max(self.list_of_exercise[index - 1], self.list_of_exercise[index + 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)
        elif "@" in self.list_of_exercise:
            index = self.list_of_exercise.index('@')
            result = math_funcs.average(int(self.list_of_exercise[index + 1]), int(self.list_of_exercise[index - 1]))
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)
        elif "!" in self.list_of_exercise:
            index = self.list_of_exercise.index('!')
            result = math_funcs.factorial(self.list_of_exercise[index - 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index - 1)
        elif "%" in self.list_of_exercise:
            index = self.list_of_exercise.index('%')
            result = int(self.list_of_exercise[index - 1]) % int(self.list_of_exercise[index + 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)
        elif "^" in self.list_of_exercise:
            index = self.list_of_exercise.index('^')
            result = int(self.list_of_exercise[index - 1]) ** int(self.list_of_exercise[index + 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)
        elif "*" in self.list_of_exercise:
            index = self.list_of_exercise.index('*')
            result = int(self.list_of_exercise[index - 1]) * int(self.list_of_exercise[index + 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)
        elif "/" in self.list_of_exercise:
            index = self.list_of_exercise.index('/')
            result = int(self.list_of_exercise[index - 1]) / int(self.list_of_exercise[index + 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)
        elif "+" in self.list_of_exercise:
            index = self.list_of_exercise.index('+')
            result = int(self.list_of_exercise[index - 1]) + int(self.list_of_exercise[index + 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)
        elif "-" in self.list_of_exercise:
            index = self.list_of_exercise.index('-')
            result = int(self.list_of_exercise[index - 1]) - int(self.list_of_exercise[index + 1])
            self.list_of_exercise[index] = result
            self.list_of_exercise.pop(index + 1)
            self.list_of_exercise.pop(index - 1)


def main():
    exercise = input("Write a exercise:")
    lst_from_exercise = exercise.split()
    my_instance = Calculator(lst_from_exercise)
    while len(lst_from_exercise) > 1:
        my_instance.scanner()
    print(lst_from_exercise[0])


if __name__ == '__main__':
    main()
