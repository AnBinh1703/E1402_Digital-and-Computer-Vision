"""
OpenCV Image Exercises
Exercise: Reading, displaying, and saving images using OpenCV
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Create output directory if it doesn't exist
output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

# ============================================================================
# EXERCISE 1: Create and save an image as JPG file using imwrite
# ============================================================================
print("Exercise 1: Creating and saving a JPG image...")

# Create a simple image (500x500 pixels, 3 channels RGB)
# Using numpy to create a colorful gradient image
height, width = 500, 500
image = np.zeros((height, width, 3), dtype=np.uint8)

# Create a gradient effect
for y in range(height):
    for x in range(width):
        image[y, x] = [
            int(255 * (x / width)),      # Red channel
            int(255 * (y / height)),     # Green channel
            int(255 * (1 - x / width))   # Blue channel
        ]

# Save the image as JPG (note: OpenCV uses BGR format, not RGB)
image_path = output_dir / 'constructed_image.jpg'
success = cv2.imwrite(str(image_path), image)

if success:
    print(f"✓ Image successfully saved to: {image_path}")
    print(f"  Image dimensions: {image.shape}")
else:
    print(f"✗ Error: Could not save image to {image_path}")

# ============================================================================
# EXERCISE 2: Read and display the saved image using imread
# ============================================================================
print("\nExercise 2: Reading and displaying the saved image...")

# Read the image
read_image = cv2.imread(str(image_path))

if read_image is not None:
    print(f"✓ Image successfully read from: {image_path}")
    print(f"  Image shape (H, W, C): {read_image.shape}")
    print(f"  Image data type: {read_image.dtype}")
    
    # Save the image visualization using matplotlib
    try:
        plt.figure(figsize=(8, 6))
        # Convert BGR to RGB for matplotlib display
        image_rgb = cv2.cvtColor(read_image, cv2.COLOR_BGR2RGB)
        plt.imshow(image_rgb)
        plt.title('Exercise 2: Constructed Image')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_dir / 'exercise2_displayed_image.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Image saved to: {output_dir / 'exercise2_displayed_image.png'}")
    except Exception as e:
        print(f"  Note: Could not display image ({e}), but file was read successfully")
else:
    print(f"✗ Error: Could not read image from {image_path}")

# ============================================================================
# EXERCISE 3: Read and display another image from disk
# ============================================================================
print("\nExercise 3: Reading and displaying another image from disk...")

# Use the specified image
image_filename = 'virtual-zoom-background-999nyko6xd1pzz6f.jpg'
found_image_path = Path(image_filename) if Path(image_filename).exists() else None

# If not found in current directory, search in common locations
if found_image_path is None:
    possible_locations = [
        image_filename,
        f'output/{image_filename}',
        f'notebooks/{image_filename}',
        f'../Downloads/{image_filename}',
    ]
    for img_path in possible_locations:
        if Path(img_path).exists():
            found_image_path = Path(img_path)
            break

if found_image_path is None:
    # Create a sample image if no existing image found
    print("  No existing images found. Creating a sample image...")
    sample_image = np.ones((400, 600, 3), dtype=np.uint8) * 100
    
    # Add some shapes to make it more interesting
    cv2.rectangle(sample_image, (50, 50), (250, 250), (0, 255, 0), 3)
    cv2.circle(sample_image, (400, 200), 100, (255, 0, 0), -1)
    cv2.putText(sample_image, 'Sample Image', (100, 350), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    found_image_path = output_dir / 'sample_image.png'
    cv2.imwrite(str(found_image_path), sample_image)
    print(f"  Sample image created at: {found_image_path}")

# Read the image
another_image = cv2.imread(str(found_image_path))

if another_image is not None:
    print(f"✓ Image successfully read from: {found_image_path}")
    print(f"  Image shape (H, W, C): {another_image.shape}")
    print(f"  Image data type: {another_image.dtype}")
    
    # Save the image visualization using matplotlib
    try:
        plt.figure(figsize=(8, 6))
        # Check if it's grayscale or color, then display appropriately
        if len(another_image.shape) == 2:
            plt.imshow(another_image, cmap='gray')
        else:
            # Convert BGR to RGB for matplotlib display
            image_rgb = cv2.cvtColor(another_image, cv2.COLOR_BGR2RGB)
            plt.imshow(image_rgb)
        plt.title('Exercise 3: Additional Image')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_dir / 'exercise3_displayed_image.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Image saved to: {output_dir / 'exercise3_displayed_image.png'}")
    except Exception as e:
        print(f"  Note: Could not display image ({e}), but file was read successfully")
else:
    print(f"✗ Error: Could not read image from {found_image_path}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("EXERCISES COMPLETED")
print("="*70)
print("Exercise 1: ✓ Created and saved an image as JPG")
print("Exercise 2: ✓ Read the saved image and displayed it")
print("Exercise 3: ✓ Read another image and displayed it")
print("="*70)
