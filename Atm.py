bank_file_details_path = r'C:\temp\Bank_Test.txt'


def change_from_file_to_dictionary(bank_file_details_path: str):
    with open(bank_file_details_path, 'r') as file_descriptor:
        client_dictionary = {}
        lines = file_descriptor.readlines()
    for line in lines:
        line = line.rstrip("\n")
        temp_list = line.split(",")
        client_dictionary[temp_list[0]] = [temp_list[1], temp_list[2], temp_list[3]]
    return client_dictionary


def check_if_password_correct(number_of_account: str, password_to_account: str):
    dictionary_of_details = change_from_file_to_dictionary(bank_file_details_path)
    values = dictionary_of_details[number_of_account]
    password = values[1]
    if password_to_account == password:
        return True
    return False


def check_if_there_is_account(number_of_account: str):
    dictionary_of_details = change_from_file_to_dictionary(bank_file_details_path)
    keys = dictionary_of_details.keys()
    if number_of_account in keys:
        return True
    else:
        return False


class BankOptions(object):

    def __init__(self, number_of_bank_account="", password_to_account=""):
        self.password_to_account = password_to_account
        self.number_of_bank_account = number_of_bank_account
        self.dictionary_of_details = change_from_file_to_dictionary(bank_file_details_path)
        self.values = self.dictionary_of_details.values()
        self.keys = self.dictionary_of_details.keys()

    def change_account_password(self, new_password_to_account: str):
        values = self.dictionary_of_details[self.number_of_bank_account]
        values = [values[0], new_password_to_account, values[2]]
        self.dictionary_of_details[self.number_of_bank_account] = [values[0], values[1], values[2]]
        return "Your new password is:" + self.dictionary_of_details[self.number_of_bank_account][1]

    def check_balance(self):
        values = self.dictionary_of_details[self.number_of_bank_account]
        balance = values[2]
        return balance

    def deposit_money(self, money_for_deposit: str):
        values = self.dictionary_of_details[self.number_of_bank_account]
        balance = self.check_balance()
        new_balance = int(balance) + int(money_for_deposit)
        values = [values[0], values[1], new_balance]
        self.dictionary_of_details[self.number_of_bank_account] = [values[0], values[1], values[2]]
        print("You have deposited " + money_for_deposit + "$, now your balance is: " + str(new_balance) + "$")
        print(self.dictionary_of_details[self.number_of_bank_account])

    def withdraw_money(self, money_for_withdraw: str):
        values = self.dictionary_of_details[self.number_of_bank_account]
        balance = self.check_balance()
        new_balance = int(balance) - int(money_for_withdraw)
        values = [values[0], values[1], new_balance]
        self.dictionary_of_details[self.number_of_bank_account] = [values[0], values[1], values[2]]
        print("You have pulled " + money_for_withdraw + "$, now your balance is: " + str(new_balance) + "$")

    # def save_to_file(self, dictionary_of_details: dict):


def main():
    while (True):
        bank_number_account = input("Hello! "
                                    "What's your number bank account? ")
        if bank_number_account == "-1":
            print("Thanks for using and goodbye!")
            break
        else:
            if check_if_there_is_account(bank_number_account):
                bank_password = input("What is your password?")
                if check_if_password_correct(bank_number_account, bank_password):
                    client = BankOptions(bank_number_account, bank_password)
                    clint_action = input("For check your balance press 1,"
                                         " for deposit press 2,"
                                         " for withdraw press 3,"
                                         " to Change your password press 4.")
                    if clint_action == "1":
                        print (client.check_balance())
                    if clint_action == "2":
                        money_for_deposit = input("How much money you want to deposit?")
                        client.deposit_money(money_for_deposit)
                    if clint_action == "3":
                        money_for_withdraw = input("How much money you want to pull?")
                        client.withdraw_money(money_for_withdraw)
                    if clint_action == "4":
                        new_password_for_account = input("Enter your new password:")
                        client.change_account_password(new_password_for_account)
                else:
                    print("Error! Wrong password")
            else:
                print("Error! Wrong bank account number")


if __name__ == '__main__':
    main()
