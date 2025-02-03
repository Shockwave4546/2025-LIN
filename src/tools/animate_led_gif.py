import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageSequence
import cv2

# Prompt user for the filename
filename = input("Enter the GIF filename (including .gif extension): ")
gif_path = os.path.join("Media", filename)

# Load a frame from the GIF and resize it to fit the matrix
def frame_to_matrix(frame, matrix_width, matrix_height, grayscale=False):
  # Resize the frame to match the LED matrix size
  frame_resized = frame.resize((matrix_width, matrix_height))

  if grayscale:
    frame_resized = frame_resized.convert('L')  # Convert to grayscale
    matrix = np.array(frame_resized)  # 2D array (grayscale)
  else:
    matrix = np.array(frame_resized)  # 3D array (height, width, 3)

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

# Function to play GIF frames as animation
def play_gif_as_animation(gif_path, matrix_width, matrix_height, fps=10, rotation_speed=0):
  if not os.path.exists(gif_path):
    print(f"Error: The file '{gif_path}' does not exist.")
    return

  gif = Image.open(gif_path)  # Open GIF file

  # Get all frames of the GIF
  frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]

  plt.ion()  # Enable interactive mode
  fig, ax = plt.subplots(figsize=(5, 5))
  img_plot = ax.imshow(np.zeros((matrix_height, matrix_width, 3), dtype=np.uint8), interpolation='nearest')
  ax.axis('off')

  frame_time = 1 / fps  # Time per frame
  angle = 0  # Initial angle for rotation
  num_frames = len(frames)

  while True:
    for i in range(num_frames):
      frame = frames[i]  # Get the current frame

      matrix = frame_to_matrix(frame, matrix_width, matrix_height, grayscale=False)  # Convert frame to matrix

      # Skip rotation if rotation_speed is 0
      if rotation_speed != 0:
        angle += rotation_speed  # Increment angle
        angle %= 360  # Keep angle within 0-360 degrees
        matrix = rotate_matrix(matrix, angle)  # Apply rotation

      img_plot.set_data(matrix)  # Update plot with new matrix (frame)
      plt.pause(frame_time)  # Control frame rate

# Example Usage
matrix_width = 64  # Set LED matrix width
matrix_height = 64  # Set LED matrix height

# Start animation (play GIF as animation on matrix without rotation)
play_gif_as_animation(gif_path, matrix_width, matrix_height, fps=10, rotation_speed=0)
