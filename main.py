import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
from collections import Counter

# --- Fungsi Kriptografi ---
def encrypt_vigenere(plaintext, key):
    ciphertext = ''
    key = key.upper()
    key_len = len(key)
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % key_len]) - ord('A')
            ciphertext += chr((ord(char) - offset + shift) % 26 + offset)
            key_index += 1
        else:
            ciphertext += char
    return ciphertext

def decrypt_vigenere(ciphertext, key):
    plaintext = ''
    key = key.upper()
    key_len = len(key)
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % key_len]) - ord('A')
            plaintext += chr((ord(char) - offset - shift) % 26 + offset)
            key_index += 1
        else:
            plaintext += char
    return plaintext

def find_factors(n):
    return [i for i in range(2, 21) if n % i == 0]

def kasiski_examination(ciphertext):
    text = re.sub('[^A-Z]', '', ciphertext.upper())
    trigrams = {}

    for i in range(len(text) - 3):
        trigram = text[i:i+3]
        if trigram in trigrams:
            trigrams[trigram].append(i)
        else:
            trigrams[trigram] = [i]

    distances = []
    for positions in trigrams.values():
        if len(positions) > 1:
            for i in range(len(positions)-1):
                distances.append(positions[i+1] - positions[i])

    if not distances:
        return "Tidak ditemukan trigram berulang."

    factor_counts = Counter()
    for d in distances:
        for f in find_factors(d):
            factor_counts[f] += 1

    result = "Faktor-faktor paling mungkin sebagai panjang kunci:\n"
    for factor, count in factor_counts.most_common():
        result += f"- Panjang: {factor}, Jumlah: {count}\n"
    return result

# --- UI Tkinter ---
def run_gui():
    def on_encrypt():
        text = input_text.get("1.0", tk.END).strip()
        key = key_entry.get().strip()
        if not text or not key:
            messagebox.showwarning("Input Error", "Isi teks dan kunci terlebih dahulu!")
            return
        result = encrypt_vigenere(text, key)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    def on_decrypt():
        text = input_text.get("1.0", tk.END).strip()
        key = key_entry.get().strip()
        if not text or not key:
            messagebox.showwarning("Input Error", "Isi teks dan kunci terlebih dahulu!")
            return
        result = decrypt_vigenere(text, key)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    def on_kasiski():
        text = input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Isi ciphertext terlebih dahulu!")
            return
        result = kasiski_examination(text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    # Window utama
    root = tk.Tk()
    root.title("🔐 Vigenère Cipher & Kasiski Tool")
    root.geometry("700x600")

    ttk.Label(root, text="Teks Masukan (Plaintext / Ciphertext):").pack(anchor="w", padx=10, pady=(10, 0))
    input_text = scrolledtext.ScrolledText(root, height=8, wrap=tk.WORD)
    input_text.pack(fill="x", padx=10)

    ttk.Label(root, text="Kunci:").pack(anchor="w", padx=10, pady=(10, 0))
    key_entry = ttk.Entry(root)
    key_entry.pack(fill="x", padx=10)

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="🔐 Enkripsi", command=on_encrypt).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="🔓 Dekripsi", command=on_decrypt).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="🔍 Kasiski", command=on_kasiski).grid(row=0, column=2, padx=5)

    ttk.Label(root, text="Hasil Output:").pack(anchor="w", padx=10)
    output_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
    output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    root.mainloop()

# ✅ Inisialisasi program
if __name__ == "__main__":
    print("Menjalankan GUI...")
    run_gui()
