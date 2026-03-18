"""
=============================================================
  STEGANOGRAPHY DECODER - For Educational / Lab Use Only
  File: decoder.py
  How to run: python3 decoder.py
=============================================================
  What this does:
  - Takes a stego image (image with hidden message)
  - Extracts the LSB (last bit) from each pixel channel
  - Rebuilds the binary string
  - Converts binary back to readable text
  - Shows you the hidden secret message!
=============================================================
"""

from PIL import Image
import os
import sys

# Must match the END_MARKER used in encoder.py
END_MARKER = "###END###"


def extract_lsb_bits(image_path):
    """
    Extracts the Least Significant Bit from every
    R, G, B channel of every pixel in the image.
    
    This is the reverse of what encoder.py did.
    We read the last bit of each color value and
    collect them all into one long binary string.
    """
    print(f"[+] Opening stego image: {image_path}")
    img = Image.open(image_path)
    img = img.convert('RGB')

    width, height = img.size
    print(f"[+] Image size: {width} x {height} pixels")
    print(f"[+] Extracting LSBs from all pixels...")

    pixels = list(list(img.getdata()))
    binary_string = ""

    for pixel in pixels:
        r, g, b = pixel
        # Extract last bit using & 1 (bitwise AND with 1)
        # Example: 11001011 & 00000001 = 00000001 = 1
        # Example: 11001010 & 00000001 = 00000000 = 0
        binary_string += str(r & 1)
        binary_string += str(g & 1)
        binary_string += str(b & 1)

    print(f"[+] Extracted {len(binary_string)} bits total")
    return binary_string


def binary_to_text(binary):
    """
    Converts binary string to readable text, stopping
    at the END_MARKER so we don't read garbage data.
    """
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        text += char
        # Stop as soon as we find the end marker
        if text.endswith(END_MARKER):
            # Remove the end marker from output
            return text[:-len(END_MARKER)], True
    return text, False


def decode(image_path):
    """
    MAIN DECODING FUNCTION
    
    Steps:
    1. Open the stego image
    2. Extract LSB from every pixel channel
    3. Build binary string from all LSBs
    4. Convert binary to text
    5. Stop at END_MARKER
    6. Display the secret message
    """

    # ── Step 1 & 2: Extract all LSBs ──
    binary_string = extract_lsb_bits(image_path)

    # ── Step 3 & 4: Convert to text ──
    print(f"[+] Converting bits back to text...")
    message, found_end = binary_to_text(binary_string)

    # ── Step 5: Show result ──
    print(f"\n{'='*55}")
    if found_end:
        print(f"  ✅ HIDDEN MESSAGE FOUND!")
        print(f"{'='*55}")
        print(f"\n  SECRET MESSAGE:")
        print(f"  ┌─────────────────────────────────────────┐")
        # Print message with nice formatting
        words = message.split('\n')
        for line in words:
            print(f"  │  {line}")
        print(f"  └─────────────────────────────────────────┘")
        print(f"\n  Message length : {len(message)} characters")
        print(f"  Status         : Successfully decoded ✅")
    else:
        print(f"  ❌ NO HIDDEN MESSAGE FOUND")
        print(f"{'='*55}")
        print(f"  This image does not appear to contain a")
        print(f"  hidden message encoded with this tool.")
        print(f"  Make sure you are using the correct stego image.")
    print(f"{'='*55}")

    return message if found_end else None


def main():
    print("=" * 55)
    print("  STEGANOGRAPHY DECODER")
    print("  LSB (Least Significant Bit) Method")
    print("  Educational use only — Lab project")
    print("=" * 55)

    # ── Get stego image path ──
    print("\n[?] Enter path to the stego image")
    print("    (the image that has the hidden message)")
    image_path = input("    Image path: ").strip()

    if not os.path.exists(image_path):
        print(f"\n[!] ERROR: File not found: {image_path}")
        print("[!] Make sure the stego image file exists")
        sys.exit(1)

    # ── Run decoder ──
    decode(image_path)


if __name__ == "__main__":
    main()
