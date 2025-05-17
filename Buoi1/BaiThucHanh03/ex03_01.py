def tinh_tong_chan(lst):
    tong = 0
    for num in lst:
        if num % 2 == 0:
            tong += num
        return tong
intput_list = input("Nhập danh sách số nguyên cách nhau bởi dấu phẩy: ")
number = list(map(int, intput_list.split(",")))

tong_chan = tinh_tong_chan(number)
print("Tổng các số chẵn trong danh sách là:", tong_chan)