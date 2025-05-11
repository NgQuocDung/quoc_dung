import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Hinh3DApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nhập đỉnh và cạnh để vẽ hình 3D")

        self.vertices = []
        self.edges = []

        self.init_gui()

    def init_gui(self):
        tk.Button(self.root, text="1. Nhập số đỉnh và tọa độ", command=self.nhap_dinh).pack(pady=5)
        tk.Button(self.root, text="2. Nhập các cạnh", command=self.nhap_canh).pack(pady=5)
        tk.Button(self.root, text="3. Vẽ hình", command=self.ve_hinh).pack(pady=10)

    def nhap_dinh(self):
        try:
            self.vertices.clear()
            n = simpledialog.askinteger("Số đỉnh", "Nhập số đỉnh:")
            if n is None or n <= 0: return

            for i in range(n):
                text = simpledialog.askstring("Tọa độ đỉnh", f"Đỉnh {i} (dạng x y z):")
                if not text: return
                x, y, z = map(float, text.strip().split())
                self.vertices.append((x, y, z))

            messagebox.showinfo("Thông báo", f"Đã nhập {n} đỉnh.")
        except:
            messagebox.showerror("Lỗi", "Dữ liệu không hợp lệ.")

    def nhap_canh(self):
        try:
            self.edges.clear()
            if not self.vertices:
                messagebox.showwarning("Chưa có đỉnh", "Bạn cần nhập đỉnh trước.")
                return

            m = simpledialog.askinteger("Số cạnh", "Nhập số cạnh:")
            if m is None or m <= 0: return

            for i in range(m):
                text = simpledialog.askstring("Cạnh", f"Cạnh {i+1} (dạng a b):")
                if not text: return
                a, b = map(int, text.strip().split())
                if a >= len(self.vertices) or b >= len(self.vertices):
                    messagebox.showerror("Lỗi", "Chỉ số đỉnh không hợp lệ.")
                    return
                self.edges.append((a, b))

            messagebox.showinfo("Thông báo", f"Đã nhập {m} cạnh.")
        except:
            messagebox.showerror("Lỗi", "Dữ liệu không hợp lệ.")

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

# Khởi động ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = Hinh3DApp(root)
    root.mainloop()
