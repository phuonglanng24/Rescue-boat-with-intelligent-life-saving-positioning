
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw  # Add ImageDraw
from tkinter import Canvas, LEFT, RIGHT, BOTH
import cv2
from ultralytics import YOLO
import numpy as np
import requests
import socket
import tkinter as tk
from tkinter import Frame, Button
import cv2
import threading
import customtkinter
from tkintermapview import TkinterMapView
customtkinter.set_default_color_theme("blue")
names = {0: 'Người', 1: 'Xe đạp', 2: 'ô Tô', 3: 'Xe máy', 4: 'airplane', 5: 'Xe bus', 6: 'tàu', 7: 'Xe tải', 8: 'boat', 9: 'Đèn giao thông', 10: 'Vòi chữa cháy', 11: 'Biển báo dừng', 12: 'parking meter', 13: 'Băng ghế', 14: 'bird', 15: 'mèo', 16: 'chó', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'Cốc', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'Cái ghế', 57: 'couch', 58: 'cây trồng trong chậu', 59: 'Giường', 60: 'Bàn ăn', 61: 'Phòng vệ sinh', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 
'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'Bồn Rửa', 72: 'Tủ Lạnh', 73: 'book', 74: 'clock', 75: 'Lọ cắm hoa', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
esp_ip = '192.168.137.196'
esp_port = 23
# Địa chỉ IP và cổng của ESP32-CAM
esp32cam_url = "http://"+esp_ip+"/image"
# Tạo một socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kinhdo=0
vido=0
ktratoado=0
# Kết nối đến server
sock.connect((esp_ip, esp_port))
def on_button_click(dta):
    message = dta+'\n'
    print(f'Sending: {message}')
    sock.sendall(message.encode('utf-8'))
def receive_data_from_server():
    while True:
        try:
            data = sock.recv(1024)  # Đọc dữ liệu từ server
            dulieu = str(data)
            if len(data)>10:
                dulieu = dulieu.replace("b'", "").replace("'", "")
                dulieu = dulieu.replace("\\n", "").replace("\\r", "")
                dulieu=dulieu[0:22]
                print(dulieu)
                fruits = dulieu.split(',')
                global kinhdo
                kinhdo =float(fruits[0])
                # cleaned_string2 = fruits[1].replace("b'", "").replace("'", "")
                # cleaned_string2 = cleaned_string2.replace("\\n", "").replace("\\r", "")
                global vido 
                vido = float(fruits[1])
                print(vido)
            if not data:
                break
            print(f'Received data: {data.decode("utf-8")}')
            # Xử lý dữ liệu nhận được ở đây
        except Exception as e:
            print(f"Lỗi khi nhận dữ liệu từ server: {e}")
            break
def capture_image_from_esp32cam(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        else:
            print("Không thể lấy hình ảnh từ ESP32-CAM")
            return None
    except Exception as e:
        print(f"Lỗi: {e}")
        return None
class App(customtkinter.CTk):

    APP_NAME = "BẢNG ĐIỀU KHIỂN THUYỀN THÔNG MINH"
    WIDTH = 800
    HEIGHT = 500
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set Marker",
                                                command=self.set_marker_event2)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=5, column=0)
        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=6, column=0)
        self.button_open_second_window = customtkinter.CTkButton(master=self.frame_right,
                                                                  text="Open Second Window",
                                                                  command=self.open_second_window)
        self.button_open_second_window.grid(row=0, column=3, sticky="w", padx=(12, 0), pady=12)
        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=7, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=8, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=1, sticky="we", padx=(5, 0), pady=4)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=2, sticky="w", padx=(12, 0), pady=12)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

        # Set default values
        self.map_widget.set_address("Berlin")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")
        self.second_window = None
        self.video_canvas = None
        self.capture = None
        self.photo_image = None
        # Buttons to control camera movement
        self.create_control_buttons()
    def integrate_map_view(self):
        global ktratoado
        # Create map widget in the right frame (or replace the existing map widget)
        # self.map_widget = TkinterMapView(self.frame_right, width=500, height=400, corner_radius=0)
        # self.map_widget.grid(row=1, column=0, sticky="nswe")
        if ktratoado==0:
            self.map_widget.set_address("Hà Nội", marker=True, text="Hà Nội")
            self.map_widget.set_zoom(8)
            self.map_widget.set_marker(16.5256322,111.9385003, text="Quần Đảo Hoàng Sa", text_color="black", font=("Helvetica Bold", 20))
            ktratoado=1
        # # Example to set a marker and zoom level

        # Example to create a polygon
        self.create_polygon()

    def create_polygon(self):
        # Define a polygon
        print("ban_Do")
        print(kinhdo)
        print(vido)
        self.polygon = self.map_widget.set_polygon([(kinhdo, vido), ],
                                                   outline_color="blue",
                                                   border_width=3,
                                                   command=self.polygon_click,
                                                   name="switzerland_polygon")

    def polygon_click(self, polygon):
        print(f"polygon clicked - text: {polygon.name}")
    def create_control_buttons(self):
        button_frame = tk.Frame(self, bg="white")
        button_frame.grid(row=0, column=0, sticky="ew")  # Use grid instead of pack

        left_button = tk.Button(button_frame, text="Trái", command=self.send_command_left)
        right_button = tk.Button(button_frame, text="Phải", command=self.send_command_right)
        forward_button = tk.Button(button_frame, text="Tiến", command=self.send_command_forward)
        stop_button = tk.Button(button_frame, text="Dừng", command=self.send_command_stop)
        mo_button = tk.Button(button_frame, text="Mở", command=self.send_command_mo)
        dong_button = tk.Button(button_frame, text="Đóng", command=self.send_command_dong)
        left_button.grid(row=0, column=0, padx=10)
        right_button.grid(row=0, column=1, padx=10)
        forward_button.grid(row=0, column=2, padx=10)
        stop_button.grid(row=0, column=3, padx=10)
        mo_button.grid(row=0, column=4, padx=10)
        dong_button.grid(row=0, column=5, padx=10)
        # Create video canvas inside the main window
        self.video_canvas = Canvas(self, width=640, height=480)
        self.video_canvas.place(x=0, y=button_frame.winfo_height(), anchor=tk.NW)
    def open_second_window(self):
        if not self.capture:
            self.capture = cv2.VideoCapture(0)

        # Create video canvas inside the video frame
        # self.video_canvas = Canvas(self.video_frame, width=640, height=480)
        # self.video_canvas.grid(row=0, column=0, sticky="nsew")

        # Update video feed
        self.update_video_feed()
    def update_image():
        img = capture_image_from_esp32cam(esp32cam_url)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # im = Image.fromarray(frame)
        results = model(frame)
        annotated_frame = results[0].plot()
        # img = ImageTk.PhotoImage(image=img)
        # cv2.imshow("ESP32-CAM Image", img)
        image = Image.fromarray(annotated_frame)
        anh = ImageTk.PhotoImage(image=image)
        # img = ImageTk.PhotoImage(image=anh)
        # tk.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
        lmain.imgtk = anh
        lmain.configure(image=anh)
        lmain.after(10, update_image)
    def update_video_feed(self):
        img = capture_image_from_esp32cam(esp32cam_url)
        height, width = img.shape[:2]

