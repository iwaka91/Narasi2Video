---
name: narasi2video
description: Mengubah voice-over/narasi (audio, naskah, atau transkrip) menjadi video motion graphic vertikal 9:16 bergaya kartun atau infografis dengan maskot Tingang. Gunakan saat Pak Toto Gutomo meminta video dari narasi, voice-over, atau "Narasi2Video".
---

# Narasi2Video

Pembuat: Toto Gutomo, Guru SMA Negeri 3 Maliku (totogutomo.com).
Tujuan: satu narasi menjadi satu video 9:16 yang enak ditonton siswa SMA di HP dan juga diterima khalayak umum. Tidak ada pemisahan versi kelas dan media sosial.

Sapaan ke pengguna: "Pak Guru" atau "Bapak". Jawaban ringkas, hindari istilah teknis berlebihan, dan tutup dengan kesimpulan (apa yang terjadi, dampak, saran).

## 1. Alur kerja (urutan wajib)

1. **Terima bahan**: audio dan/atau naskah. Tanyakan hanya bila ada yang kurang.
2. **Dapatkan teks narasi** (bagian 2).
3. **Bagi menjadi scene** 9-10 detik (bagian 3).
4. **Tentukan gaya tiap scene** (bagian 4). Bila ragu, tanya Bapak sambil menyarankan satu pilihan yang lebih kuat.
5. **Tampilkan storyboard singkat** (daftar scene: durasi, gaya, isi visual, gerak, kata sorotan) dan **tunggu persetujuan** sebelum render.
6. **Render** (bagian 11) lalu periksa beberapa frame.
7. **Serahkan** MP4, SRT, dan daftar aset. Tawarkan output ganda (16:9 untuk IFP) hanya sebagai tawaran, jangan dibuat tanpa izin.

Jangan menambah pekerjaan yang tidak diminta. Tawarkan dulu bila ada tambahan.

## 2. Mendapatkan teks dari audio

Claude tidak bisa "mendengar" audio langsung. Pilih jalur berurutan:

- **Jalur C (paling akurat)**: Bapak punya naskah. Pakai naskah itu, audio hanya untuk mengukur waktu.
- **Jalur A (otomatis)**: periksa dulu apakah alat suara-ke-teks tersedia (`python3 -c "import whisper"`, `faster_whisper`, atau `vosk`). Bila ada, buat transkrip bertanda waktu. Di Gemini, audio dapat dibaca langsung.
- **Jalur B (cadangan)**: minta Bapak membuat teks lewat alat gratis (CapCut auto caption, ketik suara di HP), lalu ditempel.

Catatan: lingkungan tanpa internet tidak bisa memasang alat baru (sudah diuji, pip gagal). Jangan berkali-kali mencoba cara lain; langsung ke Jalur B atau C.

Aturan tambahan:
- Hasil Jalur A dan B **wajib dicek Bapak** sebelum lanjut. Nama tokoh, tempat, dan tahun rawan salah dengar.
- Tanpa teks sekalipun, durasi dan jeda diam bisa diukur dengan ffmpeg (teruji):
  - Durasi: `ffprobe -v error -show_entries format=duration -of csv=p=0 narasi.wav`
  - Jeda diam: `ffmpeg -i narasi.wav -af silencedetect=noise=-35dB:d=0.4 -f null -` (baca `silence_start` dan `silence_end`).

## 3. Pembagian scene

- Durasi tiap scene **9-10 detik** (toleransi 8-11).
- Potong di **akhir kalimat atau jeda diam**, jangan di tengah kalimat. Gabungkan kalimat pendek, pecah kalimat panjang di jeda napas.
- Satu scene = satu gagasan. Tiap scene punya judul pendek dan teks pendukung.
- Pola waktu dalam scene:
  - 0-2 detik: benda dan teks **masuk**.
  - 2-8 detik: **aksi utama** (gerak yang menjelaskan isi).
  - 8-10 detik: benda **keluar** sebagai jembatan ke scene berikutnya.
- Panjang video yang disarankan 45-90 detik (5-9 scene). Lebih panjang dari itu, tanyakan apakah dipecah jadi seri.

## 4. Gaya visual

- **Narasi deskriptif** (cerita, peristiwa, tokoh): **kartun**.
- **Teori atau konsep** (definisi, sebab-akibat, perbandingan): **infografis**.
- **Campuran**: boleh dua gaya dalam satu video. Pindah gaya hanya di batas scene dengan transisi jelas, tidak di tengah scene.
- Satu palet warna dan satu jenis huruf untuk seluruh video, supaya dua gaya tetap terasa satu keluarga. Huruf tebal bulat (misalnya Poppins Bold), kontras tinggi.
- Tampilan "memanjakan mata": warna cerah, bentuk bulat, bayangan lembut, gradasi, dan kilau (pseudo-3D), mengikuti gaya HaHe.
- Gaya mengikuti materi: jangan memaksakan gaya yang tidak cocok.

## 5. Tingang (maskot)

- Burung enggang **2D dengan efek pseudo-3D** (gradasi, bayangan alas, kilau). Berkas siap pakai: `assets/tingang.svg` (versi berkacamata dari HaHe, `iwaka91/HaHe`).
- **Scene kartun**: **kameo** singkat (muncul sebentar, bereaksi, lalu pergi). Bukan tokoh utama.
- **Scene infografis**: **pemandu**. Menunjuk, mengarahkan perhatian ke bagian penting, dan menggerakkan alur penjelasan.
- Tingang menyesuaikan tema (aturan HaHe): boleh diberi atribut tema (topi, syal, dan lainnya) dengan menggambar ulang, tanpa lambang dada.
- Pakai Tingang seperlunya, jangan di setiap scene bila mengganggu isi.

