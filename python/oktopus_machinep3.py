#!/usr/bin/python
import time
from tkinter import *
from tkinter import filedialog
from threading import Thread
from threading import Timer
from optparse import OptionParser
import serial
print("starting oktopus machine!")
class mainstorage:
    def __init__(self,viso,size):
        self.__mainstorage = []
        self.__size = size
        self.__buffer = []
        self.__input_read_flag = 0
        self.__input_buffer = 0
        self.console = None
        self.__last_read_byte = 0
        self.__last_write_byte = 0
        self.__last_read_word = 0
        self.__last_write_word = 0
        mf = Toplevel()
        vscrollbar = Scrollbar(mf, orient=VERTICAL)
        self.__fr = Canvas(mf,width=210,height=600,scrollregion=(0,0,0,20*(int(self.__size/4))),yscrollcommand=vscrollbar.set)
        self.__fr.pack(side=LEFT)
        vscrollbar.config(command=self.__fr.yview)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        for i in range(0,size):
            wa = int(i/4)
            col = i % 4
            r = self.__fr.create_rectangle(42+col*42,(wa*20+1),80+col*42,(wa*20+19) -2,fill='yellow')
            if col == 0:
                a = self.__fr.create_text(25,(wa*20+10),fill='red',text=wa)
            t = self.__fr.create_text(57+col*42,(wa*20+10),fill='black',text='0')
            self.__mainstorage.append({'val':0,'rect':r,'text':t})

            
    def start_console(self):
        self.console = screen(self)

    def set_char(self,c):
        self.__input_buffer = c
        self.__input_read_flag = 1

    def reset_history_read_byte(self):
        self.__fr.itemconfig(self.__mainstorage[self.__last_read_byte]['rect'],fill="yellow")

    def reset_history_read_word(self):
        self.__fr.itemconfig(self.__mainstorage[self.__last_read_word]['rect'],fill="yellow")
        self.__fr.itemconfig(self.__mainstorage[self.__last_read_word+1]['rect'],fill="yellow")
        self.__fr.itemconfig(self.__mainstorage[self.__last_read_word+2]['rect'],fill="yellow")
        self.__fr.itemconfig(self.__mainstorage[self.__last_read_word+3]['rect'],fill="yellow")

    def reset_history_write_byte(self):
        self.__fr.itemconfig(self.__mainstorage[self.__last_write_byte]['rect'],fill="yellow")

    def reset_history_write_word(self):
        self.__fr.itemconfig(self.__mainstorage[self.__last_write_word]['rect'],fill="yellow")
        self.__fr.itemconfig(self.__mainstorage[self.__last_write_word+1]['rect'],fill="yellow")
        self.__fr.itemconfig(self.__mainstorage[self.__last_write_word+2]['rect'],fill="yellow")
        self.__fr.itemconfig(self.__mainstorage[self.__last_write_word+3]['rect'],fill="yellow")

    def save_word(self,addr,value):
        if value > 4294967295:
            value = 4294967295
        v1 = value & 255
        v2 = value>>8 & 255
        v3 = value>>16 & 255
        v4 = value>>24
        # draw to console
        print("draw memory address: " + str(addr))
        if addr >= self.__size/4:
            print("Draw in to console!!!! " + str(addr))
            #addr = addr<<2
            if self.console != None:
                a = addr - self.__size/4
                pos = int(a/2)
                if a % 2:
                    td = 1
                else:
                    td = 0
                y = pos % 30
                x = int(pos/30)
                print("pos: " + str(pos) + " x: " + str(x) + " y: " + str(y) + " "  + str(value) + " " + str(v1) + " " + str(v2) + " " + str(v3) + " " + str(v4))
                self.console.draw(x,y,td,[v4,v3,v2,v1])
            print("bad address")
        else:
            self.__fr.itemconfig(self.__mainstorage[addr*4]['text'],text=hex(v1))
            self.__fr.itemconfig(self.__mainstorage[addr*4+1]['text'],text=hex(v2))
            self.__fr.itemconfig(self.__mainstorage[addr*4+2]['text'],text=hex(v3))
            self.__fr.itemconfig(self.__mainstorage[addr*4+3]['text'],text=hex(v4))
            print("nummer: " + str(value))
            self.__mainstorage[addr*4]['val'] = v1
            self.__mainstorage[addr*4+1]['val'] = v2
            self.__mainstorage[addr*4+2]['val'] = v3
            self.__mainstorage[addr*4+3]['val'] = v4
            self.reset_history_write_word()
            self.__fr.itemconfig(self.__mainstorage[addr*4]['rect'],fill="lightblue")
            self.__fr.itemconfig(self.__mainstorage[addr*4+1]['rect'],fill="lightblue")
            self.__fr.itemconfig(self.__mainstorage[addr*4+2]['rect'],fill="lightblue")
            self.__fr.itemconfig(self.__mainstorage[addr*4+3]['rect'],fill="lightblue")
            self.__last_write_word = addr*4
        print("save " + str(value) + " on " + str(addr))

    def save_byte(self,addr,value):
       if value > 255:
           value = 255
       if addr >= self.__size:
            if self.console != None:
                a = addr - self.__size
                pos = int(a/8)
                line = a % 8
                   
                y = pos % 30
                x = int(pos/30)
                print("address: " + str(addr) + " a: " + str(a) + " pos: " + str(pos) + " x: " + str(x) + " y: " + str(y) + " "  + str(value) )
                self.console.draw_line(x,y,line,value)
            print("bad address")
       else:
           self.__mainstorage[addr]['val'] = value
           self.__fr.itemconfig(self.__mainstorage[addr]['text'],text=  hex(value)[0:4])
           self.reset_history_write_byte()
           self.__fr.itemconfig(self.__mainstorage[addr]['rect'],fill="lightblue")
           self.__last_write_byte = addr
           
    def read_word(self,addr):
        if addr >= self.__size/4  + 1:
            print("bad address: " + str(addr))
        elif addr == self.__size/4:
            self.__input_read_flag = 0
            return self.__input_buffer
        elif addr == self.__size/4 + 1:
            return self.__input_read_flag
    
        else:
            #big endian
            print("No bad Address: " + str(addr))
            v1 = self.__mainstorage[addr*4]['val']
            v2 = self.__mainstorage[addr*4+1]['val']
            v3 = self.__mainstorage[addr*4+2]['val']
            v4 = self.__mainstorage[addr*4+3]['val']
            ret = v1 + (v2<<8) + (v3<<16) + (v4<<24)
            self.reset_history_read_word()
            self.__fr.itemconfig(self.__mainstorage[addr*4]['rect'],fill="white")
            self.__fr.itemconfig(self.__mainstorage[addr*4+1]['rect'],fill="white")
            self.__fr.itemconfig(self.__mainstorage[addr*4+2]['rect'],fill="white")
            self.__fr.itemconfig(self.__mainstorage[addr*4+3]['rect'],fill="white")
            self.__last_read_word = addr*4
            return ret
        
    def read_byte(self,addr):
        if addr >= self.__size:
            print("bad address: " + str(addr))
        else:
            b = self.__mainstorage[addr]['val']
            self.reset_history_read_byte()
            self.__fr.itemconfig(self.__mainstorage[addr]['rect'],fill="white")
            self.__last_read_byte = addr
            return b
        

        

