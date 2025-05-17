print("Nhập các dòng văn bản ( Nhập 'done' để dừng):")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)
print("\nCác dòng văn bản đã nhập là:")
for line in lines:
    print(line)