import random

import pygame

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Gradient Settings
SEGMENT_WIDTH = 50  # Width of each gradient slice
SEGMENTS = WIDTH // SEGMENT_WIDTH + 2  # Enough to cover the screen + buffer


# Generate initial gradient segments with random colors
def random_color():
    return [random.randint(0, 255) for _ in range(3)]


gradient_segments = [[random_color(), random_color()] for _ in range(SEGMENTS)]

# Scroll speed
SCROLL_SPEED = 2  # Pixels per frame


def draw_gradient():
    """Draws the horizontally scrolling gradient background."""
    for i in range(len(gradient_segments) - 1):
        left_color = gradient_segments[i][1]  # End color of this segment
        right_color = gradient_segments[i + 1][0]  # Start color of next segment

        for x in range(SEGMENT_WIDTH):
            # Interpolating between left_color and right_color
            t = x / SEGMENT_WIDTH
            blended_color = [
                int(left_color[c] * (1 - t) + right_color[c] * t) for c in range(3)
            ]
            pygame.draw.line(
                screen,
                blended_color,
                (i * SEGMENT_WIDTH + x, 0),
                (i * SEGMENT_WIDTH + x, HEIGHT),
            )


def update_gradient():
    """Scrolls the gradient left and manages segment replacement."""
    global gradient_segments

    # Shift left
    for segment in gradient_segments:
        segment.append(segment.pop(0))  # Move colors left in each segment

    # Remove first segment if it's fully out of view
    if SEGMENT_WIDTH <= SCROLL_SPEED:
        gradient_segments.pop(0)  # Remove first segment
        gradient_segments.append(
            [random_color(), random_color()]
        )  # Add new random segment at the end


def main():
    running = True
    x_offset = 0  # Tracks horizontal movement
    while running:
        screen.fill((0, 0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Scroll logic
        x_offset -= SCROLL_SPEED
        if x_offset <= -SEGMENT_WIDTH:
            x_offset = 0
            update_gradient()

        draw_gradient()

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()


if __name__ == "__main__":
    main()