class register:
    def __init__(self,canvas,x,y,name):
        self._x = x
        self._y = y
        self._value = 0
        self._canvas = canvas
        self._rect = self._canvas.create_rectangle(self._x,self._y,self._x+80,self._y-20,fill='yellow')
        self._text = self._canvas.create_text(x+35,y-26,text=name)
        self._value_string = self._canvas.create_text(x+35,y-10,text="0x00000000")
    def write(self,value):
        self._value = value

        print("self.__value: " + str(value) + " self.__value_string: " + str(self._value_string))
        self._canvas.itemconfig(self._value_string,text=str(hex(value)))
    def reset(self):
        self._value = 0
        self._canvas.itemconfig(self._value_string,text=str(hex(0)))

        
    def read(self,name):
        #Vorzeichenerweiterung
        if name == "MBR" and self._value & 128 != 0:
            print("Vorzeichenerweiterung: " + str(bin(self._value & 4294967040)) + " org: " + str(self._value) + "########################################" )
            return self._value | 4294967040           
        else:
            return self._value  

    
    def sll8(self):
        self._value = self._value<<8
        #self._value = self.value & (2**32-1)
    def sra1(self):
        self._value = self._value>>1
        
class control_unit:
    def __init__(self,mir):
        self.__mir = mir
    
    def decode(self,mc):
        print("decode")
        ret = {"next_address" : int(mc/pow(2,27)) ,\
               "jmpc" : int((mc & (pow(2,27)-1))/pow(2,26)),\
               "jamn" : int((mc & (pow(2,26)-1))/pow(2,25)),\
               "jamz" : int((mc & (pow(2,25)-1))/pow(2,24)),\
               "sll8" : int((mc & (pow(2,24)-1))/pow(2,23)),\
               "sra1" : int((mc & (pow(2,23)-1))/pow(2,22)),\
               "f0"   : int((mc & (pow(2,22)-1))/pow(2,21)),\
               "f1"   : int((mc & (pow(2,21)-1))/pow(2,20)),\
               "ena"  : int((mc & (pow(2,20)-1))/pow(2,19)),\
               "enb"  : int((mc & (pow(2,19)-1))/pow(2,18)),\
               "inva" : int((mc & (pow(2,18)-1))/pow(2,17)),\
               "inc"  : int((mc & (pow(2,17)-1))/pow(2,16)),\
               "h"    : int((mc & (pow(2,16)-1))/pow(2,15)),\
               "opc"  : int((mc & (pow(2,15)-1))/pow(2,14)),\
               "tos"  : int((mc & (pow(2,14)-1))/pow(2,13)),\
               "cpp"  : int((mc & (pow(2,13)-1))/pow(2,12)),\
               "lv"   : int((mc & (pow(2,12)-1))/pow(2,11)),\
               "sp"   : int((mc & (pow(2,11)-1))/pow(2,10)),\
               "pc"   : int((mc & (pow(2,10)-1))/pow(2,9)),\
               "mdr"  : int((mc & (pow(2,9)-1))/pow(2,8)),\
               "mar"  : int((mc & (pow(2,8)-1))/pow(2,7)),\
               "write": int((mc & (pow(2,7)-1))/pow(2,6)),\
               "read" : int((mc & (pow(2,6)-1))/pow(2,5)),\
               "fetch": int((mc & (pow(2,5)-1))/pow(2,4)),\
               "bbus" : int((mc & (pow(2,4)-1)))
               }
        print("struct bbus: " + str(ret["bbus"]))
        return ret
    
