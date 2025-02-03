import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

# Prompt user for the filename
filename = input("Enter the image filename (including extension, e.g., image.jpg): ")
image_path = os.path.join("Media", filename)

# Load and resize image
def image_to_matrix(image_path, matrix_width, matrix_height, grayscale=False):
  img = Image.open(image_path)
  img = img.resize((matrix_width, matrix_height), Image.LANCZOS)  # Correct resolution

  if grayscale:
    img = img.convert('L')  # Convert to grayscale
    matrix = np.array(img)  # 2D array (grayscale)
  else:
    img = img.convert('RGB')  # Convert to RGB
    matrix = np.array(img)  # 3D array (height, width, 3)

  return matrix

# Function to rotate the image around its center
def rotate_matrix(matrix, angle):
  h, w = matrix.shape[:2]  # Get height and width
  center = (w // 2, h // 2)  # Find center of image

  # Compute the rotation matrix
  rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

  # Apply the rotation (keeping the original size)
  rotated_matrix = cv2.warpAffine(matrix, rotation_matrix, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

  return rotated_matrix

# Animation loop (smooth rotation)
def animate(matrix, fps=5, rotation_speed=5):
  plt.ion()  # Enable interactive mode
  fig, ax = plt.subplots(figsize=(5, 5))
  img_plot = ax.imshow(matrix, interpolation='nearest')
  ax.axis('off')

  frame_time = 1 / fps  # Time per frame
  angle = 0  # Start angle

  while True:
    angle += rotation_speed  # Increment angle
    angle %= 360  # Keep angle within 0-360 degrees

    rotated_matrix = rotate_matrix(matrix, angle)  # Apply rotation

    img_plot.set_data(rotated_matrix)  # Update plot with new matrix
    plt.pause(frame_time)  # Maintain frame rate

# Example Usage
matrix_width = 64  # Set LED matrix width
matrix_height = 64  # Set LED matrix height

# Check if file exists before proceeding
if os.path.exists(image_path):
  matrix = image_to_matrix(image_path, matrix_width, matrix_height, grayscale=False)
  # Start animation (5 FPS, rotates smoothly)
  animate(matrix, fps=5, rotation_speed=5)
else:
  print(f"Error: The file '{image_path}' does not exist.")
