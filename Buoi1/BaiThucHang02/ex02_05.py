so_gio_lam = float(input("Nhập số giờ làm: "))
luong_gio = float(input("Nhập lương theo giờ: "))
gio_tieu_chuan = 40;
gio_vuot_chuan = max(0, so_gio_lam - gio_tieu_chuan)
thuc_linh = luong_gio * gio_tieu_chuan + gio_vuot_chuan * luong_gio * 1.5
print("Lương thực lĩnh là: ", {thuc_linh}) 