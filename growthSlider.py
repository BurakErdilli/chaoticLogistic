import pygame
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg

# Initialize Pygame
pygame.init()

# Screen dimensions (1080p resolution)
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Logistic Map Simulation with Initial Population Slider')

# Slider parameters
slider_x = 100
slider_y = height - 100
slider_width = width - 200
slider_height = 20
initial_population = 0.2  # Initial population value controlled by the slider
slider_value = initial_population
maxGrowthRate = 3.99
generations = 400
resolution = 0.01

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
HOVER_RED = (200, 0, 0)  # Color when hovered

# Fonts
font = pygame.font.SysFont(None, 36)

# Function to create a logistic map graph for a given initial population
def create_logistic_map_graph(initial_population):
    equil = []
    growth_rates = []
    CurrentGrowthRate = 0

    # Run the logistic map simulation
    while CurrentGrowthRate < maxGrowthRate - resolution:
        currentPopulation = initial_population
        for gen in range(generations):
            next_population = CurrentGrowthRate * currentPopulation * (1 - currentPopulation)
            currentPopulation = next_population
        
        # Collect population values only from the last 100 generations
        for gen in range(100):
            next_population = CurrentGrowthRate * currentPopulation * (1 - currentPopulation)
            currentPopulation = next_population
            equil.append(currentPopulation)
            growth_rates.append(CurrentGrowthRate)
        
        CurrentGrowthRate += resolution

    # Plot the logistic map
    fig, ax = plt.subplots(figsize=(14, 10))  # Upscale the figure size
    ax.plot(growth_rates, equil, 'b.', markersize=0.5)
    ax.set_title('Logistic Map: Population Equilibrium vs Growth Rate', fontsize=16)
    ax.set_xlabel('Growth Rate', fontsize=14)
    ax.set_ylabel('Equilibrium Population', fontsize=14)

    # Add periodic tick values to both sides
    ax.xaxis.set_major_locator(plt.MultipleLocator(0.5))  # X-axis ticks every 0.5 units
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.2))  # Y-axis ticks every 0.2 units

    # Draw the canvas
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()

    size = canvas.get_width_height()
    plt.close(fig)  # Close the figure to avoid memory leaks
    return pygame.image.fromstring(raw_data.tobytes(), size, "RGBA"), fig  # Return the figure for saving

# Function to draw the slider
def draw_slider(screen, x, y, width, height, value):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    # Draw slider knob based on the value (range 0 to 1)
    knob_x = int(x + value * width)
    pygame.draw.circle(screen, BLUE, (knob_x, y + height // 2), 10)

# Function to draw the save button with hover effect
def draw_save_button(screen, x, y, width, height, is_hovered):
    color = HOVER_RED if is_hovered else RED
    pygame.draw.rect(screen, color, (x, y, width, height))
    text = font.render("Save Graph", True, WHITE)
    screen.blit(text, (x + 10, y + 10))

# Main loop
running = True
graph_image, graph_fig = create_logistic_map_graph(initial_population)  # Generate initial graph

while running:
    screen.fill(WHITE)
    is_hovered = False  # Track if the mouse is hovering over the button

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Slider control
        if event.type == pygame.MOUSEBUTTONDOWN:
            if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y <= event.pos[1] <= slider_y + slider_height:
                slider_value = (event.pos[0] - slider_x) / slider_width
                initial_population = slider_value
                # Update graph when slider is adjusted
                graph_image, graph_fig = create_logistic_map_graph(initial_population)

            # Save button control
            if 50 <= event.pos[0] <= 200 and 50 <= event.pos[1] <= 100:  # Save button dimensions
                # Save the graph as SVG, PNG, and JPEG
                graph_fig.savefig('logistic_map.svg')
                graph_fig.savefig('logistic_map.png', dpi=300)  # High DPI for better quality
                graph_fig.savefig('logistic_map.jpg', dpi=300)  # High DPI for better quality
                print("Graph saved as 'logistic_map.svg', 'logistic_map.png', and 'logistic_map.jpg'.")

        # Check for hover
        if 50 <= event.pos[0] <= 200 and 50 <= event.pos[1] <= 100:
            is_hovered = True

    # Display the graph (centered on screen)
    screen.blit(graph_image, (100, 50))  # Adjusted for 1080p resolution

    # Draw the slider
    draw_slider(screen, slider_x, slider_y, slider_width, slider_height, slider_value)

    # Draw slider value
    value_text = font.render(f'Initial Population: {initial_population:.3f}', True, BLACK)
    screen.blit(value_text, (slider_x + slider_width + 20, slider_y - 20))

    # Draw the save button with hover effect
    draw_save_button(screen, 50, 50, 150, 40, is_hovered)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
