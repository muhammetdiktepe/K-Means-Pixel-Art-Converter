import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # BURASI DUZELTILDI (ImageT -> ImageTk)
import numpy as np
from sklearn.cluster import KMeans
import os

# --- Dil Ayarları / Language Settings ---
TEXTS = {
    "tr": {
        "title": "Piksel Sanata Çevirici",
        "btn_load": "Resim Yükle",
        "btn_process": "İşle (Küçült > Kümele > Büyüt)",
        "btn_save": "Kaydet",
        "lbl_k": "Renk Sayısı (K):",
        "lbl_scale": "Küçültme Oranı (1/x):",
        "status_wait": "Resim bekleniyor...",
        "status_ready": "Hazır. İşle'ye basınız.",
        "status_proc": "İşleniyor, lütfen bekleyin...",
        "status_done": "Tamamlandı!",
        "err_no_img": "Lütfen önce bir resim yükleyin!",
        "lang_switch": "Switch to English"
    },
    "en": {
        "title": "Pixel Art Converter",
        "btn_load": "Load Image",
        "btn_process": "Process (Shrink > Cluster > Enlarge)",
        "btn_save": "Save Result",
        "lbl_k": "Color Count (K):",
        "lbl_scale": "Downscale Ratio (1/x):",
        "status_wait": "Waiting for image...",
        "status_ready": "Ready. Press Process.",
        "status_proc": "Processing, please wait...",
        "status_done": "Done!",
        "err_no_img": "Please load an image first!",
        "lang_switch": "Türkçe'ye Geç"
    }
}