class microeditor:
    def __init__(self,micromemory,om):
        # c-Bus
        self.micromem = micromemory
        self.__om = om
        microeditor = Toplevel()
        Label(microeditor, text="B-Bus").grid(row=0,column=0)
        self.BBus = IntVar()
         
        Radiobutton(microeditor,  text="MDR",variable=self.BBus,value=0).grid(sticky="W",row=1,column=0)
        Radiobutton(microeditor,  text="PC",variable=self.BBus,value=1).grid(sticky="W",row=2,column=0)
        Radiobutton(microeditor,  text="MBR",variable=self.BBus,value=2).grid(sticky="W",row=3,column=0)
        Radiobutton(microeditor,  text="MBRU",variable=self.BBus,value=3).grid(sticky="W",row=4,column=0)
        Radiobutton(microeditor,  text="SP",variable=self.BBus,value=4).grid(sticky="W",row=5,column=0)
        Radiobutton(microeditor,  text="LV",variable=self.BBus,value=5).grid(sticky="W",row=6,column=0)
        Radiobutton(microeditor,  text="CPP",variable=self.BBus,value=6).grid(sticky="W",row=7,column=0)
        Radiobutton(microeditor,  text="TOS", variable=self.BBus,value=7).grid(sticky="W",row=8,column=0)
        Radiobutton(microeditor,  text="OPC",variable=self.BBus,value=8).grid(sticky="W",row=9,column=0)
        

        #B-Bus
        Label(microeditor, text="C-Bus").grid(row=0,column=1)

        self.C_MAR = IntVar()
        Checkbutton(microeditor, text="MAR",variable=self.C_MAR).grid(sticky="W",row=1,column=1)
        self.C_MDR = IntVar()
        Checkbutton(microeditor, text="MDR",variable=self.C_MDR).grid(sticky="W",row=2,column=1)
        self.C_PC = IntVar()
        Checkbutton(microeditor,text="PC", variable=self.C_PC).grid(sticky="W",row=3,column=1)
        self.C_SP = IntVar()
        Checkbutton(microeditor,text="SP", variable=self.C_SP).grid(sticky="W",row=4,column=1)
        self.C_LV = IntVar()
        Checkbutton(microeditor,text="LV", variable=self.C_LV).grid(sticky="W",row=5,column=1)
        self.C_CPP = IntVar()
        Checkbutton(microeditor,text="CPP", variable=self.C_CPP).grid(sticky="W",row=6,column=1)
        self.C_TOS = IntVar()
        Checkbutton(microeditor,text="TOS", variable=self.C_TOS).grid(sticky="W",row=7,column=1)
        self.C_OPC = IntVar()
        Checkbutton(microeditor,text="OPC", variable=self.C_OPC).grid(sticky="W",row=8,column=1)
        self.C_H = IntVar()
        Checkbutton(microeditor, text="H",variable=self.C_H).grid(sticky="W",row=9,column=1)
        
        #CPU
        Label(microeditor, text="CPU").grid(row=0,column=2)
        self.function = IntVar()
        Radiobutton(microeditor,text="AND", variable=self.function,value=0).grid(sticky="W",row=1,column=2)
        Radiobutton(microeditor,text="OR", variable=self.function,value=1).grid(sticky="W",row=2,column=2)
        Radiobutton(microeditor,text="NEG", variable=self.function,value=2).grid(sticky="W",row=3,column=2)
        Radiobutton(microeditor,text="ADD", variable=self.function,value=3).grid(sticky="W",row=4,column=2)
        self.ena = IntVar()
        Checkbutton(microeditor,text="ENA", variable=self.ena).grid(sticky="W",row=5,column=2)
        self.enb = IntVar()
        Checkbutton(microeditor,text="ENB", variable=self.enb).grid(sticky="W",row=6,column=2)
        self.inva = IntVar()
        Checkbutton(microeditor,text="INV", variable=self.inva).grid(sticky="W",row=7,column=2)
        self.inc = IntVar()
        Checkbutton(microeditor,text="INC", variable=self.inc).grid(sticky="W",row=8,column=2)
        self.shift = IntVar()
        Radiobutton(microeditor,text="No Shift", variable=self.shift,value=0).grid(sticky="W",row=9,column=2)
        Radiobutton(microeditor,text="SLL8", variable=self.shift,value=2).grid(sticky="W",row=10,column=2)
        Radiobutton(microeditor,text="SRA1", variable=self.shift,value=1).grid(sticky="W",row=11,column=2)
        
        Label(microeditor, text="Speicher").grid(row=0,column=3)
        self.read_write = IntVar()
        self.fetch = IntVar()
        Radiobutton(microeditor,text="not", variable=self.read_write,value=0).grid(sticky="W",row=1,column=3)
        Radiobutton(microeditor,text="read", variable=self.read_write,value=1).grid(sticky="W",row=2,column=3)
        Radiobutton(microeditor,text="write", variable=self.read_write,value=2).grid(sticky="W",row=3,column=3)
        Checkbutton(microeditor,text="fetch", variable=self.fetch).grid(sticky="W",row=4,column=3)
        # Jump
        Label(microeditor, text="Jump").grid(row=0,column=4)
        self.jmpc = IntVar()
        self.jamn = IntVar()
        self.jamz = IntVar()
        Checkbutton(microeditor,text="JMPC", variable=self.jmpc).grid(sticky="W",row=1,column=4)
        Checkbutton(microeditor,text="JAMN", variable=self.jamn).grid(sticky="W",row=2,column=4)
        Checkbutton(microeditor,text="JAMZ", variable=self.jamz).grid(sticky="W",row=3,column=4)
        # Next
        Label(microeditor, text="Next Microaddress").grid(row=0,column=5)
        self.switch_na = IntVar()
        self.next_address = StringVar()
        Entry(microeditor,textvariable=self.next_address).grid(sticky="W",row=1,column=5)
        Checkbutton(microeditor,text="swich", variable=self.switch_na,command=self.swich_na).grid(sticky="W",row=2,column=5)
        
        Label(microeditor,text="Current Address").grid(sticky="W",row=3,column=5)
        self.switch_ca = IntVar()
        self.current_address = StringVar()
        Entry(microeditor,textvariable=self.current_address).grid(sticky="W",row=4,column=5)
        Checkbutton(microeditor,text="swich curren address", variable=self.switch_ca,command=self.swich_ca).grid(sticky="W",row=5,column=5)
        Button(microeditor,text="Insert Command",command=self.new_microcommand).grid(sticky="W",row=9,column=5)
        self.color = StringVar()
        self.color.set("#fffffffff")
        Radiobutton(microeditor,bg="#8a2be2",variable=self.color,value="#8a2be2").grid(sticky="W",row=1,column=6)
        Radiobutton(microeditor,bg="#5f9ea0",variable=self.color,value="#5f9ea0").grid(sticky="W",row=2,column=6)
        Radiobutton(microeditor,bg="#00008b",variable=self.color,value="#00008b").grid(sticky="W",row=3,column=6)
        Radiobutton(microeditor,bg="#1874CD",variable=self.color,value="#1874CD").grid(sticky="W",row=4,column=6)
        Radiobutton(microeditor,bg="#BC8F8F",variable=self.color,value="#BC8F8F").grid(sticky="W",row=5,column=6)
        Radiobutton(microeditor,bg="#8B4513",variable=self.color,value="#8B4513").grid(sticky="W",row=6,column=6)
        Radiobutton(microeditor,bg="#A52A2A",variable=self.color,value="#A52A2A").grid(sticky="W",row=1,column=7)
        Radiobutton(microeditor,bg="#CD3333",variable=self.color,value="#CD3333").grid(sticky="W",row=2,column=7)
        Radiobutton(microeditor,bg="#8B7355",variable=self.color,value="#8B7355").grid(sticky="W",row=3,column=7)
        Radiobutton(microeditor,bg="#D2691E",variable=self.color,value="#D2691E").grid(sticky="W",row=4,column=7)
        Radiobutton(microeditor,bg="#006400",variable=self.color,value="#006400").grid(sticky="W",row=5,column=7) 
        Radiobutton(microeditor,bg="DarkKhaki",variable=self.color,value="DarkKhaki").grid(sticky="W",row=6,column=7)
        Radiobutton(microeditor,bg="#a2cd5a",variable=self.color,value="#a2cd5a").grid(sticky="W",row=1,column=8)
        Radiobutton(microeditor,bg="#00fa9a",variable=self.color,value="#00fa9a").grid(sticky="W",row=2,column=8)
        Radiobutton(microeditor,bg="#9ACD32",variable=self.color,value="#9ACD32").grid(sticky="W",row=3,column=8)
        Radiobutton(microeditor,bg="#EEE685",variable=self.color,value="#EEE685").grid(sticky="W",row=4,column=8)
        Radiobutton(microeditor,bg="#f08080",variable=self.color,value="#f08080").grid(sticky="W",row=5,column=8)
        Radiobutton(microeditor,bg="#ee1289",variable=self.color,value="#ee1289").grid(sticky="W",row=6,column=8)

    def load(self,mc,address,color):
        print("in methode load " + str(mc))
        struct = self.__om.cu.decode(mc)
        self.next_address.set(struct["next_address"])
        self.current_address.set(address)
        self.jmpc.set(struct["jmpc"])  
        self.jamn.set(struct["jamn"])
        self.jamz.set(struct["jamz"])
        self.shift.set(2 * struct["sll8"] + struct["sra1"])
        self.function.set(struct["f1"] + 2*struct["f0"])
        self.ena.set(struct["ena"])
        self.enb.set(struct["enb"])
        self.inva.set(struct["inva"])
        self.inc.set(struct["inc"])
        self.C_H.set(struct["h"])
        self.C_OPC.set(struct["opc"])
        self.C_TOS.set(struct["tos"])
        self.C_CPP.set(struct["cpp"])
        self.C_LV.set(struct["lv"])
        self.C_SP.set(struct["sp"])
        self.C_PC.set(struct["pc"])
        self.C_MDR.set(struct["mdr"])
        self.C_MAR.set(struct["mar"])
        self.read_write.set(int(struct["write"])*2 + int(struct["read"]))
        self.fetch.set(struct["fetch"])
        self.color.set(color)
        print("BBUS: " + str(struct["bbus"]))
        self.BBus.set(struct["bbus"])
        
    def new_microcommand(self):
        command = 0
        try:
           next_addr =int(self.next_address.get())
           curr_addr =int(self.current_address.get())
           command = command + pow(2,27)* next_addr + pow(2,26) * self.jmpc.get() + pow(2,25) * self.jamn.get() + pow(2,24) * self.jamz.get() + pow(2,22) * self.shift.get() \
                             + pow(2,20) * self.function.get() + pow(2,19) * self.ena.get() + pow(2,18) * self.enb.get() + pow(2,17) * self.inva.get() + pow(2,16) * self.inc.get() \
                             + pow(2,15) * self.C_H.get() + pow(2,14) * self.C_OPC.get() + pow(2,13) * self.C_TOS.get() + pow(2,12) * self.C_CPP.get() + pow(2,11) * self.C_LV.get() \
                             + pow(2,10) * self.C_SP.get() + pow(2,9) * self.C_PC.get() + pow(2,8) * self.C_MDR.get() + pow(2,7) * self.C_MAR.get() + pow(2,5) * self.read_write.get() + pow(2,4) * self.fetch.get() +self.BBus.get()
           print(bin(command)[2:len(bin(command))].rjust(36,"0"))
           print(str(self.jamn.get()))
           # insert the created microcommand into the microcommandmemory
           self.micromem.insert(curr_addr,command,self.color.get())
           self.current_address.set(str(curr_addr+1))
           self.next_address.set(str(next_addr+1))
        except:
            raise()
            print("No Address ist given!")
            
    def swich_ca(self):
        sca = self.switch_ca.get()
        try:
            ca = int(self.current_address.get())
            if sca:
                if ca < 256:
                    self.current_address.set(str(ca+256))
                else:
                    print("invalid address - too big!")
            else:
                if ca > 256:
                    self.current_address.set(str(ca-256))
                else:    
                    print("invalid address - too small!")
        except:
            raise()
            print("invalid address - not a number!")

    def swich_na(self):
        sna = self.switch_na.get()
        try:
            na = int(self.next_address.get())
            if sna:
                if na < 256:
                    self.next_address.set(str(na+256))
                else:
                    print("invalid address - too big!")
            else:
                if na > 256:
                    self.next_address.set(str(na-256))
                else:    
                    print("invalid address - too small!")
        except:
            raise()
            print("invalid address - not a number!")
            
  
