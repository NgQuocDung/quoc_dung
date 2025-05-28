import tkinter as tk
from tkinter import messagebox
import subprocess
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HAMSO_PATH = os.path.join(CURRENT_DIR, "Hamso.py")
MENU_2D_PATH = os.path.join(CURRENT_DIR, "2d_menu.py")
MENU_3D_PATH = os.path.join(CURRENT_DIR, "3d_menu.py")

# Kiểm tra file Hamso.py có tồn tại
for path, name in [(HAMSO_PATH, "Hamso.py"), (MENU_2D_PATH, "2d_menu.py"), (MENU_3D_PATH, "3d_menu.py")]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file {name}!")


def ve_do_thi_ham_so():
    try:
        subprocess.Popen(["python", HAMSO_PATH])
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {HAMSO_PATH}: {e}")

def ve_hinh_2d():
    try:
        subprocess.run(["python", MENU_2D_PATH], check=True)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {MENU_2D_PATH}: {e}")

def ve_hinh_3d():
    try:
        subprocess.run(["python", MENU_3D_PATH], check=True)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {MENU_3D_PATH}: {e}")

def main_gui():
    root = tk.Tk()
    root.title("Chọn Chức Năng")
    root.geometry("400x400")

    tk.Label(root, text="Chọn một chức năng:", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Tính hàm số", font=("Arial", 12), command=ve_do_thi_ham_so).pack(pady=10)
    tk.Button(root, text="Vẽ các hình 2D và tô màu", font=("Arial", 12), command=ve_hinh_2d).pack(pady=10)
    tk.Button(root, text="Vẽ các hình 3D", font=("Arial", 12), command=ve_hinh_3d).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
