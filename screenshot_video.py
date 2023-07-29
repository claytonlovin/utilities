import cv2
import pyautogui
import numpy as np
import time
import tkinter as tk
from tkinter import messagebox
import threading

capturing = False
video_filename = ""
start_time = 0
video_counter = 1

def start_capture():
    global capturing, start_time, video_counter
    capturing = True
    start_time = time.time()
    
    start_button.config(state=tk.DISABLED)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 1.0

    global video_filename
    video_filename = f"captura_tela_{video_counter}.mp4"
    video_counter += 1

    video_out = cv2.VideoWriter(video_filename, fourcc, fps, (screen_width, screen_height))

    update_timer()

    while capturing:
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(
            np.array(screenshot),
            cv2.COLOR_RGB2BGR
        )

        video_out.write(frame)

        time.sleep(0.1)

    video_out.release()
    start_button.config(state=tk.NORMAL)

def update_timer():
    if capturing:
        elapsed_time = time.time() - start_time
        hours = int(elapsed_time / 3600)
        minutes = int((elapsed_time % 3600) / 60)
        seconds = int(elapsed_time % 60)
        timer_label.config(text=f"Tempo decorrido: {hours:02d}:{minutes:02d}:{seconds:02d}")
        root.after(1000, update_timer)

def stop_capture():
    global capturing
    capturing = False

def show_info():
    messagebox.showinfo("Informações", "Pressione o botão 'Iniciar Captura' para começar a gravar a tela. Pressione o botão 'Parar Captura' para interromper a gravação.")

screen_width, screen_height = pyautogui.size()

root = tk.Tk()
root.title("Captura de Tela")
root.geometry("300x250")

timer_label = tk.Label(root, text="Tempo decorrido: 00:00:00")
timer_label.pack(pady=20)

start_button = tk.Button(root, text="Iniciar Captura", command=lambda: threading.Thread(target=start_capture).start())
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Parar Captura", command=stop_capture)
stop_button.pack(pady=10)

info_button = tk.Button(root, text="Informações", command=show_info)
info_button.pack(pady=5)

root.mainloop()
