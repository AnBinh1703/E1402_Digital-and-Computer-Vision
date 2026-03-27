import cv2
import numpy as np
from pathlib import Path

# Create output directory
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

# Create a blank white image
image = np.ones((500, 500, 3), dtype='uint8') * 255

# Define the center and radius of the circle
center_coordinates = (250, 250)
radius = 100
color = (0, 0, 255)  # Red color in BGR
thickness = 2  # Line thickness (-1 to fill the circle)

# Draw the circle
cv2.circle(image, center_coordinates, radius, color, thickness)

# Save the image
output_path = output_dir / 'circle.jpg'
cv2.imwrite(str(output_path), image)
print(f"✓ Circle image saved to: {output_path}")
print(f"  Image shape: {image.shape}")

# Also create a visualization with matplotlib
import matplotlib.pyplot as plt

plt.figure(figsize=(6, 6))
# Convert BGR to RGB for matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.title('Red Circle on White Background')
plt.axis('off')
plt.tight_layout()
plt.savefig(output_dir / 'circle_visualization.png', dpi=150, bbox_inches='tight')
plt.close()
print(f"✓ Visualization saved to: {output_dir / 'circle_visualization.png'}")
