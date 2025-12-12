# 🎨 K-Means Pixel Art Converter

![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**K-Means Pixel Art Converter** is a desktop application that transforms high-resolution images into retro-style "Pixel Art" using Machine Learning. 

It utilizes the **K-Means Clustering** algorithm to determine the dominant color palette of an image and applies intelligent downscaling/upscaling techniques to create a pixelated aesthetic.

## 📸 Screenshot
https://github.com/user-attachments/assets/9ce4067c-729f-4c9c-a2e1-81b6c020628c


## ✨ Features

* **AI-Powered Color Quantization:** Uses `scikit-learn` K-Means to reduce millions of colors to a specific palette size ($K$).
* **Dynamic Pixelation:** Adjustable downscaling ratio to control the "blockiness" of the pixel art.
* **Dual Language Support:** Switch between **English** and **Turkish** interfaces instantly.
* **Real-time Processing:** Fast image processing using `NumPy` vectorization.
* **Save Functionality:** Export your pixel art creations as PNG or JPG.
* **User-Friendly GUI:** Built with `Tkinter` for easy interaction.

## 🛠️ Tech Stack

* **Python 3.10+**
* **Scikit-Learn** (Machine Learning / Clustering)
* **OpenCV & Pillow** (Image Processing)
* **NumPy** (Matrix Operations)
* **Tkinter** (Graphical User Interface)

## 🚀 Installation & Usage

1.  **Clone the repository:**
    ```bash
   https://github.com/muhammetdiktepe/K-Means-Pixel-Art-Converter.git
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python PixelArtConverter.py
    ```

## 🎮 How to Use

1.  Click **"Load Image"** to upload a photo.
2.  Adjust the **Color Count (K)** slider to set the palette size (e.g., 8 colors, 16 colors).
3.  Adjust the **Downscale Ratio** to determine the pixel size.
4.  Click **"Process"** to see the magic!
5.  If you like the result, click **"Save Result"**.

## 📦 Download (Executable)

Don't want to deal with code? You can download the ready-to-use `.exe` file from the **[Releases](../../releases)** section.

---

### 👨‍💻 Author

**Muhammet Diktepe**

* **GitHub:** https://github.com/muhammetdiktepe
* **LinkedIn:** https://www.linkedin.com/in/muhammet-diktepe-08a48839b/

---
*This project was developed as an assignment for [University/Course Name] to demonstrate the application of K-Means clustering in image processing.*
