"""
=============================================================
  STEGANOGRAPHY DETECTOR - For Educational / Lab Use Only
  File: steg_detector.py
  How to run: python3 steg_detector.py
=============================================================
  What this does:
  - Analyzes an image statistically
  - Checks if the LSBs (last bits) look suspicious
  - Natural images have NON-RANDOM LSB patterns
  - Stego images have VERY RANDOM LSBs (close to 50/50)
  - Uses 3 detection methods:
      1. LSB Randomness Analysis
      2. Pixel Pair Analysis (RS Analysis)
      3. Chi-Square Statistical Test
  - Gives a final verdict: CLEAN or STEGO DETECTED
=============================================================
"""

from PIL import Image
import os
import sys
import math
import numpy as np

# ──────────────────────────────────────────────
# DETECTION METHOD 1: LSB Randomness
# ──────────────────────────────────────────────

def lsb_randomness_analysis(pixels):
    """
    THEORY:
    In a natural photo, pixel values follow natural patterns.
    The LSBs are NOT perfectly random — they lean toward 0 or 1
    depending on the image content.
    
    In a stego image using LSB technique:
    We forcefully set LSBs to 0 or 1 based on the message.
    This makes them very close to 50% zeros and 50% ones.
    
    So: if LSB ratio is between 0.45 and 0.55 → suspicious!
    Natural images are usually outside this range.
    
    Returns:
    - ratio: fraction of LSBs that are 1
    - is_suspicious: True if ratio is in the suspicious range
    """
    lsb_ones = 0
    total_bits = 0

    for pixel in pixels:
        r, g, b = pixel
        lsb_ones += (r & 1) + (g & 1) + (b & 1)
        total_bits += 3

    ratio = lsb_ones / total_bits
    # Natural images: ratio is usually < 0.42 or > 0.58
    # Stego images: ratio is suspiciously close to 0.5
    is_suspicious = 0.45 <= ratio <= 0.55

    return ratio, is_suspicious


# ──────────────────────────────────────────────
# DETECTION METHOD 2: Pixel Value Distribution
# ──────────────────────────────────────────────

def pixel_distribution_analysis(pixels):
    """
    THEORY:
    In natural images, consecutive even and odd pixel values
    appear in roughly natural proportions following image gradients.
    
    LSB steganography changes some even values to odd (or vice versa)
    which disrupts this natural distribution.
    
    We count even vs odd pixel values.
    If they're suspiciously equal (close to 50/50) → stego likely.
    
    Returns:
    - even_ratio: fraction of pixel values that are even numbers
    - is_suspicious: True if distribution looks tampered
    """
    even_count = 0
    total_values = 0

    for pixel in pixels:
        for channel_val in pixel:
            if channel_val % 2 == 0:
                even_count += 1
            total_values += 1

    even_ratio = even_count / total_values
    # Natural images usually don't have exactly 50% even values
    is_suspicious = 0.47 <= even_ratio <= 0.53

    return even_ratio, is_suspicious


# ──────────────────────────────────────────────
# DETECTION METHOD 3: Chi-Square Test
# ──────────────────────────────────────────────

def chi_square_analysis(pixels):
    """
    THEORY:
    Chi-Square test is a statistical test that measures how much
    an observed distribution differs from expected distribution.
    
    For LSB steganography:
    - Pairs of values (0,1), (2,3), (4,5)... should appear equally
      in stego images because LSB flipping toggles between pairs.
    - In natural images, these pairs are NOT equal.
    
    A high chi-square value = natural image
    A low chi-square value = stego image (pairs are too equal)
    
    Returns:
    - chi_score: the chi-square statistic
    - is_suspicious: True if score suggests hidden data
    """
    # Count frequency of each pixel value (0-255) in red channel only
    freq = [0] * 256
    for pixel in pixels:
        r = pixel[0]
        freq[r] += 1

    # Chi-square calculation on value pairs
    chi_score = 0
    pair_count = 0

    for i in range(0, 256, 2):
        observed_even = freq[i]
        observed_odd  = freq[i + 1] if i + 1 < 256 else 0
        expected = (observed_even + observed_odd) / 2

        if expected > 0:
            # Chi-square formula: (observed - expected)^2 / expected
            chi_score += ((observed_even - expected) ** 2) / expected
            chi_score += ((observed_odd  - expected) ** 2) / expected
            pair_count += 1

    # Normalize by number of pairs
    if pair_count > 0:
        chi_score = chi_score / pair_count

    # Low chi-score means pairs are very equal = stego likely
    is_suspicious = chi_score < 1.5

    return chi_score, is_suspicious