class om:
    def __init__(self,viso,ms,bbc):
        ##############################################
        #
        #  Fake Snakerace
        #
        ##############################################
        self.__fake_segmente = [1300,1301,1302,1303,1304,1305,1306,1307]
        self.__fake_head = 0
        self.__fake_direction = [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,60,60,60,60,-2,-2,-2,60,60,60,60,60,60,2,2,2,-60,-60,-60,-60,-60,2,2,2,2,2,2,2,2,-60,2,2,-60,-60,-60,-60]
        self.__fake_pos_dir = 0

        ###############################################

        self.mainstorage = ms
        self.__bbc = bbc
        try:
            self.__serial = serial.Serial('COM15',115200,)
        except:
            print("Serial port not active!")
        #self.__serial.write(bytes("MAR#1\n",'ascii'))
        self.__mem_wr = 0
        self.__mem_rd = 0
        self.__mem_fetch = 0
        self.__mem_addr = 0
        self.__mem_pc = 0
        self.__fr = Canvas(viso,width=1000,height=800)
        self.__fr.pack(side="top",fill="x")
        self.__running = False
        self.__bbc = bbc
        self.__frequency = IntVar()
        self.__register = {}
        self.draw_datapath()
        self.A = Abus(self.__fr)
        self.B = Bbus(self.__fr)
        self.C = Cbus(self.__fr)
        self.CPU = CPU(self.__fr)
        self.mpm = MPM(self.__fr,self)
        self.mir = MIR(self.__fr)
        self.mpc = MPC(self.__fr)
  
        self.cu = control_unit(self.mir)
        #self.A.write(8934)
        #self.B.write(15347)
        #self.C.write(15347)
        self.controller = Frame(viso)
        self.controller.pack(side="bottom",fill="x")
        self.start = Button(self.controller,text="Start",command=self.start_stop)
        self.start.pack(side="left")
        self.frequency = Scale(self.controller,length=800,from_=0,to=1000,orient=HORIZONTAL,variable=self.__frequency)
        self.frequency.pack(side="left",fill=X)
        ### parse commandline ###
        parser = OptionParser()
        parser.add_option("-m", "--microprogramm" , dest="microprogramm", default="",help="load am Microgramm given by filename")
        parser.add_option("-s", "--storagedupm" , dest="storagedump", default="",help="load dump from given file to storage")
        (options, args )= parser.parse_args()
        if options.microprogramm != "":
            self.insert_microcommands(options.microprogramm)
            
        if options.storagedump != "":
            self.insert_memory(options.storagedump)
        
    def reset_reg(self):
        for i in self.__register:
            self.__register[i].reset()
        
    def start_stop(self):
        print("freq: " + str(self.__frequency.get()))
        if self.__frequency.get() == 0:
            self.step()
        else:    
            if self.__running:
                self.start.config(text="Start")
                self.__running = False
                
                print("stop thread")
            else:
                self.start.config(text="Stop")
                self.__running = True
                thr = Timer(0.1,self.loop_om)
                thr.start()
                print("start thread")

    def loop_om(self):
        freq = self.__frequency.get()
        while self.__running and freq > 0:          
            time.sleep(1/freq)
            self.step()
            
    def step(self):
        if self.__frequency.get() < 20:
            
            #Microbefehl auswerten
            ma = self.mpc.get_value() 
            print("Adresse des naechsten Microbefehles: " + str(ma))
            # lade den naechsten Microbefehl in MIR
            mc = self.mpm.read(ma)
            print("Command: " + str(mc))
            self.mir.set_value(mc)
            # Microbefehl decodieren
            lanes = self.cu.decode(mc)
            print("decodiert: " + str(lanes))
            # Register auf Bus B legen
            regs = ["mdr","pc","mbr","mbru","sp","lv","cpp","tos","opc"]
            print("bbus: " + str(regs[lanes['bbus']]))
            val = self.__register[regs[lanes['bbus']]].read(regs[lanes['bbus']].upper())
            print("value in Register " + str(lanes['bbus']) + " mit Namen " + regs[lanes['bbus']] + ": " + str(val) )
            self.B.write(val)
            self.A.write(self.__register["h"].read("H"))   
            # Alu arbeiten lassen und Ergebnis ins Schieberegister
            self.CPU.compute(self.A,self.B,lanes,self.__register["shift"])
            # send to serial port
            if self.__bbc.get():
                if lanes["enb"]:
                    B = str(regs[lanes['bbus']])
                else:
                    B ="0"
                if lanes["ena"]:
                    H = "H"
                else:
                    H = "0"
                if lanes["f0"] == 0 and lanes["f1"] == 0:
                    self.__serial.write(bytes("ALU" +"#" + H + "#" + B + "#&\r\n",'ascii'))
                elif lanes["f1"] == 0 and lanes["f0"] == 1:
                    self.__serial.write(bytes("ALU" +"#" + H + "#" + B + "#|\r\n",'ascii'))
                elif lanes["f1"] == 1 and lanes["f0"] == 0:
                    self.__serial.write(bytes("ALU" +"#" + H + "#" + B + "#-\r\n",'ascii'))
                else:
                    self.__serial.write(bytes("ALU" +"#" + H + "#" + B + "#+\r\n",'ascii'))
                # verschiebung durchfuehren
            if lanes["sll8"]:
                self.__register["shift"].sll8()
            if lanes["sra1"]:
                self.__register["shift"].sra1()
            # Ergebnis auf Bis C legen
            erg = self.__register["shift"].read("SHIFT")
            print("Ergebnis: " + str(erg))
            # Wert von Bus C in Register Ueuebernehmen
            self.C.write(erg)
            for i in self.__register:
                if i != "shift" and i != "mbr" and i != "mbru" and lanes[i]:
                    #print("trage ergebnis " + str(erg) + " in Register " + i)
                    self.__register[i].write(erg)
                    if self.__bbc.get():
                        self.__serial.write(bytes(i.upper()+"#"+str(erg)+"\r\n",'ascii'))
            # Speichersignale senden
            addr = self.__register["mar"].read("MAR")
            pc = self.__register["pc"].read("PC")
            print("Schreibe in Speicher auf Addresse: " + str(addr))
            if self.__mem_wr:
                val = self.__register["mdr"].read("MDR")
                self.mainstorage.save_word(self.__mem_addr,val)
            if self.__mem_rd:
                #print("read_storage from: " + str(self.__mem_addr))
                val = self.mainstorage.read_word(self.__mem_addr)
                self.__register["mdr"].write(val)
                if self.__bbc.get():
                        self.__serial.write(bytes("MDR#"+str(val)+"\r\n",'ascii'))
            if self.__mem_fetch:
                val = self.mainstorage.read_byte(self.__mem_pc)
                self.__register["mbr"].write(val)
                if self.__bbc.get():
                        self.__serial.write(bytes("MBR#"+str(val)+"\r\n",'ascii'))
            # Signale auswerten fuer naechsten Takt    
            self.__mem_wr = lanes["write"]
            self.__mem_rd = lanes["read"]
            self.__mem_fetch = lanes["fetch"]
            self.__mem_pc   = pc
            self.__mem_addr = addr
            # naechste Addresse im Microprogramm berechnen
            naddr = lanes["next_address"]
            jpc  = lanes["jmpc"]
            print("Addr: " + str(naddr) + " jpc: " + str(jpc) + " jmnz: " + str(lanes["jamn"]) + " jamz: " + str(lanes["jamz"]))
            if jpc:
                naddr = naddr | self.__register["mbru"].read("MBRU")
            if lanes['jamz'] and self.CPU.get_state_z():
                naddr = naddr ^ (2**8)
            if lanes['jamn'] and self.CPU.get_state_n():
                naddr = naddr ^ (2**8)
            print("Adresse: " + str(naddr))    
            self.mpc.set_value(naddr)
        else:
            
            #Microbefehl auswerten
            ma = self.mpc.get_value() 
            # lade den naechsten Microbefehl in MIR
            print("ma: " + str(ma))
            mc = self.mpm.read(ma)
            self.mir.set_value(mc)
            # Microbefehl decodieren
            lanes = self.cu.decode(mc)
            # Register auf Bus B legen
            regs = ["mdr","pc","mbr","mbru","sp","lv","cpp","tos","opc"]   
            # Alu arbeiten lassen und Ergebnis ins Schieberegister
            #self.CPU.compute(self.A,self.B,lanes,self.__register["shift"])
            # Alu inline
            if lanes["ena"]:
                #A = self.__register[regs[lanes['h']]].read(regs[lanes['H']].upper())
                A = self.__register['h'].read("H")
            else:
                A = 0
            if lanes["enb"]:    
                B = self.__register[regs[lanes['bbus']]].read(regs[lanes['bbus']].upper())
            else:
                B=0
            if lanes["inva"]:
                A = ~A & 4294967295
            if lanes["f0"] == 0:
                if lanes["f1"] == 1:
                    erg = A | B
                else:
                    erg = A & B

            else:
                if lanes["f1"] == 0:
                    erg = ~B & 4294967295
                else:
                    # modulo 11111111111111111111111111111111 oder & 1111111111111111111111111111111111
                    erg = (A + B) & 4294967295
            if lanes["inc"]:
                erg = (erg + 1) & 4294967295
            z = n = 0    
            if erg == 0:
                z = 1
            if erg < 0:
                n = 1 
           
            self.__register["shift"].write(erg)    

            # verschiebung durchfuehren
            if lanes["sll8"]:
                self.__register["shift"].sll8()
            if lanes["sra1"]:
                self.__register["shift"].sra1()
            # Ergebnis auf Bis C legen
            erg = self.__register["shift"].read("SHIFT")
            # send on serial Interface
            #if self.__bbc.get():
            #    if lanes["enb"]:
            #        B = str(regs[lanes['bbus']])
            #    else:
            #        B ="0"
            #    if lanes["ena"]:
            #        H = "H"
            #    else:
            #        H = "0"
            #    if lanes["f0"] == 0 and lanes["f1"] == 0:
            #        self.__serial.write(bytes("ALU" +"#" + H + "#" + B + "#&\r\n",'ascii'))
            #    elif lanes["f1"] == 0 and lanes["f0"] == 1:
            #        self.__serial.write(bytes("ALU" +"#" + H + "#" + B + "#|\r\n",'ascii'))
            #    elif lanes["f1"] == 1 and lanes["f0"] == 0:
            #        self.__serial.write(bytes("ALU" +"#" + H + "#" + B + "#-\r\n",'ascii'))
            #    else:
            #        self.__serial.write(bytes("ALU" +"#" + H + "#" + B + "#+\r\n",'ascii'))

            # Wert von Bus C in Register Ueuebernehmen
            
            for i in self.__register:
                if i != "shift" and i != "mbr" and i != "mbru" and lanes[i]:
                    self.__register[i].write(erg)
            #        if self.__bbc.get():
            #            self.__serial.write(bytes(i.upper()+"#"+str(erg)+"\r\n",'ascii'))
            # Speichersignale senden
            addr = self.__register["mar"].read("MAR")
            pc = self.__register["pc"].read("PC")
            
            if self.__mem_wr:
                val = self.__register["mdr"].read("MDR")
                self.mainstorage.save_word(self.__mem_addr,val)
            if self.__mem_rd:
                val = self.mainstorage.read_word(self.__mem_addr)
                self.__register["mdr"].write(val)
            #    if self.__bbc.get():
            #            self.__serial.write(bytes("MBR#"+str(val)+"\r\n",'ascii'))
            if self.__mem_fetch:
                val = self.mainstorage.read_byte(self.__mem_pc)
                self.__register["mbr"].write(val)
            #    if self.__bbc.get():
            #            self.__serial.write(bytes("MBR#"+str(val)+"\r\n",'ascii'))
            # Signale auswerten fuer naechsten Takt    
            self.__mem_wr = lanes["write"]
            self.__mem_rd = lanes["read"]
            self.__mem_fetch = lanes["fetch"]
            self.__mem_pc   = pc
            self.__mem_addr = addr
            # naechste Addresse im Microprogramm berechnen
            naddr = lanes["next_address"]
            jpc  = lanes["jmpc"]
            print("Addr: " + str(naddr) + " jpc: " + str(jpc) + " jmnz: " + str(lanes["jamn"]) + " jamz: " + str(lanes["jamz"]))
            if jpc:
                naddr = naddr | self.__register["mbru"].read("MBRU")
            if lanes['jamz'] and z:
                naddr = naddr ^ (2**8)
            if lanes['jamn'] and n:
                naddr = naddr ^ (2**8)
                
            self.mpc.set_value(naddr)
            
            
    def draw_datapath(self):
        # draw ALU
        #self.__fr.create_rectangle(153,360,233,340,fill='yellow')
        #self.__fr.create_rectangle(153,330,233,310,fill='yellow')
        self.__register["h"] =register(self.__fr,153,345,"H")
        self.__register["opc"] =register(self.__fr,153,310,"OPC")
        self.__register["tos"] =register(self.__fr,153,275,"TOS")
        self.__register["cpp"] = register(self.__fr,153,240,"CPP")
        self.__register["lv"] = register(self.__fr,153,205,"LV")
        self.__register["sp"] = register(self.__fr,153,170,"SP")
        self.__register["mbru"] = self.__register["mbr"] = register(self.__fr,153,135,"MBR")
        self.__register["pc"] = register(self.__fr,153,100,"PC")
        self.__register["mdr"] = register(self.__fr,153,65,"MDR")
        self.__register["mar"] = register(self.__fr,153,30,"MAR")

        # schieberegister
        self.__register["shift"] = register(self.__fr,240,560,"")



    def load_mem(self):
        path = filedialog.askopenfilename()
        self.insert_memory(path)
        
    def insert_memory(self,path):
        f = open(path)
        code = f.readlines()
        f.close()
        for l in code:
            v = l.rstrip('\n').lstrip(' ').rstrip(' ').split(":")
            if v[1] != '' and v[1] != " ":
                self.mainstorage.save_byte(int(v[0]),int(v[1],16))
                

        print("speicheradresse 5: " + str(self.mainstorage.read_byte(3)))
        
        
    def load_mic(self):
        path = filedialog.askopenfilename()
        self.insert_microcommands(path)
        
    def insert_microcommands(self,path):
        f = open(path)
        code = f.readlines()
        f.close()
        for l in code:
            v = l.rstrip('\n').lstrip(' ').rstrip(' ').split(":")
            if v[1] != '' and v[1] != " ":
                self.mpm.insert(int(v[0]),int(v[1].rstrip('\n'),base=16),v[2])
              
        
        
    def save_mic(self):
        microprog = self.mpm.dump()
        path = filedialog.asksaveasfile(mode='w',defaultextension='mic')
        path.write(microprog)
        path.close()
        
    def create_microcommand(self):
        print("SChreibe Mikrobefehl")
        self.microeditor = microeditor(self.mpm,self)
        
        
