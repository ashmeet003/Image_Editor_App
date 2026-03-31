# Ashmeet Kaur
# CompB10 Fall 2025
# Image editing app using pillow and tkinter
# This app gives option to open an image on your system, filter the image and save it

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont


class ImageEditorApp:

    def __init__(self, root):
        self.root = root                                # initializes root of app
        self.root.title("Image Editor App")             # title of app
        self.root.geometry("1000x600")                  # geometry of app

        # Main image stored here (None until opened)
        self.img = None                                 # saves instance of image

        self.createFrame()                              # calls to create layout of app
        self.emptyImage()                               # calls to create placeholder as empty image


    # UI Layout
    # ------------------------------------------------------------------------------------------------------------------
    def createFrame(self):
        self.leftFrame = tk.Frame(self.root, width=200, bg="#e0e0e0")       # left frame
        self.leftFrame.pack(side=tk.LEFT, fill=tk.Y)

        self.rightFrame = tk.Frame(self.root, bg="black")                   # right frame
        self.rightFrame.pack(side=tk.RIGHT, fill="both", expand=True)

        # -----------------------------------------------------------------------------------
        self.appLabel = tk.Label(self.rightFrame,text="Filter It!", font=("Arial", 12), width=10)
        self.appLabel.pack(pady=(40, 10))                                   # Label on right frame

        self.picLabel = tk.Label(self.rightFrame, bg="white")               # image will be held at picLabel, right frame
        self.picLabel.pack(expand=True)

        # ---------------------------------------------------------------------------------------
        # Buttons and related command functions
        # open image, filter(s), save image as
        tk.Label(self.leftFrame, text="Click a Button:", font=("Arial", 12), width = 15).pack(pady=50)

        tk.Button(self.leftFrame, text="Open Image", command=self.openImage).pack(pady=10, padx=50)

        tk.Button(self.leftFrame, text="Filter 1", command=self.filterOne).pack(pady=10, padx=50)

        tk.Button(self.leftFrame, text="Filter 2", command=self.filterTwo).pack(pady=10, padx=50)

        tk.Button(self.leftFrame, text="Filter 3", command=self.filterThree).pack(pady=10, padx=50)

        tk.Button(self.leftFrame, text="Save Image As", command=self.saveImage).pack(pady=10, padx=50)



    # repetitive function to update image and picLabel after each modification
    # ------------------------------------------------------------------------------------------------------------------
    def update_display(self, image):
        self.displayImg = ImageTk.PhotoImage(image)
        self.picLabel.config(image=self.displayImg) # updates picLabel with new image PhotoImage
        self.picLabel.image = self.displayImg       # prevent garbage collection


    # Placeholder image - empty image at start when no image is loaded
    # ------------------------------------------------------------------------------------------------------------------
    def emptyImage(self):
        blank = Image.new("RGB", (500, 350), "white")
        draw = ImageDraw.Draw(blank)                                            # creates new image
        text = "Open an Image to Load"                                          # text to be written in image
        try:                                                                    # uses arial font or else default font
            font = ImageFont.truetype("arial.ttf", 22)
        except:
            font = ImageFont.load_default()

        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)   # uses textbbox to centralize the text
        x = (500 - (right - left)) // 2
        y = (350 - (bottom - top)) // 2
        draw.text((x, y), text, fill="black", font=font)                    # writes text in empty image
        self.update_display(blank)                                              # stores instance and updates image


    # ------------------------------------------------------------------------------------------------------------------
    def openImage(self):                                                        # asks user to open an image
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp *.gif")]
        )
        if not path:
            return

        self.img = Image.open(path).resize((500, 350), Image.LANCZOS)      # resizes and upscales image
        self.update_display(self.img)                                           # stores instance and updates image


    # ------------------------------------------------------------------------------------------------------------------
    def saveImage(self):
        if self.img is None:                                                    # shows error if no image is yet loaded
            messagebox.showerror("Error", "No image to save.")
            return
        path = filedialog.asksaveasfilename(                                    # shows dialog box for user to save image
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"), ("JPEG", "*.jpg"),
                ("Bitmap", "*.bmp"), ("All Files", "*.*")
            ]
        )
        if not path:
            return
        try:                                                                     # if image saved successfully else shows error
            self.img.save(path)
            messagebox.showinfo("Saved", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    # ------------------------------------------------------------------------------------------------------------------
    # FILTERS
    # ---------------------------------------------------------
    def filterOne(self):                                                    # filter one
        if self.img is None:
            return self.no_image_error()

        r, g, b = self.img.split()                                          # splits rgb
        r = r.rotate(3)                                                     # rotates r by 3
        g = g.rotate(358)                                                   # rotates g by 358
        b = b.filter(ImageFilter.GaussianBlur(30))                          # applies blur
        b = ImageEnhance.Brightness(b).enhance(1.5)                         # increases enhancement
        new_img = Image.merge("RGB", (r, g, b))                # merges rgb factors
        new_img = ImageEnhance.Brightness(new_img).enhance(1.5)
        self.img = new_img                                                  # stores instance
        self.update_display(self.img)                                       # updates image


    # ------------------------------------------------------------------------------------------------------------------
    def filterTwo(self):                                                    # filter 2
        if self.img is None:                                                # shows error if no image is opened
            return self.no_image_error()

        r, g, b = self.img.split()                                          # splits rgb, applies filter to r and b
        r = ImageEnhance.Brightness(r.filter(ImageFilter.GaussianBlur(30))).enhance(0.8)
        b = ImageEnhance.Color(b.filter(ImageFilter.EDGE_ENHANCE)).enhance(0.2)
        g = ImageEnhance.Contrast(g).enhance(2.0)                           # applies contrast for g
        self.img = Image.merge("RGB", (r, g, b))               # merges rgb factors and stores instance
        self.update_display(self.img)                                       # updates image

    # ------------------------------------------------------------------------------------------------------------------
    def filterThree(self):                                                  # filter 3 is based on sepia
        if self.img is None:                                                # if no image is opened shows error
            return self.no_image_error()
        sepia = self.img.convert("RGB")                                     # converts RGB
        width, height = sepia.size
        pixels = sepia.load()
        for py in range(height):                                            # goes through each pixel in image
            for px in range(width):
                r, g, b = pixels[px, py]                                    # modifies pixels
                tr = int(0.393*r + 0.769*g + 0.189*b)
                tg = int(0.349*r + 0.686*g + 0.168*b)
                tb = int(0.272*r + 0.534*g + 0.131*b)
                pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255)) # makes pixels limited to 255
        self.img = sepia                                                    # stores instance
        self.update_display(self.img)                                       # updates image


    # ------------------------------------------------------------------------------------------------------------------
    def no_image_error(self):                                               # shows error message if file not opened
        messagebox.showerror("Error", "Please open an image first.")


# ---------------------------------------------------------
# main program - run app
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()