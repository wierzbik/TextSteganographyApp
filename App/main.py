from collections import deque
from math import floor

from tkinter import filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master

        self.master.title("Inżynierka")

        padx = 5
        pady = 5

        self.button_load = Button(self.master, text="Otwórz obraz", command=self.load_file)
        self.button_load.grid(row=0, column=0, sticky=NW, padx=padx, pady=pady)
        self.button_save = Button(self.master, text="Zapisz obraz", command=self.save_file)
        self.button_save.grid(row=0, column=1, sticky=NE, padx=padx, pady=pady)

        self.how_many_bits_label = Label(self.master, text="Na ilu bitach kodować/dekodować?")
        self.how_many_bits_label.grid(row=1, column=0, sticky=N, padx=padx, pady=pady)
        self.how_many_bits = IntVar(self.master)
        self.how_many_bits.set(1)  # default value
        self.how_many_bits_option = OptionMenu(self.master, self.how_many_bits, 1, 2, 3, 4, 5, 6, 7, 8,
                                               command=self.update_message_size_label)
        self.how_many_bits_option.grid(row=1, column=1, sticky=N, padx=padx, pady=pady)

        self.image_size_label = Label(self.master)
        self.image_size_label.grid(row=2, column=0, columnspan=2, sticky=N, padx=padx, pady=pady)

        self.message_size_label = Label(self.master, text="Przy X bitach zmieści się Y znaków")
        self.message_size_label.grid(row=3, column=0, columnspan=2, sticky=N, padx=padx, pady=pady)
        self.message_size = 0

        self.encrypt_text_box = Text(self.master, height=4, width=30)
        self.encrypt_text_box.grid(row=4, column=0, rowspan=2, columnspan=2, sticky=N, padx=padx, pady=pady)
        self.encrypt_text_box.insert(END, "Tekst do zakodowania")

        self.button_encode = Button(self.master, text="Zakoduj tekst powyżej", command=self.encode)
        self.button_encode.grid(row=6, column=0, columnspan=2, sticky=N, padx=padx, pady=pady)

        self.decrypted_text_box = Text(self.master, height=4, width=30)
        self.decrypted_text_box.grid(row=7, column=0, rowspan=2, columnspan=2, sticky=N, padx=padx, pady=pady)
        self.decrypted_text_box.insert(END, "Tekst odkodowany")

        self.button_decode = Button(self.master, text="Odkoduj tekst z obrazka", command=self.decode)
        self.button_decode.grid(row=9, column=0, columnspan=2, sticky=N, padx=padx, pady=pady)

        self.image = None
        self.photo_image = None

        self.canvas = Canvas(self.master, width=800, height=500)
        self.canvas.grid(row=0, column=2, columnspan=10, rowspan=10,
                         sticky=W + E + N + S, padx=padx, pady=pady)
        self.update_canvas()

    def load_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik",
                                              filetypes=(("bitmap files", "*.bmp"),
                                                         ("all files", ".")))
        try:
            self.image = Image.open(filename)
        except:
            messagebox.showerror(title="Błąd!", message="Nie udało się wczytać pliku!")
            return

        self.update_canvas()

    def save_file(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Wybierz plik",
                                                filetypes=(("bitmap files", ".bmp"), ("wszystkie pliki", ".*")))
        try:
            self.image.save(filename)
        except:
            messagebox.showerror(title="Błąd!", message="Nie udało się zapisać obrazu!")

    def update_message_size_label(self, _=None):
        if self.image:
            self.message_size = floor(self.image.size[0] * self.image.size[1] * self.how_many_bits.get() * 3 / 8)
            self.message_size_label["text"] = f"Przy {self.how_many_bits.get()} bitach zmieści się {self.message_size} znaków"
        else:
            self.message_size = 0
            self.message_size_label["text"] = "Nie wczytano pliku!"

    def encode(self):
        if not self.image:
            messagebox.showerror(title="Błąd", message="Kodowanie wymaga wczytania obrazu")
            return

        to_encode = self.encrypt_text_box.get("1.0", 'end-1c')

        if len(to_encode) > self.message_size:
            messagebox.showerror(title="Błąd!", message="Wiadomość jest zbyt długa dla tego obrazu przy tej ilości bitów")
            return

        if not all([ord(x) < 256 for x in to_encode]):
            messagebox.showerror(title="Błąd!", message="Wiadomość zawiera znaki spoza kodu ASCII")
            return

        buffer = deque()
        for letter in to_encode:
            letter_as_binary_string = bin(ord(letter))[2:].zfill(8)
            for x in letter_as_binary_string:
                buffer.append(x)
        for _ in range(8):
            buffer.append("0")

        pixels = self.image.load()
        how_many_bits = self.how_many_bits.get()
        for i in range(self.image.size[0]):
            if not buffer:
                break
            for j in range(self.image.size[1]):
                if not buffer:
                    break
                pixel = pixels[i, j]
                R = bin(pixel[0])[2:].zfill(8)
                G = bin(pixel[1])[2:].zfill(8)
                B = bin(pixel[2])[2:].zfill(8)

                # R
                tmp = ""
                for _ in range(how_many_bits):
                    if buffer:
                        tmp += buffer.popleft()
                    else:
                        tmp += "0"
                R = int(R[:-how_many_bits] + tmp, 2)

                # G
                tmp = ""
                for _ in range(how_many_bits):
                    if buffer:
                        tmp += buffer.popleft()
                    else:
                        tmp += "0"
                G = int(G[:-how_many_bits] + tmp, 2)

                # B
                tmp = ""
                for _ in range(how_many_bits):
                    if buffer:
                        tmp += buffer.popleft()
                    else:
                        tmp += "0"
                B = int(B[:-how_many_bits] + tmp, 2)
                pixels[i, j] = (R, G, B)

        self.update_canvas()

    def decode(self):
        if not self.image:
            messagebox.showerror(title="Błąd!", message="Dekodowanie wymaga wczytania obrazu")
            return

        binary_buffer = deque()
        decrypted_buffer = deque()
        pixels = self.image.load()
        how_many_bits = self.how_many_bits.get()

        finished = False
        for i in range(self.image.size[0]):
            if finished:
                break
            for j in range(self.image.size[1]):
                if finished:
                    break
                pixel = pixels[i, j]
                R = bin(pixel[0])[2:].zfill(8)
                G = bin(pixel[1])[2:].zfill(8)
                B = bin(pixel[2])[2:].zfill(8)

                tmp = R[-how_many_bits:] + G[-how_many_bits:] + B[-how_many_bits:]
                binary_buffer.extend(tmp)

                while len(binary_buffer) >= 8:
                    tmp = ""
                    for _ in range(8):
                        tmp += binary_buffer.popleft()
                    tmp = int(tmp, 2)
                    if tmp == 0:
                        finished = True
                        break
                    decrypted_buffer += chr(tmp)

        decrypted_text = "".join(decrypted_buffer)
        self.decrypted_text_box.delete("1.0", END)
        self.decrypted_text_box.insert(END, decrypted_text)

    def update_canvas(self):
        self.canvas.delete("all")
        if self.image:
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.photo_image, anchor=NW)
            self.image_size_label["text"] = f"Rozmiar obrazka: {self.image.size[0]}x{self.image.size[1]}"
        else:
            width = self.canvas["width"]
            height = self.canvas["height"]
            self.canvas.create_line(0, 0, width, height, fill="blue", dash=(4, 4))
            self.canvas.create_line(0, height, width, 0, fill="blue", dash=(4, 4))
            self.image_size_label["text"] = "Rozmiar obrazka: nie wczytano"
        self.update_message_size_label()


if __name__ == "__main__":
    root = Tk()
    root.geometry("1200x600")
    app = Window(root)
    root.mainloop()