class Abus:
    def __init__(self,can):
        self.__canvas = can
        self.lanes={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[],21:[],22:[],23:[],24:[],25:[],26:[],27:[],28:[],29:[],30:[],31:[]}
        self.draw()
        self.__value = 0
        self.write(129)
        self.update(self.__value)
    def draw(self):
        for i in range(0,32):
            line = self.__canvas.create_line(165+(2*i),400,165+(2*i),345,fill="grey")
            self.lanes[i].append(line)
    def update(self,value):
        for i in range(0,32):
            k = 0
            if value % 2:
                #print("value: " + str(i))
                value = value - 1
                for l in self.lanes[k]:
                    self.__canvas.itemconfig(l,fill="black")
            else:
                for l in self.lanes[k]:
                    self.__canvas.itemconfig(l,fill="grey")
            value = value/2
            k = k +1
    def write(self,val):
        self.__value = val
        self.update(self.__value)
    def read(self):
        return self.__value
    
class Bbus:
    def __init__(self,can):
        self.__canvas = can
        self.lanes={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[],21:[],22:[],23:[],24:[],25:[],26:[],27:[],28:[],29:[],30:[],31:[]}
        self.draw()
        self.__value = 0
    def draw(self):
        for i in range(0,32):
            line = self.__canvas.create_line(330+(2*i),400,330+(2*i),15,fill="grey")
            self.lanes[i].append(line)
    def update(self,value):
        k = 0
        for i in range(0,32):
            if value % 2:
                #print("value: " + str(i))
                value = value - 1
                for l in self.lanes[k]:
                    self.__canvas.itemconfig(l,fill="black")
            else:
                for l in self.lanes[k]:
                    self.__canvas.itemconfig(l,fill="grey")
            value = value/2
            k = k + 1
    def write(self,val):
        self.__value = val
        self.update(self.__value)
    def read(self):
        return self.__value

