abstand_list = [2, 2, 2, 52, 10, 48, 4, 6, 4, 46, 4, 6, 4, 46, 10, 46, 4, 6, 4, 48, 4, 2, 4, 52, 2, 2, 2]
#sieg = 2, 2, 2, 52, 10, 48, 4, 6, 4, 46, 4, 6, 4, 46, 10, 46, 4, 6, 4, 48, 4, 2, 4, 52, 2, 2, 2
#niederlage = 2, 2, 2, 52, 10, 48, 2, 2, 2, 2, 2, 2, 48, 4, 6, 4, 46, 2, 4, 2, 4, 2, 46, 14, 48, 10, 52, 2, 2, 2
start = 3300

lines = []

for abstand in abstand_list:
    
    lines.append(f"{start+1}: push\n")
    lines.append(f"{start+2}: 0x33\n")
    lines.append(f"{start+3}: dload\n")
    lines.append(f"{start+4}: push\n")
    lines.append(f"{start+5}: {hex(abstand)}\n")
    lines.append(f"{start+6}: add\n")
    lines.append(f"{start+7}: push\n")
    lines.append(f"{start+8}: 0x33\n")
    lines.append(f"{start+9}: dstore\n")
    lines.append(f"{start+10}: call\n")
    lines.append(f"{start+11}: 0x0C\n")
    lines.append(f"{start+12}: 0xC7\n")

    start = start + 12

f = open("code.txt", "a")
f.writelines(lines)
f.close()