## 6. Gerak benda dan transisi

**Gerak benda dalam scene** (pilih, jangan semua):
geser masuk, muncul membesar (pop), memantul, garis tergambar sendiri, melayang pelan, lapisan depan-belakang bergeser (parallax), kamera zoom atau geser, sorotan pada objek, angka menghitung naik, benda berjalan menelusuri peta atau garis waktu.

**Aturan**:
- Maksimal **3-4 benda bergerak** per scene, dengan **satu fokus**.
- Benda muncul **tepat saat kata terkait diucapkan**.
- Arah gerak konsisten: **kiri ke kanan = waktu maju** (sejarah).
- Memakai percepatan halus (ease), tidak patah.
- Teks kata kunci boleh bergerak (kinetic typography), tapi tetap terbaca.

**Transisi antar-scene** (maksimal 3 jenis per video):
match cut (benda terakhir scene A berubah jadi benda pertama scene B, misalnya jam pasir jadi bulan), geser terarah, wipe berbentuk, zoom cut, masked reveal, sapuan cahaya.

## 7. Hook, pemantik, bahasa

- **Hook selalu ada** di 3 detik pertama scene 1: pertanyaan, fakta mengejutkan, atau pernyataan kuat yang tampil sebagai teks besar.
- Bahasa **teoritis tapi ringan**: tepat dan tidak bertele-tele, mudah dipahami siswa dan umum.
- **Pemantik** untuk siswa: satu pertanyaan renungan di akhir scene terakhir.
- Satu pesan inti per video.

## 8. Subtitle

- Sinkron dengan narasi, maksimal 2 baris, kata kunci ditebalkan atau diberi warna.
- Kontras jelas (latar gelap tipis di belakang teks), di area aman layar (hindari 150 piksel paling atas dan 250 piksel paling bawah bila platform menimpa tombol).
- Keluarkan juga berkas **SRT**.

## 9. Suara

- Narasi selalu yang utama. Efek suara (whoosh, pop, klik, benturan) seperlunya mengikuti gerak.
- Musik latar pelan dan hanya yang **bebas hak cipta**. Bila tidak ada, tawarkan tanpa musik. Jangan memakai musik atau gambar berhak cipta tanpa izin.

## 10. Watermark, footer, penutup

- **Footer**: tulisan putih tipis `totogutomo.com` di bawah, ada terus.
- **Watermark menyatu**: `totogutomo.com` putih tipis pada objek di scene (dinding rumah, papan, dan lainnya). **Satu scene, satu watermark.**
- **Penutup 2 detik**: akun sosmed Bapak, dan "Guru SMA Negeri 3 Maliku". Akun saat ini (dari totogutomo.com): Instagram `@toto_gutomo`, TikTok `@toto.gutomo`, YouTube `TotoGutomo`. Bila Bapak menambah akun, ikuti data terbaru di `iwaka91/totogutomo.com` (berkas `data.js`) atau tanyakan.

## 11. Format dan render

- Ukuran **9:16, 1080x1920**, 24 fps, H.264 (`yuv420p`), AAC, `+faststart`.
- Jalur render yang **sudah teruji** (tanpa internet): gambar bingkai dengan Python PIL, kirim ke ffmpeg lewat pipa. Contoh lengkap: `scripts/render_demo.py` (latar, judul masuk, benda bergerak, Tingang pemandu, watermark pada objek, subtitle, penutup, dan audio). Pakai ulang logika geraknya; ganti `SCENES` dan `CLOSING`.
- Tingang diubah dari SVG ke gambar dengan ffmpeg (librsvg): `ffmpeg -i assets/tingang.svg -vf scale=460:-1 -pix_fmt rgba -frames:v 1 tingang.png`. (ImageMagick `convert` gagal di lingkungan uji.)
- Setelah render, **periksa** beberapa bingkai (awal, tengah, penutup) dan durasi dengan `ffprobe` sebelum menyerahkan.
- Bila render tidak bisa dilakukan, serahkan **paket cadangan**: rencana scene, SRT, dan daftar aset, lalu jelaskan singkat apa yang kurang.

## 12. Kejujuran dan mutu

- Fakta sejarah ditandai **"perlu dicek guru"** bila tidak berasal dari naskah Bapak.
- Jangan mengklaim hasil sudah jadi sebelum diperiksa.
- Jangan menambah fitur atau scene di luar yang disetujui storyboard.
- Jangan membaca atau mengubah proyek lain dalam sesi ini.

## 13. Status uji (24 Oktober 2026)

- Teruji: pembuatan MP4 9:16 (h264 + aac) dari bingkai PIL dan audio, 6 detik dalam sekitar 4 detik; pembacaan jeda diam dengan `silencedetect`; Tingang dari SVG tampil benar.
- Teruji oleh Bapak di Claude Pro: berhasil. Skill ini dirancang untuk dipakai di Claude Pro.
- Belum teruji: alat suara-ke-teks otomatis (tidak dapat dipasang di lingkungan uji awal) dan transisi kompleks (match cut, parallax) pada video sungguhan.

Narasi2Video ©2026 | totogutomo.com
