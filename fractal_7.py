import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageGrab
import fractal_lib

# 建立GUI應用程式
def create_gui():
    root = tk.Tk()
    root.title('Fractal Generator')
    previous_views = []
    canvas_width = 1024
    canvas_height = 768
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # 設定區域範圍和迭代次數的預設值
    x_start, y_start, x_end, y_end = -2, -2, 2, 2
    max_iter = 512
    start_x, start_y = None, None
    def save_fractal_image(canvas, filename):
        # 取得Canvas的視窗座標
        x, y, width, height = canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_width(), canvas.winfo_height()

        # 擷取Canvas的螢幕截圖
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # 將截圖儲存為JPEG格式的圖片
        screenshot.save(filename, "JPEG")

    def save_button_click():
        # 詢問使用者要儲存圖片的檔案路徑和檔名
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
        # 檢查是否有前一個檢視畫面
        #print(f'length of previous_views = {len(previous_views)}')
        if len(previous_views) >= 1:
            # 移除目前檢視畫面

            #print(f'*** after pop :::length of previous_views = {len(previous_views)}')
            # 取得前一個檢視畫面
            x_start, y_start, x_end, y_end = previous_views[-1]

            #print(f'*** before re-draw {previous_views}')
            # 重新繪製碎形
            draw_button_click()

            #print(f'**** after re_draw {previous_views}')
            previous_views.pop()


    def on_release(event):
        nonlocal x_start, y_start, x_end, y_end, start_x, start_y, previous_views

        # 將目前檢視畫面儲存到前一個檢視畫面清單
        previous_views.append((x_start, y_start, x_end, y_end))
        #print(f'* previous append:: {previous_views}, len = {len(previous_views)}')
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


        # 重新繪製碎形
        #canvas.delete('all')
        draw_button_click()
        # 刪除選擇區域的框線
        canvas.delete('selection_rectangle')
        start_x, start_y = None, None

    def draw_fractal():
        print(f'x_start={x_start},y_start={y_start},x_end={x_end},y_end={y_end}')
        fractal_lib.draw_fractal_image(canvas, x_start, y_start, x_end, y_end, max_iter)

    def draw_julia():
        c_real, c_imag = -0.7, 0.27
        fractal_lib.draw_julia_image(canvas, x_start, y_start, x_end, y_end, c_real, c_imag, max_iter)

    def draw_gravity():
        fractal_lib.draw_gravity_image(canvas, x_start, y_start, x_end, y_end, max_iter)

    def draw_button_click():
        # 重新繪製碎形
        canvas.delete('all')
        if selected_fractal.get() == 'Mandelbrot':
            draw_fractal()
        elif selected_fractal.get() == 'Julia Set':
            draw_julia()
        elif selected_fractal.get() == 'Gravity':
            draw_gravity()


    # 綁定滑鼠事件
    canvas.bind('<ButtonPress-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)

    # 建立碎形繪製函式的選擇框
    selected_fractal = tk.StringVar(value='Mandelbrot')
    fractal_options = tk.OptionMenu(root, selected_fractal, 'Mandelbrot', 'Julia Set', 'Gravity')
    fractal_options.pack()

    # 建立儲存圖片的按鈕
    save_button = tk.Button(root, text="Save", command=save_button_click)
    save_button.pack()

    # 建立回到前一個檢視畫面的按鈕
    previous_button = tk.Button(root, text="Previous View", command=previous_view)
    previous_button.pack()

    # 建立重新繪製碎形的按鈕
    draw_button = tk.Button(root, text="Draw", command=draw_button_click)
    draw_button.pack()

    # 初始畫面繪製
    draw_fractal()

    root.mainloop()

if __name__ == '__main__':
    create_gui()
