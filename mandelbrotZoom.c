#include <stdio.h>
#include <stdlib.h>

// Function to compute Mandelbrot set and store it in a file
void mandelbrot(int width, int height, double x_min, double x_max, double y_min, double y_max, const char *output_filename) {
    int max_iter = height / 5;
    FILE *file = fopen(output_filename, "w");

    if (!file) {
        printf("Error: Could not open output file.\n");
        exit(1);
    }

    double x_step = (x_max - x_min) / width;
    double y_step = (y_max - y_min) / height;

    for (int i = 0; i < height; i++) {
        double y = y_min + i * y_step;
        for (int j = 0; j < width; j++) {
            double x = x_min + j * x_step;

            // Initialize z and c as complex numbers with real and imaginary parts
            double real_c = x;
            double imag_c = y;
            double real_z = 0.0;
            double imag_z = 0.0;

            int iter = 0;
            while ((real_z * real_z + imag_z * imag_z) <= 4.0 && iter < max_iter) {
                // Compute z^2 + c (real and imaginary parts)
                double real_z_new = real_z * real_z - imag_z * imag_z + real_c;
                double imag_z_new = 2 * real_z * imag_z + imag_c;

                real_z = real_z_new;
                imag_z = imag_z_new;
                iter++;
            }
            // Store the number of iterations for each pixel
            fprintf(file, "%d ", iter);
        }
        fprintf(file, "\n");
    }
    fclose(file);
    printf("Mandelbrot set calculation finished and saved to %s\n", output_filename);
}

int main() {
    // Parameters for the Mandelbrot set
    int width = 2000, height = 2000;
    double x_min = -2.0, x_max = 1.0;
    double y_min = -1.5, y_max = 1.5;

    // File to store the results
    const char *output_filename = "mandelbrot_data.txt";

    // Calculate the Mandelbrot set and store it
    mandelbrot(width, height, x_min, x_max, y_min, y_max, output_filename);

    return 0;
}
