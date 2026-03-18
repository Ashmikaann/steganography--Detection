# 🖼️ Steganography Encoder & Detector Lab

> Academic Lab Project | Ethical Hacking & Cybersecurity  
> Tested on Kali Linux inside VirtualBox  
> For educational purposes only

---

## 📌 Topic
Steganography Encoder and Detector using LSB (Least Significant Bit) technique

---

## 📁 Files

| File | Purpose |
|---|---|
| `encoder.py` | Hides secret message inside an image |
| `decoder.py` | Extracts hidden message from stego image |
| `steg_detector.py` | Detects hidden data using statistical analysis |
| `requirements.txt` | Required Python libraries |

---

## 💡 How LSB Works

Every pixel has RGB values stored in binary.  
We change only the **last bit** of each channel:
```
Original Red:  11001010 = 202
After hiding:  11001011 = 203  ← difference of just 1!
```
This is completely invisible to the human eye.

---

## ⚙️ Installation
```bash
pip3 install Pillow --break-system-packages
```

---

## ▶️ How to Run

### Step 1 — Encode (hide message)
```bash
python3 encoder.py
```
```
Image path:   images.jpeg
Message:      hello am ashmika
Output:       stego_output.png
```

### Step 2 — Decode (extract message)
```bash
python3 decoder.py
```

### Step 3 — Detect steganography
```bash
python3 steg_detector.py
```
Choose option **2** to compare original vs stego image.

---

## 🔍 Detection Methods

| Test | Natural Image | Stego Image |
|---|---|---|
| LSB Randomness | < 0.45 or > 0.55 | ≈ 0.50 |
| Pixel Pair Analysis | Imbalanced | Balanced |
| Chi-Square Test | Score > 3.0 | Score < 1.5 |

---

## 📊 Lab Results

| Metric | Value |
|---|---|
| Image size | 168 × 299 pixels |
| Message hidden | "hello am ashmika" |
| Pixels modified | 59 out of 50,232 (0.12%) |
| Max color change | 3 units out of 765 |
| Visually detectable | ❌ No — completely invisible |
| Statistically detected | ✅ Yes — 2/3 tests flagged |

---

## 📚 References

- MDPI 2023 — Image Steganography Using LSB and Hybrid Encryption
- Nature 2025 — Novel Digital Image Steganography Using LSB
- PMC 2024 — Image Steganography Techniques for Resisting Steganalysis

---

## ⚠️ Disclaimer

This project is strictly for **educational and academic purposes only**.  
Tested only on the developer's own machine inside a Virtual Machine.

---

*Built with Python 🐍 | Kali Linux 🐉 | Academic Use Only 📚*
```
