# bbt.py
import sympy as sp
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox


def ve_bang_bien_thien(expr_str):
    x = sp.symbols('x')
    try:
        f = sp.sympify(expr_str)
        df = sp.diff(f, x)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Hàm số không hợp lệ: {e}")
        return

    # Tạo một cửa sổ matplotlib gồm 2 phần: đạo hàm và bảng biến thiên hoặc thông báo lỗi
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), height_ratios=[1, 2])
    fig.suptitle("Đạo hàm và Bảng biến thiên", fontsize=14)

    # Hiển thị biểu thức đạo hàm
    ax1.axis('off')
    ax1.text(0.5, 0.5, r"$f'(x) = %s$" % sp.latex(df), ha='center', va='center', fontsize=16)

    try:
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
            mid = (left + right) / 2 if right != sp.oo and left != -sp.oo else (
                (right - 1) if right != sp.oo else (left + 1)
            )
            sign = sp.N(df.subs(x, mid))
            intervals.append(("+" if sign > 0 else "-" if sign < 0 else "0", mid))

        values_fx = [f.subs(x, pt).evalf() for pt in all_points_real]

        # Vẽ bảng biến thiên
        ax2.axis("off")

        x_labels = [r"$-\infty$"] + [f"{pt:.2f}" for pt in all_points_real] + [r"$+\infty$"]
        y_positions = [2.5, 1.4, 0.6]

        ax2.hlines(y_positions[0], -1, len(x_labels), color='black', linewidth=1.2)
        ax2.hlines(y_positions[1], -1, len(x_labels), color='black', linewidth=1.2)
        ax2.vlines(-0.5, 0, 3, color='black', linewidth=1.2)

        ax2.text(-1.2, y_positions[0] + 0.1, "x", fontsize=12, weight='bold')
        ax2.text(-1.2, y_positions[1] + 0.1, "$f'(x)$", fontsize=12, weight='bold')
        ax2.text(-1.2, y_positions[2] + 0.1, "$f(x)$", fontsize=12, weight='bold')

        for i, lbl in enumerate(x_labels):
            ax2.text(i, y_positions[0] + 0.1, lbl, ha='center', va='center', fontsize=12)

        for i, (sgn, _) in enumerate(intervals):
            pos_x = i + 0.5
            if i < len(all_points_real) and all_points_real[i] in critical_points:
                ax2.text(i + 1, y_positions[1] + 0.05, "0", ha='center', va='center', fontsize=12, color='blue')
            else:
                ax2.text(pos_x, y_positions[1] + 0.05, sgn, ha='center', va='center', fontsize=12)

        for i, val in enumerate(values_fx):
            ax2.text(i + 1, y_positions[2] - 0.2, f"{val:.2f}" if val.is_real else "undef", ha='center', va='center', fontsize=12)

        for i, (sgn, _) in enumerate(intervals):
            x1, x2 = i, i + 1
            if sgn == '+': y1, y2 = 0.7, 1.2
            elif sgn == '-': y1, y2 = 1.2, 0.7
            else: y1 = y2 = 0.95
            ax2.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', linewidth=1.5))

        ax2.set_xlim(-1.5, len(x_labels) + 1)
        ax2.set_ylim(0, 3)

    except Exception as e:
        ax2.axis("off")
        ax2.text(0.5, 0.5, f"Không thể vẽ bảng biến thiên: {e}", ha='center', va='center', fontsize=13, color='red')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def run_gui():
    def on_submit():
        expr = input_entry.get().strip()
        if not expr:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập hàm số!")
        else:
            ve_bang_bien_thien(expr)

    root = Tk()
    root.title("Vẽ Bảng Biến Thiên")
    root.geometry("500x200")

    Label(root, text="Nhập hàm số:", font=("Arial", 12)).pack(pady=10)
    input_entry = Entry(root, font=("Arial", 14), width=30)
    input_entry.pack(pady=5)
    Button(root, text="Tính và Vẽ", font=("Arial", 12), command=on_submit).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
