#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include "stb_image_write.h"

#define WIDTH 2000
#define HEIGHT 2000
#define MAX_ITER (HEIGHT / 5)

// Function to generate the Mandelbrot set
void mandelbrot(unsigned char *image, double x_min, double x_max, double y_min, double y_max) {
    for (int y = 0; y < HEIGHT; ++y) {
        for (int x = 0; x < WIDTH; ++x) {
            double complex c = x_min + (x / (double)WIDTH) * (x_max - x_min) +
                                (y_min + (y / (double)HEIGHT) * (y_max - y_min)) * I;
            double complex z = 0.0 + 0.0 * I;
            int n;

            for (n = 0; n < MAX_ITER; ++n) {
                if (cabs(z) >= 2.0) break;  // Escape condition
                z = z * z + c;
            }

            // Color the pixel based on the number of iterations
            int color = (n == MAX_ITER) ? 0 : (255 * n / MAX_ITER);
            image[(y * WIDTH + x) * 3 + 0] = color; // Red
            image[(y * WIDTH + x) * 3 + 1] = 0;     // Green
            image[(y * WIDTH + x) * 3 + 2] = 255 - color; // Blue
        }
        if (y % 100 == 0) {
            printf("Progress: %.2f%%\n", (y / (double)HEIGHT) * 100);
        }
    }
}

int main() {
    unsigned char *image = (unsigned char *)malloc(WIDTH * HEIGHT * 3);
    if (!image) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Define the range for the Mandelbrot set
    double x_min = -2.0;
    double x_max = 1.0;
    double y_min = -1.5;
    double y_max = 1.5;

    // Generate the Mandelbrot set
    mandelbrot(image, x_min, x_max, y_min, y_max);

    // Save the image as PNG
    stbi_write_png("mandelbrot_set.png", WIDTH, HEIGHT, 3, image, WIDTH * 3);

    // Free allocated memory
    free(image);

    printf("Mandelbrot set generated and saved as 'mandelbrot_set.png'.\n");
    return 0;
}

