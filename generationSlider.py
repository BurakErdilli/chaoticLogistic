import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Constants for the window size and colors
WIDTH, HEIGHT = 1280, 1024
DARK_GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Arial", 24)

# Universal metrics
class Metrics:
    INITIAL_POPULATION_MIN = 0.0
    INITIAL_POPULATION_MAX = 1.0
    INITIAL_POPULATION_DEFAULT = 0.4

    GROWTH_RATE_MIN = 0
    GROWTH_RATE_MAX = 4
    GROWTH_RATE_DEFAULT = 1.506

    GENERATION_COUNT_MIN = 1
    GENERATION_COUNT_MAX = 500
    GENERATION_COUNT_DEFAULT = 100

# Slider class
class Slider:
    def __init__(self, x, y, width, min_value, max_value, initial_value):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect, 2)
        handle_x = self.rect.x + (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width
        pygame.draw.circle(screen, LIGHT_GRAY, (int(handle_x), self.rect.y + 10), 10)
        
        # Draw value label
        label = FONT.render(f"{self.value:.2f}", True, LIGHT_GRAY)
        screen.blit(label, (self.rect.x + self.rect.width + 10, self.rect.y))

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.value = (mouse_pos[0] - self.rect.x) / self.rect.width * (self.max_value - self.min_value) + self.min_value
            self.value = max(self.min_value, min(self.value, self.max_value))

# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
        label = FONT.render(self.text, True, DARK_GRAY)
        screen.blit(label, (self.rect.x + (self.rect.width - label.get_width()) // 2,
                            self.rect.y + (self.rect.height - label.get_height()) // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Function to draw the population growth graph
def draw_graph(screen, populations_this_year, populations_next_year, generation_count):
    graph_width = WIDTH - 200
    graph_height = HEIGHT - 250
    start_x = 100
    start_y = 100

    # Draw the axes
    pygame.draw.line(screen, LIGHT_GRAY, (start_x, start_y + graph_height), (start_x + graph_width, start_y + graph_height), 2)  # X-axis
    pygame.draw.line(screen, LIGHT_GRAY, (start_x, start_y), (start_x, start_y + graph_height), 2)  # Y-axis

    # Draw labels for axes
    x_label = FONT.render("Generation", True, LIGHT_GRAY)
    y_label = FONT.render("Population", True, LIGHT_GRAY)
    screen.blit(x_label, (start_x + graph_width / 2 - x_label.get_width() / 2, start_y + graph_height + 10))
    screen.blit(y_label, (start_x - 50, start_y + graph_height / 2 - y_label.get_height() / 2))

    # Normalize population values for graphing
    max_population = max(populations_next_year) if populations_next_year else 1
    min_population = min(populations_next_year) if populations_next_year else 0

    # Draw grid lines
    for i in range(0, 11):
        grid_y = start_y + graph_height - (i / 10) * graph_height
        pygame.draw.line(screen, DARK_GRAY, (start_x, grid_y), (start_x + graph_width, grid_y), 1)
        if max_population > 0:
            grid_value = min_population + i / 10 * (max_population - min_population)
            label = FONT.render(f"{grid_value:.2f}", True, LIGHT_GRAY)
            screen.blit(label, (start_x - 50, grid_y - label.get_height() / 2))

    # Draw x-axis labels at generation*0.1 intervals
    for i in range(0, generation_count + 1, max(1, int(generation_count * 0.1))):
        grid_x = start_x + (i / generation_count) * graph_width
        pygame.draw.line(screen, DARK_GRAY, (grid_x, start_y), (grid_x, start_y + graph_height), 1)
        label = FONT.render(f"{i}", True, LIGHT_GRAY)
        screen.blit(label, (grid_x - label.get_width() / 2, start_y + graph_height + 5))

    # Draw the graph points
    for i in range(len(populations_this_year)):
        x = start_x + (i / (len(populations_this_year) - 1)) * graph_width
        y = start_y + graph_height - (populations_next_year[i] - min_population) / (max_population - min_population) * graph_height
        pygame.draw.circle(screen, LIGHT_GRAY, (int(x), int(y)), 5)

    # Draw lines connecting the points
    for i in range(len(populations_this_year) - 1):
        x1 = start_x + (i / (len(populations_this_year) - 1)) * graph_width
        y1 = start_y + graph_height - (populations_next_year[i] - min_population) / (max_population - min_population) * graph_height
        x2 = start_x + ((i + 1) / (len(populations_this_year) - 1)) * graph_width
        y2 = start_y + graph_height - (populations_next_year[i + 1] - min_population) / (max_population - min_population) * graph_height
        pygame.draw.line(screen, LIGHT_GRAY, (int(x1), int(y1)), (int(x2), int(y2)), 2)

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Population Growth Simulation")

    # Create sliders using universal metrics
    initial_population_slider = Slider(50, 50, 300, 
                                        Metrics.INITIAL_POPULATION_MIN, 
                                        Metrics.INITIAL_POPULATION_MAX, 
                                        Metrics.INITIAL_POPULATION_DEFAULT)

    growth_rate_slider = Slider(50, 100, 300, 
                                 Metrics.GROWTH_RATE_MIN, 
                                 Metrics.GROWTH_RATE_MAX, 
                                 Metrics.GROWTH_RATE_DEFAULT)

    generation_count_slider = Slider(50, 150, 300, 
                                      Metrics.GENERATION_COUNT_MIN, 
                                      Metrics.GENERATION_COUNT_MAX, 
                                      Metrics.GENERATION_COUNT_DEFAULT)

    # Create Save button
    save_button = Button(WIDTH - 150, HEIGHT - 50, 100, 40, "Save Graph")

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(DARK_GRAY)

        # Draw sliders and save button
        initial_population_slider.draw(screen)
        growth_rate_slider.draw(screen)
        generation_count_slider.draw(screen)
        save_button.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    initial_population_slider.update(event.pos)
                    growth_rate_slider.update(event.pos)
                    generation_count_slider.update(event.pos)
                    if save_button.is_clicked(event.pos):
                        pygame.image.save(screen, "population_growth_graph.png")
                        print("Graph saved as population_growth_graph.png")

        # Calculate population growth
        population_status = initial_population_slider.value
        growth_rate = growth_rate_slider.value
        generation_count = int(generation_count_slider.value)

        populations_this_year = []
        populations_next_year = []

        for _ in range(generation_count):
            # Check for division by zero
            if population_status > 0: 
                next_population = growth_rate * (population_status * (1 - population_status))
            else:
                next_population = 0  # If the population is zero, the next population remains zero

            populations_this_year.append(population_status)
            populations_next_year.append(next_population)
            population_status = next_population

        # Draw the graph directly on the Pygame screen
        draw_graph(screen, populations_this_year, populations_next_year, generation_count)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
