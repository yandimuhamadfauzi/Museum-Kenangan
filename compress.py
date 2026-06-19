import os
from PIL import Image

def compress_images(directory):
    compressed_count = 0
    saved_bytes = 0
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(directory, filename)
            filesize = os.path.getsize(filepath)
            
            # Compress if size > 300KB
            if filesize > 300 * 1024:
                try:
                    with Image.open(filepath) as img:
                        # Convert to RGB if it's PNG with alpha to save as JPEG, but let's keep original format
                        if filename.lower().endswith('.png'):
                            # For PNG, optimize
                            img.save(filepath, "PNG", optimize=True)
                        else:
                            # For JPEG
                            if img.mode in ("RGBA", "P"):
                                img = img.convert("RGB")
                            img.save(filepath, "JPEG", optimize=True, quality=50)
                            
                    new_size = os.path.getsize(filepath)
                    saved_bytes += (filesize - new_size)
                    compressed_count += 1
                    print(f"Compressed {filename}: {filesize//1024}KB -> {new_size//1024}KB")
                except Exception as e:
                    print(f"Failed to compress {filename}: {e}")
                    
    print(f"\nDone! Compressed {compressed_count} images. Saved {(saved_bytes / 1024 / 1024):.2f} MB.")

if __name__ == "__main__":
    compress_images("img")
