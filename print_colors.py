print("This script prints out every possible color in the two supported color modes (3 bit and 8 bit). \
The values printed are what need to be input into the colors dictionary of the Colors class in colors.py \
The first value of the tuple is the 3 bit color and the second is the 8 bit color. If you want to \
forego either of these values, enter -1 for either of these values.")

print("3 bit colors:")
for i in range(30,38):
    print(f"\033[{i}m{i}",end=" ")
print()
print("8 bit colors:")
for row in range(0,16):
    for i in range(0,16):
        print(f"\033[38:5:{16*row + i}m{16 * row + i:03d}",end=" ")
    print()
