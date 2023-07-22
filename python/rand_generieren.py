# #!/usr/bin/python
# for i in range(0,30):
#     print(str(4098+(i*8)) + ":"+ hex(255)[0:4])
#     print(str(4102+(19*240)+(i*8)) + ":" +   hex(255)[0:4])            
#     #Rand links und rechts
# for i in range(0, 20):
#     print(str(4096 + (i*240)) + ":" + hex(64<<24)[0:4])
#     print(str(4097 + (i*240)) + ":" + hex(64<<16)[0:4])
#     print(str(4098 + (i*240)) + ":" + hex(64<<8)[0:4])
#     print(str(4099 + (i*240)) + ":" + hex(64)[0:4])
#     print(str(4100 + (i*240)) + ":" + hex(64<<24)[0:4])
#     print(str(4101 + (i*240)) + ":" + hex(64<<16)[0:4])
#     print(str(4102 + (i*240)) + ":" + hex(64<<8)[0:4])
#     print(str(4103 + (i*240)) + ":" + hex(64)[0:4])

#     print(str(4328 +(i*240)) + ":" + hex(2)[0:4])
#     print(str(4329 +(i*240)) + ":" + hex(2)[0:4])
#     print(str(4330 +(i*240)) + ":" + hex(2)[0:4])
#     print(str(4331 +(i*240)) + ":" + hex(2)[0:4])
#     print(str(4332 +(i*240)) + ":" + hex(2)[0:4])
#     print(str(4333 +(i*240)) + ":" + hex(2)[0:4])
#     print(str(4334 +(i*240)) + ":" + hex(2)[0:4])
#     print(str(4335 +(i*240)) + ":" + hex(2)[0:4])
 
file = open("spielfeld_speicher.txt", "w")
lines = []
for i in range(30):
    lines.append(str(4097 + (i*8)) + ":0x7e\n")
    lines.append(str(4098 + (i*8)) + ":0x7e\n")
    lines.append(str(4099 + (i*8)) + ":0x7e\n")
    lines.append(str(4100 + (i*8)) + ":0x7e\n")
    lines.append(str(4101 + (i*8)) + ":0x7e\n")
    lines.append(str(4102 + (i*8)) + ":0x7e\n")

for i in range(1,19):
    lines.append(str(4097 + (i*240)) + ":0x7e\n")
    lines.append(str(4098 + (i*240)) + ":0x7e\n")
    lines.append(str(4099 + (i*240)) + ":0x7e\n")
    lines.append(str(4100 + (i*240)) + ":0x7e\n")
    lines.append(str(4101 + (i*240)) + ":0x7e\n")
    lines.append(str(4102 + (i*240)) + ":0x7e\n")
    lines.append(str(4097 + (i*240) + (29*8)) + ":0x7e\n")
    lines.append(str(4098 + (i*240) + (29*8)) + ":0x7e\n")
    lines.append(str(4099 + (i*240) + (29*8)) + ":0x7e\n")
    lines.append(str(4100 + (i*240) + (29*8)) + ":0x7e\n")
    lines.append(str(4101 + (i*240) + (29*8)) + ":0x7e\n")
    lines.append(str(4102 + (i*240) + (29*8)) + ":0x7e\n")

for i in range(30):
    lines.append(str(4097 + (i*8) + (19*240)) + ":0x7e\n")
    lines.append(str(4098 + (i*8) + (19*240)) + ":0x7e\n")
    lines.append(str(4099 + (i*8) + (19*240)) + ":0x7e\n")
    lines.append(str(4100 + (i*8) + (19*240)) + ":0x7e\n")
    lines.append(str(4101 + (i*8) + (19*240)) + ":0x7e\n")
    lines.append(str(4102 + (i*8) + (19*240)) + ":0x7e\n")

lines.append(str(4096 + (14*8) + (9*240)) + ":0x3c\n")
lines.append(str(4097 + (14*8) + (9*240)) + ":0x42\n")
lines.append(str(4098 + (14*8) + (9*240)) + ":0x81\n")
lines.append(str(4099 + (14*8) + (9*240)) + ":0xa5\n")
lines.append(str(4100 + (14*8) + (9*240)) + ":0xa5\n")
lines.append(str(4101 + (14*8) + (9*240)) + ":0x81\n")
lines.append(str(4102 + (14*8) + (9*240)) + ":0x42\n")
lines.append(str(4103 + (14*8) + (9*240)) + ":0x3c\n")

file.writelines(lines)
file.close()