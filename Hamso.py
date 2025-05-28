import tkinter as tk
from tkinter import messagebox
import sys
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Biến toàn cục
x = sp.symbols('x')
zoom = 50  # Zoom mặc định
expr = None  # Biểu thức hàm số
solutions_real = []  # Danh sách nghiệm thực
solutions_all = []   # Danh sách tất cả nghiệm

# === Hàm vẽ bảng biến thiên (cập nhật vẽ vào ax_left) ===
def ve_bang_bien_thien(expr_str, ax_left):
    ax_left.clear()
    try:
        f = sp.sympify(expr_str)
        df = sp.diff(f, x)
        
        # toạn độ của đạo hàm
        ax_left.text(0.5, 1.08, r"$f'(x) = %s$" % sp.latex(df), ha='center', va='center', fontsize=18, transform=ax_left.transAxes)

        critical_points = sp.solve(df, x)
        denominator = sp.denom(f)
        undefined_points = sp.solve(denominator, x)
        all_points = sorted(set(critical_points + undefined_points))
        all_points_real = [pt.evalf() for pt in all_points if sp.im(pt) == 0]

        if len(all_points_real) > 10:
            raise ValueError("Hàm số quá phức tạp để vẽ bảng biến thiên.")

        intervals = []
        for i in range(len(all_points_real) + 1):
            if i == 0:
                left, right = -sp.oo, all_points_real[i]
            elif i == len(all_points_real):
                left, right = all_points_real[i - 1], sp.oo
            else:
                left, right = all_points_real[i - 1], all_points_real[i]

            if left == -sp.oo and right != sp.oo:
                mid = right - 1
            elif right == sp.oo and left != -sp.oo:
                mid = left + 1
            elif left == -sp.oo and right == sp.oo:
                mid = 0
            else:
                mid = (left + right) / 2

            sign = sp.N(df.subs(x, mid))
            if sign > 0:
                intervals.append(("+", mid))
            elif sign < 0:
                intervals.append(("-", mid))
            else:
                intervals.append(("0", mid))

        values_fx = [f.subs(x, pt).evalf() for pt in all_points_real]

        ax_left.set_xlim(-1.5, len(all_points_real) + 1)
        ax_left.set_ylim(0, 3)
        ax_left.axis("off")

        x_labels = [r"$-\infty$"] + [f"{pt:.2f}" for pt in all_points_real] + [r"$+\infty$"]
        y_positions = [2.5, 1.4, 0.6]

        ax_left.hlines(y_positions[0], -1, len(x_labels), color='black', linewidth=1.2)
        ax_left.hlines(y_positions[1], -1, len(x_labels), color='black', linewidth=1.2)
        ax_left.hlines(y_positions[2], -1, len(x_labels), color='black', linewidth=1.2)
        ax_left.vlines(-0.5, 0, 3, color='black', linewidth=1.2)

        ax_left.text(-1.2, y_positions[0] + 0.1, "x", fontsize=14, weight='bold')
        ax_left.text(-1.2, y_positions[1] + 0.1, "$f'(x)$", fontsize=14, weight='bold')
        ax_left.text(-1.2, y_positions[2] + 0.1, "$f(x)$", fontsize=14, weight='bold')

        for i, lbl in enumerate(x_labels):
            ax_left.text(i, y_positions[0] + 0.1, lbl, ha='center', va='center', fontsize=14)

        for i, (sgn, _) in enumerate(intervals):
            pos_x = i + 0.5
            if i < len(all_points_real) and all_points_real[i] in critical_points:
                ax_left.text(i + 1, y_positions[1] + 0.05, "0", ha='center', va='center', fontsize=14, color='blue')
            else:
                ax_left.text(pos_x, y_positions[1] + 0.05, sgn, ha='center', va='center', fontsize=14)

        for i, val in enumerate(values_fx):
            text_val = f"{val:.2f}" if val.is_real else "undef"
            ax_left.text(i + 1, y_positions[2] - 0.2, text_val, ha='center', va='center', fontsize=14)

        for i, (sgn, _) in enumerate(intervals):
            x1, x2 = i, i + 1
            if sgn == '+':
                y1, y2 = 0.7, 1.2
            elif sgn == '-':
                y1, y2 = 1.2, 0.7
            else:
                y1 = y2 = 0.95
            ax_left.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', linewidth=1.5))

    except Exception as e:
        ax_left.axis("off")
        ax_left.text(0.5, 0.5, f"Không thể vẽ bảng biến thiên vì hàm số có nghiệm phức:\n{e}", ha='center', va='center', fontsize=14, color='red')

