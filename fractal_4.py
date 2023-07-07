import tkinter as tk
import numpy as np
from numba import jit, prange
from tkinter import filedialog
from PIL import Image, ImageGrab
import math
import fractal_lib
# 建立GUI應用程式
def create_gui():
    root = tk.Tk()
    root.title('Mandelbrot Fractal')
    previous_views = []
    canvas_width = 800
    canvas_height = 600
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # 設定Mandelbrot集合的區域範圍
    x_start, y_start, x_end, y_end = -2, -1.5, 1, 1.5
    max_iter = 256
    #fractal_lib.draw_fractal(canvas, x_start, y_start, x_end, y_end, max_iter)
    #fractal_lib.draw_mandelbrot(canvas, x_start, y_start, x_end, y_end, max_iter)
    fractal_lib.draw_fractal_image(canvas, x_start, y_start, x_end, y_end, max_iter)
    #x_start, y_start, x_end, y_end = -2, -2, 2, 2  # Initial region to display
    #max_iter = 256
    #draw_julia(canvas, x_start, y_start, x_end, y_end, max_iter)
    # 紀錄使用者選擇的區域起始位置
    '''
    # Set the initial triangle coordinates
    x1, y1 = canvas_width / 2, 50
    x2, y2 = 50, canvas_height - 50
    x3, y3 = canvas_width - 50, canvas_height - 50
    # Set the recursion depth to control the level of detail
    depth = 5
    #draw_sierpinski(canvas, x1, y1, x2, y2, x3, y3, depth)
    x_start, y_start, x_end, y_end = x1, y1, x2, y2
    '''
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

    def previous_view():
        nonlocal x_start, y_start, x_end, y_end, previous_views
        #print('previous_vies=',previous_views)
        # Check if there are previous views available
        if len(previous_views) > 1:
            # Remove the current view from the list
            previous_views.pop()

            # Get the previous view from the list
            x_start, y_start, x_end, y_end = previous_views[-1]

            # Redraw the fractal
            canvas.delete('all')
            fractal_lib.draw_fractal_image(canvas, x_start, y_start, x_end, y_end, max_iter)

    def on_release(event):
        #nonlocal x_start, y_start, x_end, y_end, start_x, start_y
        nonlocal x_start, y_start, x_end, y_end, start_x, start_y, previous_views

        # Save the current view to the list of previous views
        previous_views.append((x_start, y_start, x_end, y_end))
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
        #fractal_lib.draw_fractal(canvas, x_start, y_start, x_end, y_end, max_iter)
        #fractal_lib.draw_mandelbrot(canvas, x_start, y_start, x_end, y_end, max_iter)
        fractal_lib.draw_fractal_image(canvas, x_start, y_start, x_end, y_end, max_iter)
        # Set the parameters for the Julia Set
        #c_real, c_imag = -0.7, 0.27
        #max_iter = 100
        #draw_julia(canvas, x_start, y_start, x_end, y_end, max_iter)


        # 刪除選擇區域的框線
        canvas.delete('selection_rectangle')
        start_x, start_y = None, None

    # 綁定滑鼠事件
    canvas.bind('<ButtonPress-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)



    save_button = tk.Button(root, text="Save", command=save_button_click)
    save_button.pack()
    previous_button = tk.Button(root, text="Previous View", command=previous_view)
    previous_button.pack()

    root.mainloop()

if __name__ == '__main__':
    create_gui()
