from tkinter import *
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
from tkinter import ttk


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (800, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=800, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'green'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.brush_size_scale = 1

    def setup_ui(self):
        """
        Метод отвечает за создание и расположение виджетов управления
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        brush_button = ttk.Button(control_frame, text="Размер кисти", command=self.drop_down_menu)
        brush_button.pack(side=tk.LEFT)

        eraser_button = ttk.Button(control_frame, text="Eraser", command=self.eraser)
        eraser_button.pack(side=tk.RIGHT)

    def paint(self, event):
        """  Функция вызывается при движении мыши с нажатой левой кнопкой по холсту.
        Она рисует линии на холсте Tkinter и параллельно на объекте Image из Pillow: """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale)
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """ Сбрасывает последние координаты кисти. Это необходимо для корректного
        начала новой линии после того, как пользователь отпустил кнопку мыши
        и снова начал рисовать."""
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """ Очищает холст, удаляя все нарисованное, и пересоздает
        объекты Image и ImageDraw  для нового изображения."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """ Открывает стандартное диалоговое окно выбора цвета и устанавливает
        выбранный цвет для кисти как текущий."""
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        """ Позволяет пользователю сохранить изображение, используя стандартное
        диалоговое окно для сохранения файла. Поддерживает только формат PNG.
        В случае успешного сохранения выводится сообщение об успешном сохранении."""
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

# *******  NEW MODULES (task №1) *********************
    def drop_down_menu(self):
        """ Создает выпадающее окно со значениями размера кисти в пикселях.
            Выбор значения из списка и установка параметров кисти
            завершается нажатием кнопки Enter"""
            # Dropdown menu options
        options = [1, 3, 5, 8, 10]
            # datatype of menu text
        self.clicked = IntVar()
            # Create Dropdown menu
        self.drop = tk.OptionMenu(self.root, self.clicked, *options)
        self.drop.pack()

        self.button = Button(self.root, text="Enter", command=self.show)
        self.button.pack()

    def show(self):
        """ Присваивает кисти выбранный размер и убирает выпадающее окно с экрана
            после  выбора  размера  кисти"""
        print('Выбран размер кисти - ', self.clicked.get())
        self.brush_size_scale = self.clicked.get()
        #        print(self.brush_size_scale)
        if self.brush_size_scale > 0:
            self.button = Button(self.root, text="Close", command=self.hide_button(self.button))
            self.button = Button(self.root, text="Close", command=self.hide_button(self.drop))

    def hide_button(self, btn_name):
        """ Функция убирает изображение кнопки с экрана"""
        self.btn_name = btn_name
        self.btn_name.pack_forget()

# *******  NEW MODULES (task №2) *********************
    def eraser(self):
        """ Функция активирует Eraser (Ластик) с толщиной
            выбранного  размера  кисти. Для продолжения
            рисования  необходимо выбрать цвет линии.
        """
        self.pen_color = 'white'
        self.paint

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