class Cbus:
    def __init__(self,can):
        self.__canvas = can
        self.lanes={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[],21:[],22:[],23:[],24:[],25:[],26:[],27:[],28:[],29:[],30:[],31:[]}
        self.draw()
        self.__value = 0
    def draw(self):
        for i in range(0,32):
            line = self.__canvas.create_line(245+(2*i),560,245+(2*i),565+(2*i),fill="grey")
            self.lanes[i].append(line)
            line = self.__canvas.create_line(245+(2*i),565+(2*i),130-(2*i),565+(2*i),fill="grey")
            self.lanes[i].append(line)
            line = self.__canvas.create_line(130-(2*i),565+(2*i),130-(2*i),15,fill="grey")
            self.lanes[i].append(line)
    def update(self,value):
        k = 0
        for i in range(0,32):
            if value % 2:
                #print("value: " + str(i))
                value = value - 1
                for l in self.lanes[k]:
                    self.__canvas.itemconfig(l,fill="black")
            else:
                for l in self.lanes[k]:
                    self.__canvas.itemconfig(l,fill="grey")
            value = value/2
            k = k +1
    def write(self,val):
        self.__value = val
        self.update(self.__value)
    def read(self):
        return self.__value

class CPU:
    def __init__(self,can):
        self.__canvas = can
        self.lanes={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[],21:[],22:[],23:[],24:[],25:[],26:[],27:[],28:[],29:[],30:[],31:[]}
        self.draw()
        self.__z = self.__n = 0
        self.__value = 0
    def draw(self):
        self.__canvas.create_polygon(160,400,240,400,260,420,300,420,320,400,400,400,320,520,240,520,fill="light blue")
        self.__n = self.__canvas.create_rectangle(400,440,410,450,fill="grey")
        self.__line_n = self.__canvas.create_line(370,445,400,445,fill="grey")
        self.__z = self.__canvas.create_rectangle(400,460,410,470,fill="grey")
        self.__line_z = self.__canvas.create_line(358,465,400,465,fill="grey")
        for i in range(0,32):
            line = self.__canvas.create_line(245+(2*i),520,245+(2*i),540,fill="grey")
            self.lanes[i].append(line)
            
    def get_state_z(self):
        return self.__z
    
    def get_state_n(self):
        return self.__n
    
    def set_n(self,active):
        if active:
            self.__n = 1
            self.__canvas.itemconfig(self.__n,fill="red")
            self.__canvas.itemconfig(self.__line_n,fill="black")                         
        else:
            self.__n = 0
            self.__canvas.itemconfig(self.__n,fill="grey")
            self.__canvas.itemconfig(self.__line_n,fill="black")
            
    def set_z(self,active):
        if active:
            self.__z = 1
            self.__canvas.itemconfig(self.__z,fill="red")
            self.__canvas.itemconfig(self.__line_z,fill="black")                         
        else:
            self.__z = 0
            self.__canvas.itemconfig(self.__z,fill="grey")
            self.__canvas.itemconfig(self.__line_z,fill="black")

            
    def ausgabe(self,value):
        k = 0
        print("Ausgabe: " + str(value))
        for i in range(0,32):
            if value % 2:
                value = value -1
                for l in self.lanes[k]:
                    self.__canvas.itemconfig(l,fill="black")
            else:
      
                for l in self.lanes[k]:
                    self.__canvas.itemconfig(l,fill="grey")
            value = value/2
            k = k + 1

    def compute(self,A_Bus,B_Bus,state,shift):
        # 0 0  AND
        # 0 1  OR
        # 1 0  NEG 
        # 1 1  ADD
        
        if state["ena"]:
            A = A_Bus.read()
        else:
            A = 0
        if state["enb"]:    
            B = B_Bus.read()
        else:
            B=0    
        if state["inva"]:
            A = ~A & 4294967295
        if state["f0"] == 0:
            if state["f1"] == 1:
                erg = A | B
            else:
                erg = A & B

        else:
            if state["f1"] == 0:
                erg = ~B & 4294967295
            else:
                erg = (A + B) & 4294967295
        if state["inc"]:
            erg = erg + 1
            
        self.ausgabe(erg)
        if erg == 0:
            self.set_z(1)
        else:
            self.set_z(0)
        if erg < 0:
            self.set_n(1)
        else:
            self.set_n(0)
            
        shift.write(erg)

