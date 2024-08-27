import tkinter as tk
from tkinter import ttk
import cv2
import threading
from PIL import Image, ImageTk
import ctypes  # For getting the screen size


def open_multiple_camera_streams(cam_urls):
    """
    Open multiple camera streams using OpenCV in separate threads and display them in new windows.
    """
    # Get the screen size
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Calculate optimal window sizes
    num_cams = len(cam_urls)
    grid_cols = int(num_cams ** 0.5)
    grid_rows = (num_cams + grid_cols - 1) // grid_cols

    win_width = screen_width // grid_cols
    win_height = screen_height // grid_rows

    def open_camera(cam_url, window_name, x, y):
        cap = cv2.VideoCapture(cam_url)

        if not cap.isOpened():
            print(f"Error: Could not open camera stream for {window_name}.")
            return

        cv2.namedWindow(window_name)
        cv2.moveWindow(window_name, x, y)
        cv2.resizeWindow(window_name, win_width, win_height)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to grab frame for {window_name}.")
                break

            frame = cv2.resize(frame, (win_width, win_height))
            cv2.imshow(window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

        cap.release()
        cv2.destroyWindow(window_name)

    for i, cam_url in enumerate(cam_urls):
        col = i % grid_cols
        row = i // grid_cols
        x = col * win_width
        y = row * win_height
        window_name = f"Camera Feed {i + 1}"
        threading.Thread(target=open_camera, args=(cam_url, window_name, x, y), daemon=True).start()


def create_camera_frame(parent, cam_label, cam_urls):
    """
    Create a frame for a group of cameras with a label and a button.
    """
    frame = ttk.Frame(parent, style="Custom.TFrame")
    label = ttk.Label(frame, text=cam_label, font=("Arial", 12, "bold"), style="Custom.TLabel")
    label.pack(padx=5, pady=5)

    button = ttk.Button(frame, text="Open Cameras", style="Rounded.TButton",
                        command=lambda: open_multiple_camera_streams(cam_urls))
    button.pack(pady=10)

    return frame


def start_drag(event):
    """Initialize the drag operation by storing the initial cursor position."""
    global drag_data
    drag_data = {'x': event.x, 'y': event.y}


def on_drag(event):
    """Handle the drag motion by updating the window's position."""
    global drag_data
    new_x = canvas.canvasx(event.x) - drag_data['x']
    new_y = canvas.canvasy(event.y) - drag_data['y']
    canvas.move(main_frame_window, new_x, new_y)


def main():
    global canvas, main_frame, main_frame_window, drag_data

    drag_data = {'x': 0, 'y': 0}

    root = tk.Tk()
    root.title("Camera Interface")
    root.geometry("1200x800")

    background_image = Image.open("tiny-cute-cute-animal-chick_2451418_wh860.png")
    background_image = background_image.resize((1800, 1000), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    canvas = tk.Canvas(root, width=1200, height=800)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=background_photo, anchor="nw")

    style = ttk.Style()
    style.configure("Custom.TFrame", background="#ffffff", relief="solid", padding=15)
    style.configure("Custom.TLabel", font=("Arial", 12), background="#ffffff", foreground="#007bff")
    style.configure("Rounded.TButton", font=("Arial", 10, "bold"), foreground="#000000",
                    background="#007bff", padding=10, relief="flat")
    style.map("Rounded.TButton",
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', '#0056b3'), ('active', '#0056b3')])

    main_frame = ttk.Frame(root, style="Custom.TFrame")
    main_frame_window = canvas.create_window(600, 400, window=main_frame, anchor="center")

    main_frame.bind("<Button-1>", start_drag)
    main_frame.bind("<B1-Motion>", on_drag)

    camera_urls_f1 = [
        "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=1&subtype=0",
        # "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=2&subtype=0",
        "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=3&subtype=0",
    ]

    f1_frame = create_camera_frame(main_frame, "Cam 1 (2 Cameras)", camera_urls_f1)
    f1_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    camera_urls_f2 = [
        "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=4&subtype=0",
        "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=5&subtype=0",
    ]
    f2_frame = create_camera_frame(main_frame, "Cam 2 (2 Cameras)", camera_urls_f2)
    f2_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    camera_urls_f3 = [
        "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=6&subtype=0",
        "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=7&subtype=0",
        "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=8&subtype=0",
        "rtsp://long:Zaq%4012345@nongdanonlnine.ddns.net:554/cam/realmonitor?channel=9&subtype=0",
    ]

    f3_frame = create_camera_frame(main_frame, "Cam 3 (4 Cameras)", camera_urls_f3)
    f3_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    exit_button = ttk.Button(root, text="Exit", style="Rounded.TButton", command=root.destroy)
    canvas.create_window(600, 760, window=exit_button)

    canvas.image = background_photo

    root.mainloop()


if __name__ == "__main__":
    main()
