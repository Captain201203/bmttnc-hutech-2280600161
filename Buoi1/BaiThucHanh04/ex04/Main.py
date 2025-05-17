from QuanLySinhVien import QuanLySinhVien

qlsv = QuanLySinhVien()
while (1==1):
    print("1. Nhap sinh vien")
    print("2. Cap nhat sinh vien")
    print("3. Xoa sinh vien")
    print("4. Tim kiem sinh vien theo ten")
    print("5. Sap xep sinh vien")
    print("6. Thong ke sinh vien")
    print("7. Thoat")
    choice = int(input("Nhap lua chon: "))
    
    if (choice == 1):
        qlsv.nhapSinhVien()
    elif (choice == 2):
        id = int(input("Nhap ID sinh vien can cap nhat: "))
        qlsv.updateSinhVien(id)
    elif (choice == 3):
        id = int(input("Nhap ID sinh vien can xoa: "))
        qlsv.deleteSinhVien(id)
    elif (choice == 4):
        name = input("Nhap ten sinh vien can tim: ")
        qlsv.findByName(name)
    elif (choice == 5):
        qlsv.sortBySinhVien()
        qlsv.sortByName()
        qlsv.sortByDiemTB()
    elif (choice == 6):
        qlsv.thongKe()
    elif (choice == 7):
        break
    else:
        print("Lua chon khong hop le")
        