# ──────────────────────────────────────────────
# MAIN ANALYSIS FUNCTION
# ──────────────────────────────────────────────

def analyze_image(image_path):
    """
    Runs all 3 detection methods and combines results
    into a final verdict with confidence score.
    """

    print(f"\n[+] Loading image: {image_path}")
    img = Image.open(image_path)
    img = img.convert('RGB')

    width, height = img.size
    total_pixels = width * height
    print(f"[+] Image dimensions : {width} x {height}")
    print(f"[+] Total pixels     : {total_pixels:,}")
    print(f"[+] Running detection tests...\n")

    pixels = list(list(img.getdata()))

    # ── Run all 3 tests ──
    lsb_ratio,   lsb_suspicious   = lsb_randomness_analysis(pixels)
    even_ratio,  dist_suspicious  = pixel_distribution_analysis(pixels)
    chi_score,   chi_suspicious   = chi_square_analysis(pixels)

    # ── Calculate confidence score ──
    # Each suspicious test adds points
    suspicion_score = 0
    if lsb_suspicious:  suspicion_score += 1
    if dist_suspicious: suspicion_score += 1
    if chi_suspicious:  suspicion_score += 1

    # ── Print detailed results ──
    print("=" * 60)
    print("  DETECTION ANALYSIS RESULTS")
    print("=" * 60)

    # Test 1
    lsb_status = "⚠️  SUSPICIOUS" if lsb_suspicious else "✅ CLEAN"
    print(f"\n  TEST 1: LSB Randomness Analysis")
    print(f"  {'─'*50}")
    print(f"  LSB ratio (1s vs total): {lsb_ratio:.4f}")
    print(f"  Expected natural range : < 0.45 or > 0.55")
    print(f"  Measured value         : {lsb_ratio:.4f}")
    print(f"  Result                 : {lsb_status}")
    if lsb_suspicious:
        print(f"  Reason: LSB ratio {lsb_ratio:.3f} is suspiciously close to 0.5")
        print(f"          indicating forcefully randomized bits")

    # Test 2
    dist_status = "⚠️  SUSPICIOUS" if dist_suspicious else "✅ CLEAN"
    print(f"\n  TEST 2: Pixel Value Distribution Analysis")
    print(f"  {'─'*50}")
    print(f"  Even pixel value ratio : {even_ratio:.4f}")
    print(f"  Expected natural range : outside 0.47–0.53")
    print(f"  Measured value         : {even_ratio:.4f}")
    print(f"  Result                 : {dist_status}")
    if dist_suspicious:
        print(f"  Reason: Even/odd pixel ratio is too balanced,")
        print(f"          suggesting LSB modification")

    # Test 3
    chi_status = "⚠️  SUSPICIOUS" if chi_suspicious else "✅ CLEAN"
    print(f"\n  TEST 3: Chi-Square Statistical Test")
    print(f"  {'─'*50}")
    print(f"  Chi-square score       : {chi_score:.4f}")
    print(f"  Expected stego range   : < 1.5")
    print(f"  Measured score         : {chi_score:.4f}")
    print(f"  Result                 : {chi_status}")
    if chi_suspicious:
        print(f"  Reason: Low chi-square means value pairs are too")
        print(f"          equal — hallmark of LSB steganography")

    # ── Final verdict ──
    print(f"\n{'='*60}")
    print(f"  FINAL VERDICT")
    print(f"{'='*60}")
    print(f"  Tests flagged : {suspicion_score} out of 3")

    if suspicion_score == 3:
        verdict = "🚨 STEGO DETECTED — HIGH CONFIDENCE"
        detail  = "All 3 tests flagged this image. Almost certainly\n  contains hidden steganographic data."
    elif suspicion_score == 2:
        verdict = "⚠️  STEGO LIKELY — MEDIUM CONFIDENCE"
        detail  = "2 out of 3 tests flagged this image.\n  Likely contains hidden data."
    elif suspicion_score == 1:
        verdict = "❓ INCONCLUSIVE — LOW SUSPICION"
        detail  = "Only 1 test flagged. Could be natural image\n  variation or very short hidden message."
    else:
        verdict = "✅ CLEAN IMAGE — NO HIDDEN DATA DETECTED"
        detail  = "All tests passed. No steganographic data found."

    print(f"\n  {verdict}")
    print(f"  {detail}")
    print(f"\n{'='*60}\n")

    return suspicion_score


