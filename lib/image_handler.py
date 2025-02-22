import os
from PIL import Image

def save_temp_png(image: Image.Image, temp_path: str) -> None:
    """
    Sauvegarde une image temporaire au format PNG.
    Assure que le dossier existe et que l'image est en RGBA.
    """
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    image.save(temp_path, 'PNG')

def load_and_convert_image(image_path: str) -> Image.Image:
    """
    Charge une image de n'importe quel format supporté et la convertit en format compatible
    avec le comportement attendu (RGBA).
    
    Args:
        image_path (str): Chemin vers l'image à charger
        
    Returns:
        Image.Image: Image au format RGBA
        
    Raises:
        ValueError: Si le format d'image n'est pas supporté
        FileNotFoundError: Si le fichier n'existe pas
    """
    try:
        # Vérifier l'existence du fichier
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier {image_path} n'existe pas")
            
        # Ouvrir l'image avec Pillow
        image = Image.open(image_path)
        
        # Liste des formats supportés
        SUPPORTED_FORMATS = {'PNG', 'JPEG', 'JPG', 'BMP', 'WEBP', 'TIFF', 'GIF'}
        
        # Vérifier si le format est supporté
        if image.format not in SUPPORTED_FORMATS:
            raise ValueError(f"Format {image.format} non supporté. Formats supportés: {', '.join(SUPPORTED_FORMATS)}")
            
        # Si l'image est un GIF animé, prendre la première frame
        if image.format == 'GIF' and getattr(image, 'is_animated', False):
            image.seek(0)
            image = image.convert('RGBA')
            
        # Pour les images sans transparence, créer un canal alpha blanc
        if image.mode in ['RGB', 'L']:
            # Convertir en RGBA
            rgba_image = Image.new('RGBA', image.size, (255, 255, 255, 0))
            rgba_image.paste(image, (0, 0))
            image = rgba_image
        elif image.mode != 'RGBA':
            # Pour tous les autres modes, convertir directement en RGBA
            image = image.convert('RGBA')
            
        return image
        
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement de l'image: {str(e)}")

def save_as_png(image: Image.Image, output_path: str) -> None:
    """
    Sauvegarde une image au format PNG en préservant la transparence.
    
    Args:
        image (Image.Image): Image à sauvegarder
        output_path (str): Chemin de sortie
    """
    # S'assurer que l'image est en mode RGBA
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Créer le dossier de sortie si nécessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Sauvegarder l'image
    image.save(output_path, 'PNG')