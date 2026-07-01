# 🔐 Image Encryption Tool

---

## 📌 What is this project?

This is a Python-based Image Encryption Tool that encrypts and decrypts images using **pixel-level manipulation**. Instead of encrypting files like normal software, this tool goes deeper — it directly manipulates the numbers that make up each pixel of the image.

Built as part of the **SkillCraft Technology Internship Program — Task 02**.

---

## 🧠 How does it work?

Every image is just a giant grid of numbers.
Each pixel has 3 values — **Red, Green, Blue** (each between 0 and 255).

```
Normal pixel  →  Red: 200,  Green: 150,  Blue: 50
After encrypt →  Red: 102,  Green: 88,   Blue: 179  (looks random!)
After decrypt →  Red: 200,  Green: 150,  Blue: 50   (back to original!)
```

We offer **2 methods** to scramble those numbers:

---

## ⚙️ Encryption Methods

### Method 1 — Pixel Manipulation
```
Step 1 → Swap Red and Blue color channels
          (warm colors become cold, image looks wrong)

Step 2 → Shuffle all pixel positions randomly
          (like cutting a photo into pieces and scattering them)

Result → Image looks like colorful noise
Reverse → Unshuffle + swap back = perfect original
```

### Method 2 — Basic Math / XOR Operation
```
XOR is a math operation that is perfectly reversible:

  Pixel value : 200
  Key (from password) : 158
  200 XOR 158 = 102   ← encrypted!
  102 XOR 158 = 200   ← decrypted back!

Same key, same operation = always gives original back.
```

---

## 📁 Project Structure

```
image-encryption-tool/
│
├── encrypt_tool.py     ← MAIN FILE — run this!
├── README.md           ← This file
└── requirements.txt    ← Libraries needed
```

---

## ⚙️ Setup & Installation

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/image-encryption-tool.git
cd image-encryption-tool
```

### Step 2 — Install dependencies
```bash
pip install Pillow numpy
```

### Step 3 — Run the tool
```bash
python encrypt_tool.py
```

---

## 🚀 How to Use

Just run the file and answer the questions:

```
====================================================
   IMAGE ENCRYPTION TOOL
   SkillCraft Technology — Task 02
====================================================

Enter the path of your image.
Image path: /home/user/Pictures/photo.jpg

What do you want to do?
  1 → Encrypt  (lock the image)
  2 → Decrypt  (unlock the image)
Enter 1 or 2: 1

Choose encryption method:
  1 → Pixel Manipulation  (swaps colors + shuffles pixels)
  2 → Basic Math / XOR    (scrambles pixel numbers with math)
Enter 1 or 2: 1

Enter your secret password: mypassword123

✅ Encrypted successfully!
   Output saved as: encrypted.png
```

---

## 🔁 To Decrypt

Run the tool again with the **same password**:

```
Image path: encrypted.png
1 or 2: 2  (Decrypt)
Method: 1  (same method you used to encrypt)
Password: mypassword123

✅ Decrypted successfully!
   Output saved as: decrypted.png
```

⚠️ **Wrong password = scrambled garbage. Same password = perfect original!**

---

## 🖼️ Supported Image Formats

| Format | Supported |
|--------|-----------|
| .jpg / .jpeg | ✅ |
| .png | ✅ |
| .bmp | ✅ |
| .webp | ✅ |

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3 | Core programming language |
| Pillow (PIL) | Opening and saving images |
| NumPy | Fast pixel-level number operations |
| hashlib (SHA-256) | Converting password into a numeric key |
| os | Checking file paths |

---

## ✅ Task Requirements Covered

| Requirement | Status |
|-------------|--------|
| Pixel manipulation | ✅ Done (color swap + shuffle) |
| Swapping pixel values | ✅ Done (Red ↔ Blue channels) |
| Basic mathematical operation | ✅ Done (XOR cipher) |
| Encrypt images | ✅ Done |
| Decrypt images | ✅ Done |

---

## 👤 Author

**mahammad nazneen**
GitHub: nazneen0304
LinkedIn: Nazneen M

---

## 📄 License

MIT License — Free to use, modify and share.
