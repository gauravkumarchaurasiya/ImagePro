import cv2
import numpy as np
class ImageProcessor:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)

    def convert_to_rgb(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
    
    def convert_to_grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    
    def convert_to_binary(self, threshold):
        _, self.image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY)
    
    def adjust_brightness_contrast(self, alpha, beta):
        self.image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
    
    def add_line(self, start_point, end_point, color=(0, 255, 0), thickness=2):
        self.image = cv2.line(self.image, start_point, end_point, color, thickness)
    
    def add_rectangle(self, start_point, end_point, color=(0, 255, 0), thickness=2):
        self.image = cv2.rectangle(self.image, start_point, end_point, color, thickness)
    
    def add_circle(self, center, radius, color=(0, 255, 0), thickness=2):
        self.image = cv2.circle(self.image, center, radius, color, thickness)
    
    def add_text(self, text, org, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255, 255, 255), thickness=2):
        self.image = cv2.putText(self.image, text, org, font, font_scale, color, thickness)
    
    def crop(self, x, y, w, h):
        self.image = self.image[y:y+h, x:x+w]

    def resize(self, width=None, height=None):
        if width and height:
            self.image = cv2.resize(self.image, (width, height))
        elif width:
            self.image = cv2.resize(self.image, (width, self.image.shape[0]))
        elif height:
            self.image = cv2.resize(self.image, (self.image.shape[1], height))

    def scale(self, factor):
        self.image = cv2.resize(self.image, None, fx=factor, fy=factor)

    def flip(self, flip_code):
        self.image = cv2.flip(self.image, flip_code)

    def add(self, value):
        self.image = cv2.add(self.image, np.array([value]))

    def subtract(self, value):
        self.image = cv2.subtract(self.image, np.array([value]))

    def multiply(self, value):
        self.image = cv2.multiply(self.image, np.array([value]))

    def contrast(self, alpha):
        self.image = cv2.multiply(self.image, alpha)

    def threshold(self, threshold):
        _, self.image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY)

    def bitwise_and(self, other_image):
        self.image = cv2.bitwise_and(self.image, other_image)

    def bitwise_or(self, other_image):
        self.image = cv2.bitwise_or(self.image, other_image)

    def bitwise_xor(self, other_image):
        self.image = cv2.bitwise_xor(self.image, other_image)

    def bitwise_not(self):
        self.image = cv2.bitwise_not(self.image)

    def show_image(self):
        cv2.imshow('Image', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Example usage:
if __name__ == "__main__":
    image_path = 'your_image_path.jpg'  # Provide your image path here
    processor = ImageProcessor(image_path)
    
    # # Convert to RGB
    # processor.convert_to_rgb()
    # processor.show_image()
    
    # # Convert to grayscale
    # processor.convert_to_grayscale()
    # processor.show_image()
    
    # # Convert to binary
    # threshold = 127  # Adjust threshold value as needed
    # processor.convert_to_binary(threshold)
    # processor.show_image()
    
    # # Adjust brightness and contrast
    # alpha = 1.5  # Adjust alpha and beta values as needed
    # beta = 25
    # processor.adjust_brightness_contrast(alpha, beta)
    # processor.show_image()
    
    # # Add annotations
    # processor.add_line((10, 10), (100, 100))
    # processor.add_rectangle((50, 50), (150, 150))
    # processor.add_circle((100, 100), 50)
    # processor.add_text("Example Text", (50, 50))
    # processor.show_image()


# import cv2
# import numpy as np

# class ImageProcessor:
#     def __init__(self, image_path):
#         self.image = cv2.imread(image_path)
#         self.image_path = image_path

#     def convert_to_rgb(self):
#         self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

#     def convert_to_grayscale(self):
#         self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

#     def convert_to_binary(self, threshold):
#         _, self.image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY)

#     def adjust_brightness_contrast(self, alpha, beta):
#         self.image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)

    