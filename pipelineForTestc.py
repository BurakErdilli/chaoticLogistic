import numpy as np
import matplotlib.pyplot as plt

def load_mandelbrot_data(filename):
    params = {}
    
    with open(filename, 'r') as file:
        # Read the image data
        data = []
        for line in file:
            line = line.strip()  # Remove whitespace
            if line:  # Only process non-empty lines
                try:
                    data.append(list(map(int, line.split())))
                except ValueError:
                    print(f"Warning: Data line is not valid: '{line}'")
                    continue  # Skip lines that can't be converted

    return np.array(data)

def load_parameters(filename):
    params = {}
    
    with open(filename, 'r') as file:
        # Read header parameters
        for line in file:
            line = line.strip()
            if line:  # Check if the line is not empty
                key, value = line.split(": ")
                params[key] = float(value) if '.' in value else int(value)
    
    return params

# Load parameters and the Mandelbrot data
params = load_parameters('config.txt')
mandelbrot_image = load_mandelbrot_data('mandelbrot_data.txt')

# Create the plot with high quality
plt.figure(figsize=(10, 10), dpi=300)
plt.imshow(mandelbrot_image, extent=(params['X_min'], params['X_max'], params['Y_min'], params['Y_max']), cmap='hot', interpolation='bilinear')
plt.colorbar()
plt.title('Mandelbrot Set')
plt.xlabel('Real')
plt.ylabel('Imaginary')

# Save as PNG and PDF with high DPI and no compression
plt.savefig('mandelbrot_set_dynamic.png', format='png', dpi=600)
plt.savefig('mandelbrot_set_dynamic.pdf', format='pdf', dpi=600)

plt.show()
