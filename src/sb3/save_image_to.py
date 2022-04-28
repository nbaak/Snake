
from PIL import Image

def save_image_to(frame, filename="frame.png"):
    im = Image.fromarray(frame)
    im.save(filename)    
    
def save_images_as_animation(frames, filename="video.gif", duration=10, loop=1):
    animation_images = []
    for frame in frames:
        animation_images.append(frame)
        
    animation_images[0].save(filename, save_all=True, append_images=animation_images[1:], duration=duration, loop=loop)