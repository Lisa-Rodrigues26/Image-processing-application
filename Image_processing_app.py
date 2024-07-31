import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk, ImageFilter
import cv2

# Create a new window
window = tk.Tk()
window.geometry("1300x800")

# Set window title
window.title("Image Processing App")

# Load and resize background image
bg_image = Image.open("purple_image.jpg").resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label for the background image
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add a label for image display
image_label = tk.Label(window)
image_label.pack()

# Define image processing functions
def open_image():
    global original_image, current_image
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename()
    
    # Load the image and display it in the label
    with open(file_path, 'rb') as f:
        original_image = Image.open(f)
        current_image = ImageTk.PhotoImage(original_image)
        image_label.config(image=current_image)
    
def grayscale():
    global current_image
    # Get the original image and convert it to grayscale
    gray_image = original_image.convert("L")
    
    # Display the grayscale image in the label
    current_image = ImageTk.PhotoImage(gray_image)
    image_label.config(image=current_image)
    
def detect_edges():
    global current_image, file_path

    # Load the image and convert it to grayscale
    image = cv2.imread("C:/Users/hp/AppData/Local/Programs/Python/Python310/download.jpg")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect edges using Canny edge detection
    edges = cv2.Canny(gray_image, 100, 200)

    # Display the edge detection result in the label
    edge_image = Image.fromarray(edges)
    current_image = ImageTk.PhotoImage(edge_image)
    image_label.config(image=current_image)

def blur():
    global current_image
    # Get the original image and apply a Gaussian blur
    blurred_image = original_image.filter(ImageFilter.GaussianBlur(radius=5))
    
    # Display the blurred image in the label
    current_image = ImageTk.PhotoImage(blurred_image)
    image_label.config(image=current_image)

def thresholding():
    global current_image
    # Get the original image and convert it to grayscale
    gray_image = original_image.convert("L")

    # Prompt user for threshold value
    threshold_value = simpledialog.askinteger("Threshold Value", "Enter a threshold value:")

    # Apply thresholding to the grayscale image
    thresholded_image = gray_image.point(lambda x: 255 if x > threshold_value else 0, '1')

    # Display the thresholded image in the label
    current_image = ImageTk.PhotoImage(thresholded_image)
    image_label.config(image=current_image)


def low_pass():
    global current_image
    # Get the original image and convert it to grayscale
    gray_image = original_image.convert("L")
    
    # Apply low pass filter to the grayscale image
    kernel = [1/9, 1/9, 1/9,1/9, 1/9, 1/9,1/9, 1/9, 1/9]
    low_pass_image = gray_image.filter(ImageFilter.Kernel((3,3), kernel))
    
    # Display the low pass image in the label
    current_image = ImageTk.PhotoImage(low_pass_image)
    image_label.config(image=current_image)

def bit_plane_slicing():
    global current_image
    # Get the original image and convert it to grayscale
    gray_image = original_image.convert("L")
    
    # Convert the grayscale image to binary
    binary_image = gray_image.convert('1')
    
    # Get the bit plane of the binary image
    plane_number = 7
    plane_image = binary_image.point(lambda x: x&(1<<plane_number))
    
    # Display the bit plane image in the label
    current_image = ImageTk.PhotoImage(plane_image)
    image_label.config(image=current_image)

def close_window():
    window.destroy()

# Create a frame to hold the image and buttons
frame = tk.Frame(window)


def restore_original():
    global current_image
    current_image = ImageTk.PhotoImage(original_image)
    image_label.config(image=current_image)

# Add buttons for image processing
open_button = tk.Button(window, text="Open Image", command=open_image, bg="purple", fg="white")
open_button.pack(pady=10)

restore_button = tk.Button(window, text="Restore Original", command=restore_original, bg="white", fg="black")
restore_button.pack(pady=10)

grayscale_button = tk.Button(window, text="Grayscale", command=grayscale, bg="white", fg="black")
grayscale_button.pack(pady=10)

edge_button = tk.Button(window, text="Edge Detection", command=detect_edges, bg="white", fg="black")
edge_button.pack(pady=10)

blur_button = tk.Button(window, text="Blur Image", command=blur, bg="white", fg="black")
blur_button.pack(pady=10)

threshold_button = tk.Button(window, text="Thresholding", command=thresholding, bg="white", fg="black")
threshold_button.pack(pady=10)

low_pass_button = tk.Button(window, text="Low Pass Filter", command=low_pass, bg="white", fg="black")
low_pass_button.pack(pady=10)

bit_plane_button = tk.Button(window, text="Bit Plane Slicing", command=bit_plane_slicing, bg="white", fg="black")
bit_plane_button.pack(pady=10)

# Add a button to exit the app
close_window = tk.Button(window, text="Exit", command=window.quit, bg="red", fg="white")
close_window.pack(pady=10)

# Run the event loop
window.mainloop()
window.destroy()
