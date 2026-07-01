# ============================================================
#   IMAGE ENCRYPTION TOOL
# ============================================================

from PIL import Image
import numpy as np
import hashlib
import os


# ── Password → numbers ──────────────────────────────────────
def password_to_key(password):
    return hashlib.sha256(password.encode()).digest()[0]

def password_to_seed(password):
    return int.from_bytes(hashlib.sha256(password.encode()).digest()[:4], 'big')


# ── METHOD 1: Pixel Manipulation (swap + shuffle) ───────────
def pixel_encrypt(grid, seed):
    # Swap Red and Blue channels
    result = grid.copy()
    result[:, :, 0] = grid[:, :, 2]
    result[:, :, 2] = grid[:, :, 0]
    # Shuffle pixel positions
    flat = result.reshape(-1, result.shape[2])
    rng  = np.random.default_rng(seed)
    idx  = np.arange(len(flat))
    rng.shuffle(idx)
    return flat[idx].reshape(grid.shape)

def pixel_decrypt(grid, seed):
    # Unshuffle pixel positions
    flat = grid.reshape(-1, grid.shape[2])
    rng  = np.random.default_rng(seed)
    idx  = np.arange(len(flat))
    rng.shuffle(idx)
    rev  = np.empty_like(idx)
    rev[idx] = np.arange(len(idx))
    result = flat[rev].reshape(grid.shape)
    # Swap Red and Blue back
    final = result.copy()
    final[:, :, 0] = result[:, :, 2]
    final[:, :, 2] = result[:, :, 0]
    return final


# ── METHOD 2: Basic Math Operation (XOR) ────────────────────
def math_encrypt(grid, key):
    # XOR every pixel value with the key number
    # Example: pixel 200 XOR key 158 = 102 (scrambled)
    return grid ^ key

def math_decrypt(grid, key):
    # XOR again with same key = original back
    # Example: 102 XOR 158 = 200 (original!)
    return grid ^ key


# ── MAIN PROGRAM ─────────────────────────────────────────────
def main():
    print("=" * 50)
    print("   IMAGE ENCRYPTION TOOL")
    print("   SkillCraft Technology — Task 02")
    print("=" * 50)

    # ── Ask for image path ───────────────────
    print("\nEnter the path of your image.")
    print("Example: photo.jpg  or  C:/Users/You/Desktop/photo.png")
    image_path = input("\nImage path: ").strip().strip('"')

    if not os.path.exists(image_path):
        print(f"\nCannot find that file: {image_path}")
        print("Make sure the path is correct and try again.")
        return

    # ── Ask encrypt or decrypt ───────────────
    print("\nWhat do you want to do?")
    print("  1 → Encrypt  (lock the image)")
    print("  2 → Decrypt  (unlock the image)")
    action = input("\nEnter 1 or 2: ").strip()

    if action not in ["1", "2"]:
        print("Invalid choice. Please enter 1 or 2.")
        return

    # ── Ask which method ─────────────────────
    print("\nChoose encryption method:")
    print("  1 → Pixel Manipulation  (swaps colors + shuffles pixels)")
    print("  2 → Basic Math / XOR    (scrambles pixel numbers with math)")
    method = input("\nEnter 1 or 2: ").strip()

    if method not in ["1", "2"]:
        print("Invalid choice. Please enter 1 or 2.")
        return

    # ── Ask for password ─────────────────────
    password = input("\nEnter your secret password: ").strip()
    if not password:
        print("Password cannot be empty!")
        return

    # ── Ask for output file name ─────────────
    if action == "1":
        default_out = "encrypted.png"
    else:
        default_out = "decrypted.png"

    print(f"\nWhat should the output file be named?")
    out_name = input(f"Press Enter to use '{default_out}', or type a name: ").strip()
    if not out_name:
        out_name = default_out
    if not out_name.endswith(".png"):
        out_name += ".png"

    # ── Load image ───────────────────────────
    print("\nLoading image...")
    img  = Image.open(image_path).convert("RGB")
    grid = np.array(img, dtype=np.uint8)
    print(f"Image size: {img.width} x {img.height} pixels")

    key  = password_to_key(password)
    seed = password_to_seed(password)

    # ── Do the work ──────────────────────────
    if action == "1":
        print("\nEncrypting your image...")
        if method == "1":
            print("Method: Pixel Manipulation (color swap + pixel shuffle)")
            result = pixel_encrypt(grid, seed)
        else:
            print("Method: Basic Math / XOR")
            result = math_encrypt(grid, key)
        verb = "Encrypted"

    else:
        print("\nDecrypting your image...")
        if method == "1":
            print("Method: Pixel Manipulation (reversing shuffle + color swap)")
            result = pixel_decrypt(grid, seed)
        else:
            print("Method: Basic Math / XOR")
            result = math_decrypt(grid, key)
        verb = "Decrypted"

    # ── Save output ──────────────────────────
    Image.fromarray(result).save(out_name)

    print(f"\n✅ {verb} successfully!")
    print(f"   Output saved as: {out_name}")
    print(f"   Location: {os.path.abspath(out_name)}")

    if action == "1":
        print("\n   Remember your password to decrypt later!")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()