import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Đường dẫn đến các file bbt.py, CuoiKy.py, 2d_menu.py và 3d_menu.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BBT_PATH = os.path.join(CURRENT_DIR, "Bangbienthien.py")
DOTHI_PATH = os.path.join(CURRENT_DIR, "Dothihamso.py")
MENU_2D_PATH = os.path.join(CURRENT_DIR, "2d_menu.py")
MENU_3D_PATH = os.path.join(CURRENT_DIR, "3d_menu.py")


# Kiểm tra các file có tồn tại không
if not os.path.exists(BBT_PATH) or not os.path.exists(DOTHI_PATH):
    raise FileNotFoundError("Không tìm thấy file bbt.py hoặc CuoiKy.py!")

# Hàm gọi file bbt.py để tính đạo hàm và vẽ bảng biến thiên
def ve_bang_bien_thien():
    try:
        subprocess.run(["python", BBT_PATH], check=True)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {BBT_PATH}: {e}")

# Hàm gọi file CuoiKy.py để tìm nghiệm và vẽ đồ thị
def ve_do_thi():
    try:
        subprocess.run(["python", DOTHI_PATH], check=True)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {DOTHI_PATH}: {e}")

# Hàm gọi file 2d_menu.py để vẽ hình 2D
def ve_hinh_2d():
    try:
        subprocess.run(["python", MENU_2D_PATH], check=True)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {MENU_2D_PATH}: {e}")

# Hàm gọi file 3d_menu.py để vẽ hình 3D
def ve_hinh_3d():
    try:
        subprocess.run(["python", MENU_3D_PATH], check=True)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy {MENU_3D_PATH}: {e}")

# Giao diện chính
def main_gui():
    root = tk.Tk()
    root.title("Chọn Chức Năng")
    root.geometry("400x400")

    tk.Label(root, text="Chọn một chức năng:", font=("Arial", 14)).pack(pady=20)

    # Nút cho từng chức năng
    tk.Button(root, text="Tính đạo hàm và vẽ bảng biến thiên", font=("Arial", 12), command=ve_bang_bien_thien).pack(pady=10)
    tk.Button(root, text="Tìm nghiệm và vẽ đồ thị", font=("Arial", 12), command=ve_do_thi).pack(pady=10)
    tk.Button(root, text="Vẽ các hình 2D và tô màu", font=("Arial", 12), command=ve_hinh_2d).pack(pady=10)
    tk.Button(root, text="Vẽ các hình 3D", font=("Arial", 12), command=ve_hinh_3d).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_gui()
