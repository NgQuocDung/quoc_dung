import pygame
import sympy as sp
import os

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vẽ đồ thị hàm số và nghiệm - Hỗ trợ tiếng Việt")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Đường dẫn tới phông chữ hỗ trợ tiếng Việt (ví dụ: Arial hoặc Noto Sans)
FONT_PATH = "C:/Windows/Fonts/Arial.ttf"  # Đường dẫn tới phông chữ Arial trên Windows

# Kiểm tra phông chữ tồn tại
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Không tìm thấy phông chữ tại: {FONT_PATH}")

# Phông chữ hỗ trợ tiếng Việt
font = pygame.font.Font(FONT_PATH, 20)

# Hàm vẽ giao diện
def draw_ui(equation, solutions, zoom):
    screen.fill(WHITE)

    # Hiển thị dòng chữ "Nhập hàm số" ở phía trên ô nhập
    text = font.render("Nhập hàm số y = (ấn Enter để vẽ):", True, BLACK)
    screen.blit(text, (50, 10))  # Đặt dòng chữ cao hơn ô nhập

    # Vẽ ô nhập phương trình
    pygame.draw.rect(screen, BLACK, (50, 40, WIDTH - 100, 50), 2)  # Ô nhập ở dưới dòng chữ

    # Hiển thị phương trình
    if equation:
        equation_text = font.render(f"Hàm số: y = {equation}", True, BLACK)
        screen.blit(equation_text, (50, 110))

    # Hiển thị nghiệm
    if solutions:
        solution_text = font.render("Nghiệm thực của hàm số:", True, BLACK)
        screen.blit(solution_text, (50, 150))
        for idx, sol in enumerate(solutions):
            sol_text = font.render(f"x = {sp.N(sol):.2f}", True, BLACK)
            screen.blit(sol_text, (50, 180 + idx * 30))

    # Hiển thị mức độ phóng to (Zoom)
    zoom_text = font.render(f"Zoom: {zoom}", True, BLACK)
    screen.blit(zoom_text, (WIDTH - 150, HEIGHT - 40))

# Hàm vẽ đồ thị
def plot_graph(equation, zoom):
    try:
        # Chuyển phương trình thành hàm số
        x = sp.symbols('x')
        expr = sp.sympify(equation)

        # Kích thước khu vực đồ thị
        graph_left = 50
        graph_right = WIDTH - 50
        graph_top = 250
        graph_bottom = HEIGHT - 50

        graph_width = graph_right - graph_left
        graph_height = graph_bottom - graph_top

        # Vẽ lưới và đánh số trục
        x_axis = graph_top + graph_height // 2
        y_axis = graph_left + graph_width // 2

        # Vẽ lưới
        for i in range(graph_left, graph_right, 50):  # Các đường lưới dọc (trục x)
            pygame.draw.line(screen, GRAY, (i, graph_top), (i, graph_bottom))
        for i in range(graph_top, graph_bottom, 50):  # Các đường lưới ngang (trục y)
            pygame.draw.line(screen, GRAY, (graph_left, i), (graph_right, i))

        # Vẽ trục x và y
        pygame.draw.line(screen, BLACK, (graph_left, x_axis), (graph_right, x_axis), 2)  # Trục x
        pygame.draw.line(screen, BLACK, (y_axis, graph_top), (y_axis, graph_bottom), 2)  # Trục y

        # Đánh số trục (số nguyên)
        for i in range(graph_left, graph_right, 100):  # Trục x
            x_val = round((i - y_axis) / zoom)
            label = font.render(f"{x_val}", True, BLACK)
            screen.blit(label, (i - 10, x_axis + 10))
        for i in range(graph_top, graph_bottom, 100):  # Trục y
            y_val = round(-(i - x_axis) / zoom)
            label = font.render(f"{y_val}", True, BLACK)
            screen.blit(label, (y_axis + 10, i - 10))

        # Vẽ đồ thị
        prev_point = None
        for px in range(graph_left, graph_right):
            x_val = (px - y_axis) / zoom
            try:
                y_val = expr.subs(x, x_val)
                if not y_val.is_real:  # Bỏ qua các giá trị không thực
                    prev_point = None
                    continue
                py = -int(y_val * zoom) + x_axis

                # Chỉ vẽ các điểm trong phạm vi hiển thị
                if graph_top <= py <= graph_bottom:
                    current_point = (px, py)
                    if prev_point:
                        pygame.draw.line(screen, BLUE, prev_point, current_point, 2)
                    prev_point = current_point
                else:
                    prev_point = None  # Ngắt đoạn nếu điểm nằm ngoài phạm vi
            except (ZeroDivisionError, OverflowError):  # Bỏ qua các điểm bất định
                prev_point = None
    except Exception as e:
        error_text = font.render("Lỗi khi vẽ đồ thị: " + str(e), True, RED)
        screen.blit(error_text, (50, 200))

# Vòng lặp chính
running = True
input_active = True
input_text = ""
zoom = 50  # Mặc định mức zoom
draw_graph = False
solutions = []
equation = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:  # Nhấn Enter để vẽ đồ thị
                    draw_graph = True
                    input_active = False
                    equation = input_text
                    x = sp.symbols('x')
                    expr = sp.sympify(equation)
                    solutions = sp.solveset(expr, x, domain=sp.S.Reals)  # Tìm nghiệm thực
                    if isinstance(solutions, sp.FiniteSet):
                        solutions = list(solutions)
                    else:
                        solutions = []
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            else:
                # Phím điều khiển zoom
                if event.key == pygame.K_UP:  # Phóng to
                    zoom += 10
                elif event.key == pygame.K_DOWN:  # Thu nhỏ
                    zoom = max(10, zoom - 10)

    # Vẽ giao diện
    draw_ui(equation, solutions, zoom)

    # Vẽ khung nhập phương trình
    color = RED if input_active else BLACK
    pygame.draw.rect(screen, color, (50, 40, WIDTH - 100, 50), 2)
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (60, 50))

    # Vẽ đồ thị (nếu được yêu cầu)
    if draw_graph and equation:
        plot_graph(equation, zoom)

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát pygame
pygame.quit()