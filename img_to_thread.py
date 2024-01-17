import PIL

def load_image(path):
    image = Image.open(path).convert("L")  # Convert to grayscale
    # Convert the image to a NumPy array
    image_array = np.array(image)

# Computes the change of the rsulting picture for a nail pair
def pixel_map(start_nail, end_nail, x_size, y_size):
    pass

def make_StringArt(img, nails):
    pass

def random_pattern(nails, thread):
    import random
    print(nails)
    for i in range(thread):
        a = random.randint(0,nails)
        b = random.randint(0,nails)
        print(f"{a} {b}")