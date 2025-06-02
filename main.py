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


    def on_reset():
        """Reset semua field input dan output"""
        if messagebox.askyesno("Konfirmasi Reset", "Apakah Anda yakin ingin menghapus semua isi?"):
            input_text.delete("1.0", tk.END)
            key_entry.delete(0, tk.END)
            output_text.delete("1.0", tk.END)
            messagebox.showinfo("Reset", "Semua field telah direset!")

    # Window utama
    root = tk.Tk()
    root.title("🔐 Vigenère Cipher Tool")
    root.geometry("750x650")

    # Header dengan informasi
    header_frame = ttk.Frame(root)
    header_frame.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(header_frame, text="🔐 VIGENÈRE CIPHER TOOL", 
              font=("Arial", 12, "bold")).pack()
    ttk.Label(header_frame, text="Tool untuk enkripsi, dekripsi, dan analisis cipher Vigenère", 
              font=("Arial", 9)).pack()

    # Input section
    ttk.Label(root, text="📝 Teks Masukan (Plaintext / Ciphertext):").pack(anchor="w", padx=10, pady=(10, 0))
    input_text = scrolledtext.ScrolledText(root, height=8, wrap=tk.WORD)
    input_text.pack(fill="x", padx=10)

    ttk.Label(root, text="🔑 Kunci:").pack(anchor="w", padx=10, pady=(10, 0))
    key_entry = ttk.Entry(root, font=("Arial", 11))
    key_entry.pack(fill="x", padx=10)

    # Button section
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=15)

    ttk.Button(button_frame, text="🔐 Enkripsi", command=on_encrypt, width=12).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="🔓 Dekripsi", command=on_decrypt, width=12).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="🗑 Reset", command=on_reset, width=12).grid(row=0, column=3, padx=5)


    # Output section
    output_frame = ttk.Frame(root)
    output_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))
    
    ttk.Label(output_frame, text="📋 Hasil Output:").pack(anchor="w")
    output_text = scrolledtext.ScrolledText(output_frame, height=12, wrap=tk.WORD, font=("Consolas", 10))
    output_text.pack(fill="both", expand=True, pady=(0, 10))


    root.mainloop()

# ✅ Inisialisasi program
if __name__ == "__main__":
    print("🚀 Menjalankan Vigenère Ciphe& Kasiski Tool...")
    print("📌 Fitur yang tersedia:")
    print("   • Enkripsi dan Dekripsi Vigenère")
    print("   • Reset semua field")
    run_gui()
