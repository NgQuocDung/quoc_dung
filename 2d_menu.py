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

        # Giao diện chính
        tk.Button(root, text="Nhập đỉnh", command=self.nhap_dinh).pack(pady=5)
        tk.Button(root, text="Chọn màu tô", command=self.chon_mau).pack(pady=5)
        tk.Button(root, text="Vẽ & tô", command=self.ve_hinh).pack(pady=10)

    def nhap_dinh(self):
        self.vertices.clear()
        n = simpledialog.askinteger("Số đỉnh", "Nhập số đỉnh (>=3):")
        if not n or n < 3:
            messagebox.showwarning("Lỗi", "Cần ít nhất 3 đỉnh để tạo đa giác.")
            return
        # Khởi tạo danh sách đỉnh mặc định (0,0)
        self.vertices = [(0.0, 0.0) for _ in range(n)]

        # Mở bảng nhập tọa độ đỉnh
        self.bang_nhap_toa_do(n)

    def bang_nhap_toa_do(self, n):
        # Tạo cửa sổ con
        self.bang = tk.Toplevel(self.root)
        self.bang.title("Nhập tọa độ các đỉnh")

        tk.Label(self.bang, text="Chỉnh sửa tọa độ x, y cho từng đỉnh:", font=("Arial", 12)).grid(row=0, column=0, columnspan=3, pady=10)

        self.entries = []  # lưu Entry để đọc dữ liệu

        for i in range(n):
            tk.Label(self.bang, text=f"Đỉnh {i}").grid(row=i + 1, column=0, padx=5, pady=2)

            entry_x = tk.Entry(self.bang, width=10)
            entry_x.grid(row=i + 1, column=1, padx=5)
            entry_x.insert(0, str(self.vertices[i][0]))

            entry_y = tk.Entry(self.bang, width=10)
            entry_y.grid(row=i + 1, column=2, padx=5)
            entry_y.insert(0, str(self.vertices[i][1]))

            self.entries.append((entry_x, entry_y))

        # Nút lưu tọa độ
        tk.Button(self.bang, text="Lưu tọa độ", command=self.luu_toa_do).grid(row=n + 1, column=0, columnspan=3, pady=10)

    def luu_toa_do(self):
        new_vertices = []
        try:
            for i, (entry_x, entry_y) in enumerate(self.entries):
                x = float(entry_x.get())
                y = float(entry_y.get())
                new_vertices.append((x, y))
        except ValueError:
            messagebox.showerror("Lỗi", "Tọa độ phải là số thực hợp lệ!")
            return

        self.vertices = new_vertices
        self.bang.destroy()  # Đóng cửa sổ nhập tọa độ

    def chon_mau(self):
        color = colorchooser.askcolor(title="Chọn màu tô")
        if color[1]:
            self.fill_color = color[1]

    def tinh_dien_tich(self):
        # Thuật toán diện tích đa giác (công thức Shoelace)
        x = [p[0] for p in self.vertices]
        y = [p[1] for p in self.vertices]
        n = len(self.vertices)
        s = 0
        for i in range(n):
            s += x[i] * y[(i + 1) % n] - y[i] * x[(i + 1) % n]
        return abs(s) / 2

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

        # Hiển thị diện tích ở góc trên bên trái
        dien_tich = self.tinh_dien_tich()
        fig.text(0.05, 0.02, f"Diện tích = {dien_tich:.3f}", fontsize=12, color='black')


        ax.set_aspect('equal')
        ax.set_title("Đa giác có tô màu")
        ax.grid(True)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = VeHinh2D(root)
    root.mainloop()
