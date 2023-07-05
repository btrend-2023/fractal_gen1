import tkinter as tk
import numpy as np
from numba import jit, prange
from tkinter import filedialog
from PIL import Image, ImageGrab
@jit
def mandelbrot(c_real, c_imag, max_iter):
    z_real = 0
    z_imag = 0
    n = 0
    while z_real * z_real + z_imag * z_imag <= 4 and n < max_iter:
        new_real = z_real * z_real - z_imag * z_imag + c_real
        new_imag = 2 * z_real * z_imag + c_imag
        z_real = new_real
        z_imag = new_imag
        n += 1
    return n


# 函數用於繪製Mandelbrot集合
def draw_fractal(canvas, x_start, y_start, x_end, y_end, max_iter):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()

    x = np.linspace(x_start, x_end, width)
    y = np.linspace(y_start, y_end, height)
    x, y = np.meshgrid(x, y)

    # 使用 numpy.vectorize 讓函數支援向量化運算
    mandelbrot_vectorized = np.vectorize(mandelbrot)

    # 進行並行計算
    result = mandelbrot_vectorized(x, y, max_iter)

    # 將收斂值轉換成顏色並繪製像素點
    r = (result % 256)
    g = ((result * 3) % 256)
    b = ((result * 5) % 256)

    for i in prange(width):
        for j in prange(height):
            # Using 'int()' to convert floating-point values to integers for indexing
            canvas.create_rectangle(int(i), int(j), int(i) + 1, int(j) + 1,
                                    fill=f'#{r[j, i]:02x}{g[j, i]:02x}{b[j, i]:02x}', outline='')

# Function to save the canvas content as an image file
@jit
def julia(z_real, z_imag, c_real, c_imag, max_iter):
    n = 0
    while z_real * z_real + z_imag * z_imag <= 4 and n < max_iter:
        new_real = z_real * z_real - z_imag * z_imag + c_real
        new_imag = 2 * z_real * z_imag + c_imag
        z_real = new_real
        z_imag = new_imag
        n += 1
    return n

def draw_julia(canvas, x_start, y_start, x_end, y_end, max_iter):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()

    x = np.linspace(x_start, x_end, width)
    y = np.linspace(y_start, y_end, height)
    x, y = np.meshgrid(x, y)

    r = np.zeros((height, width), dtype=np.uint8)
    g = np.zeros((height, width), dtype=np.uint8)
    b = np.zeros((height, width), dtype=np.uint8)

    for i in prange(width):
        for j in prange(height):
            iterations = julia(x[j, i], y[j, i], -0.7, 0.27, max_iter)  # Set the constant for the Julia Set equation
            r[j, i] = (iterations % 256)
            g[j, i] = ((iterations * 3) % 256)
            b[j, i] = ((iterations * 5) % 256)

    for i in prange(width):
        for j in prange(height):
            canvas.create_rectangle(i, j, i + 1, j + 1, fill=f'#{r[j, i]:02x}{g[j, i]:02x}{b[j, i]:02x}', outline='')

# 建立GUI應用程式
def create_gui():
    root = tk.Tk()
    root.title('Mandelbrot Fractal')

    canvas_width = 800
    canvas_height = 600
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # 設定Mandelbrot集合的區域範圍
    #x_start, y_start, x_end, y_end = -2, -1.5, 1, 1.5
    #max_iter = 100
    #c_real, c_imag = -0.7, 0.27
    x_start, y_start, x_end, y_end = -2, -2, 2, 2  # Initial region to display
    max_iter = 256
    #draw_fractal(canvas, x_start, y_start, x_end, y_end, max_iter)
    draw_julia(canvas, x_start, y_start, x_end, y_end, max_iter)
    # 紀錄使用者選擇的區域起始位置
    start_x, start_y = None, None

    def save_fractal_image(canvas, filename):
        # Get the window coordinates of the canvas
        x, y, width, height = canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_width(), canvas.winfo_height()

        # Take a screenshot of the canvas
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Save the screenshot as a JPEG image
        screenshot.save(filename, "JPEG")

    def save_button_click():
        # Ask the user for the filename and path to save the image
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".jpg",
                                                    filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            save_fractal_image(canvas, file_path)

    def on_press(event):
        nonlocal start_x, start_y
        start_x = event.x
        start_y = event.y

    def on_drag(event):
        nonlocal start_x, start_y
        # 在滑鼠拖曳期間，更新選擇區域的框線
        canvas.delete('selection_rectangle')
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline='white', tags='selection_rectangle')

    def on_release(event):
        nonlocal x_start, y_start, x_end, y_end, start_x, start_y
        # 取得使用者選擇的區域範圍
        x1 = min(start_x, event.x)
        y1 = min(start_y, event.y)
        x2 = max(start_x, event.x)
        y2 = max(start_y, event.y)

        # 將像素位置映射到區域內的複數
        a1 = x_start + (x1 / canvas.winfo_reqwidth()) * (x_end - x_start)
        b1 = y_start + (y1 / canvas.winfo_reqheight()) * (y_end - y_start)
        a2 = x_start + (x2 / canvas.winfo_reqwidth()) * (x_end - x_start)
        b2 = y_start + (y2 / canvas.winfo_reqheight()) * (y_end - y_start)

        # 更新新的區域範圍
        x_start, x_end = min(a1, a2), max(a1, a2)
        y_start, y_end = min(b1, b2), max(b1, b2)

        # 重繪碎形
        canvas.delete('all')
        #draw_fractal(canvas, x_start, y_start, x_end, y_end, max_iter)

        # Set the parameters for the Julia Set
        #c_real, c_imag = -0.7, 0.27
        max_iter = 100
        draw_julia(canvas, x_start, y_start, x_end, y_end, max_iter)

        # 刪除選擇區域的框線
        canvas.delete('selection_rectangle')
        start_x, start_y = None, None

    # 綁定滑鼠事件
    canvas.bind('<ButtonPress-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)



    save_button = tk.Button(root, text="Save", command=save_button_click)
    save_button.pack()


    root.mainloop()

if __name__ == '__main__':
    create_gui()
