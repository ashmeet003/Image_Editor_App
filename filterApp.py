from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageDraw, ImageFont

img = None

def update_display(image):
    imgDisplay = ImageTk.PhotoImage(image)
    picLabel.config(image=imgDisplay)
    picLabel.image = imgDisplay

def applyFilterOne():
    global img
    if img is None:
        messagebox.showerror("Error", "No image loaded to filter.")
        print("No image loaded.")
        return
    # Split the image into channels
    imRed, imGreen, imBlue = img.split()
    imRed = imRed.rotate(3)
    imGreen = imGreen.rotate(358)
    imBlue = imBlue.filter(ImageFilter.GaussianBlur(30))
    enhancer = ImageEnhance.Brightness(imBlue)
    imBlue = enhancer.enhance(1.5)
    image1 = Image.merge("RGB",(imRed, imGreen, imBlue))
    enhancer = ImageEnhance.Brightness(image1)
    image1 = enhancer.enhance(1.5)
    print("\nThe Filter has Been Applied.\n")
    img = image1
    update_display(img)

def applyFilterTwo():
    global img
    if img is None:
        messagebox.showerror("Error", "No image loaded to filter.")
        print("No image loaded.")
        return
    r,g,b = img.split()
    # filters red:
    r = r.filter(ImageFilter.GaussianBlur(30))
    enhancer = ImageEnhance.Brightness(r)
    r = enhancer.enhance(0.8)
    # filters blue:
    b = b.filter(ImageFilter.EDGE_ENHANCE)
    enhancer = ImageEnhance.Color(b)
    b = enhancer.enhance(0.2)
    # filters green:
    enhancer = ImageEnhance.Contrast(g)
    g = enhancer.enhance(2.0)
    # merges image
    image1 = Image.merge("RGB",(r,g,b))
    print("\nThe Filter has Been Applied.\n")
    # displays and returns image
    img = image1
    update_display(img)

def openImage():
    global img, picLabel
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp *.gif")]
    )
    if not file_path:
        return
    # Load and resize image
    img = Image.open(file_path)
    img = img.resize((500, 350), Image.LANCZOS)
    update_display(img)


def saveImage():
    global img
    if img is None:
        messagebox.showerror("Error", "No image loaded to save.")
        return
    # Ask user where to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("Bitmap Image", "*.bmp"),
            ("All Files", "*.*")
        ]
    )
    if not file_path:
        return  # user canceled

    try:
        img.save(file_path)
        messagebox.showinfo("Success", "Image saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save image:\n{e}")

# GUI
# ----------------------------------------------------------------------------------------------
root = tk.Tk()
root.title("Filter Image App")
root.geometry("1000x600")

leftFrame = tk.Frame(root, width=200, bg="#e0e0e0")
leftFrame.pack(side=tk.LEFT, fill=tk.Y)

rightFrame = tk.Frame(root, bg = "black")
rightFrame.pack(side=tk.RIGHT, fill="both", expand=True)

txtLabel = tk.Label(rightFrame,text="Picture!", font=("Arial", 10), width=10)
txtLabel.pack(pady=(40,10))
# --- Create blank white 500x500 placeholder ---
blank_img = Image.new("RGB", (500, 350), "white")
draw = ImageDraw.Draw(blank_img)
text = "Open an Image to load"
try:
    font = ImageFont.truetype("arial.ttf", size=20)
except IOError:
    print("Arial font not found. Using default Pillow font (size cannot be changed).")
    font = ImageFont.load_default() # Fallback, note that size cannot be controlled here
left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
text_width = right - left
text_height = bottom - top
x = (500 - text_width) // 2
y = (350 - text_height) // 2
draw.text((x, y), text, fill="black", font=font)
blank_display = ImageTk.PhotoImage(blank_img)

picLabel = tk.Label(rightFrame, image=blank_display, bg="white")
picLabel.image = blank_display
picLabel.pack(expand=True)

# buttons in left frame
# ------------------------------------------------------------------------------
buttonLabel = tk.Label(leftFrame, text="Click a Button:", font=("Arial", 10), width=15)
buttonLabel.pack(pady=50)

filter1Button = tk.Button(leftFrame, text = "Filter 1", command = applyFilterOne)
filter1Button.pack(pady=10, padx=50)

filter2Button = tk.Button(leftFrame, text = "Filter 2", command = applyFilterTwo)
filter2Button.pack(pady=10, padx=50)

