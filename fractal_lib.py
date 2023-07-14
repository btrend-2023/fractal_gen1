import tkinter as tk
import numpy as np
from numba import jit, prange
from PIL import Image
from PIL import ImageTk
@jit(nopython=True)
def mandelbrot(c_real, c_imag, max_iter):
    z_real = 0
    z_imag = 0
    power = 2
    n = 0
    while z_real * z_real + z_imag * z_imag <= 4 and n < max_iter:
        # ******** original formula **********
        #new_real = z_real * z_real - z_imag * z_imag + c_real
        #new_imag = 2 * z_real * z_imag + c_imag
        # ******** modified formula **********
        new_real = z_real ** power - z_imag ** power + c_real
        new_imag = 2 * z_real * z_imag + c_imag
        #z_real, z_imag = z_real ** 2 - z_imag ** 2 + c_real, 2 * z_real * z_imag + c_imag

        z_real = new_real
        z_imag = new_imag
        n += 1
    return n

@jit(nopython=True)
def gravity(c_real, c_imag, wx,wy, max_iter):
    z_real = 0
    z_imag = 0
    power = 2
    n = 0
    #wx = weight*4
    while z_real * z_real + z_imag * z_imag <= 4 and n < max_iter:
        # ******** original formula **********
        #new_real = z_real * z_real - z_imag * z_imag + c_real
        #new_imag = 2 * z_real * z_imag + c_imag
        # ******** modified formula **********
        new_real = z_real ** power - z_imag ** power + c_real+wx
        new_imag = 2 * z_real * z_imag + c_imag+ wy
        #z_real, z_imag = z_real ** 2 - z_imag ** 2 + c_real, 2 * z_real * z_imag + c_imag

        z_real = new_real
        z_imag = new_imag
        n += 1

    #n = weight
    return n

def draw_mandelbrot(canvas, x_start, y_start, x_end, y_end, max_iter):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()

    x = np.linspace(x_start, x_end, width)
    y = np.linspace(y_start, y_end, height)
    x, y = np.meshgrid(x, y)

    # Use numpy.vectorize to support vectorized computation
    mandelbrot_vectorized = np.vectorize(mandelbrot)

    # Perform parallel computation
    result = mandelbrot_vectorized(x, y, max_iter)

    # Normalize the result to the range [0, 1]
    normalized_result = result / np.max(result)

    # Create an image from the normalized result
    image = np.zeros((height, width), dtype=np.uint8)
    image[:, :] = np.uint8(normalized_result * 255)

    # Clear the canvas
    canvas.delete("all")

    # Iterate over each pixel and draw a rectangle with the corresponding color
    for i in range(width):
        for j in range(height):
            color = image[j, i]  # Get the color at pixel (i, j)
            color_hex = f'#{color:02x}{color:02x}{color:02x}'  # Convert color to hexadecimal
            x1 = i
            y1 = j
            x2 = i + 1
            y2 = j + 1
            canvas.create_rectangle(x1, y1, x2, y2, fill=color_hex, outline='')

'''    
@jit(nopython=True)
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
'''

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
@jit(nopython=True)
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

def draw_julia_image(canvas, x_start, y_start, x_end, y_end, c_real, c_imag, max_iter):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()

    x = np.linspace(x_start, x_end, width)
    y = np.linspace(y_start, y_end, height)
    x, y = np.meshgrid(x, y)

    # 使用 numpy.vectorize 讓函數支援向量化運算
    julia_vectorized = np.vectorize(julia)

    # 進行並行計算
    result = julia_vectorized(x, y, c_real, c_imag, max_iter)

    # 將收斂值轉換成顏色
    r = (result % 256)
    g = ((result * 3) % 256)
    b = ((result * 5) % 256)

    # 建立空白圖像
    image = Image.new("RGB", (width, height))

    # 將收斂值轉換成顏色並設置像素
    for i in range(width):
        for j in range(height):
            color = (r[j, i], g[j, i], b[j, i])
            image.putpixel((i, j), color)

    # 將圖像轉換為 Tkinter 可顯示的格式
    tk_image = ImageTk.PhotoImage(image)

    # 在 Canvas 上顯示圖像
    canvas.create_image(0, 0, anchor="nw", image=tk_image)

    # 設定 Canvas 的圖像參考，避免圖像被垃圾回收
    canvas.image = tk_image


