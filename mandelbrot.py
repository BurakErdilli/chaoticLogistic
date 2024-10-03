import numpy as np
import matplotlib.pyplot as plt

# Function to compute the Mandelbrot set
def mandelbrot(c, max_iter):
    z = np.zeros(c.shape, dtype=np.complex64)
    mask = np.full(c.shape, True, dtype=bool)
    output = np.zeros(c.shape, dtype=int)

    for i in range(max_iter):
        z[mask] = z[mask] ** 2 + c[mask]
        mask = np.abs(z) <= 2
        output += mask
        print(str(i) + " / "+ str(max_iter) + " % " + str((i/max_iter)*100))


    return output

# Parameters for the Mandelbrot set
width, height = 4000, 4000  # High resolution
x_min, x_max = -2.5, 1.5
y_min, y_max = -2.0, 2.0
max_iterations = 1000

# Create the complex grid
x = np.linspace(x_min, x_max, width)
y = np.linspace(y_min, y_max, height)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

# Compute the Mandelbrot set
mandelbrot_set = mandelbrot(C, max_iterations)

# Plot the Mandelbrot set
plt.figure(figsize=(10, 10), dpi=300)
plt.imshow(mandelbrot_set, extent=[x_min, x_max, y_min, y_max], cmap='inferno')
plt.colorbar(label='Iterations')
plt.title('Mandelbrot Set')

# Save the image without loss (max resolution PNG)
plt.savefig("mandelbrot_high_res.png", format='png', dpi=300, bbox_inches='tight')

# Show the image on the screen (optional)
plt.show()



