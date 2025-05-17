from SinhVien import SinhVien

class QuanLySinhVien:
    listSinhVien = []
    
    def generateId(self):
        maxId = 1
        if (self.soLuongSinhVien() > 0):
            for sv in self.listSinhVien:
                if (sv.getId() > maxId):
                    maxId = sv.getId()
            maxId += 1
        return maxId
    
    def soLuongSinhVien(self):
        return self.listSinhVien.__len__()
    
    def nhapSinhVien(self):
        svId = self.generateId()
        name = input("Nhap ten sinh vien: ")
        sex = input("Nhap gioi tinh sinh vien: ")
        major = input("Nhap nganh hoc sinh vien: ")
        diemTB = float(input("Nhap diem trung binh sinh vien: "))
        sv = SinhVien(svId, name, sex, major, diemTB)
        self.xeploaihocluc(sv)
        self.listSinhVien.append(sv)
        
    def updateSinhVien(self, ID):
        sv:SinhVien = self.findById(ID)
        if (sv != None):
            name = input("Nhap ten sinh vien: ")
            sex = input("Nhap gioi tinh sinh vien: ")
            major = input("Nhap nganh hoc sinh vien: ")
            diemTB = float(input("Nhap diem trung binh sinh vien: "))
            sv._name = name
            sv._sex = sex
            sv._major = major
            sv._diemTB = diemTB
            self.xeploaihocluc(sv)
        else:
            print("Khong tim thay sinh vien co ID = ", ID)  
            
    def sortBySinhVien(self):
        self.listSinhVien.sort(key=lambda x: x._id, reverse=False)
        
    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x._name, reverse=False)
        
    def sortByDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x._diemTB, reverse=False)
        
    def findById(self, ID):
        searchResult = None
        if(self.soLuongSinhVien() > 0):
            for sv in self.listSinhVien:
                if (sv._id() == ID):
                    searchResult = sv
            return searchResult
        
    def findByName(self, name):
        listSV = []
        if(self.soLuongSinhVien() > 0):
            for sv in self.listSinhVien:
                if (keyword.upper() in sv._name.upper()):
                    listSV.append(sv)
            return listSV
        
    def deleteById(self, ID):
        isDeleted = False
        sv = self.findById(ID)
        if (sv != None):
            self.listSinhVien.remove(sv)
            isDeleted = True
        return isDeleted
    
    
    def xeploaihocluc(self, sv):
        if (sv._diemTB >= 8):
            sv._hocluc = "Gioi"
        elif (sv._diemTB >= 6.5):
            sv._hocluc = "Kha"
        elif (sv._diemTB >= 5):
            sv._hocluc = "Trung binh"
        else:
            sv._hocluc = "Yeu"
            
    def showSinhVien(self, listSV):
        print("{:<8} {:<18} {:<8} {:<8} {:<8} {:<10}".format(sv._id, sv._name, sv._sex, sv._major, sv._diemTB, sv._hocluc))
        print("\n")
        
    def getListSinhVien(self):
        return self.listSinhVien
    
            