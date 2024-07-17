import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# Ścieżka do katalogu z obrazami
output_dir = 'data/output'

# Lista folderów
folders = [f'combined_river_van_bigger_{i}k' for i in range(1, 11)]

# Wczytaj obrazy
images = [Image.open(os.path.join(output_dir, folder, '1000.jpg')).convert("RGBA") for folder in folders]

# Ustal rozmiar obrazów (zakładam, że wszystkie mają ten sam rozmiar)
img_width, img_height = images[0].size

# Wysokość jednego obrazka w siatce
grid_img_height = 3 * img_height  # Wysokość siatki 3x3

# Szerokość jednego obrazka w siatce, proporcjonalnie zmieniona
desired_width = 4 * img_width  # Szerokość, którą chcemy osiągnąć
scale_factor_width = desired_width / img_width
grid_img_width = int(img_width * scale_factor_width)

# Skalowanie obrazków w siatce
images_resized = [img.resize((img_width, img_height), Image.ANTIALIAS) for img in images]

# Tworzenie siatki 3x3 dla pierwszych 9 obrazów
grid_img = Image.new('RGBA', (grid_img_width, grid_img_height), (255, 255, 255, 0))

for i in range(9):
    x = (i % 3) * img_width
    y = (i // 3) * img_height
    grid_img.paste(images_resized[i], (x, y))

# Odstęp między siatką a ostatnim obrazem
spacing = 20

# Nowe wymiary ostatniego obrazka (chcemy, aby jego wysokość wynosiła 3 * img_height)
new_height = 3 * img_height
new_width = int(new_height * (images_resized[9].width / images_resized[9].height))

# Skalowanie ostatniego obrazka
last_image_resized = images_resized[9].resize((new_width, new_height), Image.ANTIALIAS)

# Rozmiar finalnego obrazu
final_img_height = grid_img_height
final_img_width = grid_img_width + new_width + spacing

# Tworzenie finalnego obrazu z siatką 3x3 i ostatnim obrazem obok
final_img = Image.new('RGBA', (final_img_width, final_img_height), (255, 255, 255, 0))

# Wklej siatkę 3x3
final_img.paste(grid_img, (0, 0))

# Centrowanie ostatniego obrazu w osi Y
last_img_y = (final_img_height - new_height) // 2

# Wklej ostatni obraz obok siatki, po skalowaniu
final_img.paste(last_image_resized, (grid_img_width + spacing, last_img_y))

# Zapisz finalny obraz
final_img.save(os.path.join(output_dir, 'combined_grid_centered_with_spacing_enlarged.png'))

# Wyświetl obraz
plt.figure(figsize=(20, 20))
plt.imshow(final_img)
plt.axis('off')
plt.show()
