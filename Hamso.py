import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

x = sp.symbols('x')
zoom = 50
expr = None
solutions_real = []

# ======= ĐOẠN 1: VẼ BẢNG BIẾN THIÊN & ĐẠO HÀM =======
def hamso(expr_str, ax_left):
    ax_left.clear()
    try:
        f = sp.sympify(expr_str)
        df = sp.diff(f, x)
        ax_left.text(0.5, 1.08, r"$f'(x) = %s$" % sp.latex(df), ha='center', va='center', fontsize=16, transform=ax_left.transAxes)

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

        ax_left.text(-1.2, y_positions[0] + 0.1, "x", fontsize=13, weight='bold')
        ax_left.text(-1.2, y_positions[1] + 0.1, "$f'(x)$", fontsize=13, weight='bold')
        ax_left.text(-1.2, y_positions[2] + 0.1, "$f(x)$", fontsize=13, weight='bold')

        for i, lbl in enumerate(x_labels):
            ax_left.text(i, y_positions[0] + 0.1, lbl, ha='center', va='center', fontsize=13)

        for i, (sgn, _) in enumerate(intervals):
            pos_x = i + 0.5
            if i < len(all_points_real) and all_points_real[i] in critical_points:
                ax_left.text(i + 1, y_positions[1] + 0.05, "0", ha='center', va='center', fontsize=12, color='blue')
            else:
                ax_left.text(pos_x, y_positions[1] + 0.05, sgn, ha='center', va='center', fontsize=12)

        for i, val in enumerate(values_fx):
            text_val = f"{val:.2f}" if val.is_real else "undef"
            ax_left.text(i + 1, y_positions[2] - 0.2, text_val, ha='center', va='center', fontsize=12)

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
        ax_left.text(0.5, 0.5, f"Không thể vẽ bảng biến thiên:\n{e}", ha='center', va='center', fontsize=12, color='red')

# ======= ĐOẠN 2: TÍNH NGHIỆM & VẼ ĐỒ THỊ =======
def plot_graph():
    global expr, zoom, solutions_real
    ax_right.clear()
    if expr is None:
        ax_right.text(0.5, 0.5, "Chưa có hàm số để vẽ", ha='center', va='center', fontsize=14, color='gray', transform=ax_right.transAxes)
        canvas_right.draw()
        return
    try:
        f = sp.lambdify(x, expr, modules=["numpy"])
        range_x = 10 * 50 / zoom
        x_vals = np.linspace(-range_x, range_x, 1000)
        y_vals = f(x_vals)
        y_vals = np.array(y_vals, dtype=np.float64)
        mask = np.isfinite(y_vals)
        x_plot = x_vals[mask]
        y_plot = y_vals[mask]

        ax_right.axhline(0, color='black', linewidth=1)
        ax_right.axvline(0, color='black', linewidth=1)
        ax_right.grid(True, linestyle='--', alpha=0.5)
        ax_right.plot(x_plot, y_plot, label=f"y = {str(expr)}", color="blue")

        for sol in solutions_real:
            val = float(sol)
            ax_right.plot(val, 0, 'ro')
            ax_right.annotate(f"x = {val:.4f}", (val, 0), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12, color='red')

        ax_right.set_title("Đồ thị hàm số", fontsize=15)
        ax_right.set_xlim(-range_x, range_x)
        ax_right.set_ylim(-range_x, range_x)
        ax_right.legend(fontsize=11)
        canvas_right.draw()
    except Exception as e:
        ax_right.text(0.5, 0.5, f"Không thể vẽ đồ thị:\n{e}", ha='center', va='center', fontsize=12, color='red')
        canvas_right.draw()

def run():
    global expr, solutions_real
    equation_str = entry_equation.get()
    try:
        expr = sp.sympify(equation_str)
        # Đạo hàm
        derivative_str = str(sp.diff(expr, x))
        # Nghiệm thực
        all_solutions = sp.solve(expr, x)
        solutions_real = []
        for sol in all_solutions:
            val = complex(sol.evalf())
            if abs(val.imag) < 1e-8:
                solutions_real.append(val.real)
        # Nếu không có nghiệm thực rõ ràng, thử tìm nghiệm gần đúng trong khoảng [-100, 100]
        if not solutions_real and expr.is_polynomial(x):
            coeffs = sp.Poly(expr, x).all_coeffs()
            degree = len(coeffs) - 1
            try:
                for guess in np.linspace(-100, 100, 5 * degree + 1):
                    try:
                        s = sp.nsolve(expr, x, guess)
                        sval = complex(s.evalf())
                        if abs(sval.imag) < 1e-8:
                            sval = round(sval.real, 8)
                            if not any(abs(sval - t) < 1e-6 for t in solutions_real):
                                solutions_real.append(sval)
                    except Exception:
                        pass
            except Exception:
                pass
        if solutions_real:
            solution_str = ", ".join([f"x = {sol:.4f}" for sol in solutions_real])
        else:
            solution_str = "Không có nghiệm thực"
        label_result.config(text="Nghiệm thực: " + solution_str, font=("Arial", 13, "bold"))

        hamso(equation_str, ax_left)
        canvas_left.draw()
        plot_graph()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Hàm không hợp lệ: {e}")
        expr = None
        solutions_real = []
        label_result.config(text="Nghiệm thực: ")
        ax_left.clear()
        ax_left.text(0.5, 0.5, "Không thể vẽ bảng biến thiên.", ha='center', va='center', fontsize=12, color='red')
        canvas_left.draw()
        ax_right.clear()
        canvas_right.draw()

def on_key(event):
    global zoom
    if event.keysym == "Up":
        zoom += 10
        if expr:
            plot_graph()
    elif event.keysym == "Down":
        zoom = max(10, zoom - 10)
        if expr:
            plot_graph()

def on_closing():
    root.destroy()
    sys.exit()

root = tk.Tk()
root.title("Vẽ Đồ Thị, Đạo Hàm & Bảng Biến Thiên (Zoom: phím ↑↓)")
root.geometry("1250x650")

frame_left = tk.Frame(root)
frame_left.pack(side="left", fill="both", expand=True)

fig_left, ax_left = plt.subplots(figsize=(6, 6))
canvas_left = FigureCanvasTkAgg(fig_left, master=frame_left)
canvas_left.get_tk_widget().pack(fill="both", expand=True)

frame_right = tk.Frame(root)
frame_right.pack(side="right", fill="both", expand=True)

label_input = tk.Label(frame_right, text="Nhập hàm số y =", font=("Arial", 17))
label_input.pack(pady=(10, 0))
entry_equation = tk.Entry(frame_right, width=30, font=("Arial", 17))
entry_equation.pack(pady=10)

btn_run = tk.Button(frame_right, text="Tính & Vẽ", font=("Arial", 14), command=run)
btn_run.pack(pady=10)

label_result = tk.Label(frame_right, text="Nghiệm thực: ", fg="blue", font=("Arial", 13))
label_result.pack(pady=3)

fig_right, ax_right = plt.subplots(figsize=(6, 5))
canvas_right = FigureCanvasTkAgg(fig_right, master=frame_right)
canvas_right.get_tk_widget().pack(fill="both", expand=True)

root.bind("<Key>", on_key)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