# === Hàm vẽ đồ thị + nghiệm (cập nhật ax_right) ===
def plot_graph(ax_right):
    global expr, solutions_real, zoom
    ax_right.clear()
    if expr is None:
        ax_right.text(0.5, 0.5, "Chưa có hàm số để vẽ", ha='center', va='center', fontsize=14, color='gray', transform=ax_right.transAxes)
        return
    try:
        f = sp.lambdify(x, expr, modules=["numpy"])
        range_x = 10 * 50 / zoom
        x_vals = np.linspace(-range_x, range_x, 1000)
        y_vals = f(x_vals)

        ax_right.axhline(0, color='black', linewidth=1)
        ax_right.axvline(0, color='black', linewidth=1)
        ax_right.grid(True, linestyle='--', alpha=0.5)
        ax_right.plot(x_vals, y_vals, label=f"y = {str(expr)}", color="blue")

        for sol in solutions_real:
            val = float(sp.N(sol))
            ax_right.plot(val, 0, 'ro')
            ax_right.annotate(f"x = {val:.2f}", (val, 0), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12, color='red')

        ax_right.set_title("Đồ thị hàm số và nghiệm", fontsize=16)
        ax_right.set_xlim(-range_x, range_x)
        ax_right.set_ylim(-range_x, range_x)
        ax_right.legend(fontsize=12)
    except Exception as e:
        ax_right.text(0.5, 0.5, f"Không thể vẽ đồ thị:\n{e}", ha='center', va='center', fontsize=14, color='red')

# Hàm xử lý khi nhấn nút Thực hiện
def run():
    global expr, solutions_real, solutions_all, zoom
    equation_str = entry_equation.get()
    try:
        expr = sp.sympify(equation_str)
        solutions_all = sp.solve(expr, x)

        # Lọc nghiệm thực: chỉ lấy nghiệm có phần ảo = 0
        solutions_real = [sol.evalf() for sol in solutions_all if sp.im(sol.evalf()) == 0]

        if solutions_real:
            solution_str = ", ".join([f"x = {sol:.2f}" for sol in solutions_real])
        else:
            solution_str = "Không có nghiệm thực"

        label_result.config(text="Nghiệm thực: " + solution_str, font=("Arial", 14, "bold"))

        ve_bang_bien_thien(equation_str, ax_left)
        canvas_left.draw()

        plot_graph(ax_right)
        canvas_right.draw()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Hàm không hợp lệ: {e}")
        expr = None
        solutions_real = []
        label_result.config(text="Nghiệm: ", font=("Arial", 14))
        ax_left.clear()
        canvas_left.draw()
        ax_right.clear()
        canvas_right.draw()


    except Exception as e:
        messagebox.showerror("Lỗi", f"Hàm không hợp lệ: {e}")
        expr = None
        solutions_real = []
        label_result.config(text="Nghiệm: ", font=("Arial", 14))
        ax_left.clear()
        ax_left.text(0.5, 0.5,
                    "Không thể vẽ bảng biến thiên.\n"
                    "Hàm số có thể quá phức tạp hoặc không có điểm tới hạn thực.",
                    ha='center', va='center', fontsize=14, color='red',
                    wrap=True)
        ax_left.axis('off')

# Hàm zoom bằng phím mũi tên
def on_key(event):
    global zoom
    if event.keysym == "Up":
        zoom += 10
        if expr:
            plot_graph(ax_right)
            canvas_right.draw()
    elif event.keysym == "Down":
        zoom = max(10, zoom - 10)
        if expr:
            plot_graph(ax_right)
            canvas_right.draw()

# === Tạo GUI chính ===
root = tk.Tk()
root.title("Bảng biến thiên và Đồ thị hàm số (Zoom: phím mũi tên ↑↓)")
root.geometry("1200x600")

frame_left = tk.Frame(root)
frame_left.pack(side="left", fill="both", expand=True)

fig_left, ax_left = plt.subplots(figsize=(6, 6))
canvas_left = FigureCanvasTkAgg(fig_left, master=frame_left)
canvas_left.get_tk_widget().pack(fill="both", expand=True)

frame_right = tk.Frame(root)
frame_right.pack(side="right", fill="both", expand=True)

label_input = tk.Label(frame_right, text="Nhập hàm số y =", font=("Arial", 20))
label_input.pack(pady=(10, 0))
entry_equation = tk.Entry(frame_right, width=30, font=("Arial", 20))
entry_equation.pack(pady=10)

btn_run = tk.Button(frame_right, text="Thực hiện", font=("Arial", 20), command=run)
btn_run.pack(pady=10)

label_result = tk.Label(frame_right, text="Nghiệm: ", fg="blue", font=("Arial", 16))
label_result.pack(pady=5)

fig_right, ax_right = plt.subplots(figsize=(6, 4))
canvas_right = FigureCanvasTkAgg(fig_right, master=frame_right)
canvas_right.get_tk_widget().pack(fill="both", expand=True)

root.bind("<Key>", on_key)


def on_closing():
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
