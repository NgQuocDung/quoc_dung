import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

class VeHinh2D:
    def __init__(self, root):
        self.root = root
        self.root.title("Vẽ đa giác và tô màu")
        self.vertices = []
        self.fill_color = '#00FFFF'  # Màu tô mặc định

        # Giao diện
        tk.Button(root, text="Nhập đỉnh", command=self.nhap_dinh).pack(pady=5)
        tk.Button(root, text="Chọn màu tô", command=self.chon_mau).pack(pady=5)
        tk.Button(root, text="Vẽ & tô", command=self.ve_hinh).pack(pady=10)

    def nhap_dinh(self):
        self.vertices.clear()
        n = simpledialog.askinteger("Số đỉnh", "Nhập số đỉnh (>=3):")
        if not n or n < 3:
            messagebox.showwarning("Lỗi", "Cần ít nhất 3 đỉnh để tạo đa giác.")
            return

        for i in range(n):
            text = simpledialog.askstring("Tọa độ", f"Đỉnh {i} (x y):")
            if not text:
                return
            try:
                x, y = map(float, text.strip().split())
                self.vertices.append((x, y))
            except:
                messagebox.showerror("Lỗi", "Nhập tọa độ không hợp lệ.")
                return

    def chon_mau(self):
        color = colorchooser.askcolor(title="Chọn màu tô")
        if color[1]:
            self.fill_color = color[1]

    def ve_hinh(self):
        if len(self.vertices) < 3:
            messagebox.showwarning("Thiếu đỉnh", "Cần ít nhất 3 đỉnh.")
            return

        fig, ax = plt.subplots()

        # Tô đa giác
        polygon = Polygon(self.vertices, closed=True, facecolor=self.fill_color, edgecolor='black', linewidth=1)
        ax.add_patch(polygon)

        # Vẽ các đỉnh
        xs, ys = zip(*self.vertices)
        ax.plot(xs + (xs[0],), ys + (ys[0],), 'bo-')  # Nối lại về đỉnh đầu

        for idx, (x, y) in enumerate(self.vertices):
            ax.text(x, y, f'{idx}', fontsize=9, ha='right', va='bottom', color='black')

        ax.set_aspect('equal')
        ax.set_title("Đa giác có tô màu")
        ax.grid(True)
        plt.show()

# Chạy chương trình
if __name__ == "__main__":
    root = tk.Tk()
    app = VeHinh2D(root)
    root.mainloop()
