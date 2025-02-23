from PIL import Image, ImageTk
from data import globals
import tkinter as tk

class ImageProcessor:
    @staticmethod
    def ensure_rgba(image: Image.Image) -> Image.Image:
        """Convert image to RGBA if needed"""
        return image if image.mode == 'RGBA' else image.convert('RGBA')

    @staticmethod
    def safe_resize(image: Image.Image, width: int, height: int) -> Image.Image:
        """Safely resize image checking for valid dimensions"""
        if width > 0 and height > 0:
            return image.resize((width, height), Image.Resampling.LANCZOS)
        return image

    @staticmethod
    def calculate_dimensions(original_size: tuple, scale: int) -> tuple:
        """Calculate new dimensions based on scale percentage"""
        return (
            int(original_size[0] * scale / 100),
            int(original_size[1] * scale / 100)
        )

    @staticmethod
    def calculate_center_position(container_size: tuple, percentage: tuple) -> tuple:
        """Calculate centered position based on percentages"""
        x = container_size[0] * percentage[0] / 100
        y = container_size[1] * percentage[1] / 100
        return (x, y)

class CanvasElement:
    def __init__(self, canvas: tk.Canvas, container_id: str):
        self.canvas = canvas
        self.container_id = container_id
        self.processor = ImageProcessor()

    def update_position(self, x_percent: float, y_percent: float):
        """Update element position on canvas"""
        if not self.canvas:
            return
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        x = width / 2 + (width * x_percent / 100)
        y = height / 2 + (height * y_percent / 100)
        self.canvas.coords(self.container_id, x, y)
        self.canvas.itemconfig(self.container_id, anchor="center")

    def transform_image(self, image: Image.Image, scale: int, rotation: int) -> Image.Image:
        """Apply scale and rotation transformations"""
        image = ImageProcessor.ensure_rgba(image)
        new_width, new_height = ImageProcessor.calculate_dimensions(image.size, scale)
        image = ImageProcessor.safe_resize(image, new_width, new_height)
        return image.rotate(rotation, expand=True) if rotation != 0 else image
    
    def apply_transforms(self) -> None:
        """Applique toutes les transformations à l'élément"""
        if not hasattr(self, 'canvas') or not self.canvas:
            return
            
        image = Image.open(globals["render"][self.path_key])
        image = self.transform_image(
            image,
            int(globals["render"]["val"][self.scale_key]),
            int(globals["render"]["val"][self.rotate_key])
        )
        
        # Créer et sauvegarder la nouvelle image
        globals[self.image_key] = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(
            self.container_id,
            image=globals[self.image_key],
            anchor="center"
        )

