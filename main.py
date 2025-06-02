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
    """
    Kasiski Examination: Metode kriptanalisis untuk menentukan panjang kunci Vigenère
    
    Cara kerja:
    1. Mencari trigram (3 huruf) yang berulang dalam ciphertext
    2. Menghitung jarak antara kemunculan trigram yang sama
    3. Mencari faktor persekutuan dari jarak-jarak tersebut
    4. Faktor yang paling sering muncul kemungkinan adalah panjang kunci
    
    Prinsip: Jika trigram yang sama muncul di posisi berbeda, kemungkinan
    mereka dienkripsi dengan bagian kunci yang sama (karena pola berulang kunci)
    """
    text = re.sub('[^A-Z]', '', ciphertext.upper())
    trigrams = {}
    trigram_details = []

    # Mencari semua trigram dan posisinya
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in trigrams:
            trigrams[trigram].append(i)
        else:
            trigrams[trigram] = [i]

    # Menghitung jarak antar trigram yang sama
    distances = []
    for trigram, positions in trigrams.items():
        if len(positions) > 1:
            trigram_distances = []
            for i in range(len(positions)-1):
                distance = positions[i+1] - positions[i]
                distances.append(distance)
                trigram_distances.append(distance)
            
            if trigram_distances:
                trigram_details.append({
                    'trigram': trigram,
                    'positions': positions,
                    'distances': trigram_distances
                })

    if not distances:
        return "❌ Tidak ditemukan trigram berulang.\nCoba dengan ciphertext yang lebih panjang."

    # Menghitung faktor dari setiap jarak
    factor_counts = Counter()
    for d in distances:
        for f in find_factors(d):
            factor_counts[f] += 1

    # Membuat laporan detail
    result = "🔍 ANALISIS KASISKI EXAMINATION\n"
    result += "=" * 50 + "\n\n"
    
    result += "📊 TRIGRAM BERULANG DITEMUKAN:\n"
    for detail in trigram_details[:5]:  # Tampilkan maksimal 5 trigram
        result += f"• Trigram '{detail['trigram']}' muncul di posisi: {detail['positions']}\n"
        result += f"  Jarak: {detail['distances']}\n"
    
    if len(trigram_details) > 5:
        result += f"... dan {len(trigram_details) - 5} trigram lainnya\n"
    
    result += f"\n📏 TOTAL JARAK DITEMUKAN: {len(distances)}\n"
    result += f"Jarak-jarak: {sorted(set(distances))}\n\n"
    
    result += "🎯 KEMUNGKINAN PANJANG KUNCI:\n"
    result += "(Berdasarkan faktor yang paling sering muncul)\n\n"
    
    for factor, count in factor_counts.most_common(8):
        percentage = (count / len(distances)) * 100
        confidence = "🔥 SANGAT TINGGI" if percentage > 50 else "⭐ TINGGI" if percentage > 30 else "💡 SEDANG"
        result += f"• Panjang {factor:2d}: muncul {count:2d}x ({percentage:5.1f}%) - {confidence}\n"
    
    result += "\n" + "=" * 50 + "\n"
    result += "💡 TIPS INTERPRETASI:\n"
    result += "• Panjang kunci dengan persentase tertinggi paling mungkin benar\n"
    result += "• Jika beberapa faktor memiliki skor tinggi, coba yang terkecil dulu\n"
    result += "• Faktor 2 dan 3 sering muncul secara kebetulan, pertimbangkan faktor lain\n"
    
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

    def on_reset():
        """Reset semua field input dan output"""
        if messagebox.askyesno("Konfirmasi Reset", "Apakah Anda yakin ingin menghapus semua isi?"):
            input_text.delete("1.0", tk.END)
            key_entry.delete(0, tk.END)
            output_text.delete("1.0", tk.END)
            messagebox.showinfo("Reset", "Semua field telah direset!")

    def show_kasiski_help():
        """Menampilkan penjelasan detail tentang Kasiski Examination"""
        help_text = """
🔍 KASISKI EXAMINATION - PANDUAN LENGKAP

Kasiski Examination adalah metode kriptanalisis yang dikembangkan oleh Friedrich Kasiski pada tahun 1863 untuk memecahkan cipher Vigenère tanpa mengetahui kunci.

📋 CARA KERJA:

1. PENCARIAN POLA BERULANG
   • Metode ini mencari trigram (kelompok 3 huruf) yang muncul berulang
   • Contoh: Dalam "ABCDEFABCGHI", trigram "ABC" muncul 2 kali

2. PENGUKURAN JARAK
   • Hitung jarak antara kemunculan trigram yang sama
   • Jarak ini kemungkinan kelipatan dari panjang kunci

3. ANALISIS FAKTOR
   • Cari faktor persekutuan dari semua jarak
   • Faktor yang paling sering muncul = kemungkinan panjang kunci

🎯 CONTOH PRAKTIS:

Misal kunci "KEY" (panjang 3):
- Plaintext : "ATTACKATDAWN"
- Ciphertext: "KEXEGOEXJKIR"

Jika "ATT" dan "AT" dienkripsi di posisi yang jaraknya kelipatan 3,
mereka akan menghasilkan pola serupa karena menggunakan bagian kunci yang sama.

📊 INTERPRETASI HASIL:

• PERSENTASE TINGGI (>50%): Kemungkinan besar benar
• PERSENTASE SEDANG (30-50%): Patut dicoba
• PERSENTASE RENDAH (<30%): Kemungkinan kecil

⚠ CATATAN PENTING:

• Butuh ciphertext yang cukup panjang (minimal 100-200 karakter)
• Faktor 2 dan 3 sering muncul secara kebetulan
• Teks dengan banyak pengulangan memberikan hasil lebih akurat

🛠 TIPS PENGGUNAAN:

1. Masukkan ciphertext yang panjang
2. Klik tombol "🔍 Kasiski"
3. Lihat faktor dengan persentase tertinggi
4. Coba panjang kunci yang disarankan untuk dekripsi
5. Jika hasil tidak masuk akal, coba faktor berikutnya
        """
        
        help_window = tk.Toplevel(root)
        help_window.title("📚 Panduan Kasiski Examination")
        help_window.geometry("600x500")
        
        help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=("Consolas", 10))
        help_text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)

    # Window utama
    root = tk.Tk()
    root.title("🔐 Vigenère Cipher & Kasiski Tool")
    root.geometry("750x650")

    # Header dengan informasi
    header_frame = ttk.Frame(root)
    header_frame.pack(fill="x", padx=10, pady=5)
    
    ttk.Label(header_frame, text="🔐 VIGENÈRE CIPHER & KASISKI EXAMINATION TOOL", 
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
    ttk.Button(button_frame, text="🔍 Kasiski", command=on_kasiski, width=12).grid(row=0, column=2, padx=5)
    ttk.Button(button_frame, text="🗑 Reset", command=on_reset, width=12).grid(row=0, column=3, padx=5)

    # Help button
    help_frame = ttk.Frame(root)
    help_frame.pack()
    ttk.Button(help_frame, text="❓ Panduan Kasiski", command=show_kasiski_help, width=20).pack()

    # Output section
    output_frame = ttk.Frame(root)
    output_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))
    
    ttk.Label(output_frame, text="📋 Hasil Output:").pack(anchor="w")
    output_text = scrolledtext.ScrolledText(output_frame, height=12, wrap=tk.WORD, font=("Consolas", 10))
    output_text.pack(fill="both", expand=True, pady=(0, 10))

    # Status bar
    status_frame = ttk.Frame(root)
    status_frame.pack(fill="x", side="bottom")
    ttk.Label(status_frame, text="💡 Tip: Gunakan Kasiski untuk menganalisis panjang kunci dari ciphertext", 
              font=("Arial", 8)).pack(pady=2)

    root.mainloop()

# ✅ Inisialisasi program
if __name__ == "__main__":
    print("🚀 Menjalankan Vigenère Cipher & Kasiski Tool...")
    print("📌 Fitur yang tersedia:")
    print("   • Enkripsi dan Dekripsi Vigenère")
    print("   • Analisis Kasiski Examination")
    print("   • Reset semua field")
    print("   • Panduan lengkap Kasiski")
    run_gui()