class KMeansApp:
    def __init__(self, root):
        self.root = root
        self.lang = "tr"  # Varsayılan dil / Default language
        self.original_image = None
        self.processed_image = None
        self.file_path = None

        self.setup_ui()
        self.update_texts()

    def setup_ui(self):
        # Ana Ayarlar / Main Config
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Kontrol Paneli (Sol Taraf) / Control Panel (Left)
        control_frame = tk.Frame(self.root, width=250, bg="#ddd", padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Dil Butonu / Language Button
        self.btn_lang = tk.Button(control_frame, command=self.toggle_language, bg="#555", fg="white")
        self.btn_lang.pack(fill=tk.X, pady=(0, 20))

        # Yükle Butonu / Load Button
        self.btn_load = tk.Button(control_frame, command=self.load_image, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.btn_load.pack(fill=tk.X, pady=5)

        # Ayarlar / Settings
        self.lbl_k = tk.Label(control_frame, bg="#ddd", anchor="w")
        self.lbl_k.pack(fill=tk.X, pady=(20, 0))
        
        self.slider_k = tk.Scale(control_frame, from_=2, to=32, orient=tk.HORIZONTAL, bg="#ddd")
        self.slider_k.set(8)
        self.slider_k.pack(fill=tk.X)

        self.lbl_scale = tk.Label(control_frame, bg="#ddd", anchor="w")
        self.lbl_scale.pack(fill=tk.X, pady=(20, 0))
        
        # 1 means original size, 10 means 1/10th size
        self.slider_scale = tk.Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL, bg="#ddd")
        self.slider_scale.set(4)
        self.slider_scale.pack(fill=tk.X)

        # İşle Butonu / Process Button
        self.btn_process = tk.Button(control_frame, command=self.process_image, bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        self.btn_process.pack(fill=tk.X, pady=20)

        # Kaydet Butonu / Save Button
        self.btn_save = tk.Button(control_frame, command=self.save_image, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_save.pack(fill=tk.X, pady=5)

        # Durum Çubuğu / Status Bar
        self.lbl_status = tk.Label(control_frame, text="...", fg="gray", bg="#ddd", wraplength=200)
        self.lbl_status.pack(side=tk.BOTTOM, pady=20)

        # Resim Alanı (Sağ Taraf) / Image Area (Right)
        self.canvas_frame = tk.Frame(self.root, bg="#333")
        self.canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        
        self.canvas_label = tk.Label(self.canvas_frame, bg="#333", text="No Image")
        self.canvas_label.pack(expand=True)

    def update_texts(self):
        # Arayüz metinlerini seçili dile göre güncelle
        t = TEXTS[self.lang]
        self.root.title(t["title"])
        self.btn_lang.config(text=t["lang_switch"])
        self.btn_load.config(text=t["btn_load"])
        self.btn_process.config(text=t["btn_process"])
        self.btn_save.config(text=t["btn_save"])
        self.lbl_k.config(text=t["lbl_k"])
        self.lbl_scale.config(text=t["lbl_scale"])
        
        # Durum metnini sadece bekliyorsa güncelle
        if self.original_image is None:
            self.lbl_status.config(text=t["status_wait"])

    def toggle_language(self):
        self.lang = "en" if self.lang == "tr" else "tr"
        self.update_texts()

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not path:
            return

        self.file_path = path
        img = Image.open(path)
        img = img.convert("RGB") # Her zaman RGB'ye çevir
        self.original_image = img
        
        self.display_image(img)
        self.lbl_status.config(text=TEXTS[self.lang]["status_ready"])

    def display_image(self, img_pil):
        # Resmi ekrana sığacak şekilde ölçekle (görüntüleme için)
        display_width = self.canvas_frame.winfo_width()
        display_height = self.canvas_frame.winfo_height()
        
        # Pencere daha yüklenmediyse varsayılan değer al
        if display_width < 10: display_width = 700
        if display_height < 10: display_height = 600

        img_copy = img_pil.copy()
        img_copy.thumbnail((display_width, display_height))
        
        self.tk_image = ImageTk.PhotoImage(img_copy)
        self.canvas_label.config(image=self.tk_image, text="")

    def process_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", TEXTS[self.lang]["err_no_img"])
            return

        self.lbl_status.config(text=TEXTS[self.lang]["status_proc"])
        self.root.update() # Arayüzün donmasını engelle

        # 1. Parametreleri Al
        k = self.slider_k.get()
        scale = self.slider_scale.get()

        # 2. Resmi Küçült (Downscale)
        w, h = self.original_image.size
        small_w, small_h = max(1, w // scale), max(1, h // scale)
        
        # Image.BILINEAR küçültürken yumuşatır, daha iyi renk ortalaması verir
        # Modern PIL sürümleri için Resampling.BILINEAR kontrolü
        try:
            resample_method = Image.Resampling.BILINEAR
        except AttributeError:
            resample_method = Image.BILINEAR

        small_img = self.original_image.resize((small_w, small_h), resample_method)

        # 3. K-Means Uygula
        img_np = np.array(small_img)
        pixels = img_np.reshape((-1, 3))

        kmeans = KMeans(n_clusters=k, random_state=42, n_init=5)
        kmeans.fit(pixels)

        centers = np.uint8(kmeans.cluster_centers_)
        labels = kmeans.labels_

        # 4. Resmi Yeniden Oluştur
        segmented_data = centers[labels]
        segmented_img_np = segmented_data.reshape((small_h, small_w, 3))
        segmented_img_pil = Image.fromarray(segmented_img_np)

        # 5. Resmi Tekrar Büyüt (Upscale) - NEAREST çok önemli!
        try:
            resample_nearest = Image.Resampling.NEAREST
        except AttributeError:
            resample_nearest = Image.NEAREST

        final_img = segmented_img_pil.resize((w, h), resample_nearest)

        self.processed_image = final_img
        self.display_image(final_img)
        self.lbl_status.config(text=TEXTS[self.lang]["status_done"])

    def save_image(self):
        if self.processed_image is None:
            return
            
        save_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                 filetypes=[("PNG file", "*.png"), ("JPG file", "*.jpg")])
        if save_path:
            self.processed_image.save(save_path)
            messagebox.showinfo("Info", "Saved / Kaydedildi: " + os.path.basename(save_path))

if __name__ == "__main__":
    root = tk.Tk()
    app = KMeansApp(root)
    root.mainloop()