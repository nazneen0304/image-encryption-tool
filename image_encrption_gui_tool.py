"""
IMAGE ENCRYPTION TOOL — GUI Version
====================================
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import hashlib
from PIL import Image, ImageTk
import numpy as np


def password_to_key(password):
    return hashlib.sha256(password.encode()).digest()[0]

def password_to_seed(password):
    return int.from_bytes(hashlib.sha256(password.encode()).digest()[:4], 'big')

def swap_red_and_blue(grid):
    result = grid.copy()
    result[:, :, 0] = grid[:, :, 2]
    result[:, :, 2] = grid[:, :, 0]
    return result

def scatter_pixels(grid, seed):
    flat = grid.reshape(-1, grid.shape[2])
    rng  = np.random.default_rng(seed)
    idx  = np.arange(len(flat))
    rng.shuffle(idx)
    return flat[idx].reshape(grid.shape)

def restore_pixels(grid, seed):
    flat = grid.reshape(-1, grid.shape[2])
    rng  = np.random.default_rng(seed)
    idx  = np.arange(len(flat))
    rng.shuffle(idx)
    rev  = np.empty_like(idx)
    rev[idx] = np.arange(len(idx))
    return flat[rev].reshape(grid.shape)

def xor_pixels(grid, key):
    return grid ^ key

def encrypt_image(input_path, output_path, password):
    img  = Image.open(input_path).convert("RGB")
    grid = np.array(img, dtype=np.uint8)
    key  = password_to_key(password)
    seed = password_to_seed(password)
    grid = swap_red_and_blue(grid)
    grid = scatter_pixels(grid, seed)
    grid = xor_pixels(grid, key)
    Image.fromarray(grid).save(output_path)

def decrypt_image(input_path, output_path, password):
    img  = Image.open(input_path).convert("RGB")
    grid = np.array(img, dtype=np.uint8)
    key  = password_to_key(password)
    seed = password_to_seed(password)
    grid = xor_pixels(grid, key)
    grid = restore_pixels(grid, seed)
    grid = swap_red_and_blue(grid)
    Image.fromarray(grid).save(output_path)


# ──────────────────────────────────────────────
#  THE GUI APP
# ──────────────────────────────────────────────

class ImageEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Image Encryption Tool")
        self.root.geometry("620x780")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f1a")

        # State
        self.selected_file = tk.StringVar(value="")
        self.password_var  = tk.StringVar()
        self.mode          = tk.StringVar(value="encrypt")
        self.output_path   = None

        self._build_ui()

    # ── Build the entire UI ──────────────────
    def _build_ui(self):
        BG       = "#0f0f1a"
        CARD     = "#1a1a2e"
        ACCENT   = "#7c3aed"       # purple
        ACCENT2  = "#06b6d4"       # cyan
        SUCCESS  = "#10b981"
        TEXT     = "#e2e8f0"
        SUBTEXT  = "#94a3b8"
        BORDER   = "#2d2d44"

        # ── Header ──────────────────────────
        header = tk.Frame(self.root, bg="#16213e", pady=20)
        header.pack(fill="x")

        tk.Label(header, text="🔐", font=("Segoe UI Emoji", 32),
                 bg="#16213e", fg=TEXT).pack()
        tk.Label(header, text="Image Encryption Tool",
                 font=("Segoe UI", 18, "bold"),
                 bg="#16213e", fg=TEXT).pack()
        tk.Label(header, text="SkillCraft Technology  •  Task 02",
                 font=("Segoe UI", 9),
                 bg="#16213e", fg=SUBTEXT).pack(pady=(2, 0))

        # ── Main content area ────────────────
        content = tk.Frame(self.root, bg=BG, padx=30)
        content.pack(fill="both", expand=True, pady=10)

        # ── Mode selector ────────────────────
        self._section_label(content, "STEP 1 — Choose what to do", TEXT, BG)

        mode_frame = tk.Frame(content, bg=BG)
        mode_frame.pack(fill="x", pady=(0, 16))

        self.btn_encrypt = self._mode_button(
            mode_frame, "🔒  Encrypt", "encrypt", ACCENT, BG, TEXT)
        self.btn_decrypt = self._mode_button(
            mode_frame, "🔓  Decrypt", "decrypt", BORDER, BG, SUBTEXT)

        self.btn_encrypt.pack(side="left", padx=(0, 8), expand=True, fill="x")
        self.btn_decrypt.pack(side="left", expand=True, fill="x")

        # ── File picker ──────────────────────
        self._section_label(content, "STEP 2 — Pick your image", TEXT, BG)

        file_box = tk.Frame(content, bg=CARD, bd=0,
                            highlightthickness=1,
                            highlightbackground=BORDER)
        file_box.pack(fill="x", pady=(0, 16))

        self.file_label = tk.Label(
            file_box,
            text="No image selected yet — click the button below",
            font=("Segoe UI", 9), bg=CARD, fg=SUBTEXT,
            wraplength=480, justify="left", padx=14, pady=12)
        self.file_label.pack(fill="x")

        tk.Button(
            content,
            text="📂  Browse for Image",
            font=("Segoe UI", 10, "bold"),
            bg=CARD, fg=TEXT,
            activebackground=BORDER,
            activeforeground=TEXT,
            bd=0, pady=10, cursor="hand2",
            command=self._pick_file
        ).pack(fill="x", pady=(0, 16))

        # ── Image preview ────────────────────
        self._section_label(content, "PREVIEW", TEXT, BG)

        self.preview_frame = tk.Frame(
            content, bg=CARD, width=560, height=160,
            highlightthickness=1, highlightbackground=BORDER)
        self.preview_frame.pack(fill="x", pady=(0, 16))
        self.preview_frame.pack_propagate(False)

        self.preview_label = tk.Label(
            self.preview_frame,
            text="Your selected image will appear here",
            font=("Segoe UI", 9), bg=CARD, fg=SUBTEXT)
        self.preview_label.pack(expand=True)

        # ── Password ─────────────────────────
        self._section_label(content, "STEP 3 — Enter your password", TEXT, BG)

        pw_frame = tk.Frame(content, bg=CARD,
                            highlightthickness=1,
                            highlightbackground=BORDER)
        pw_frame.pack(fill="x", pady=(0, 6))

        self.pw_entry = tk.Entry(
            pw_frame,
            textvariable=self.password_var,
            font=("Segoe UI", 12),
            bg=CARD, fg=TEXT,
            insertbackground=TEXT,
            bd=0, show="•",
            highlightthickness=0)
        self.pw_entry.pack(fill="x", padx=14, pady=12)

        tk.Label(
            content,
            text="⚠️  Remember this password — you need the SAME one to decrypt!",
            font=("Segoe UI", 8), bg=BG,
            fg="#f59e0b", justify="left"
        ).pack(anchor="w", pady=(0, 16))

        # ── Go button ────────────────────────
        self.go_btn = tk.Button(
            content,
            text="🔒  Encrypt Image",
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT, fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            bd=0, pady=14, cursor="hand2",
            command=self._run
        )
        self.go_btn.pack(fill="x", pady=(0, 12))

        # ── Status bar ───────────────────────
        self.status_var = tk.StringVar(value="Ready — pick an image to begin!")
        self.status_label = tk.Label(
            content,
            textvariable=self.status_var,
            font=("Segoe UI", 9), bg=BG, fg=SUBTEXT,
            wraplength=540, justify="center")
        self.status_label.pack()

        # ── Progress bar ─────────────────────
        style = ttk.Style()
        style.theme_use("default")
        style.configure("custom.Horizontal.TProgressbar",
                        troughcolor=CARD,
                        background=ACCENT,
                        thickness=6)
        self.progress = ttk.Progressbar(
            content, style="custom.Horizontal.TProgressbar",
            mode="indeterminate", length=560)
        self.progress.pack(fill="x", pady=(8, 0))

        # Store colors for mode switching
        self._colors = {
            "BG": BG, "CARD": CARD, "ACCENT": ACCENT,
            "ACCENT2": ACCENT2, "SUCCESS": SUCCESS,
            "TEXT": TEXT, "SUBTEXT": SUBTEXT, "BORDER": BORDER
        }

    def _section_label(self, parent, text, fg, bg):
        tk.Label(parent, text=text,
                 font=("Segoe UI", 8, "bold"),
                 bg=bg, fg=fg,
                 anchor="w").pack(fill="x", pady=(8, 4))

    def _mode_button(self, parent, text, value, bg, frame_bg, fg):
        btn = tk.Button(
            parent, text=text,
            font=("Segoe UI", 10, "bold"),
            bg=bg, fg=fg, bd=0,
            pady=10, cursor="hand2",
            command=lambda: self._set_mode(value)
        )
        return btn

    # ── Mode switching ───────────────────────
    def _set_mode(self, value):
        c = self._colors
        self.mode.set(value)
        if value == "encrypt":
            self.btn_encrypt.config(bg=c["ACCENT"], fg="white")
            self.btn_decrypt.config(bg=c["BORDER"], fg=c["SUBTEXT"])
            self.go_btn.config(text="🔒  Encrypt Image", bg=c["ACCENT"])
        else:
            self.btn_decrypt.config(bg=c["ACCENT2"], fg="white")
            self.btn_encrypt.config(bg=c["BORDER"], fg=c["SUBTEXT"])
            self.go_btn.config(text="🔓  Decrypt Image", bg=c["ACCENT2"])

        self.status_var.set("Ready — pick an image to begin!")
        self.selected_file.set("")
        self.file_label.config(
            text="No image selected yet — click the button below")
        self._clear_preview()

    # ── File picker ─────────────────────────
    def _pick_file(self):
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp"),
                ("All files", "*.*")
            ]
        )
        if path:
            self.selected_file.set(path)
            name = os.path.basename(path)
            size = os.path.getsize(path)
            self.file_label.config(
                text=f"📄 {name}   ({size:,} bytes)\n📁 {path}",
                fg=self._colors["TEXT"])
            self._show_preview(path)
            self.status_var.set("Image selected! Enter your password and click the button.")

    def _show_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((520, 140))
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo   # prevent garbage collection
        except Exception:
            self.preview_label.config(text="(preview not available)")

    def _clear_preview(self):
        self.preview_label.config(
            image="",
            text="Your selected image will appear here")
        self.preview_label.image = None

    # ── Run encrypt/decrypt ──────────────────
    def _run(self):
        path     = self.selected_file.get()
        password = self.password_var.get().strip()
        mode     = self.mode.get()

        # Validate
        if not path:
            messagebox.showwarning("No image", "Please select an image first!")
            return
        if not password:
            messagebox.showwarning("No password", "Please enter a password!")
            return

        # Ask where to save
        default_name = ("encrypted.png"
                        if mode == "encrypt" else "decrypted.png")
        out_path = filedialog.asksaveasfilename(
            title="Save output as...",
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")]
        )
        if not out_path:
            return

        self.output_path = out_path

        # Run in background thread so UI doesn't freeze
        self.go_btn.config(state="disabled")
        self.progress.start(10)
        self.status_var.set(
            f"{'Encrypting' if mode == 'encrypt' else 'Decrypting'}... please wait ⏳")

        thread = threading.Thread(
            target=self._worker,
            args=(path, out_path, password, mode),
            daemon=True
        )
        thread.start()

    def _worker(self, input_path, output_path, password, mode):
        """Runs in background — does the actual work."""
        try:
            if mode == "encrypt":
                encrypt_image(input_path, output_path, password)
            else:
                decrypt_image(input_path, output_path, password)

            # Back on main thread → show success
            self.root.after(0, self._on_success, output_path, mode)

        except Exception as e:
            self.root.after(0, self._on_error, str(e))

    def _on_success(self, output_path, mode):
        self.progress.stop()
        self.progress["value"] = 100
        self.go_btn.config(state="normal")

        emoji = "🔒" if mode == "encrypt" else "🔓"
        name  = os.path.basename(output_path)
        verb  = "Encrypted" if mode == "encrypt" else "Decrypted"

        self.status_var.set(f"✅  {verb} successfully! Saved as: {name}")
        self.status_label.config(fg=self._colors["SUCCESS"])

        messagebox.showinfo(
            f"{verb} Successfully! 🎉",
            f"✅ Your image has been {verb.lower()}!\n\n"
            f"Saved to:\n{output_path}\n\n"
            + ("🔑 Keep your password safe — you'll need it to decrypt!"
               if mode == "encrypt"
               else "🖼️ Open the file to see your restored image!")
        )

    def _on_error(self, error_msg):
        self.progress.stop()
        self.go_btn.config(state="normal")
        self.status_var.set("❌ Something went wrong.")
        self.status_label.config(fg="#ef4444")
        messagebox.showerror("Error", f"Something went wrong:\n\n{error_msg}")


# ──────────────────────────────────────────────
#  LAUNCH THE APP
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = ImageEncryptionApp(root)
    root.mainloop()