class MIR:
    def __init__(self,can):
        self.__canvas = can
        self.bits = []
        self.__value = 0
        for i in range(0,36):
            self.__canvas.create_rectangle(500+(10*i),760,510+(10*i),770,fill="grey",tag=str(i))
            bit = self.__canvas.create_text(505+(10*i),765,text="0")
            self.bits.append(bit)
    
    def set_value(self,val):
        self.__value = val
        for i in range(0,36):
            if val % 2:
                self.__canvas.itemconfig(self.bits[35-i],text="1")
            else:
                self.__canvas.itemconfig(self.bits[35-i],text="0")
            val = int(val/2)
            
    def get_value(self,index):
        return self.__value
    
class MPC:
    def __init__(self,can):
        self.__canvas = can
        self.bits = []
        self.__value = 0
        for i in range(0,9):
            self.__canvas.create_rectangle(500+(10*i),10,510+(10*i),20,fill="grey")
            bit = self.__canvas.create_text(505+(10*i),15,text="0")
            self.bits.append(bit)

    def set_value(self,val):
        self.__value = val
        for i in range(0,9):
            if val % 2:
                self.__canvas.itemconfig(self.bits[8-i],text=str(1))
            else:
                self.__canvas.itemconfig(self.bits[8-i],text=str(0))
            val = int(val/2)
            
    def get_value(self):
        return self.__value
    
