import os
import base64
import sys
import requests
from urllib.parse import quote
from PIL import Image

def optimize_image(image_path, max_size=(64, 64)):
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size)
            
            optimized_path = "optimized_image.png"
            img.save(optimized_path, format='PNG', optimize=True)
            
            return optimized_path
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return None

if len(sys.argv) != 2:
    print("Usage: python create-markdown-badges.py <full_base_path>")
    input("")
    sys.exit(1)

base_path = sys.argv[1]

script_path = os.path.realpath(os.path.dirname(__file__))

os.chdir(script_path)

download_folder = os.path.join(script_path, "SVG Files")

os.makedirs(download_folder, exist_ok=True)

os.chdir(download_folder)

optimized_image_path = optimize_image(base_path)
if optimized_image_path:
    with open(optimized_image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    badge_name = input("What is the badge name? ")
    badge_color = input("What is the badge color? ")

    encoded_badge_name = quote(badge_name)
    encoded_badge_color = quote(badge_color)

    badge_url = f"https://img.shields.io/badge/{encoded_badge_name}-{encoded_badge_color}?style=for-the-badge&logo=image/png;base64,{encoded_string}"

    response = requests.get(badge_url)

    if response.status_code == 200:
        output_file = f"{badge_name.replace(' ', '_')}.svg"
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"SVG file saved as {output_file}")
    else:
        print(f"Failed to download SVG: {response.status_code}")
else:
    print("Failed to optimize the image")

os.remove("optimized_image.png")