def draw_sierpinski(canvas, x1, y1, x2, y2, x3, y3, depth):
    if depth == 0:
        canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill='black', outline='white')
    else:
        x12 = (x1 + x2) / 2
        y12 = (y1 + y2) / 2
        x13 = (x1 + x3) / 2
        y13 = (y1 + y3) / 2
        x23 = (x2 + x3) / 2
        y23 = (y2 + y3) / 2

        draw_sierpinski(canvas, x1, y1, x12, y12, x13, y13, depth - 1)
        draw_sierpinski(canvas, x12, y12, x2, y2, x23, y23, depth - 1)
        draw_sierpinski(canvas, x13, y13, x23, y23, x3, y3, depth - 1)


def draw_fractal_image(canvas, x_start, y_start, x_end, y_end, max_iter):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()

    x = np.linspace(x_start, x_end, width)
    y = np.linspace(y_start, y_end, height)
    x, y = np.meshgrid(x, y)
    # 使用 numpy.vectorize 讓函數支援向量化運算
    mandelbrot_vectorized = np.vectorize(mandelbrot)

    # 進行並行計算
    result = mandelbrot_vectorized(x, y, max_iter)

    # 將收斂值轉換成顏色
    r = (result % 256)
    g = ((result * 3) % 256)
    b = ((result * 5) % 256)

    # 建立空白圖像
    image = Image.new("RGB", (width, height))

    # 繪製每個像素
    for i in range(width):
        for j in range(height):
            # 將收斂值轉換成顏色並設置像素
            pixel_color = (r[j, i], g[j, i], b[j, i])
            image.putpixel((i, j), pixel_color)

    # 將圖像轉換為Tkinter可顯示的格式
    tk_image = ImageTk.PhotoImage(image)

    # 在Canvas上顯示圖像
    canvas.create_image(0, 0, anchor="nw", image=tk_image)

    # 設定Canvas的圖像參考，避免圖像被垃圾回收
    canvas.image = tk_image

def draw_gravity_image(canvas, x_start, y_start, x_end, y_end, max_iter):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()

    x = np.linspace(x_start, x_end, width)
    y = np.linspace(y_start, y_end, height)
    x, y = np.meshgrid(x, y)
    #w = np.random.randint(0,255,(height, width))
    #w = np.random.random((height, width))
    kx = 10*(x_end-x_start)/width
    ky = 10*(y_end-y_start)/height
    wx = np.random.random(width)*kx
    wy = np.random.random(height)*ky
    wx, wy = np.meshgrid(wx, wy)
    # 使用 numpy.vectorize 讓函數支援向量化運算
    gravity_vectorized = np.vectorize(gravity)

    # 進行並行計算
    result = gravity_vectorized(x, y, wx, wy, max_iter)
    #result = w
    # 將收斂值轉換成顏色
    r = (result % 256)
    g = ((result * 3) % 256)
    b = ((result * 5) % 256)

    # 建立空白圖像
    image = Image.new("RGB", (width, height))

    # 繪製每個像素
    for i in range(width):
        for j in range(height):
            # 將收斂值轉換成顏色並設置像素
            pixel_color = (r[j, i], g[j, i], b[j, i])
            image.putpixel((i, j), pixel_color)

    # 將圖像轉換為Tkinter可顯示的格式
    tk_image = ImageTk.PhotoImage(image)

    # 在Canvas上顯示圖像
    canvas.create_image(0, 0, anchor="nw", image=tk_image)

    # 設定Canvas的圖像參考，避免圖像被垃圾回收
    canvas.image = tk_image
