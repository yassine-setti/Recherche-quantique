import cv2
import os

def create_video_from_images(image_folder, output_video_file, fps):
    # Get all image file names from the folder
    images = [img for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))]
    images.sort()  # Sort images alphabetically or numerically for proper sequence

    if not images:
        print("No images found in the folder!")
        return
    
    # Read the first image to get the frame size
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape
    frame_size = (width, height)
    
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 format
    video = cv2.VideoWriter(output_video_file, fourcc, fps, frame_size)

    print(f"Creating video: {output_video_file} at {fps} FPS.")
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)  # Add frame to video
        print(f"Added {image} to the video.")
    
    # Release the video writer object
    video.release()
    print(f"Video saved as {output_video_file}.")

# Folder containing images
image_folder = r"C:\Users\yassi\Desktop\2A\Recherche\Scripts"
# Output video file name
output_video_file =r"C:\Users\yassi\Desktop\2A\Recherche\Multiwfn_3.8_dev_bin_Win64\video\4nitroaniline_NH2_orbitale35.mp4"
# Frames per second
fps = 5

create_video_from_images(image_folder, output_video_file, fps)