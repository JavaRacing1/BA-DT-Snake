import tkinter as tk

class maschine:
    def __init__(self, tk_widget: tk.Tk, bg_color: str ="black", icon_color: str = "lightgreen"):
        self.__ram = {}
        self.__display = {}
        self.input = 0
        self.__fill_storage()

        self.__bg_color = bg_color
        self.__icon_color = icon_color
        self.stopped = False

        
        tk_widget.bind("<Key>", self.__key_pressed)
        self.canvas = tk.Canvas(master=tk_widget, width=480, height = 320)
        self.canvas.pack(side="left", padx=5, pady=5)
        self.blocks = []
        for block_y in range(20):
            self.blocks.append([])
            for block_x in range(30):
                self.blocks[block_y].append([])
                for rect_y in range(8):
                    for rect_x in range(8):
                        start_x = 16*block_x + 2*rect_x + 2
                        start_y = 16*block_y + 2*rect_y + 2
                        rect = self.canvas.create_rectangle(start_x, start_y, start_x + 1, start_y + 1, outline=self.__bg_color)
                        self.blocks[block_y][block_x].append(rect)
        
        from snake_code import loop_init

        start_button = tk.Button(tk_widget ,text="Start", width=5, height=2, command= lambda : loop_init(tk_widget, self))
        start_button.pack(side="top", padx=5, pady=5)
        stop_button = tk.Button(tk_widget ,text="Stop", width=5, height=2, command = lambda: self.__stop())
        stop_button.pack(side="top", padx=5)

        self.__init_ram_window()

    def __fill_storage(self):
        for i in range(4096):
            self.__ram[i] = 0
        for i in range(4080):
            self.__display[i] = 0
    
    def __key_pressed(self, event):
        char = event.char
        if len(char)>0:
            print(str(ord(char)))

    def __stop(self):
        self.stopped = True

    def __init_ram_window(self):
        ram_window = tk.Toplevel()
        scrollbar = tk.Scrollbar(ram_window, orient=tk.VERTICAL)
        self.__ram_canvas = tk.Canvas(ram_window, width=600, height=400, scrollregion=(0,0,0, ((1512 // 4) + 8 ) * 25), yscrollcommand=scrollbar.set)
        self.__ram_canvas.pack(side="left")
        scrollbar.config(command=self.__ram_canvas.yview)
        scrollbar.pack(fill="y", side="right", expand=False)

        self.__ram_canvas.create_text(150, 10, text="STACK:", font=("Arial", 10, "bold"))
        self.__ram_canvas.create_text(450, 10, text="GPM:", font=("Arial", 10, "bold"))
        rect_width = 70
        rect_height = 25
        for i in range(512):
            col = i % 4
            row = i // 4
            self.__ram_canvas.create_rectangle(10 + col * rect_width, 20 + row * rect_height, 10 + col * rect_width + (rect_width - 5), 20 + row * rect_height + (rect_height - 10))
            self.__ram_canvas.create_text(14 + col * rect_width, 28 + row * rect_height, text=str(i) + ": " + str(self.__ram[i]), anchor='w', font=("Arial", 9))
        for i in range(512, 2048):
            col = i % 4
            row = (i-512) // 4
            self.__ram_canvas.create_rectangle(310 + col * rect_width, 20 + row * rect_height, 310 + col * rect_width + (rect_width - 5), 20 + row * rect_height + (rect_height - 10))
            self.__ram_canvas.create_text(314 + col * rect_width, 28 + row * rect_height, text=str(i) + ": " + str(self.__ram[i]), anchor='w', font=("Arial", 9))



    def draw_row(self, addr, value):
        if (addr > 4095):
            display_addr = addr - 4096
            block_x = (display_addr // 8) % 30
            block_y = (display_addr // 240)
            row = display_addr % 8

            for rect in self.blocks[block_y][block_x][row*8:row*8+8]:
                if (value % 2 == 1):
                    col = self.__icon_color
                else:
                    col = self.__bg_color
                self.canvas.itemconfig(rect, outline=col)
                value = value//2

    def output_ram(self, from_addr=0, to_addr=4095):
        k = from_addr
        for i in range((to_addr+8)//8):
            if k == 0:
                print(' ')
                print('================================ STACK ================================')
            elif k == 512:
                print(' ')
                print('================================= GPM =================================')
            elif k == 2048:
                print(' ')
                print('=============================== PROGRAM ===============================')

            line = ''
            for j in range(8):
                if k > to_addr:
                    break

                addr_zeros = ""
                if k < 10:
                    addr_zeros = "0"
                if k < 100:
                    addr_zeros = addr_zeros + "0"
                if k < 1000:
                    addr_zeros = addr_zeros + "0"

                spaces = " "
                if self.__ram[k] < 10:
                    spaces = spaces + " "
                if self.__ram[k] < 100:
                    spaces = spaces + " "
                    
                line = line + addr_zeros + str(k) + ": " + str(self.__ram[k]) + spaces
                k = k + 1
            print(line)

    def load_memory(self, path):
        f = open(path)
        lines = f.readlines()
        f.close()

        for line in lines:
            l = line.rstrip('\n').lstrip(' ').rstrip(' ').split(':')
            if l[0] != '' and l[1] != '' and l[1] != " ":
                addr = int(l[0])

                if (l[1].find('x') != -1):
                    value = int(l[1], 16)
                else:
                    value = int(l[1])

                if (addr < 4096):
                    self.__ram[addr] = value
                else:
                    self.__display[addr - 4096] = value
                    self.draw_row(addr, value)


    def load8(self, addr: int):
        addr = addr + 512
        if addr < 0 or (addr > 2047 and addr < 4096):
            return
        
        if addr > 4095:
            value = self.__display[addr - 4096]
        else:
            value = self.__ram[addr]
        self.push(value)

    def store(self, addr:int):
        addr = addr + 512

        if addr < 0 or (addr > 2047 and addr < 4096):
            return
        
        value = self.__ram[0]

        if addr > 4095:
            self.__display[addr - 4096] = value
            self.draw_row(addr, value)
        else:
            self.__ram[addr] = value
        
    
    def push(self, value: int):
        for i in range(510, -1, -1):
            if self.__ram[i] != 0:
                self.__ram[i + 1] = self.__ram[i]
        self.__ram[0] = value

    def pop(self):
        self.__ram[0] = 0
        for i in range(1, 512):
            if (self.__ram[i] != 0):
                self.__ram[i - 1] = self.__ram[i]
                self.__ram[i] = 0
    
    def add(self):
        first_value = self.__ram[0]
        self.pop()
        second_value = self.__ram[0]
        self.pop()
        new_value = first_value + second_value
        self.push(new_value)

    def sub(self):
        first_value = self.__ram[0]
        self.pop()
        second_value = self.__ram[0]
        self.pop()
        new_value = first_value - second_value
        self.push(new_value)

    def inc(self):
        self.__ram[0] = self.__ram[0] + 1
    
    def dec(self):
        self.__ram[0] = self.__ram[0] - 1

    def swap(self):
        first_value = self.__ram[0]
        self.pop()
        second_value = self.__ram[0]
        self.pop()
        self.push(first_value)
        self.push(second_value)

if __name__ == '__main__':
    root = tk.Tk(className="Stackmaschine")
    machine = maschine(root, "black", "lightgreen")
    root.mainloop()