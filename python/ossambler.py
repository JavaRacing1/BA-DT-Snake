#!/usr/bin/python
# init script


CPP = 500
PC = 20


microcommands = {"main":[10,"Der Befehl verzweigt zum naechsten Mikroprogramm abhaengig vom Inhalt von MBR"],\
                 "iadd":[11,"Der Befehl addiert die obersten beiden Elemente des Stack"],\
                 "isub":[14,"Der Befehl subtrahiert das operste Element des Stack vom darunterliegende"],\
                 "iand":[17,"Der Befehl fuehrt ein bitweises AND der beiden obersten Elemente des Stack durch"],\
                 "ior":[20,"Der Befehl fuehrt ein bitweises OR der beiden obersten Elemente des Stack durch"],\
                 "dup":[23,"Der Befehl dupliziert das oberste Element des Stack"],\
                 "pop":[25,"Der Befehl entfernt das oberste Element des Stack"],\
                 "swap":[28,"Der Befehl tauscht die obersten Elemente des Stack"],\
                 "bipush":[34,"Der Befehl legt einen Operanden auf den Keller"],\
                 "iload":[37,"Der Befehl laedt eine lokale Variable und legt diese auf den Stack"],\
                 "istore":[42,"Der Befehl nimmt das oberste Element des Stack und speichert den Wert in eine lokale Variable"],\
                 "wide":[48,"Erweitert den Adressraum der lokalen Variablen"],\
                 "wide_iload":[50,"Der Befehlt arbeitet analog zu iload, verwendet aber 16 Bit Adressen"],\
                 "wide_istore":[54,"Der Befehl arbeitet analog zu istore, verwendet aber 16 Bit Adressen"],\
                 "ldc_2":[58,""],\
                 "iinc":[62,"Addiert zu einer lokalen Variable einen Wert."],\
                 "goto":[68,"Fuehrt einen unbedingten Sprung durch"],\
                 "iflt":[74,"Fuehrt einen Sprung durch, falls das obersten Kellerelement kleiner oder gleich Null ist"],\
                 "ifequ":[78,"Macht einen Sprung falls beiden obersten Kellereleente gleic hsind"],\
                 "if_icmpq":[82,""],\
                 "invokevirtual":[88,"Der Befehl ruft eine Funktion auf."],\
                 "ireturn":[110,"Der Befehl wird fuer den Ruecksprung aus einer Funktion verwendet. "],\
                 "memcp":[138,"Der Befehl kopiert den Wert auf der obersten Adresse des Stack in die darunterliegende Adresse."],\
                 "valcp":[147,"Wert auf dem Stack in die darunterliegende Adresse des Speichers."],\
                 "loadw":[128,"Der Befehlt laedt vier Bytes aus dem Befehlsstrom und legt sie auf den Stack"],\
                 "goto":[118,"Der Befehl springt zu der entsprechende Marke"],\
                  "oinput":[155,"Der Befehl liest den Eingabpuffer aus und schreibt den Wert auf den Stack"],\
                 "declare":[0,"Das SChluesselwort reserviert speicher im LV-Bereich"]}

# read commads
f = open("input.oasm")
c = f.readlines()
lines = []
for i in c:
    lines.append(i.lstrip(" ").rstrip("\n").split(" "))
    

symboltable = {"constants":{},"variables":{},"functions":[]}
co = lo = 0
instructions = []
anker = {}
for i in lines:
    print(str(i) + " erstes zeichen: " + str(i[0][0]))
    #print(str(i) + " microprogramm on address: " + str(microcommands[i[0]][0]) + " Description: " +str(microcommands[i[0]][1]))
    if i[0][0] != "#":
        if i[0] == "declare":
            symboltable["variables"][i[1]]=[i[2],lo]
            lo = lo+1
        elif i[0] == "const":
            symboltable["constants"][i[1]]=[i[2],co]
            co = co + 1
        elif i[0][0] == ":":
            anker[i[0][1:len(i[0])]]=0
            instructions.append([i[0][1:len(i[0])]])
        elif i[0] in microcommands:
            print("i: " + str(i[0]))
            instructions.append(i)
        else:
            print("Syntax Error: Bad Command!")

###################################
##
##  Output
##
###################################
output = open("outputfile.olf","w")
# write init sequence
print(hex(CPP).lstrip("0x").rjust(10,"0"))
output.write("0:" + hex(PC).lstrip("0x").rjust(8,"0")[6:8] + "\n")
output.write("1:" + hex(PC).lstrip("0x").rjust(8,"0")[4:6] + "\n")
output.write("2:" + hex(PC).lstrip("0x").rjust(8,"0")[2:4] + "\n")
output.write("3:" + hex(PC).lstrip("0x").rjust(8,"0")[0:2] + "\n")
# Word Address
output.write("4:" + hex(int(CPP/4)+(co+lo)).lstrip("0x").rjust(8,"0")[6:8] + "\n") #SP
output.write("5:" + hex(int(CPP/4)+(co+lo)).lstrip("0x").rjust(8,"0")[4:6] + "\n")
output.write("6:" + hex(int(CPP/4)+(co+lo)).lstrip("0x").rjust(8,"0")[2:4] + "\n")
output.write("7:" + hex(int(CPP/4)+(co+lo)).lstrip("0x").rjust(8,"0")[0:2] + "\n")
# Word Address
output.write("8:" + hex(int(CPP/4)+(co)).lstrip("0x").rjust(8,"0")[6:8] + "\n") #LV
output.write("9:" + hex(int(CPP/4)+(co)).lstrip("0x").rjust(8,"0")[4:6] + "\n")
output.write("10:" + hex(int(CPP/4)+(co)).lstrip("0x").rjust(8,"0")[2:4] + "\n")
output.write("11:" + hex(int(CPP/4)+(co)).lstrip("0x").rjust(8,"0")[0:2] + "\n")

