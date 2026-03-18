"""
=============================================================
  STEGANOGRAPHY ENCODER - For Educational / Lab Use Only
  File: encoder.py
  How to run: python3 encoder.py
=============================================================
  What this does:
  - Takes a normal image (cover image)
  - Hides a secret text message inside it
  - Uses LSB (Least Significant Bit) technique
  - Output image looks EXACTLY the same as original
  - But secretly contains your hidden message inside!

  HOW LSB WORKS (Simple Explanation):
  Every pixel has 3 color values: Red, Green, Blue
  Each value is a number like 200 = 11001000 in binary
  We only change the LAST bit: 11001000 → 11001001
  This changes color from 200 to 201 — human eye CANNOT see this!
  But the hidden bit is now stored inside the pixel!
=============================================================
"""

from PIL import Image
import os
import sys

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────
END_MARKER = "###END###"   # Secret marker so decoder knows where message ends


def text_to_binary(text):
    """
    Converts each character in text to 8-bit binary.
    
    Example:
    'H' → ASCII 72 → binary '01001000'
    'i' → ASCII 105 → binary '01101001'
    'Hi' → '0100100001101001'
    """
    binary = ""
    for char in text:
        # ord() gets ASCII number, format(n, '08b') converts to 8-bit binary
        binary += format(ord(char), '08b')
    return binary


def binary_to_text(binary):
    """
    Converts binary string back to readable text.
    Opposite of text_to_binary().
    
    Every 8 bits = 1 character
    '01001000' → 72 → 'H'
    """
    text = ""
    # Process 8 bits at a time
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            # int(byte, 2) converts binary to decimal
            # chr() converts decimal to character
            text += chr(int(byte, 2))
    return text


def get_image_capacity(image_path):
    """
    Calculates how many characters can be hidden in an image.
    
    Formula:
    Each pixel has 3 channels (R, G, B)
    Each channel can hide 1 bit
    So each pixel hides 3 bits
    8 bits = 1 character
    Max characters = (total pixels × 3) ÷ 8
    """
    img = Image.open(image_path)
    width, height = img.size
    total_pixels = width * height
    max_bits = total_pixels * 3
    max_chars = max_bits // 8
    return max_chars, width, height, total_pixels


def encode(image_path, secret_message, output_path):
    """
    MAIN ENCODING FUNCTION
    
    Steps:
    1. Open the cover image
    2. Add end marker to message so decoder knows where to stop
    3. Convert message to binary bits
    4. Replace LSB of each pixel channel with one message bit
    5. Save the new image (stego image)
    """

    # ── Step 1: Open image ──
    print(f"\n[+] Opening cover image: {image_path}")
    img = Image.open(image_path)

    # Convert to RGB (in case it's RGBA or grayscale)
    img = img.convert('RGB')
    width, height = img.size
    print(f"[+] Image size: {width} x {height} pixels")

    # ── Step 2: Check capacity ──
    max_chars, _, _, total_pixels = get_image_capacity(image_path)
    full_message = secret_message + END_MARKER
    print(f"[+] Message length: {len(secret_message)} characters")
    print(f"[+] Image capacity: {max_chars} characters maximum")

    if len(full_message) > max_chars:
        print(f"\n[!] ERROR: Message too long!")
        print(f"[!] Message needs {len(full_message)} chars but image only holds {max_chars}")
        print(f"[!] Use a larger image or shorter message.")
        sys.exit(1)

    # ── Step 3: Convert message to binary ──
    print(f"[+] Converting message to binary bits...")
    binary_message = text_to_binary(full_message)
    total_bits = len(binary_message)
    print(f"[+] Total bits to hide: {total_bits}")

    # ── Step 4: Hide bits in pixels ──
    print(f"[+] Hiding message in pixels using LSB technique...")

    # Get all pixels as a flat list
    pixels = list(list(img.getdata()))
    new_pixels = []
    bit_index = 0   # Which bit of the message we're currently hiding

    for pixel in pixels:
        r, g, b = pixel

        # Hide one bit in RED channel
        if bit_index < total_bits:
            # (r & ~1) clears the last bit to 0
            # | int(binary_message[bit_index]) sets it to 0 or 1
            r = (r & ~1) | int(binary_message[bit_index])
            bit_index += 1

        # Hide one bit in GREEN channel
        if bit_index < total_bits:
            g = (g & ~1) | int(binary_message[bit_index])
            bit_index += 1

        # Hide one bit in BLUE channel
        if bit_index < total_bits:
            b = (b & ~1) | int(binary_message[bit_index])
            bit_index += 1

        new_pixels.append((r, g, b))

    # ── Step 5: Save stego image ──
    print(f"[+] Saving stego image to: {output_path}")
    img.putdata(new_pixels)
    img.save(output_path, 'PNG')   # Always save as PNG — JPEG compression destroys hidden bits!

    # ── Summary ──
    print(f"\n{'='*55}")
    print(f"  ✅ ENCODING SUCCESSFUL!")
    print(f"{'='*55}")
    print(f"  Cover image   : {image_path}")
    print(f"  Stego image   : {output_path}")
    print(f"  Message length: {len(secret_message)} characters")
    print(f"  Bits used     : {total_bits} out of {total_pixels * 3} available")
    print(f"  Pixels changed: ~{total_bits // 3} out of {total_pixels}")
    print(f"  Visibility    : ZERO — images look identical to human eye")
    print(f"{'='*55}")


def main():
    print("=" * 55)
    print("  STEGANOGRAPHY ENCODER")
    print("  LSB (Least Significant Bit) Method")
    print("  Educational use only — Lab project")
    print("=" * 55)

    # ── Get cover image path ──
    print("\n[?] Enter the path to your cover image")
    print("    (must be a PNG or JPG file — e.g. cover.png)")
    image_path = input("    Image path: ").strip()

    if not os.path.exists(image_path):
        print(f"\n[!] ERROR: File not found: {image_path}")
        print("[!] Make sure the image file is in the same folder")
        print("[!] or give the full path like /home/kali/Desktop/image.png")
        sys.exit(1)

    # ── Get secret message ──
    print("\n[?] Enter your secret message to hide:")
    secret_message = input("    Message: ").strip()

    if not secret_message:
        print("[!] ERROR: Message cannot be empty!")
        sys.exit(1)

    # ── Get output path ──
    print("\n[?] Enter output filename for stego image")
    print("    (MUST be .png — e.g. stego_output.png)")
    output_path = input("    Output path [default: stego_output.png]: ").strip()
    if not output_path:
        output_path = "stego_output.png"

    # Make sure output is PNG
    if not output_path.endswith('.png'):
        output_path += '.png'

    # ── Run encoder ──
    encode(image_path, secret_message, output_path)


if __name__ == "__main__":
    main()
