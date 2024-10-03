import pygame
import numpy as np
import hashlib
import time  # For timing and calculating ETA

# Constants
WIDTH, HEIGHT = 800, 800
MAX_ITER = 256
ZOOM_FACTOR = 2
SAVE_BUTTON_RECT = pygame.Rect(WIDTH - 150, HEIGHT - 50, 130, 40)

# Mandelbrot computation
def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

# Render the fractal
def render_fractal(surface, x_min, x_max, y_min, y_max, cache):
    pixel_array = pygame.PixelArray(surface)
    width, height = surface.get_size()

    for x in range(width):
        for y in range(height):
            # Map pixel to complex plane
            re = x_min + (x / width) * (x_max - x_min)
            im = y_min + (y / height) * (y_max - y_min)
            c = complex(re, im)

            # Use caching to avoid redundant calculations
            key = hashlib.sha256(f"{c}".encode()).hexdigest()
            if key in cache:
                color = cache[key]
            else:
                m = mandelbrot(c, MAX_ITER)
                color = (m % 8 * 32, m % 16 * 16, m % 32 * 8)  # Basic coloring
                cache[key] = color

            pixel_array[x, y] = color

    del pixel_array  # Release the lock on surface

# Draw a save button on the screen
def draw_save_button(screen):
    pygame.draw.rect(screen, (200, 200, 200), SAVE_BUTTON_RECT)
    font = pygame.font.SysFont(None, 24)
    text = font.render('Save Image', True, (0, 0, 0))
    screen.blit(text, (SAVE_BUTTON_RECT.x + 15, SAVE_BUTTON_RECT.y + 10))

# Save the fractal image as a PNG
def save_image(surface, filename='mandelbrot.png'):
    pygame.image.save(surface, filename)
    print(f"Image saved as {filename}")

# Main function
def mandelbrot_renderer():
    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mandelbrot Set Renderer with Zoom")
    
    x_min, x_max = -2.5, 1.5
    y_min, y_max = -2.0, 2.0
    cache = {}

    running = True
    eta = 0
    while running:
        start_time = time.time()  # Start timing for the render

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos

                    # Check if the "Save" button was clicked
                    if SAVE_BUTTON_RECT.collidepoint(mouse_x, mouse_y):
                        save_image(screen)  # Save the current fractal view
                    else:
                        # Zoom in on mouse click
                        zoom_x = x_min + (mouse_x / WIDTH) * (x_max - x_min)
                        zoom_y = y_min + (mouse_y / HEIGHT) * (y_max - y_min)

                        # Update bounds to zoom
                        zoom_width = (x_max - x_min) / ZOOM_FACTOR
                        zoom_height = (y_max - y_min) / ZOOM_FACTOR

                        x_min, x_max = zoom_x - zoom_width / 2, zoom_x + zoom_width / 2
                        y_min, y_max = zoom_y - zoom_height / 2, zoom_y + zoom_height / 2

                        cache.clear()  # Clear cache since we're recalculating

        # Render the fractal
        render_fractal(screen, x_min, x_max, y_min, y_max, cache)
        
        # Draw the save button
        draw_save_button(screen)

        # Calculate and display ETA
        render_time = time.time() - start_time
        eta = render_time * ZOOM_FACTOR  # Basic approximation of next render time
        print(f"Render completed in {render_time:.2f} seconds. Estimated time for next render: {eta:.2f} seconds.")
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    mandelbrot_renderer()