class MPM:
    def __init__(self,can,om):
        self.__canvas = can
        self.__canvas.create_rectangle(430,40,916,704,fill="cyan")
        self.__om = om
        self.__mem = []
        self.__current = [None,None,None]
        for i in range(0,512):
            self.__mem.append([000000000,None,"black"])
        print("MPM gefuellt")    
        self.refresh()
        print("Nach refresh")
        self.__mem[300][0] = 0
        self.refresh()
        
    def insert(self,address,command,color):
        self.__mem[address][0]=command
        self.__mem[address][2]=color
        
        self.refresh()

    def read(self,address):
        #self.refresh()
        print("Adresse: " + str(address))
        if self.__current[1] != None:
            self.__canvas.itemconfig(self.__current[1],fill=self.__current[2])
        self.__current = self.__mem[address]    
        self.__canvas.itemconfig(self.__current[1],fill="white")
        
        return self.__mem[address][0]
        
        
    def dump(self):
        output = ""
        address = 0
        for i in self.__mem:
            output = output + str(address) + ":" + str(hex(i[0]))+ ":" + str(i[2]) + "\n"
            address = address + 1
        return output
    
    def refresh(self):    
        for i in range(0,512):
            if self.__mem[i][1] !=None:
                self.__canvas.delete(self.__mem[i][1])
            cell = self.__canvas.create_text(460+60*int(i/64),56+10*(i%64),font=('Helvetica','8'),tag=str(i), text=hex(self.__mem[i][0]).lstrip("0x").rjust(9,"0"),fill=self.__mem[i][2])
            self.__canvas.tag_bind(cell,'<Enter>',self.draw_tooltip)
            self.__canvas.tag_bind(cell,'<Button-1>',self.load_command)
            self.__mem[i][1] = cell
            
    def draw_tooltip(self,event):
        element = event.widget.find_overlapping(event.x-2,event.y-2,event.x+2,event.y+2)
        tags = self.__canvas.gettags("current")
        #print(bin(self.__mem[inttags[0])][0])[2:len(bin(self.__mem[int(tags[0])][0]))].rjust(36,"0"))       
        

    def load_command(self,event):
        element = event.widget.find_overlapping(event.x-2,event.y-2,event.x+2,event.y+2)
        tags = self.__canvas.gettags("current")
        mikrocommand = self.__mem[int(tags[0])][0]
        color = self.__mem[int(tags[0])][2]
        print("load_command " + str(mikrocommand))
        try:
            self.__om.microeditor.load(mikrocommand,tags[0],color)
        except:
            raise()
            print("microeditor not open!")

class screen:
    def __init__(self,mem):
        self.__memory = mem
        self.screen = Toplevel()
        self.screen.bind("<Key>", self.key_pressed)
        self.canvas = Canvas(self.screen,width=480,height=320)
        self.canvas.pack()
        self.characters = []
        for i in range(0,20):
            self.characters.append([])
            for j in range(0,30):
                self.characters[i].append([])
                for k in range(8,0,-1):
                    for l in range(8,0,-1):
                        col = "black"
                        
                        rect = self.canvas.create_rectangle(16*j+l*2,16*i+2*(8-k), 16*j+l*2+1,16*i+(8-k)*2+1,outline=col)
                        self.characters[i][j].append(rect)
            
    def draw(self,x,y,td,data):
        pointer = bit = 0
        print("len data: " + str(data) + " x: " + str(x) + " y: " + str(y) )
  
        min = td * 4
        if len(data) > 3:
            print("len x: " + str(len(self.characters)) + " len y: " + str(len(self.characters[17])))
            #print("len self char: " + str(len(self.characters[x][y])))
            for i in self.characters[x][y][min*8:(min+4)*8]:
                if bit % 8 == 0:
                    value = data[pointer]
                    pointer = pointer +1
                if value % 2 == 1:
                    print("weiss")
                    self.canvas.itemconfig(i,outline="lightgreen")
                else:
                    self.canvas.itemconfig(i,outline="black")
                value = int(value/2)
                bit = bit + 1

    def draw_line(self,x,y,line,value):
        print("len data: " + str(value) + " x: " + str(x) + " y: " + str(y) )
        
        print("x: " + str(x) + " y: " + str(y))    
        for i in self.characters[x][y][line*8:line*8+8]:
            if value % 2 == 1:
                print("weiss")
                self.canvas.itemconfig(i,outline="lightgreen")
            else:
                self.canvas.itemconfig(i,outline="black")
            value = int(value/2)
            
            
        
        #self.canvas.create_rectangle(590,390,600,400,fill="red")         
    def key_pressed(self,event):
        char = event.char
        self.__memory.set_char(char)
        if len(char) > 0:
            print("Taste gedruckt: " + str(ord(char)))
        
t = Tk()
mb = Menu(t)
t.title('Oktopus machine')
# wir brauchen speicher
ms = mainstorage(t,4096)

#self.console.draw(1,0,[0,66,66,126,66,66,66,0])
bbc = BooleanVar()
o = om(t,ms,bbc)
load_menu = Menu(mb)
config_menu = Menu(mb)
reset_menu = Menu(mb)
load_menu.add_command(label="Load Memory",command=o.load_mem)
load_menu.add_command(label="Load Microprogram", command = o.load_mic)
reset_menu.add_command(label="reset Register",command = o.reset_reg)
mb.add_cascade(label="load",menu=load_menu)
mb.add_cascade(label="reset",menu=reset_menu)
mb.add_cascade(label="config",menu=config_menu)
mb.add_command(label="Save Microprogram", command = o.save_mic)
mb.add_command(label="Setup Microprogramm",command=o.create_microcommand)
mb.add_command(label="Console",command=ms.start_console)
config_menu.add_checkbutton(label="BBC",onvalue=1, offvalue=0, variable=bbc)
t.config(menu=mb)
t.mainloop()
