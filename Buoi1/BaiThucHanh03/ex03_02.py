def dao_nguoc_list(lst):
    return lst[::-1]
input_list = input("Nhập danh sách số nguyên cách nhau bởi dấu phẩy: ")
number = list(map(int, input_list.split(",")))
list_dao_nguoc = dao_nguoc_list(number)
print("Danh sách sau khi đảo ngược là:", list_dao_nguoc)