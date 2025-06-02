# Dokumentasi Kode Vigenère Cipher & Kasiski Examination Tool

## Ikhtisar
Repositori ini berisi kode untuk aplikasi kriptografi yang mengimplementasikan cipher Vigenère dan metode analisis Kasiski Examination. Sistem ini menyediakan fitur enkripsi, dekripsi, dan analisis kriptografis untuk memecahkan cipher Vigenère tanpa mengetahui kunci.

## Daftar Isi
- [Dependensi](#dependensi)
- [Struktur Kode Sumber](#struktur-kode-sumber)
- [Struktur Data](#struktur-data)
- [Algoritma Inti](#algoritma-inti)
- [Implementasi GUI](#implementasi-gui)
- [Analisis Kriptografi](#analisis-kriptografi)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)

## Dependensi
Aplikasi ini memerlukan pustaka Python berikut:
```
tkinter          - Framework GUI
re               - Regular expressions untuk pemrosesan teks
collections      - Struktur data Counter untuk analisis frekuensi
```

## Struktur Kode Sumber

Kode sumber diorganisir menjadi beberapa bagian logis:

1. **Fungsi Kriptografi**
   - Enkripsi Vigenère
   - Dekripsi Vigenère
   - Analisis faktor untuk Kasiski

2. **Komponen Analisis**
   - Kasiski Examination
   - Pencarian trigram berulang
   - Analisis jarak dan faktor

3. **Komponen GUI**
   - Jendela aplikasi utama
   - Formulir input teks dan kunci
   - Tampilan hasil enkripsi/dekripsi
   - Panel analisis Kasiski

4. **Alat Pendukung**
   - Sistem bantuan terintegrasi
   - Fungsi reset
   - Status bar informatif

## Struktur Data

### Kecepatan Shift Cipher
Sistem menggunakan nilai ASCII untuk melakukan shifting karakter:
```python
offset = ord('A') if char.isupper() else ord('a')
shift = ord(key[key_index % key_len]) - ord('A')
```

### Model Trigram
Analisis Kasiski menggunakan struktur dictionary untuk menyimpan trigram dan posisinya:
```python
trigrams = {}
for i in range(len(text) - 2):
    trigram = text[i:i+3]
    if trigram in trigrams:
        trigrams[trigram].append(i)
    else:
        trigrams[trigram] = [i]
```

### Analisis Faktor
Faktor dari jarak trigram dihitung untuk menentukan kemungkinan panjang kunci:
```python
def find_factors(n):
    return [i for i in range(2, 21) if n % i == 0]
```

## Algoritma Inti

### Enkripsi Vigenère
Algoritma enkripsi menggunakan kunci berulang untuk menggeser setiap karakter:

```python
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
```

### Dekripsi Vigenère
Proses dekripsi membalik operasi enkripsi:

```python
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
```

### Kasiski Examination
Algoritma Kasiski mencari pola berulang untuk menentukan panjang kunci:

```python
def kasiski_examination(ciphertext):
    text = re.sub('[^A-Z]', '', ciphertext.upper())
    trigrams = {}
    
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
            for i in range(len(positions)-1):
                distance = positions[i+1] - positions[i]
                distances.append(distance)
```

### Analisis Faktor
Sistem menganalisis faktor dari jarak untuk menentukan kemungkinan panjang kunci:

```python
# Menghitung faktor dari setiap jarak
factor_counts = Counter()
for d in distances:
    for f in find_factors(d):
        factor_counts[f] += 1
```

## Implementasi GUI

GUI diimplementasikan menggunakan Tkinter dengan pendekatan fungsional:

```python
def run_gui():
    # Window utama
    root = tk.Tk()
    root.title("🔐 Vigenère Cipher & Kasiski Tool")
    root.geometry("750x650")
```

### Komponen Utama
1. **Header Frame** - Informasi aplikasi dan deskripsi
2. **Input Section** - Area teks untuk plaintext/ciphertext
3. **Key Entry** - Field input untuk kunci enkripsi/dekripsi
4. **Button Frame** - Tombol-tombol aksi (Enkripsi, Dekripsi, Kasiski, Reset)
5. **Output Section** - Area hasil dengan font monospace
6. **Status Bar** - Tips penggunaan aplikasi

### Metode Kunci
- `on_encrypt()` - Melakukan enkripsi Vigenère
- `on_decrypt()` - Melakukan dekripsi Vigenère
- `on_kasiski()` - Menjalankan analisis Kasiski
- `on_reset()` - Reset semua field dengan konfirmasi
- `show_kasiski_help()` - Menampilkan panduan lengkap Kasiski

## Analisis Kriptografi

### Metode Kasiski Examination
Kasiski Examination adalah metode kriptanalisis yang dikembangkan oleh Friedrich Kasiski pada tahun 1863:

1. **Pencarian Pola Berulang** - Mencari trigram yang muncul berulang dalam ciphertext
2. **Pengukuran Jarak** - Menghitung jarak antara kemunculan trigram yang sama
3. **Analisis Faktor** - Mencari faktor persekutuan dari jarak-jarak tersebut
4. **Interpretasi Hasil** - Faktor yang paling sering muncul kemungkinan adalah panjang kunci

### Laporan Analisis
Sistem menghasilkan laporan detail yang mencakup:

```python
result = "🔍 ANALISIS KASISKI EXAMINATION\n"
result += "=" * 50 + "\n\n"

result += "📊 TRIGRAM BERULANG DITEMUKAN:\n"
for detail in trigram_details[:5]:
    result += f"• Trigram '{detail['trigram']}' muncul di posisi: {detail['positions']}\n"
    result += f"  Jarak: {detail['distances']}\n"

result += "🎯 KEMUNGKINAN PANJANG KUNCI:\n"
for factor, count in factor_counts.most_common(8):
    percentage = (count / len(distances)) * 100
    confidence = "🔥 SANGAT TINGGI" if percentage > 50 else "⭐ TINGGI" if percentage > 30 else "💡 SEDANG"
    result += f"• Panjang {factor:2d}: muncul {count:2d}x ({percentage:5.1f}%) - {confidence}\n"
```

## Menjalankan Aplikasi

Titik masuk aplikasi ada di bagian bawah skrip:

```python
if __name__ == "__main__":
    print("🚀 Menjalankan Vigenère Cipher & Kasiski Tool...")
    print("📌 Fitur yang tersedia:")
    print("   • Enkripsi dan Dekripsi Vigenère")
    print("   • Analisis Kasiski Examination") 
    print("   • Reset semua field")
    print("   • Panduan lengkap Kasiski")
    run_gui()
```

Untuk menjalankan aplikasi:
1. Pastikan Python 3.x terinstal dengan pustaka tkinter
2. Jalankan skrip utama: `python main.py`
3. GUI akan muncul dengan semua fitur yang tersedia
4. Masukkan teks dan kunci untuk enkripsi/dekripsi, atau gunakan Kasiski untuk analisis

## Fitur Tambahan

### Sistem Bantuan Terintegrasi
Aplikasi menyediakan panduan lengkap tentang Kasiski Examination:

```python
def show_kasiski_help():
    help_text = """
🔍 KASISKI EXAMINATION - PANDUAN LENGKAP

Kasiski Examination adalah metode kriptanalisis yang dikembangkan oleh Friedrich Kasiski pada tahun 1863 untuk memecahkan cipher Vigenère tanpa mengetahui kunci.

📋 CARA KERJA:
1. PENCARIAN POLA BERULANG
2. PENGUKURAN JARAK  
3. ANALISIS FAKTOR

🎯 CONTOH PRAKTIS:
🛠 TIPS PENGGUNAAN:
    """
```

### Validasi Input
Sistem memvalidasi input pengguna sebelum memproses:

```python
def on_encrypt():
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()
    if not text or not key:
        messagebox.showwarning("Input Error", "Isi teks dan kunci terlebih dahulu!")
        return
```

## Metode Perhitungan Kriptografi

1. **Cipher Vigenère** - Menggunakan operasi modular pada nilai ASCII:
   ```python
   # Enkripsi: (P + K) mod 26
   ciphertext += chr((ord(char) - offset + shift) % 26 + offset)
   
   # Dekripsi: (C - K) mod 26  
   plaintext += chr((ord(char) - offset - shift) % 26 + offset)
   ```

2. **Analisis Statistik** - Menggunakan Counter untuk menghitung frekuensi faktor:
   ```python
   factor_counts = Counter()
   for d in distances:
       for f in find_factors(d):
           factor_counts[f] += 1
   ```

## Interpretasi Hasil Kasiski

Sistem memberikan tingkat kepercayaan berdasarkan persentase kemunculan faktor:

- **SANGAT TINGGI (>50%)** - Kemungkinan besar merupakan panjang kunci yang benar
- **TINGGI (30-50%)** - Patut dicoba sebagai panjang kunci
- **SEDANG (<30%)** - Kemungkinan kecil, namun bisa dipertimbangkan

### Kesimpulan
Berdasarkan implementasi yang dilakukan terhadap Vigenère Cipher & Kasiski Examination Tool, diperoleh beberapa kesimpulan sebagai berikut:

1. **Efektivitas Enkripsi Vigenère**
   - Cipher Vigenère menyediakan keamanan yang lebih baik dibandingkan cipher substitusi sederhana
   - Penggunaan kunci berulang membuat analisis frekuensi menjadi lebih sulit
   - Namun tetap rentan terhadap analisis Kasiski jika panjang teks cukup besar

2. **Kekuatan Analisis Kasiski**
   - Metode Kasiski efektif untuk menentukan panjang kunci pada cipher Vigenère
   - Membutuhkan ciphertext yang cukup panjang (minimal 100-200 karakter) untuk hasil optimal
   - Akurasi meningkat dengan adanya pengulangan pola dalam plaintext asli

3. **Implementasi GUI yang User-Friendly**
   - Interface yang intuitif memudahkan pengguna untuk melakukan enkripsi, dekripsi, dan analisis
   - Sistem bantuan terintegrasi membantu pengguna memahami konsep Kasiski Examination
   - Validasi input mencegah kesalahan penggunaan

4. **Nilai Edukatif**
   - Aplikasi ini sangat berguna untuk pembelajaran kriptografi klasik
   - Mendemonstrasikan kelemahan cipher Vigenère terhadap analisis kriptografi
   - Memberikan pemahaman praktis tentang metode kriptanalisis

# Kesimpulan dari Vigenère Cipher & Kasiski Tool

Berdasarkan analisis terhadap kode sumber aplikasi Vigenère Cipher & Kasiski Tool, dapat disimpulkan beberapa hal tentang implementasi kriptografi yang digunakan:

1. **Algoritma Utama: Vigenère Cipher**
   - Menggunakan metode enkripsi polyalphabetic substitution dengan kunci berulang
   - Implementasi yang benar dengan penanganan huruf besar/kecil dan karakter non-alfabet
   - Operasi matematis modular (mod 26) untuk menjaga karakter tetap dalam rentang alfabet

2. **Metode Kriptanalisis: Kasiski Examination**
   - Implementasi lengkap metode Kasiski untuk memecahkan cipher Vigenère
   - Pencarian trigram berulang dengan analisis jarak yang sistematis
   - Sistem scoring berdasarkan frekuensi faktor untuk menentukan kemungkinan panjang kunci

3. **Struktur Data yang Efisien**
   - Penggunaan dictionary untuk menyimpan trigram dan posisinya
   - Counter dari collections untuk analisis frekuensi faktor
   - Preprocessing teks dengan regular expression untuk hasil yang akurat

4. **Antarmuka Pengguna yang Komprehensif**
   - GUI berbasis Tkinter dengan layout yang terorganisir
   - Fitur validasi input untuk mencegah kesalahan pengguna
   - Sistem bantuan terintegrasi dengan penjelasan detail tentang Kasiski

5. **Aspek Edukatif dan Praktis**
   - Aplikasi memberikan pemahaman mendalam tentang kelemahan cipher klasik
   - Hasil analisis yang detail dengan interpretasi tingkat kepercayaan
   - Cocok untuk pembelajaran kriptografi dan demonstrasi keamanan

Secara keseluruhan, aplikasi ini merupakan implementasi yang solid untuk pembelajaran dan praktik kriptografi klasik, menggabungkan enkripsi Vigenère dengan teknik kriptanalisis Kasiski dalam satu paket yang mudah digunakan dan edukatif. Tool ini sangat bermanfaat untuk memahami prinsip-prinsip dasar kriptografi dan pentingnya analisis keamanan dalam sistem enkripsi.
