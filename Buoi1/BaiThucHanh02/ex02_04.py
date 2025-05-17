
j = []#Tạo danh sách rỗng
for i in range(2000, 3021): #Duyệt từ 2000 đến 3020
    if (i% 7 == 0) and (i%5 != 0):#Kiểm tra số chia hết cho 7 và không chia hết cho 5
        j.append(i)#Thêm số vào danh sách
print(','.join(j))#In ra danh sách