def compare_images(original_path, stego_path):
    """
    BONUS ANALYSIS:
    Compares original image vs stego image side by side.
    Shows exactly how many pixels were changed and by how much.
    This is perfect for your lab report!
    """
    print(f"\n{'='*60}")
    print(f"  IMAGE COMPARISON ANALYSIS")
    print(f"{'='*60}")
    print(f"  Original : {original_path}")
    print(f"  Stego    : {stego_path}")

    img1 = Image.open(original_path).convert('RGB')
    img2 = Image.open(stego_path).convert('RGB')

    pixels1 = list(img1.getdata())
    pixels2 = list(img2.getdata())

    if len(pixels1) != len(pixels2):
        print("[!] Images have different sizes — cannot compare")
        return

    changed_pixels = 0
    total_diff = 0
    max_diff = 0

    for p1, p2 in zip(pixels1, pixels2):
        diff = sum(abs(a - b) for a, b in zip(p1, p2))
        if diff > 0:
            changed_pixels += 1
            total_diff += diff
            max_diff = max(max_diff, diff)

    total = len(pixels1)
    pct = (changed_pixels / total) * 100
    avg_diff = total_diff / changed_pixels if changed_pixels > 0 else 0

    print(f"\n  Total pixels          : {total:,}")
    print(f"  Changed pixels        : {changed_pixels:,} ({pct:.2f}%)")
    print(f"  Unchanged pixels      : {total - changed_pixels:,}")
    print(f"  Average change per px : {avg_diff:.3f} (out of 765 max)")
    print(f"  Maximum change        : {max_diff} (out of 765 max)")
    print(f"\n  Conclusion: Only {pct:.2f}% of pixels were modified,")
    print(f"  each by at most {max_diff} color units — completely invisible!")
    print(f"{'='*60}\n")


def main():
    print("=" * 60)
    print("  STEGANOGRAPHY DETECTOR")
    print("  Statistical LSB Analysis")
    print("  Educational use only — Lab project")
    print("=" * 60)

    print("\nChoose analysis mode:")
    print("  1. Analyze single image (detect if stego)")
    print("  2. Compare original vs stego image (show differences)")
    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        image_path = input("\n[?] Enter image path to analyze: ").strip()
        if not os.path.exists(image_path):
            print(f"[!] File not found: {image_path}")
            sys.exit(1)
        analyze_image(image_path)

    elif choice == "2":
        original = input("\n[?] Enter ORIGINAL image path: ").strip()
        stego    = input("[?] Enter STEGO image path   : ").strip()
        if not os.path.exists(original) or not os.path.exists(stego):
            print("[!] One or both files not found!")
            sys.exit(1)
        # First analyze both individually
        print(f"\n── Analyzing ORIGINAL image ──")
        analyze_image(original)
        print(f"\n── Analyzing STEGO image ──")
        analyze_image(stego)
        # Then compare them
        compare_images(original, stego)
    else:
        print("[!] Invalid choice")
        sys.exit(1)


if __name__ == "__main__":
    main()