output.write("12:" + hex(int(CPP/4)).lstrip("0x").rjust(8,"0")[6:8] + "\n")  # CPP
output.write("13:" + hex(int(CPP/4)).lstrip("0x").rjust(8,"0")[4:6] + "\n")
output.write("14:" + hex(int(CPP/4)).lstrip("0x").rjust(8,"0")[2:4] + "\n")
output.write("15:" + hex(int(CPP/4)).lstrip("0x").rjust(8,"0")[0:2] + "\n") #cpp


#create stack
# write constants
for i in symboltable["constants"]:
    # first bring hex number in the correct format with 0x and 10 digits
    if symboltable["constants"][i][0].isdigit():
        symboltable["constants"][i][0] = hex(int(symboltable["constants"][i][0]))
    l = len(symboltable["constants"][i][0])
    if l<10:
        symbotable["constants"][i][0] = symboltable["constants"][i][0][0:2] + "0000000"[0:10-l]  + symboltable["constants"][i][0][2:10]
    if l>10:
        symbotable["constants"][i][0] = symboltable["constants"][i][0][0:2] + symboltable["constants"][i][0][l-8:l]
    print("nachher: " + str(symboltable["constants"][i][0]))    

    output.write(str(CPP+(symboltable["constants"][i][1]*4)) + ":0x" + symbotable["constants"][i][0][8:10] + "\n")
    output.write(str(CPP+(symboltable["constants"][i][1]*4)+1) + ":0x" + symbotable["constants"][i][0][6:8]+ "\n")
    output.write(str(CPP+(symboltable["constants"][i][1]*4)+2) + ":0x" + symbotable["constants"][i][0][4:6]+ "\n")
    output.write(str(CPP+(symboltable["constants"][i][1]*4)+3) + ":0x" + symbotable["constants"][i][0][2:4]+ "\n")
for i in symboltable["variables"]:
    # first bring hex number in the correct format with 0x and 10 digits
    if symboltable["variables"][i][0].isdigit():
        symboltable["variables"][i][0] = hex(int(symboltable["variables"][i][0]))
    l = len(symboltable["variables"][i][0])
    if l<10:
        symboltable["variables"][i][0] = symboltable["variables"][i][0][0:2] + "0000000"[0:10-l]  + symboltable["variables"][i][0][2:10]
    if l>10:
        symboltable["variables"][i][0] = symboltable["variables"][i][0][0:2] + symboltable["variables"][i][0][l-8:l]
    print("nachher: " + str(symboltable["variables"][i][0]))    
    
    output.write(str(CPP+((co + symboltable["variables"][i][1])*4)) +":0x" + symboltable["variables"][i][0][8:10]+ "\n")
    output.write(str(CPP+((co + symboltable["variables"][i][1])*4)+1) +":0x" + symboltable["variables"][i][0][6:8]+ "\n")
    output.write(str(CPP+((co + symboltable["variables"][i][1])*4)+2) +":0x" + symboltable["variables"][i][0][4:6]+ "\n")
    output.write(str(CPP+((co +  symboltable["variables"][i][1])*4)+3) +":0x" + symboltable["variables"][i][0][2:4]+ "\n")
# write commands
p = PC
print("instructions: " + str(instructions) + "startwert von P: " + str(p))
for i in instructions:
    print("Position: " + str(p))
    print("instruction: " +str(i))
    print(i[0][1:len(i[0])] + " anker: " + str(anker) + "#q#q#q#q#q#q#q#q#q")
    if i[0] in anker:
        print("anker: " + str(i[0][1:len(i[0])]))
        anker[i[0]] = p
        print("anker: " + str(anker) + "#################################************************###########")
    else:          
        output.write(str(p) + ":" + hex(microcommands[i[0]][0]) + "\n")
        p = p + 1
        for j in i[1:len(i)]:
            if j in symboltable["variables"]:
              v = hex(symboltable["variables"][j][1])
            elif j in symboltable["constants"]:
              v = hex(symboltable["constants"][j][1])
            elif j in anker:
              v = hex(((anker[j]-p) & 255))
              print("jump for: " +str(anker[j]-p) + " j: " + str(anker[j]) + " anker: " +  str(anker) + " p: " + str(p)  + " 8 Bit Komplement: " + v + " binaer: " + bin((anker[j]-p) & 255))
            else:
              v = j
            print("i: " + str(i) + " j: " + str(j) + " v: " + str(v))    
            output.write(str(p) + ":" + v + "\n")
            print("Parameter")
            p = p + 1
