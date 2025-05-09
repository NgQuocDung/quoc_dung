import pygame
import sympy as sp

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 1000, 600  # Mở rộng chiều rộng để có không gian cho bảng biến thiên
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Đồ án Đồ họa Máy tính - Vẽ đồ thị và bảng biến thiên")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Phông chữ
font = pygame.font.Font(None, 20)

# Hàm vẽ giao diện
def draw_ui(zoom, equation, solutions):
    screen.fill(WHITE)

    # Vẽ khu vực nhập phương trình
    pygame.draw.rect(screen, BLACK, (10, 10, WIDTH // 2 - 20, HEIGHT - 20), 2)
    text = font.render("Nhập phương trình một ẩn (ấn Enter để vẽ):", True, BLACK)
    screen.blit(text, (20, 20))

    # Vẽ khu vực đồ thị
    pygame.draw.rect(screen, BLACK, (WIDTH // 2 + 10, 10, WIDTH // 2 - 20, HEIGHT - 20), 2)
    text = font.render("Đồ thị hàm số:", True, BLACK)
    screen.blit(text, (WIDTH // 2 + 20, 20))

    # Hiển thị mức độ phóng to (Zoom)
    zoom_box = pygame.Rect(WIDTH - 150, HEIGHT - 40, 140, 30)
    pygame.draw.rect(screen, BLACK, zoom_box, 2)
    zoom_text = font.render(f"Zoom: {zoom}", True, BLACK)
    screen.blit(zoom_text, (WIDTH - 140, HEIGHT - 35))

    # Vẽ bảng biến thiên
    pygame.draw.rect(screen, BLACK, (20, 100, WIDTH // 2 - 40, HEIGHT - 150), 1)
    text = font.render("Bảng biến thiên:", True, BLACK)
    screen.blit(text, (30, 110))

    # Hiển thị phương trình
    if equation:
        equation_text = font.render(f"Phương trình: {equation}", True, BLACK)
        screen.blit(equation_text, (30, 140))

    # Hiển thị nghiệm (solutions)
    if solutions:
        solution_text = font.render("Nghiệm thực:", True, BLACK)
        screen.blit(solution_text, (30, 170))
        for idx, sol in enumerate(solutions):
            sol_text = font.render(f"x = {sp.N(sol):.2f}", True, BLACK)
            screen.blit(sol_text, (30, 190 + idx * 20))

# Hàm vẽ đồ thị
def plot_graph(equation, zoom):
    try:
        # Chuyển phương trình thành hàm số
        x = sp.symbols('x')
        expr = sp.sympify(equation)

        # Kích thước khu vực đồ thị
        graph_left = WIDTH // 2 + 10
        graph_right = WIDTH - 10
        graph_top = 10
        graph_bottom = HEIGHT - 10

        graph_width = graph_right - graph_left
        graph_height = graph_bottom - graph_top

        # Vẽ lưới và đánh số trục
        x_axis = graph_top + graph_height // 2
        y_axis = graph_left + graph_width // 2

        # Vẽ lưới
        for i in range(graph_left, graph_right, 20):  # Các đường lưới dọc (trục x)
            pygame.draw.line(screen, GRAY, (i, graph_top), (i, graph_bottom))
        for i in range(graph_top, graph_bottom, 20):  # Các đường lưới ngang (trục y)
            pygame.draw.line(screen, GRAY, (graph_left, i), (graph_right, i))

        # Vẽ trục x và y
        pygame.draw.line(screen, BLACK, (graph_left, x_axis), (graph_right, x_axis), 2)  # Trục x
        pygame.draw.line(screen, BLACK, (y_axis, graph_top), (y_axis, graph_bottom), 2)  # Trục y

        # Đánh số trục (số nguyên)
        for i in range(graph_left, graph_right, 50):  # Trục x
            x_val = round((i - y_axis) / zoom)
            label = font.render(f"{x_val}", True, BLACK)
            screen.blit(label, (i - 10, x_axis + 5))
        for i in range(graph_top, graph_bottom, 50):  # Trục y
            y_val = round(-(i - x_axis) / zoom)
            label = font.render(f"{y_val}", True, BLACK)
            screen.blit(label, (y_axis + 5, i - 10))

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
        screen.blit(error_text, (WIDTH // 2 + 20, 70))

# Vòng lặp chính
running = True
input_active = False
input_text = ""
zoom = 50  # Mặc định mức zoom
draw_graph = False  # Biến cờ để kiểm tra có cần vẽ đồ thị hay không
solutions = []
equation = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:  # Nhấn Enter để vẽ
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Xác định click vào khu vực nhập
            if 10 < event.pos[0] < WIDTH // 2 - 10 and 10 < event.pos[1] < HEIGHT - 10:
                input_active = True

    # Vẽ giao diện
    draw_ui(zoom, equation, solutions)

    # Vẽ khung nhập phương trình
    color = RED if input_active else BLACK
    pygame.draw.rect(screen, color, (20, 60, WIDTH // 2 - 40, 40), 2)
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (30, 70))

    # Vẽ đồ thị (nếu được yêu cầu)
    if draw_graph and input_text:
        plot_graph(input_text, zoom)

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát pygame
pygame.quit()