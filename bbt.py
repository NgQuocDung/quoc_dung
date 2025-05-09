import sympy as sp
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox

def ve_bang_bien_thien(expr_str):
    try:
        x = sp.symbols('x')
        # Bước 1: Chuyển đổi chuỗi hàm số thành hàm SymPy
        try:
            f = sp.sympify(expr_str)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Hàm số không hợp lệ: {e}")
            return

        df = sp.diff(f, x)

        # 2. Tìm nghiệm của f'(x) = 0
        critical_points = sp.solve(df, x)
        denominator = sp.denom(f)
        undefined_points = sp.solve(denominator, x)
        all_points = list(set(critical_points + undefined_points))
        all_points_real = [pt.evalf() for pt in all_points if sp.im(pt) == 0]
        all_points_real = sorted(all_points_real)

        # Phân tích dấu đạo hàm trên từng khoảng
        intervals = []
        for i in range(len(all_points_real) + 1):
            if i == 0:
                left = -sp.oo
                right = all_points_real[i]
            elif i == len(all_points_real):
                left = all_points_real[i - 1]
                right = sp.oo
            else:
                left = all_points_real[i - 1]
                right = all_points_real[i]
            
            mid = (left + right) / 2 if right != sp.oo and left != -sp.oo else (right - 1 if right != sp.oo else left + 1)
            sign = sp.N(df.subs(x, mid))
            intervals.append(("+" if sign > 0 else "-" if sign < 0 else "0", mid))

        # Tính giá trị f(x) tại các điểm đặc biệt
        values_fx = [f.subs(x, pt).evalf() for pt in all_points_real]

        # Vẽ bảng biến thiên
        fig, ax = plt.subplots(figsize=(10, 6))  # Tăng chiều cao đồ thị
        ax.axis("off")

        x_labels = ["$-\\infty$"] + [f"{pt:.2f}" for pt in all_points_real] + ["$+\\infty$"]
        y_positions = [3.5, 2, 1]  # Điều chỉnh vị trí các hàng: x, f'(x), f(x)

        # Kẻ các đường ngang
        ax.hlines(y_positions[0], -1, len(x_labels), color='black', linewidth=1.2)  # Hàng x
        ax.hlines(y_positions[1], -1, len(x_labels), color='black', linewidth=1.2)  # Hàng f'(x)

        # Kẻ các đường thẳng đứng
        ax.vlines(-0.5, 0, 4, color='black', linestyle='-', linewidth=1.2)

        # Nhãn cho các dòng
        ax.text(-1.2, y_positions[0] + 0.1, "x", fontsize=12, weight="bold")
        ax.text(-1.2, y_positions[1] + 0.1, "$f'(x)$", fontsize=12, weight="bold")
        ax.text(-1.2, y_positions[2] + 0.1, "$f(x)$", fontsize=12, weight="bold")

        # Ghi các giá trị x
        for i, label in enumerate(x_labels):
            ax.text(i, y_positions[0] + 0.1, label, ha='center', va='center', fontsize=12)

        # Ghi dấu đạo hàm f'(x) và giá trị 0 của f'(x)
        for i, _ in enumerate(intervals):
            # Kiểm tra xem điểm tương ứng có phải là điểm tới hạn (critical point) không
            if i < len(all_points_real):
                pt = all_points_real[i]
                if pt in critical_points:
                    ax.text(i + 1, y_positions[1] + 0.05, "0", ha='center', va='center', fontsize=12, color="blue")
                else:
                    sign = intervals[i][0]
                    ax.text(i + 0.5, y_positions[1] + 0.05, sign, ha='center', va='center', fontsize=12)
            else:
                sign = intervals[i][0]
                ax.text(i + 0.5, y_positions[1] + 0.05, sign, ha='center', va='center', fontsize=12)

        # Ghi giá trị f(x) tại các điểm quan trọng và vẽ mũi tên biến thiên
        for i, pt in enumerate(all_points_real):
            val = values_fx[i]
            ax.text(i + 1, y_positions[2] - 0.3, f"{val:.2f}" if val.is_real else "undefined", ha='center', va='center', fontsize=12)

        # Vẽ mũi tên biến thiên
        for i in range(len(intervals)):
            x1 = i
            x2 = i + 1
            try:
                if intervals[i][0] == "+":
                    # Tăng dần: Mũi tên hướng lên
                    y1, y2 = 1.2, 1.8
                elif intervals[i][0] == "-":
                    # Giảm dần: Mũi tên hướng xuống
                    y1, y2 = 1.8, 1.2
                else:
                    # Không đổi (f'(x) = 0)
                    y1 = y2 = 1.5
                ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                            arrowprops=dict(arrowstyle="->", linewidth=1.5))
            except:
                pass

        ax.set_xlim(-1.5, len(x_labels) + 1)
        ax.set_ylim(0, 4)
        plt.title(f"Bảng biến thiên của hàm: {expr_str}", fontsize=14)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

def run_gui():
    def on_submit():
        expr = input_entry.get()
        if not expr.strip():
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập hàm số!")
        else:
            ve_bang_bien_thien(expr)

    root = Tk()
    root.title("Vẽ Bảng Biến Thiên")
    root.geometry("400x200")

    label = Label(root, text="Nhập hàm số (e.g., x**2 - 3*x):", font=("Arial", 12))
    label.pack(pady=10)

    input_entry = Entry(root, font=("Arial", 14), width=30)
    input_entry.pack(pady=10)

    submit_button = Button(root, text="Vẽ Bảng Biến Thiên", font=("Arial", 12), command=on_submit)
    submit_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_gui()