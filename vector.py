import sys, math, random, pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vector Sci-Fi Trippy Effects")

clock = pygame.time.Clock()

# Colors for neon vector look
NEON_COLORS = [
    (0, 255, 255), (255, 0, 255), (0, 255, 128),
    (255, 255, 0), (255, 128, 0), (128, 0, 255)
]

def draw_starfield(surface, stars, speed):
    for i, (x, y, z) in enumerate(stars):
        z -= speed
        if z <= 0:
            x, y, z = random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.5, 1)
        sx = int((x / z) * WIDTH/2 + WIDTH/2)
        sy = int((y / z) * HEIGHT/2 + HEIGHT/2)
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            c = int((1 - z) * 255)
            surface.set_at((sx, sy), (c, c, c))
        stars[i] = (x, y, z)

def draw_wire_tunnel(surface, t):
    # Draw concentric wireframe squares
    depth_steps = 15
    spacing = 60
    for i in range(depth_steps):
        scale = (i + 1) * spacing - (t % spacing)
        if scale <= 0: 
            continue
        color = NEON_COLORS[(i + int(t/20)) % len(NEON_COLORS)]
        half_w = WIDTH // 4
        half_h = HEIGHT // 4
        offset = scale
        points = [
            (WIDTH/2 - half_w - offset, HEIGHT/2 - half_h - offset),
            (WIDTH/2 + half_w + offset, HEIGHT/2 - half_h - offset),
            (WIDTH/2 + half_w + offset, HEIGHT/2 + half_h + offset),
            (WIDTH/2 - half_w - offset, HEIGHT/2 + half_h + offset)
        ]
        pygame.draw.polygon(surface, color, points, 1)

def draw_rotating_grid(surface, t):
    # Overlay rotating neon gridlines
    spacing = 50
    angle = t * 0.01
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    for i in range(-WIDTH//2, WIDTH//2, spacing):
        for j in [-HEIGHT//2, HEIGHT//2]:
            x1, y1 = i, j
            x2, y2 = i, -j
            # rotate
            x1r = x1*cos_a - y1*sin_a
            y1r = x1*sin_a + y1*cos_a
            x2r = x2*cos_a - y2*sin_a
            y2r = x2*sin_a + y2*cos_a
            color = NEON_COLORS[(i//spacing) % len(NEON_COLORS)]
            pygame.draw.line(surface, color,
                             (x1r + WIDTH//2, y1r + HEIGHT//2),
                             (x2r + WIDTH//2, y2r + HEIGHT//2), 1)

def main():
    stars = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.1, 1)) for _ in range(500)]
    running, t = True, 0

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                running = False

        screen.fill((0, 0, 0))

        # Background starfield
        draw_starfield(screen, stars, 0.01)

        # Wireframe tunnel
        draw_wire_tunnel(screen, t)

        # Rotating grid overlay
        draw_rotating_grid(screen, t)

        pygame.display.flip()
        t += 2
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