openImageButton = tk.Button(leftFrame, text = "Open Image", command = openImage)
openImageButton.pack(pady=10, padx=50)

saveImageButton = tk.Button(leftFrame, text="Save Image As", command=saveImage)
saveImageButton.pack(pady=10, padx=50)
# -------------------------------------------------------------------------------
root.mainloop()
# # # #
# # # #
# # # #
# # # #
# # # #
# # # # #**********************************************************************************************************************
# # #
# # # import tkinter as tk
# # # from tkinter import filedialog, messagebox
# # # from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
# # #
# # #
# # # class ImageEditorApp:
# # #
# # #     def __init__(self, root):
# # #         self.root = root
# # #         self.root.title("Image Editor App")
# # #         self.root.geometry("1000x600")
# # #
# # #         # Main image stored here (None until opened)
# # #         self.img = None
# # #
# # #         # Track cropping
# # #         self.crop_start_x = None
# # #         self.crop_start_y = None
# # #         self.crop_rect = None
# # #
# # #         self.create_layout()
# # #         self.create_placeholder()
# # #
# # #     # ---------------------------------------------------------
# # #     # UI LAYOUT
# # #     # ---------------------------------------------------------
# # #     def create_layout(self):
# # #         self.leftFrame = tk.Frame(self.root, width=200, bg="#e0e0e0")
# # #         self.leftFrame.pack(side=tk.LEFT, fill=tk.Y)
# # #
# # #         self.rightFrame = tk.Frame(self.root, bg="black")
# # #         self.rightFrame.pack(side=tk.RIGHT, fill="both", expand=True)
# # #
# # #         self.txtLabel = tk.Label(self.rightFrame, text="Picture",
# # #                                  font=("Arial", 16), fg="white", bg="black")
# # #         self.txtLabel.pack(pady=(40, 10))
# # #
# # #         self.picLabel = tk.Label(self.rightFrame, bg="white")
# # #         self.picLabel.pack(expand=True)
# # #
# # #         # Buttons
# # #         tk.Label(self.leftFrame, text="Options:", font=("Arial", 12),
# # #                  bg="#e0e0e0").pack(pady=20)
# # #
# # #         tk.Button(self.leftFrame, text="Open Image", width=18,
# # #                   command=self.open_image).pack(pady=10)
# # #
# # #         tk.Button(self.leftFrame, text="Filter 1", width=18,
# # #                   command=self.filter_one).pack(pady=10)
# # #
# # #         tk.Button(self.leftFrame, text="Filter 2", width=18,
# # #                   command=self.filter_two).pack(pady=10)
# # #
# # #         tk.Button(self.leftFrame, text="Sepia", width=18,
# # #                   command=self.filter_sepia).pack(pady=10)
# # #
# # #         tk.Button(self.leftFrame, text="Crop Image", width=18,
# # #                   command=self.activate_crop_mode).pack(pady=10)
# # #
# # #         tk.Button(self.leftFrame, text="Save Image As", width=18,
# # #                   command=self.save_image).pack(pady=10)
# # #
# # #     # ---------------------------------------------------------
# # #     # PLACEHOLDER IMAGE
# # #     # ---------------------------------------------------------
# # #     def create_placeholder(self):
# # #         blank = Image.new("RGB", (500, 350), "white")
# # #         draw = ImageDraw.Draw(blank)
# # #
# # #         text = "Open an Image to Load"
# # #         try:
# # #             font = ImageFont.truetype("arial.ttf", 22)
# # #         except:
# # #             font = ImageFont.load_default()
# # #
# # #         left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
# # #         x = (500 - (right - left)) // 2
# # #         y = (350 - (bottom - top)) // 2
# # #         draw.text((x, y), text, fill="black", font=font)
# # #
# # #         self.update_display(blank)
# # #
# # #     # ---------------------------------------------------------
# # #     # IMAGE OPERATIONS
# # #     # ---------------------------------------------------------
# # #     def update_display(self, image):
# # #         self.display_img = ImageTk.PhotoImage(image)
# # #         self.picLabel.config(image=self.display_img)
# # #         self.picLabel.image = self.display_img  # prevent gc
# # #
# # #     def open_image(self):
# # #         path = filedialog.askopenfilename(
# # #             filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp *.gif")]
# # #         )
# # #         if not path:
# # #             return
# # #
# # #         self.img = Image.open(path).resize((500, 350), Image.LANCZOS)
# # #         self.update_display(self.img)
# # #
# # #     def save_image(self):
# # #         if self.img is None:
# # #             messagebox.showerror("Error", "No image to save.")
# # #             return
# # #
# # #         path = filedialog.asksaveasfilename(
# # #             defaultextension=".png",
# # #             filetypes=[
# # #                 ("PNG", "*.png"), ("JPEG", "*.jpg"),
# # #                 ("Bitmap", "*.bmp"), ("All Files", "*.*")
# # #             ]
# # #         )
# # #         if not path:
# # #             return
# # #
# # #         try:
# # #             self.img.save(path)
# # #             messagebox.showinfo("Saved", "Image saved successfully!")
# # #         except Exception as e:
# # #             messagebox.showerror("Error", str(e))
# # #
# # #     # ---------------------------------------------------------
# # #     # FILTERS
# # #     # ---------------------------------------------------------
# # #     def filter_one(self):
# # #         if self.img is None:
# # #             return self.no_image_error()
# # #
# # #         r, g, b = self.img.split()
# # #
# # #         r = r.rotate(3)
# # #         g = g.rotate(358)
# # #         b = b.filter(ImageFilter.GaussianBlur(30))
# # #
# # #         b = ImageEnhance.Brightness(b).enhance(1.5)
# # #
# # #         new_img = Image.merge("RGB", (r, g, b))
# # #         new_img = ImageEnhance.Brightness(new_img).enhance(1.5)
# # #
# # #         self.img = new_img
# # #         self.update_display(self.img)
# # #
# # #     def filter_two(self):
# # #         if self.img is None:
# # #             return self.no_image_error()
# # #
# # #         r, g, b = self.img.split()
# # #
# # #         r = ImageEnhance.Brightness(r.filter(ImageFilter.GaussianBlur(30))).enhance(0.8)
# # #         b = ImageEnhance.Color(b.filter(ImageFilter.EDGE_ENHANCE)).enhance(0.2)
# # #         g = ImageEnhance.Contrast(g).enhance(2.0)
# # #
# # #         self.img = Image.merge("RGB", (r, g, b))
# # #         self.update_display(self.img)
# # #
# # #     def filter_sepia(self):
# # #         if self.img is None:
# # #             return self.no_image_error()
# # #
# # #         sepia = self.img.convert("RGB")
# # #         width, height = sepia.size
# # #         pixels = sepia.load()
# # #
# # #         for py in range(height):
# # #             for px in range(width):
# # #                 r, g, b = pixels[px, py]
# # #
# # #                 tr = int(0.393*r + 0.769*g + 0.189*b)
# # #                 tg = int(0.349*r + 0.686*g + 0.168*b)
# # #                 tb = int(0.272*r + 0.534*g + 0.131*b)
# # #
# # #                 pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255))
# # #
# # #         self.img = sepia
# # #         self.update_display(self.img)
# # #
# # #     # ---------------------------------------------------------
# # #     # CROP FEATURES (USER DRAG SELECT)
# # #     # ---------------------------------------------------------
# # #     def activate_crop_mode(self):
# # #         if self.img is None:
# # #             return self.no_image_error()
# # #
# # #         messagebox.showinfo("Crop Mode", "Click and drag on the image to crop.")
# # #
# # #         self.picLabel.bind("<ButtonPress-1>", self.crop_start)
# # #         self.picLabel.bind("<B1-Motion>", self.crop_drag)
# # #         self.picLabel.bind("<ButtonRelease-1>", self.crop_end)
# # #
# # #     def crop_start(self, event):
# # #         self.crop_start_x = event.x
# # #         self.crop_start_y = event.y
# # #
# # #         if self.crop_rect:
# # #             self.picLabel.delete(self.crop_rect)
# # #
# # #     def crop_drag(self, event):
# # #         # Draw selection rectangle on label
# # #         x0, y0 = self.crop_start_x, self.crop_start_y
# # #         x1, y1 = event.x, event.y
# # #
# # #         # Using a Canvas for drawing would be ideal, but to keep your code simple,
# # #         # we won’t draw the rectangle visually. (I can add Canvas if you want.)
# # #         pass
# # #
# # #     def crop_end(self, event):
# # #         if self.img is None:
# # #             return
# # #
# # #         x0, y0 = self.crop_start_x, self.crop_start_y
# # #         x1, y1 = event.x, event.y
# # #
# # #         # Fix inverted dragging
# # #         left, top = min(x0, x1), min(y0, y1)
# # #         right, bottom = max(x0, x1), max(y0, y1)
# # #
# # #         if right - left < 5 or bottom - top < 5:
# # #             messagebox.showerror("Error", "Crop area too small.")
# # #             return
# # #
# # #         self.img = self.img.crop((left, top, right, bottom))
# # #         self.update_display(self.img)
# # #
# # #         # Disable crop mode after cropping
# # #         self.picLabel.unbind("<ButtonPress-1>")
# # #         self.picLabel.unbind("<B1-Motion>")
# # #         self.picLabel.unbind("<ButtonRelease-1>")
# # #
# # #     def no_image_error(self):
# # #         messagebox.showerror("Error", "Please open an image first.")
# # #
# # #
# # # # ---------------------------------------------------------
# # # # RUN APP
# # # # ---------------------------------------------------------
# # # if __name__ == "__main__":
# # #     root = tk.Tk()
# # #     app = ImageEditorApp(root)
# # #     root.mainloop()
# #
# #
# # import tkinter as tk
# # from tkinter import filedialog, messagebox
# # from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
# #
# #
# # class ImageEditorApp:
# #
# #     CANVAS_W = 500
# #     CANVAS_H = 350
# #
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Image Editor App")
# #         self.root.geometry("1000x600")
# #
# #         # Current PIL image (not a PhotoImage)
# #         self.img = None
# #
# #         # Canvas items / state
# #         self.canvas_image_id = None
# #         self.display_img = None            # PhotoImage reference for Tk
# #         self.rect_id = None                 # selection rectangle id
# #         self.crop_mode = False
# #
# #         # Drag start coords
# #         self.start_x = None
# #         self.start_y = None
# #
# #         self.build_ui()
# #         self.create_placeholder()
# #
# #     # -----------------------
# #     # UI
# #     # -----------------------
# #     def build_ui(self):
# #         # Left frame for buttons
# #         leftFrame = tk.Frame(self.root, width=200, bg="#e0e0e0")
# #         leftFrame.pack(side=tk.LEFT, fill=tk.Y)
# #
# #         # Right frame for picture + canvas
# #         rightFrame = tk.Frame(self.root, bg="black")
# #         rightFrame.pack(side=tk.RIGHT, fill="both", expand=True)
# #
# #         tk.Label(rightFrame, text="Picture", font=("Arial", 16), fg="white", bg="black").pack(pady=(30, 8))
# #
# #         # Canvas (we use canvas so we can draw selection rectangle)
# #         self.canvas = tk.Canvas(rightFrame, width=self.CANVAS_W, height=self.CANVAS_H, bg="white", highlightthickness=0)
# #         self.canvas.pack(expand=True)
# #
# #         # Buttons
# #         tk.Label(leftFrame, text="Options:", font=("Arial", 12), bg="#e0e0e0").pack(pady=18)
# #         tk.Button(leftFrame, text="Open Image", width=18, command=self.open_image).pack(pady=6)
# #         tk.Button(leftFrame, text="Filter 1", width=18, command=self.filter_one).pack(pady=6)
# #         tk.Button(leftFrame, text="Filter 2", width=18, command=self.filter_two).pack(pady=6)
# #         tk.Button(leftFrame, text="Sepia", width=18, command=self.filter_sepia).pack(pady=6)
# #         tk.Button(leftFrame, text="Crop Image", width=18, command=self.activate_crop_mode).pack(pady=6)
# #         tk.Button(leftFrame, text="Save Image As", width=18, command=self.save_image).pack(pady=6)
# #
# #     # -----------------------
# #     # Placeholder
# #     # -----------------------
# #     def create_placeholder(self):
# #         blank = Image.new("RGB", (self.CANVAS_W, self.CANVAS_H), "white")
# #         draw = ImageDraw.Draw(blank)
# #         text = "Open an Image to Load"
# #         try:
# #             font = ImageFont.truetype("arial.ttf", 20)
# #         except Exception:
# #             font = ImageFont.load_default()
# #         bbox = draw.textbbox((0, 0), text, font=font)
# #         text_w = bbox[2] - bbox[0]
# #         text_h = bbox[3] - bbox[1]
# #         draw.text(((self.CANVAS_W - text_w) // 2, (self.CANVAS_H - text_h) // 2), text, fill="black", font=font)
# #         self.set_image_on_canvas(blank)
# #
# #     # -----------------------
# #     # Display helpers
# #     # -----------------------
# #     def set_image_on_canvas(self, pil_image):
# #         """Put a PIL image on the canvas (adjusts canvas size to image)."""
# #         self.img = pil_image
# #         w, h = pil_image.size
# #         # resize canvas to fit image
# #         self.canvas.config(width=w, height=h)
# #         self.display_img = ImageTk.PhotoImage(pil_image)
# #         if self.canvas_image_id is None:
# #             # anchor top-left
# #             self.canvas_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.display_img)
# #         else:
# #             self.canvas.itemconfig(self.canvas_image_id, image=self.display_img)
# #         # remove any selection rect
# #         if self.rect_id:
# #             self.canvas.delete(self.rect_id)
# #             self.rect_id = None
# #
# #     # -----------------------
# #     # Open / Save
# #     # -----------------------
# #     def open_image(self):
# #         path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp *.gif")])
# #         if not path:
# #             return
# #         pil = Image.open(path).convert("RGB")
# #         # scale down (if large) to fit default canvas width while keeping aspect
# #         pil.thumbnail((self.CANVAS_W, self.CANVAS_H), Image.LANCZOS)
# #         # if smaller than canvas, keep its size; canvas will adjust
# #         self.set_image_on_canvas(pil)
# #
# #     def save_image(self):
# #         if self.img is None:
# #             messagebox.showerror("Error", "No image to save.")
# #             return
# #         path = filedialog.asksaveasfilename(defaultextension=".png",
# #                                             filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Bitmap", "*.bmp"), ("All Files", "*.*")])
# #         if not path:
# #             return
# #         try:
# #             self.img.save(path)
# #             messagebox.showinfo("Saved", "Image saved successfully!")
# #         except Exception as e:
# #             messagebox.showerror("Error", f"Unable to save file:\n{e}")
# #
# #     # -----------------------
# #     # Filters
# #     # -----------------------
# #     def filter_one(self):
# #         if not self._ensure_image(): return
# #         r, g, b = self.img.split()
# #         r = r.rotate(3)
# #         g = g.rotate(358)
# #         b = b.filter(ImageFilter.GaussianBlur(30))
# #         b = ImageEnhance.Brightness(b).enhance(1.5)
# #         new_img = Image.merge("RGB", (r, g, b))
# #         new_img = ImageEnhance.Brightness(new_img).enhance(1.5)
# #         self.set_image_on_canvas(new_img)
# #
# #     def filter_two(self):
# #         if not self._ensure_image(): return
# #         r, g, b = self.img.split()
# #         r = ImageEnhance.Brightness(r.filter(ImageFilter.GaussianBlur(30))).enhance(0.8)
# #         b = ImageEnhance.Color(b.filter(ImageFilter.EDGE_ENHANCE)).enhance(0.2)
# #         g = ImageEnhance.Contrast(g).enhance(2.0)
# #         new = Image.merge("RGB", (r, g, b))
# #         self.set_image_on_canvas(new)
# #
# #     def filter_sepia(self):
# #         if not self._ensure_image(): return
# #         sepia = self.img.copy()
# #         pixels = sepia.load()
# #         w, h = sepia.size
# #         for yy in range(h):
# #             for xx in range(w):
# #                 r, g, b = pixels[xx, yy]
# #                 tr = int(0.393*r + 0.769*g + 0.189*b)
# #                 tg = int(0.349*r + 0.686*g + 0.168*b)
# #                 tb = int(0.272*r + 0.534*g + 0.131*b)
# #                 pixels[xx, yy] = (min(tr,255), min(tg,255), min(tb,255))
# #         self.set_image_on_canvas(sepia)
# #
# #     # -----------------------
# #     # Crop (interactive)
# #     # -----------------------
# #     def activate_crop_mode(self):
# #         if not self._ensure_image(): return
# #         messagebox.showinfo("Crop", "Crop mode: click and drag to draw a rectangle, release to crop.")
# #         self.crop_mode = True
# #         # bind canvas events
# #         self.canvas.bind("<ButtonPress-1>", self._on_crop_start)
# #         self.canvas.bind("<B1-Motion>", self._on_crop_drag)
# #         self.canvas.bind("<ButtonRelease-1>", self._on_crop_end)
# #
# #     def _on_crop_start(self, event):
# #         if not self.crop_mode: return
# #         self.start_x = self.canvas.canvasx(event.x)
# #         self.start_y = self.canvas.canvasy(event.y)
# #         # remove previous rect
# #         if self.rect_id:
# #             self.canvas.delete(self.rect_id)
# #             self.rect_id = None
# #         # create new rect (invisible size initially)
# #         self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
# #                                                     outline="red", width=2, dash=(4,2))
# #
# #     def _on_crop_drag(self, event):
# #         if not self.crop_mode or self.rect_id is None: return
# #         cur_x = self.canvas.canvasx(event.x)
# #         cur_y = self.canvas.canvasy(event.y)
# #         # update rectangle coords
# #         self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)
# #
# #     def _on_crop_end(self, event):
# #         if not self.crop_mode or self.rect_id is None: return
# #         end_x = self.canvas.canvasx(event.x)
# #         end_y = self.canvas.canvasy(event.y)
# #
# #         x0 = int(min(self.start_x, end_x))
# #         y0 = int(min(self.start_y, end_y))
# #         x1 = int(max(self.start_x, end_x))
# #         y1 = int(max(self.start_y, end_y))
# #
# #         # check size
# #         if (x1 - x0) < 5 or (y1 - y0) < 5:
# #             messagebox.showerror("Crop", "Selection too small.")
# #             # clean up bindings and rectangle
# #             self._end_crop_mode()
# #             return
# #
# #         # clamp to image bounds
# #         img_w, img_h = self.img.size
# #         x0 = max(0, min(x0, img_w-1))
# #         x1 = max(1, min(x1, img_w))
# #         y0 = max(0, min(y0, img_h-1))
# #         y1 = max(1, min(y1, img_h))
# #
# #         # perform crop on the current image
# #         cropped = self.img.crop((x0, y0, x1, y1))
# #         # set canvas to the cropped image (canvas will resize)
# #         self.set_image_on_canvas(cropped)
# #
# #         # finish crop mode
# #         self._end_crop_mode()
# #
# #     def _end_crop_mode(self):
# #         # unbind events and clear rectangle
# #         try:
# #             self.canvas.unbind("<ButtonPress-1>")
# #             self.canvas.unbind("<B1-Motion>")
# #             self.canvas.unbind("<ButtonRelease-1>")
# #         except Exception:
# #             pass
# #         if self.rect_id:
# #             self.canvas.delete(self.rect_id)
# #             self.rect_id = None
# #         self.crop_mode = False
# #         self.start_x = self.start_y = None
# #
# #     # -----------------------
# #     # Utilities
# #     # -----------------------
# #     def _ensure_image(self):
# #         if self.img is None:
# #             messagebox.showerror("Error", "Please open an image first.")
# #             return False
# #         return True
# #
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = ImageEditorApp(root)
# #     root.mainloop()
#
#
# import tkinter as tk
# from tkinter import filedialog, messagebox
# from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
#
#
# class ImageEditorApp:
#
#     CANVAS_W = 500
#     CANVAS_H = 350
#
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Image Editor App")
#         self.root.geometry("1000x600")
#
#         # Master image (after user presses Apply)
#         self.img_original = None
#
#         # Temporary preview image (before apply)
#         self.img_preview = None
#
#         # Canvas state
#         self.canvas_image_id = None
#         self.display_img = None
#
#         # Cropping
#         self.crop_mode = False
#         self.rect_id = None
#         self.start_x = None
#         self.start_y = None
#
#         self.build_ui()
#         self.create_placeholder()
#
#     # ------------------------------------------------------------
#     # UI BUILD
#     # ------------------------------------------------------------
#     def build_ui(self):
#         leftFrame = tk.Frame(self.root, width=200, bg="#e0e0e0")
#         leftFrame.pack(side=tk.LEFT, fill=tk.Y)
#
#         rightFrame = tk.Frame(self.root, bg="black")
#         rightFrame.pack(side=tk.RIGHT, fill="both", expand=True)
#
#         tk.Label(rightFrame, text="Picture", font=("Arial", 16),
#                  fg="white", bg="black").pack(pady=(30, 8))
#
#         # Canvas
#         self.canvas = tk.Canvas(rightFrame, width=self.CANVAS_W,
#                                 height=self.CANVAS_H,
#                                 bg="white", highlightthickness=0)
#         self.canvas.pack(expand=True)
#
#         # Left Buttons
#         tk.Label(leftFrame, text="Options:", font=("Arial", 12),
#                  bg="#e0e0e0").pack(pady=18)
#
#         tk.Button(leftFrame, text="Open Image", width=18,
#                   command=self.open_image).pack(pady=6)
#
#         tk.Button(leftFrame, text="Filter 1", width=18,
#                   command=lambda: self.start_filter(self.filter_one)).pack(pady=6)
#
#         tk.Button(leftFrame, text="Filter 2", width=18,
#                   command=lambda: self.start_filter(self.filter_two)).pack(pady=6)
#
#         tk.Button(leftFrame, text="Sepia", width=18,
#                   command=lambda: self.start_filter(self.filter_sepia)).pack(pady=6)
#
#         tk.Button(leftFrame, text="Crop Image", width=18,
#                   command=self.start_crop_mode).pack(pady=6)
#
#         tk.Button(leftFrame, text="Save Image As", width=18,
#                   command=self.save_image).pack(pady=6)
#
#         # Apply / Cancel Buttons
#         self.apply_frame = tk.Frame(leftFrame, bg="#e0e0e0")
#         self.apply_btn = tk.Button(self.apply_frame, text="Apply",
#                                    width=8, command=self.apply_changes)
#         self.cancel_btn = tk.Button(self.apply_frame, text="Cancel",
#                                     width=8, command=self.cancel_changes)
#
#     # ------------------------------------------------------------
#     # CANVAS DISPLAY
#     # ------------------------------------------------------------
#     def show_image(self, pil_image):
#         """Show PIL image on canvas (scaled to 500x350 always)."""
#         img_scaled = pil_image.copy()
#         img_scaled = img_scaled.resize((self.CANVAS_W, self.CANVAS_H), Image.LANCZOS)
#
#         self.display_img = ImageTk.PhotoImage(img_scaled)
#
#         if self.canvas_image_id is None:
#             self.canvas_image_id = self.canvas.create_image(
#                 0, 0, anchor="nw", image=self.display_img)
#         else:
#             self.canvas.itemconfig(self.canvas_image_id, image=self.display_img)
#
#     # ------------------------------------------------------------
#     # PLACEHOLDER IMAGE
#     # ------------------------------------------------------------
#     def create_placeholder(self):
#         blank = Image.new("RGB", (self.CANVAS_W, self.CANVAS_H), "white")
#         draw = ImageDraw.Draw(blank)
#
#         text = "Open an Image to Load"
#         try:
#             font = ImageFont.truetype("arial.ttf", 22)
#         except:
#             font = ImageFont.load_default()
#
#         bbox = draw.textbbox((0, 0), text, font=font)
#         w = bbox[2] - bbox[0]
#         h = bbox[3] - bbox[1]
#
#         draw.text(((self.CANVAS_W - w) // 2, (self.CANVAS_H - h) // 2),
#                   text, fill="black", font=font)
#
#         self.img_original = blank
#         self.show_image(blank)
#
#     # ------------------------------------------------------------
#     # OPEN / SAVE
#     # ------------------------------------------------------------
#     def open_image(self):
#         path = filedialog.askopenfilename(
#             filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
#         )
#         if not path:
#             return
#
#         img = Image.open(path).convert("RGB")
#         self.img_original = img
#         self.img_preview = None
#         self.show_image(img)
#
#     def save_image(self):
#         if self.img_original is None:
#             messagebox.showerror("Error", "No image to save.")
#             return
#
#         path = filedialog.asksaveasfilename(
#             defaultextension=".png",
#             filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
#         )
#         if not path:
#             return
#
#         try:
#             self.img_original.save(path)
#             messagebox.showinfo("Saved", "Image saved successfully!")
#         except Exception as e:
#             messagebox.showerror("Error", str(e))
#
#     # ------------------------------------------------------------
#     # APPLY / CANCEL SYSTEM FOR ALL OPERATIONS
#     # ------------------------------------------------------------
#     def start_filter(self, filter_function):
#         """Show preview of filter, wait for Apply/Cancel."""
#         if self.img_original is None:
#             messagebox.showerror("Error", "Open an image first.")
#             return
#
#         self.img_preview = filter_function(self.img_original.copy())
#         self.show_image(self.img_preview)
#         self.show_apply_buttons()
#
#     def apply_changes(self):
#         """Commit preview to original image."""
#         if self.img_preview is not None:
#             self.img_original = self.img_preview
#         self.img_preview = None
#         self.hide_apply_buttons()
#         self.show_image(self.img_original)
#
#     def cancel_changes(self):
#         """Revert preview."""
#         self.img_preview = None
#         self.hide_apply_buttons()
#         self.show_image(self.img_original)
#
#     def show_apply_buttons(self):
#         self.apply_frame.pack(pady=20)
#         self.apply_btn.pack(side=tk.LEFT, padx=5)
#         self.cancel_btn.pack(side=tk.LEFT, padx=5)
#
#     def hide_apply_buttons(self):
#         self.apply_frame.pack_forget()
#
#     # ------------------------------------------------------------
#     # FILTERS
#     # ------------------------------------------------------------
#     def filter_one(self, img):
#         r, g, b = img.split()
#         r = r.rotate(3)
#         g = g.rotate(358)
#         b = ImageEnhance.Brightness(b.filter(ImageFilter.GaussianBlur(30))).enhance(1.5)
#         img2 = Image.merge("RGB", (r, g, b))
#         img2 = ImageEnhance.Brightness(img2).enhance(1.5)
#         return img2
#
#     def filter_two(self, img):
#         r, g, b = img.split()
#         r = ImageEnhance.Brightness(r.filter(ImageFilter.GaussianBlur(30))).enhance(0.8)
#         b = ImageEnhance.Color(b.filter(ImageFilter.EDGE_ENHANCE)).enhance(0.2)
#         g = ImageEnhance.Contrast(g).enhance(2.0)
#         return Image.merge("RGB", (r, g, b))
#
#     def filter_sepia(self, img):
#         px = img.load()
#         w, h = img.size
#         for y in range(h):
#             for x in range(w):
#                 r, g, b = px[x, y]
#                 tr = int(0.393*r + 0.769*g + 0.189*b)
#                 tg = int(0.349*r + 0.686*g + 0.168*b)
#                 tb = int(0.272*r + 0.534*g + 0.131*b)
#                 px[x, y] = (min(tr,255), min(tg,255), min(tb,255))
#         return img
#
#     # ------------------------------------------------------------
#     # CROP MODE
#     # ------------------------------------------------------------
#     def start_crop_mode(self):
#         if self.img_original is None:
#             messagebox.showerror("Error", "Open an image first.")
#             return
#
#         self.crop_mode = True
#         messagebox.showinfo("Crop Mode", "Click and drag to select area. Release to preview crop.")
#
#         self.canvas.bind("<ButtonPress-1>", self.crop_start)
#         self.canvas.bind("<B1-Motion>", self.crop_drag)
#         self.canvas.bind("<ButtonRelease-1>", self.crop_end)
#
#     def crop_start(self, event):
#         if not self.crop_mode:
#             return
#
#         self.start_x = event.x
#         self.start_y = event.y
#
#         if self.rect_id:
#             self.canvas.delete(self.rect_id)
#
#         self.rect_id = self.canvas.create_rectangle(
#             self.start_x, self.start_y, self.start_x, self.start_y,
#             outline="red", width=2, dash=(4, 2)
#         )
#
#     def crop_drag(self, event):
#         if not self.crop_mode or not self.rect_id:
#             return
#
#         self.canvas.coords(self.rect_id,
#                            self.start_x, self.start_y, event.x, event.y)
#
#     def crop_end(self, event):
#         if not self.crop_mode:
#             return
#
#         x0, y0 = min(self.start_x, event.x), min(self.start_y, event.y)
#         x1, y1 = max(self.start_x, event.x), max(self.start_y, event.y)
#
#         if (x1 - x0) < 5 or (y1 - y0) < 5:
#             messagebox.showerror("Error", "Selection too small.")
#             self.end_crop_mode()
#             return
#
#         # convert canvas selection to source image coords
#         src = self.img_original
#         sx = int(x0 / self.CANVAS_W * src.width)
#         sy = int(y0 / self.CANVAS_H * src.height)
#         ex = int(x1 / self.CANVAS_W * src.width)
#         ey = int(y1 / self.CANVAS_H * src.height)
#
#         cropped = src.crop((sx, sy, ex, ey))
#
#         # RESIZE back to 500×350
#         cropped_resized = cropped.resize((self.CANVAS_W, self.CANVAS_H),
#                                          Image.LANCZOS)
#
#         self.img_preview = cropped_resized
#         self.show_image(self.img_preview)
#
#         self.end_crop_mode()
#         self.show_apply_buttons()
#
#     def end_crop_mode(self):
#         self.crop_mode = False
#         if self.rect_id:
#             self.canvas.delete(self.rect_id)
#         self.rect_id = None
#
#         self.canvas.unbind("<ButtonPress-1>")
#         self.canvas.unbind("<B1-Motion>")
#         self.canvas.unbind("<ButtonRelease-1>")
#
#
# # ------------------------------------------------------------
# # MAIN
# # ------------------------------------------------------------
# if __name__ == "__main__":
#     root = tk.Tk()
#     ImageEditorApp(root)
#     root.mainloop()
