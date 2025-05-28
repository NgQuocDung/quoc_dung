import tkinter as tk
from tkinter import simpledialog, messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D  # Cần để kích hoạt 3D projection

class Hinh3DApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vẽ hình 3D - Đỉnh, cạnh, và hình đặc biệt")

        self.vertices = []
        self.edges = []

        self.init_gui()

    def init_gui(self):
        tk.Button(self.root, text="1. Nhập số đỉnh và tọa độ", command=self.nhap_dinh).pack(pady=3)
        tk.Button(self.root, text="2. Nhập các cạnh", command=self.nhap_canh).pack(pady=3)
        tk.Button(self.root, text="3. Vẽ hình tùy chỉnh", command=self.ve_hinh).pack(pady=10)
        # Thêm các nút cho hình đặc biệt:
        tk.Button(self.root, text="Vẽ Hình cầu", command=self.ve_hinh_cau).pack(pady=3)
        tk.Button(self.root, text="Vẽ Hình trụ tròn đều", command=self.ve_hinh_tru).pack(pady=3)
        tk.Button(self.root, text="Vẽ Hình chóp đáy tròn", command=self.ve_hinh_chop_tron).pack(pady=3)


    # --- Nhập đỉnh và cạnh như trước ---
    def nhap_dinh(self):
        n = simpledialog.askinteger("Số đỉnh", "Nhập số đỉnh:")
        if n is None or n <= 0:
            return
        self.vertices = [(0.0, 0.0, 0.0) for _ in range(n)]
        self.bang_nhap_dinh(n)

    def bang_nhap_dinh(self, n):
        self.win_dinh = tk.Toplevel(self.root)
        self.win_dinh.title("Nhập/Sửa tọa độ các đỉnh")

        tk.Label(self.win_dinh, text="Đỉnh", width=5).grid(row=0, column=0)
        tk.Label(self.win_dinh, text="X", width=10).grid(row=0, column=1)
        tk.Label(self.win_dinh, text="Y", width=10).grid(row=0, column=2)
        tk.Label(self.win_dinh, text="Z", width=10).grid(row=0, column=3)

        self.entries_dinh = []
        for i in range(n):
            tk.Label(self.win_dinh, text=str(i)).grid(row=i+1, column=0)
            entry_x = tk.Entry(self.win_dinh, width=10)
            entry_x.grid(row=i+1, column=1)
            entry_x.insert(0, str(self.vertices[i][0]))
            entry_y = tk.Entry(self.win_dinh, width=10)
            entry_y.grid(row=i+1, column=2)
            entry_y.insert(0, str(self.vertices[i][1]))
            entry_z = tk.Entry(self.win_dinh, width=10)
            entry_z.grid(row=i+1, column=3)
            entry_z.insert(0, str(self.vertices[i][2]))
            self.entries_dinh.append((entry_x, entry_y, entry_z))

        tk.Button(self.win_dinh, text="Lưu tọa độ", command=self.luu_dinh).grid(row=n+1, column=0, columnspan=4, pady=10)

    def luu_dinh(self):
        try:
            new_vertices = []
            for entry_x, entry_y, entry_z in self.entries_dinh:
                x = float(entry_x.get())
                y = float(entry_y.get())
                z = float(entry_z.get())
                new_vertices.append((x, y, z))
            self.vertices = new_vertices
            self.win_dinh.destroy()
            messagebox.showinfo("Thông báo", "Đã lưu tọa độ đỉnh.")
        except ValueError:
            messagebox.showerror("Lỗi", "Tọa độ phải là số thực hợp lệ!")

    def nhap_canh(self):
        if not self.vertices:
            messagebox.showwarning("Chưa có đỉnh", "Bạn cần nhập đỉnh trước.")
            return

        m = simpledialog.askinteger("Số cạnh", "Nhập số cạnh:")
        if m is None or m <= 0:
            return

        self.edges = [(0, 0) for _ in range(m)]
        self.bang_nhap_canh(m)

    def bang_nhap_canh(self, m):
        self.win_canh = tk.Toplevel(self.root)
        self.win_canh.title("Nhập/Sửa các cạnh")

        tk.Label(self.win_canh, text="Cạnh", width=5).grid(row=0, column=0)
        tk.Label(self.win_canh, text="Đỉnh A", width=10).grid(row=0, column=1)
        tk.Label(self.win_canh, text="Đỉnh B", width=10).grid(row=0, column=2)

        self.entries_canh = []
        for i in range(m):
            tk.Label(self.win_canh, text=str(i)).grid(row=i+1, column=0)
            entry_a = tk.Entry(self.win_canh, width=10)
            entry_a.grid(row=i+1, column=1)
            entry_a.insert(0, str(self.edges[i][0]))
            entry_b = tk.Entry(self.win_canh, width=10)
            entry_b.grid(row=i+1, column=2)
            entry_b.insert(0, str(self.edges[i][1]))
            self.entries_canh.append((entry_a, entry_b))

        tk.Button(self.win_canh, text="Lưu các cạnh", command=self.luu_canh).grid(row=m+1, column=0, columnspan=3, pady=10)

    def luu_canh(self):
        try:
            new_edges = []
            for entry_a, entry_b in self.entries_canh:
                a = int(entry_a.get())
                b = int(entry_b.get())
                if a < 0 or b < 0 or a >= len(self.vertices) or b >= len(self.vertices):
                    messagebox.showerror("Lỗi", f"Chỉ số đỉnh không hợp lệ: {a}, {b}")
                    return
                new_edges.append((a, b))
            self.edges = new_edges
            self.win_canh.destroy()
            messagebox.showinfo("Thông báo", "Đã lưu các cạnh.")
        except ValueError:
            messagebox.showerror("Lỗi", "Chỉ số đỉnh phải là số nguyên hợp lệ!")

    def ve_hinh(self):
        if not self.vertices or not self.edges:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ đỉnh và cạnh.")
            return

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for (i, j) in self.edges:
            x = [self.vertices[i][0], self.vertices[j][0]]
            y = [self.vertices[i][1], self.vertices[j][1]]
            z = [self.vertices[i][2], self.vertices[j][2]]
            ax.plot(x, y, z, color='blue')

        xs, ys, zs = zip(*self.vertices)
        ax.scatter(xs, ys, zs, color='red')

        for idx, (x, y, z) in enumerate(self.vertices):
            ax.text(x, y, z, f'{idx}', fontsize=9, color='black')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Hình 3D do người dùng nhập')
        ax.view_init(elev=20, azim=30)
        plt.show()

        # --- Vẽ hình cầu ---
    def ve_hinh_cau(self):
        r = simpledialog.askfloat("Hình cầu", "Nhập bán kính r:")
        if r is None or r <= 0:
            return

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        u = np.linspace(0, 2 * np.pi, 40)
        v = np.linspace(0, np.pi, 20)
        x = r * np.outer(np.cos(u), np.sin(v))
        y = r * np.outer(np.sin(u), np.sin(v))
        z = r * np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_surface(x, y, z, color='cyan', alpha=0.6)
        ax.set_title('Hình cầu bán kính r={}'.format(r))

        the_tich = (4/3) * math.pi * r**3
        # Thêm text thể tích vào cửa sổ matplotlib
        fig.text(0.05, 0.05, f"Thể tích: {the_tich:.3f}", fontsize=12, color='black')

        plt.show()

    # --- Vẽ hình trụ tròn đều ---
    def ve_hinh_tru(self):
        r = simpledialog.askfloat("Hình trụ", "Nhập bán kính đáy r:")
        h = simpledialog.askfloat("Hình trụ", "Nhập chiều cao h:")
        if r is None or r <= 0 or h is None or h <= 0:
            return

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        theta = np.linspace(0, 2 * np.pi, 40)
        z = np.linspace(0, h, 20)
        theta, z = np.meshgrid(theta, z)
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        ax.plot_surface(x, y, z, color='orange', alpha=0.6)

        # Vẽ 2 đáy
        x_d = r * np.cos(theta[0])
        y_d = r * np.sin(theta[0])
        ax.plot_trisurf(x_d, y_d, np.zeros_like(x_d), color='orange', alpha=0.6)
        ax.plot_trisurf(x_d, y_d, h * np.ones_like(x_d), color='orange', alpha=0.6)

        ax.set_title('Hình trụ r={}, h={}'.format(r, h))

        the_tich = math.pi * r**2 * h
        fig.text(0.05, 0.05, f"Thể tích: {the_tich:.3f}", fontsize=12, color='black')

        plt.show()

    def ve_hinh_chop_tron(self):
        r = simpledialog.askfloat("Hình chóp tròn", "Nhập bán kính đáy r:")
        h = simpledialog.askfloat("Hình chóp tròn", "Nhập chiều cao h:")
        if r is None or r <= 0 or h is None or h <= 0:
            messagebox.showerror("Lỗi", "Bán kính và chiều cao phải > 0")
            return

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Tạo mặt đáy tròn với tam giác
        theta = np.linspace(0, 2*np.pi, 40)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.zeros_like(theta)

        # Tạo tam giác mặt đáy
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts, color='cyan', alpha=0.6))

        # Đỉnh chóp
        apex = np.array([0, 0, h])

        # Vẽ các tam giác tạo thành mặt xung quanh
        for i in range(len(theta)-1):
            xs = [x[i], x[i+1], apex[0]]
            ys = [y[i], y[i+1], apex[1]]
            zs = [z[i], z[i+1], apex[2]]
            verts = [list(zip(xs, ys, zs))]
            poly = Poly3DCollection(verts, alpha=0.5, facecolors='purple')
            ax.add_collection3d(poly)

        # Vẽ đỉnh và các điểm đáy
        ax.scatter(0, 0, h, color='red')
        ax.scatter(x, y, z, color='red')

        ax.set_title(f'Hình chóp đáy tròn r={r}, h={h}')
        ax.set_xlim(-r*1.2, r*1.2)
        ax.set_ylim(-r*1.2, r*1.2)
        ax.set_zlim(0, h*1.2)
        ax.view_init(elev=20, azim=30)

        # Thể tích hình nón
        the_tich = (1/3) * math.pi * r**2 * h
        fig.text(0.05, 0.05, f"Thể tích: {the_tich:.3f}", fontsize=12, color='black')

        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = Hinh3DApp(root)
    root.mainloop()