# Tính toán tâm xoay (center)
        center = (width // 2, height // 2)

        # # Tạo ma trận xoay
        rotation_matrix = cv2.getRotationMatrix2D(center, 180, 1.0)

        # # Xoay hình ảnh
        rotated_image = cv2.warpAffine(img, rotation_matrix, (width, height))
        rgb_frame = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
        # results = model(rgb_frame)
        # annotated_frame = results[0].plot()
        # img = ImageTk.PhotoImage(image=img)
        # cv2.imshow("ESP32-CAM Image", img)
        image1 = Image.fromarray(rotated_image)
        image = ImageTk.PhotoImage(image1)
        app.integrate_map_view()
        self.photo_image = image  # Assign to instance variable
        self.video_canvas.config(width=image.width(), height=image.height())
        self.video_canvas.create_image(0, 0, anchor=tk.NW, image=image)

        # Update the idle tasks to refresh the GUI
        self.update_idletasks()

        self.after(30, self.update_video_feed)
    def send_command_mo(self):
        on_button_click("A")
        # Send a command for camera movement to the left
        print("Sending command: Left")
    def send_command_dong(self):
        on_button_click("B")
        # Send a command for camera movement to the left
        print("Sending command: Left")
    def send_command_left(self):
        on_button_click("L")
        # Send a command for camera movement to the left
        print("Sending command: Left")

    def send_command_right(self):
        on_button_click("R")
        # Send a command for camera movement to the right
        print("Sending command: Right")

    def send_command_forward(self):
        on_button_click("F")
        # Send a command for camera movement forward
        print("Sending command: Forward")

    def send_command_stop(self):
        on_button_click("S")
        # Send a command to stop camera movement
        print("Sending command: Stop")
    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())
    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))
    def set_marker_event2(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))
    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    receive_thread = threading.Thread(target=receive_data_from_server)
    receive_thread.daemon = True  # Đặt luồng là daemon để nó tự động kết thúc khi chương trình chính kết thúc
    receive_thread.start()
    app.start()
