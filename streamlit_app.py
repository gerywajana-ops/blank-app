"""
============================================================
  APLIKASI IDENTIFIKASI BAHAYA KIMIA (CHEMICAL HAZARD ID)
============================================================
  Aplikasi CLI untuk mengidentifikasi tingkat bahaya kimia
  dengan database 30 bahan kimia.

  Kategori Bahaya:
  - Sangat Berbahaya : Bahan yang sangat beracun/korosif/meledak
  - Berbahaya        : Bahan yang beracun/korosif/mudah terbakar
  - Sedang           : Bahan yang dapat menyebabkan iritasi
  - Rendah           : Bahan yang umumnya aman

  Fitur:
  1. Cari bahan kimia berdasarkan nama, rumus, atau CAS
  2. Filter berdasarkan kategori bahaya
  3. Lihat detail bahaya lengkap dengan pictogram GHS
  4. Simpan hasil pencarian ke file JSON
  5. Statistik database bahan kimia
"""

import json
import os
import sys
from datetime import datetime

# ============================================================
# DATABASE 30 BAHAN KIMIA
# ============================================================
CHEMICALS = [
    # === SANGAT BERBAHAYA (5) ===
    {
        "id": 1,
        "nama": "Asam Sianhidrat (HCN)",
        "rumus": "HCN",
        "cas": "74-90-8",
        "kategori": "Sangat Berbahaya",
        "bahaya": "Sangat beracun, dapat menyebabkan kematian dalam hitungan menit. Dapat diserap melalui kulit dan pernapasan.",
        "pictogram": ["GHS06", "GHS08", "GHS09"],
        "peringatan": "Jauhkan dari jangkauan anak-anak. Gunakan perlengkapan pelindung lengkap. Sediakan antidot.",
        "penanganan": "Gunakan APD lengkap. Kerja di lemari asam. Sediakan kalsium glukonat jika kontak kulit."
    },
    {
        "id": 2,
        "nama": "Asam Fluorida (HF)",
        "rumus": "HF",
        "cas": "7664-39-3",
        "kategori": "Sangat Berbahaya",
        "bahaya": "Sangat korosif. Dapat menembus kulit dan merusak tulang. Dapat menyebabkan kematian akibat keracunan kalsium.",
        "pictogram": ["GHS05", "GHS06"],
        "peringatan": "Gunakan sarung tangan khusus HF. Sediakan kalsium glukonat gel sebagai antidot.",
        "penanganan": "Jika terkena kulit, segera bilas dengan air 15 menit dan oleskan kalsium glukonat."
    },
    {
        "id": 3,
        "nama": "Klorin (Cl2)",
        "rumus": "Cl2",
        "cas": "7782-50-5",
        "kategori": "Sangat Berbahaya",
        "bahaya": "Gas beracun yang sangat reaktif. Dapat menyebabkan kerusakan paru-paru parah, edema paru, dan kematian.",
        "pictogram": ["GHS04", "GHS06", "GHS09"],
        "peringatan": "Gunakan di ruang berventilasi dengan sistem pengaman gas. Sediakan masker gas.",
        "penanganan": "Jika terhirup, segera pindahkan ke udara segar. Berikan oksigen jika kesulitan bernapas."
    },
    {
        "id": 4,
        "nama": "Mercuri Klorida (HgCl2)",
        "rumus": "HgCl2",
        "cas": "7487-94-7",
        "kategori": "Sangat Berbahaya",
        "bahaya": "Sangat beracun. Racun kumulatif yang dapat menyebabkan kerusakan ginjal permanen dan kerusakan sistem saraf.",
        "pictogram": ["GHS06", "GHS08", "GHS09"],
        "peringatan": "Racun kumulatif. Penanganan memerlukan izin khusus. Hindari semua kontak.",
        "penanganan": "Jika tertelan, jangan dipaksa muntah. Segera bawa ke RS dengan membawa label kemasan."
    },
    {
        "id": 5,
        "nama": "Asam Pikrat (C6H3N3O7)",
        "rumus": "C6H3N3O7",
        "cas": "88-89-1",
        "kategori": "Sangat Berbahaya",
        "bahaya": "Sangat mudah meledak. Dapat menyebabkan ledakan hebat jika terkena guncangan, panas, atau gesekan.",
        "pictogram": ["GHS01", "GHS06"],
        "peringatan": "Simpan dalam kondisi basah. Jauhkan dari sumber panas dan bahan mudah terbakar.",
        "penanganan": "Gunakan alat tembaga/bronze. Hindari penggunaan besi. Simpan di tempat sejuk dan gelap."
    },

    # === BERBAHAYA (10) ===
    {
        "id": 6,
        "nama": "Asam Sulfat Pekat (H2SO4)",
        "rumus": "H2SO4",
        "cas": "7664-93-9",
        "kategori": "Berbahaya",
        "bahaya": "Sangat korosif dan dehydrating agent. Dapat menyebabkan luka bakar kimia parah dan kerusakan jaringan permanen.",
        "pictogram": ["GHS05"],
        "peringatan": "Selalu tambahkan asam ke air (bukan air ke asam) untuk menghindari cipratan.",
        "penanganan": "Jika terkena kulit, bilas dengan air mengalir minimal 15 menit. Jangan gunakan netralisasi."
    },
    {
        "id": 7,
        "nama": "Natrium Hidroksida (NaOH)",
        "rumus": "NaOH",
        "cas": "1310-73-2",
        "kategori": "Berbahaya",
        "bahaya": "Sangat korosif. Dapat menyebabkan luka bakar kimia parah pada kulit, mata, dan saluran pernapasan.",
        "pictogram": ["GHS05"],
        "peringatan": "Reaksi dengan asam menghasilkan panas yang sangat tinggi. Hindari kontak dengan aluminium.",
        "penanganan": "Simpan di wadah plastik. Jika terkena mata, bilas dengan air minimal 30 menit."
    },
    {
        "id": 8,
        "nama": "Benzena (C6H6)",
        "rumus": "C6H6",
        "cas": "71-43-2",
        "kategori": "Berbahaya",
        "bahaya": "Karsinogen kategori 1A. Dapat menyebabkan leukemia, kerusakan sumsum tulang, dan gangguan darah.",
        "pictogram": ["GHS02", "GHS07", "GHS08"],
        "peringatan": "Karsinogen. Hindari semua kontak termasuk inhalasi uap. Gunakan di lemari asam.",
        "penanganan": "Gunakan sarung tangan nitril. Jangan gunakan lateks. Sediakan ventilasi lokal."
    },
    {
        "id": 9,
        "nama": "Formaldehida (HCHO)",
        "rumus": "HCHO",
        "cas": "50-00-0",
        "kategori": "Berbahaya",
        "bahaya": "Karsinogen kategori 1B. Dapat menyebabkan iritasi parah mata, kulit, dan saluran pernapasan. Sensitizer.",
        "pictogram": ["GHS05", "GHS08"],
        "peringatan": "Uap sangat iritatif. Gunakan di lemari asam dengan ventilasi baik.",
        "penanganan": "Gunakan respirator dengan filter formaldehida. Sediakan air cuci mata darurat."
    },
    {
        "id": 10,
        "nama": "Metanol (CH3OH)",
        "rumus": "CH3OH",
        "cas": "67-56-1",
        "kategori": "Berbahaya",
        "bahaya": "Sangat beracun jika tertelan atau diserap kulit. Dapat menyebabkan kebutaan permanen dan kematian.",
        "pictogram": ["GHS02", "GHS06", "GHS08"],
        "peringatan": "Jangan gunakan untuk membersihkan tangan. Dapat diserap melalui kulit.",
        "penanganan": "Jika tertelan, segera ke RS. Antidot: etanol atau fomepizole."
    },
    {
        "id": 11,
        "nama": "Kalium Permanganat (KMnO4)",
        "rumus": "KMnO4",
        "cas": "7722-64-7",
        "kategori": "Berbahaya",
        "bahaya": "Oksidator kuat. Dapat menyebabkan kebakaran jika bercampur dengan bahan mudah terbakar atau organik.",
        "pictogram": ["GHS03", "GHS07"],
        "peringatan": "Dapat menyebabkan ledakan jika bercampur dengan gliserol atau bahan organik lain.",
        "penanganan": "Simpan terpisah dari bahan reduktor dan organik. Hindari kontak dengan bahan mudah terbakar."
    },
    {
        "id": 12,
        "nama": "Hidrogen Peroksida 30% (H2O2)",
        "rumus": "H2O2",
        "cas": "7722-84-1",
        "kategori": "Berbahaya",
        "bahaya": "Oksidator kuat. Dapat menyebabkan luka bakar kimia dan kebakaran. Menguraikan menjadi oksigen dan air.",
        "pictogram": ["GHS03", "GHS05"],
        "peringatan": "Konsentrasi >30% sangat berbahaya. Simpan di tempat sejuk, gelap, dan ventilasi baik.",
        "penanganan": "Jika terkena kulit, bilas dengan air banyak. Jangan campur dengan bahan organik."
    },
    {
        "id": 13,
        "nama": "Etanol Absolut (C2H5OH)",
        "rumus": "C2H5OH",
        "cas": "64-17-5",
        "kategori": "Berbahaya",
        "bahaya": "Sangat mudah terbakar. Uapnya dapat membentuk campuran ledak dengan udara.",
        "pictogram": ["GHS02"],
        "peringatan": "Jauhkan dari api, sumber panas, dan percikan api. Simpan di tempat sejuk.",
        "penanganan": "Gunakan alat anti-spark. Sediakan pemadam api CO2 di dekatnya."
    },
    {
        "id": 14,
        "nama": "Aseton (C3H6O)",
        "rumus": "C3H6O",
        "cas": "67-64-1",
        "kategori": "Berbahaya",
        "bahaya": "Sangat mudah terbakar. Dapat menyebabkan iritasi saluran pernapasan dan kulit pada paparan kronis.",
        "pictogram": ["GHS02", "GHS07"],
        "peringatan": "Jangan gunakan di dekat api terbuka. Uap lebih berat dari udara.",
        "penanganan": "Simpan di wadah logam atau kaca. Hindari penyimpanan dalam plastik PVC."
    },
    {
        "id": 15,
        "nama": "Karbon Tetraklorida (CCl4)",
        "rumus": "CCl4",
        "cas": "56-23-5",
        "kategori": "Berbahaya",
        "bahaya": "Karsinogen. Dapat menyebabkan kerusakan hati, ginjal, dan sistem saraf pusat.",
        "pictogram": ["GHS06", "GHS08"],
        "peringatan": "Dapat menyebabkan kerusakan ozon. Hindari semua kontak termasuk inhalasi.",
        "penanganan": "Gunakan di lemari asam. Sediakan ventilasi exhaust. Jangan gunakan sebagai pelarut rutin."
    },

    # === SEDANG (10) ===
    {
        "id": 16,
        "nama": "Asam Sitrat (C6H8O7)",
        "rumus": "C6H8O7",
        "cas": "77-92-9",
        "kategori": "Sedang",
        "bahaya": "Dapat menyebabkan iritasi kulit dan mata pada konsentrasi tinggi. Korosif pada konsentrasi >50%.",
        "pictogram": ["GHS07"],
        "peringatan": "Relatif aman pada konsentrasi rendah, tetapi tetap hindari kontak mata.",
        "penanganan": "Gunakan kacamata pelindung saat menangani konsentrasi tinggi. Bilas dengan air jika terkena."
    },
    {
        "id": 17,
        "nama": "Natrium Karbonat (Na2CO3)",
        "rumus": "Na2CO3",
        "cas": "497-19-8",
        "kategori": "Sedang",
        "bahaya": "Dapat menyebabkan iritasi kulit dan mata. Korosif pada konsentrasi tinggi dan larutan panas.",
        "pictogram": ["GHS07"],
        "peringatan": "Larutan panas lebih berbahaya. Hindari inhalasi debu.",
        "penanganan": "Gunakan masker debu saat menangani bubuk. Bilas dengan air jika terkena kulit."
    },
    {
        "id": 18,
        "nama": "Amonium Klorida (NH4Cl)",
        "rumus": "NH4Cl",
        "cas": "12125-02-9",
        "kategori": "Sedang",
        "bahaya": "Dapat menyebabkan iritasi saluran pernapasan dan kulit. Debu dapat mengiritasi mata.",
        "pictogram": ["GHS07"],
        "peringatan": "Hindari inhalasi debu dalam jumlah besar. Simpan di tempat kering.",
        "penanganan": "Gunakan ventilasi yang baik. Gunakan kacamata pelindung saat menangani bubuk."
    },
    {
        "id": 19,
        "nama": "Natrium Klorida (NaCl)",
        "rumus": "NaCl",
        "cas": "7647-14-5",
        "kategori": "Sedang",
        "bahaya": "Umumnya aman, tetapi dapat menyebabkan iritasi mata pada konsentrasi tinggi. Tidak beracun.",
        "pictogram": [],
        "peringatan": "Garam dapur biasa. Relatif aman tetapi tetap jaga kebersihan.",
        "penanganan": "Tidak diperlukan APD khusus. Bilas dengan air jika terkena mata."
    },
    {
        "id": 20,
        "nama": "Kalium Nitrat (KNO3)",
        "rumus": "KNO3",
        "cas": "7757-79-1",
        "kategori": "Sedang",
        "bahaya": "Oksidator lemah. Dapat menyebabkan iritasi kulit dan mata. Dapat mempercepat kebakaran.",
        "pictogram": ["GHS03", "GHS07"],
        "peringatan": "Oksidator lemah. Jauhkan dari bahan mudah terbakar dan reduktor.",
        "penanganan": "Simpan di tempat kering dan terpisah dari bahan mudah terbakar."
    },
    {
        "id": 21,
        "nama": "Asam Borat (H3BO3)",
        "rumus": "H3BO3",
        "cas": "10043-35-3",
        "kategori": "Sedang",
        "bahaya": "Dapat menyebabkan iritasi kulit dan mata. Beracun untuk reproduksi pada hewan percobaan.",
        "pictogram": ["GHS08"],
        "peringatan": "Hindari kontak berulang dengan kulit. Jangan gunakan pada produk untuk anak-anak.",
        "penanganan": "Gunakan sarung tangan saat menangani dalam jumlah besar. Cuci tangan setelah kontak."
    },
    {
        "id": 22,
        "nama": "Kalsium Klorida (CaCl2)",
        "rumus": "CaCl2",
        "cas": "10043-52-4",
        "kategori": "Sedang",
        "bahaya": "Dapat menyebabkan iritasi kulit dan mata. Sangat higroskopis dan menghasilkan panas saat larut.",
        "pictogram": ["GHS07"],
        "peringatan": "Dapat menghasilkan panas saat larut dalam air. Hindari penambahan air cepat.",
        "penanganan": "Tambahkan perlahan ke air sambil diaduk. Gunakan kacamata pelindung."
    },
    {
        "id": 23,
        "nama": "Kalsium Hidroksida (Ca(OH)2)",
        "rumus": "Ca(OH)2",
        "cas": "1305-62-0",
        "kategori": "Sedang",
        "bahaya": "Dapat menyebabkan iritasi kulit dan mata. Korosif pada konsentrasi tinggi (kapur tohor).",
        "pictogram": ["GHS07"],
        "peringatan": "Debu dapat mengiritasi saluran pernapasan. Hindari inhalasi.",
        "penanganan": "Gunakan masker debu saat menangani bubuk. Bilas dengan air jika terkena kulit."
    },
    {
        "id": 24,
        "nama": "Ferro Sulfat (FeSO4)",
        "rumus": "FeSO4",
        "cas": "7720-78-7",
        "kategori": "Sedang",
        "bahaya": "Dapat menyebabkan iritasi kulit dan mata. Beracun jika tertelan dalam jumlah besar.",
        "pictogram": ["GHS07"],
        "peringatan": "Dapat menyebabkan keracunan besi pada anak-anak. Simpan di luar jangkauan anak.",
        "penanganan": "Jika tertelan oleh anak, segera hubungi dokter. Simpan dalam wadah tertutup."
    },
    {
        "id": 25,
        "nama": "Tembaga Sulfat (CuSO4)",
        "rumus": "CuSO4",
        "cas": "7758-98-7",
        "kategori": "Sedang",
        "bahaya": "Beracun jika tertelan. Dapat menyebabkan iritasi kulit, mata, dan saluran pernapasan.",
        "pictogram": ["GHS07", "GHS09"],
        "peringatan": "Beracun bagi organisme air. Jangan buang ke saluran air.",
        "penanganan": "Kumpulkan limbah sebagai limbah B3. Gunakan sarung tangan saat menangani."
    },

    # === RENDAH (5) ===
    {
        "id": 26,
        "nama": "Air Suling (H2O)",
        "rumus": "H2O",
        "cas": "7732-18-5",
        "kategori": "Rendah",
        "bahaya": "Tidak berbahaya dalam kondisi normal. Tidak ada efek kesehatan yang diketahui.",
        "pictogram": [],
        "peringatan": "Tidak ada bahaya khusus. Namun, jangan minum air suling dalam jumlah besar.",
        "penanganan": "Tidak diperlukan APD. Penanganan standar laboratorium."
    },
    {
        "id": 27,
        "nama": "Gliserol (C3H8O3)",
        "rumus": "C3H8O3",
        "cas": "56-81-5",
        "kategori": "Rendah",
        "bahaya": "Umumnya aman. Dapat menyebabkan iritasi mata ringan pada konsentrasi tinggi. Tidak beracun.",
        "pictogram": [],
        "peringatan": "Sangat higroskopis dan kental. Dapat menjebak kotoran jika tidak dibersihkan.",
        "penanganan": "Tidak diperlukan APD khusus. Cuci tangan setelah kontak."
    },
    {
        "id": 28,
        "nama": "Natrium Sitrat (Na3C6H5O7)",
        "rumus": "Na3C6H5O7",
        "cas": "68-04-2",
        "kategori": "Rendah",
        "bahaya": "Umumnya aman. Digunakan sebagai pengawet makanan dan antikoagulan darah.",
        "pictogram": [],
        "peringatan": "Sangat aman untuk penanganan. Dapat menyebabkan iritasi mata pada konsentrasi tinggi.",
        "penanganan": "Tidak diperlukan APD khusus. Penanganan standar laboratorium."
    },
    {
        "id": 29,
        "nama": "Sukrosa (C12H22O11)",
        "rumus": "C12H22O11",
        "cas": "57-50-1",
        "kategori": "Rendah",
        "bahaya": "Umumnya aman. Gula pasir biasa. Dapat menyebabkan iritasi pada konsentrasi sangat tinggi.",
        "pictogram": [],
        "peringatan": "Sangat aman. Namun, dapat menarik semut jika tumpah dan tidak dibersihkan.",
        "penanganan": "Tidak diperlukan APD. Simpan di wadah tertutup untuk menjaga kebersihan."
    },
    {
        "id": 30,
        "nama": "Magnesium Sulfat (MgSO4)",
        "rumus": "MgSO4",
        "cas": "7487-88-9",
        "kategori": "Rendah",
        "bahaya": "Umumnya aman. Garam Epsom. Dapat menyebabkan iritasi pada konsentrasi sangat tinggi.",
        "pictogram": [],
        "peringatan": "Sangat aman untuk penanganan. Digunakan dalam kosmetik dan farmasi.",
        "penanganan": "Tidak diperlukan APD khusus. Penanganan standar laboratorium."
    }
]

# ============================================================
# KONFIGURASI WARNA ANSI
# ============================================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ============================================================
# FUNGSI UTILITAS
# ============================================================
def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Menampilkan banner aplikasi."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║           APLIKASI IDENTIFIKASI BAHAYA KIMIA                    ║
║              Chemical Hazard Identification System                ║
╠══════════════════════════════════════════════════════════════════╣
║  Database: 30 Bahan Kimia | Kategori: 4 Tingkat Bahaya          ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def get_color_by_category(kategori):
    """Mengembalikan warna berdasarkan kategori bahaya."""
    colors = {
        "Sangat Berbahaya": Colors.RED + Colors.BOLD,
        "Berbahaya": Colors.YELLOW + Colors.BOLD,
        "Sedang": Colors.CYAN + Colors.BOLD,
        "Rendah": Colors.GREEN + Colors.BOLD
    }
    return colors.get(kategori, Colors.END)

def get_symbol_by_category(kategori):
    """Mengembalikan simbol berdasarkan kategori bahaya."""
    symbols = {
        "Sangat Berbahaya": "☠️  ",
        "Berbahaya": "⚠️  ",
        "Sedang": "⚡ ",
        "Rendah": "✅ "
    }
    return symbols.get(kategori, "❓ ")

def print_separator():
    """Mencetak garis pemisah."""
    print(f"{Colors.CYAN}{'─' * 70}{Colors.END}")

# ============================================================
# FUNGSI PENCARIAN
# ============================================================
def search_chemicals(query):
    """Mencari bahan kimia berdasarkan nama, rumus, atau nomor CAS."""
    query = query.lower().strip()
    results = []

    for chem in CHEMICALS:
        if (query in chem["nama"].lower() or 
            query in chem["rumus"].lower() or 
            query in chem["cas"].lower()):
            results.append(chem)

    return results

def filter_by_category(category):
    """Memfilter bahan kimia berdasarkan kategori bahaya."""
    return [chem for chem in CHEMICALS if chem["kategori"] == category]

def get_chemical_by_id(chem_id):
    """Mengambil bahan kimia berdasarkan ID."""
    for chem in CHEMICALS:
        if chem["id"] == chem_id:
            return chem
    return None

# ============================================================
# FUNGSI TAMPILAN
# ============================================================
def display_chemical_card(chem, index=None):
    """Menampilkan kartu informasi bahan kimia."""
    color = get_color_by_category(chem["kategori"])
    symbol = get_symbol_by_category(chem["kategori"])
    idx = f"[{index}] " if index is not None else ""

    print(f"\n{color}{symbol}{idx}{chem['nama']}{Colors.END}")
    print(f"   {Colors.BOLD}Rumus:{Colors.END} {chem['rumus']}")
    print(f"   {Colors.BOLD}CAS:{Colors.END} {chem['cas']}")
    print(f"   {Colors.BOLD}Kategori:{Colors.END} {color}{chem['kategori']}{Colors.END}")
    print(f"   {Colors.BOLD}Bahaya:{Colors.END} {chem['bahaya']}")

    if chem["pictogram"]:
        pictograms = ", ".join(chem["pictogram"])
        print(f"   {Colors.BOLD}Pictogram GHS:{Colors.END} {pictograms}")
    else:
        print(f"   {Colors.BOLD}Pictogram GHS:{Colors.END} Tidak ada")

    print(f"   {Colors.BOLD}Peringatan:{Colors.END} {Colors.YELLOW}{chem['peringatan']}{Colors.END}")
    print(f"   {Colors.BOLD}Penanganan:{Colors.END} {Colors.GREEN}{chem['penanganan']}{Colors.END}")

def display_search_results(results):
    """Menampilkan hasil pencarian."""
    if not results:
        print(f"\n{Colors.RED}❌ Tidak ditemukan bahan kimia yang cocok.{Colors.END}")
        return None

    print(f"\n{Colors.GREEN}✅ Ditemukan {len(results)} bahan kimia:{Colors.END}")
    print_separator()

    for i, chem in enumerate(results, 1):
        display_chemical_card(chem, i)

    return results

def display_statistics():
    """Menampilkan statistik database."""
    stats = {}
    for chem in CHEMICALS:
        stats[chem["kategori"]] = stats.get(chem["kategori"], 0) + 1

    print(f"\n{Colors.BOLD}{Colors.CYAN}📊 STATISTIK DATABASE{Colors.END}")
    print_separator()
    print(f"   Total Bahan Kimia: {len(CHEMICALS)}")
    print()

    for cat, count in stats.items():
        color = get_color_by_category(cat)
        symbol = get_symbol_by_category(cat)
        percentage = (count / len(CHEMICALS)) * 100
        bar = "█" * int(percentage / 2)
        print(f"   {symbol}{color}{cat:<20}{Colors.END} {count:>3} ({percentage:>5.1f}%) {bar}")

    print_separator()

# ============================================================
# FUNGSI SIMPAN HASIL
# ============================================================
def save_results_to_file(results, filename=None):
    """Menyimpan hasil pencarian ke file JSON."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hasil_pencarian_{timestamp}.json"

    filepath = os.path.join(os.getcwd(), filename)

    data = {
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "jumlah_hasil": len(results),
        "hasil": results
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n{Colors.GREEN}✅ Hasil pencarian disimpan ke: {filepath}{Colors.END}")
    return filepath

# ============================================================
# MENU UTAMA
# ============================================================
def show_main_menu():
    """Menampilkan menu utama."""
    print(f"""
{Colors.BOLD}{Colors.CYAN}📋 MENU UTAMA:{Colors.END}

   {Colors.GREEN}[1]{Colors.END} 🔍 Cari Bahan Kimia (Nama/Rumus/CAS)
   {Colors.GREEN}[2]{Colors.END} 📂 Lihat Semua Bahan Kimia
   {Colors.GREEN}[3]{Colors.END} ⚠️  Filter Berdasarkan Kategori Bahaya
   {Colors.GREEN}[4]{Colors.END} 📊 Statistik Database
   {Colors.GREEN}[5]{Colors.END} ℹ️  Tentang Pictogram GHS
   {Colors.GREEN}[0]{Colors.END} 🚪 Keluar
""")

def show_category_menu():
    """Menampilkan menu kategori."""
    print(f"""
{Colors.BOLD}{Colors.CYAN}⚠️  PILIH KATEGORI BAHAYA:{Colors.END}

   {Colors.RED}[1]{Colors.END} ☠️  Sangat Berbahaya (5 bahan)
   {Colors.YELLOW}[2]{Colors.END} ⚠️  Berbahaya (10 bahan)
   {Colors.CYAN}[3]{Colors.END} ⚡ Sedang (10 bahan)
   {Colors.GREEN}[4]{Colors.END} ✅ Rendah (5 bahan)
   {Colors.BOLD}[0]{Colors.END} 🔙 Kembali
""")

def show_ghs_info():
    """Menampilkan informasi tentang pictogram GHS."""
    print(f"""
{Colors.BOLD}{Colors.CYAN}ℹ️  TENTANG PICTOGRAM GHS (Globally Harmonized System){Colors.END}

{Colors.BOLD}GHS01 - Ledakan (Explosive){Colors.END}
   Bahan yang dapat menyebabkan ledakan

{Colors.BOLD}GHS02 - Mudah Terbakar (Flammable){Colors.END}
   Bahan yang mudah terbakar

{Colors.BOLD}GHS03 - Oksidator (Oxidizing){Colors.END}
   Bahan yang dapat menyebabkan atau mempercepat kebakaran

{Colors.BOLD}GHS04 - Gas Bertekanan (Compressed Gas){Colors.END}
   Gas yang disimpan dalam tekanan tinggi

{Colors.BOLD}GHS05 - Korosif (Corrosive){Colors.END}
   Bahan yang dapat merusak logam, kulit, atau mata

{Colors.BOLD}GHS06 - Beracun (Toxic){Colors.END}
   Bahan yang sangat beracun jika tertelan, terhirup, atau terserap kulit

{Colors.BOLD}GHS07 - Iritasi/Kesehatan (Health Hazard/Irritant){Colors.END}
   Bahan yang dapat menyebabkan iritasi atau efek kesehatan lainnya

{Colors.BOLD}GHS08 - Bahaya Kesehatan Serius (Serious Health Hazard){Colors.END}
   Bahan yang dapat menyebabkan kanker, mutagen, atau toksisitas reproduksi

{Colors.BOLD}GHS09 - Bahaya Lingkungan (Environmental Hazard){Colors.END}
   Bahan yang berbahaya bagi lingkungan/aquatik
""")

# ============================================================
# FUNGSI UTAMA APLIKASI
# ============================================================
def run_app():
    """Menjalankan aplikasi utama."""
    while True:
        clear_screen()
        print_banner()
        show_main_menu()

        choice = input(f"{Colors.BOLD}Pilih menu [0-5]: {Colors.END}").strip()

        if choice == '0':
            print(f"\n{Colors.GREEN}👋 Terima kasih telah menggunakan aplikasi ini. Tetap aman!{Colors.END}\n")
            break

        elif choice == '1':
            # Pencarian
            clear_screen()
            print_banner()
            print(f"{Colors.BOLD}{Colors.CYAN}🔍 CARI BAHAN KIMIA{Colors.END}")
            print_separator()
            query = input(f"\nMasukkan nama, rumus, atau nomor CAS: ").strip()

            if query:
                results = search_chemicals(query)
                display_search_results(results)

                if results:
                    save_choice = input(f"\n{Colors.BOLD}Simpan hasil ke file? (y/n): {Colors.END}").strip().lower()
                    if save_choice == 'y':
                        save_results_to_file(results)
            else:
                print(f"\n{Colors.RED}❌ Query tidak boleh kosong.{Colors.END}")

            input(f"\n{Colors.BOLD}Tekan Enter untuk kembali...{Colors.END}")

        elif choice == '2':
            # Lihat semua
            clear_screen()
            print_banner()
            print(f"{Colors.BOLD}{Colors.CYAN}📂 SEMUA BAHAN KIMIA ({len(CHEMICALS)} item){Colors.END}")
            print_separator()

            for i, chem in enumerate(CHEMICALS, 1):
                color = get_color_by_category(chem["kategori"])
                symbol = get_symbol_by_category(chem["kategori"])
                print(f"{color}{symbol}[{chem['id']:>2}] {chem['nama']:<35} {chem['rumus']:<15} {chem['kategori']}{Colors.END}")

            print(f"\n{Colors.GREEN}✅ Total: {len(CHEMICALS)} bahan kimia{Colors.END}")
            input(f"\n{Colors.BOLD}Tekan Enter untuk kembali...{Colors.END}")

        elif choice == '3':
            # Filter kategori
            clear_screen()
            print_banner()
            show_category_menu()

            cat_choice = input(f"{Colors.BOLD}Pilih kategori [0-4]: {Colors.END}").strip()

            categories = {
                '1': 'Sangat Berbahaya',
                '2': 'Berbahaya',
                '3': 'Sedang',
                '4': 'Rendah'
            }

            if cat_choice in categories:
                cat_name = categories[cat_choice]
                results = filter_by_category(cat_name)

                clear_screen()
                print_banner()
                print(f"{Colors.BOLD}{Colors.CYAN}⚠️  BAHAN KIMIA KATEGORI: {cat_name}{Colors.END}")
                print_separator()

                display_search_results(results)

                if results:
                    save_choice = input(f"\n{Colors.BOLD}Simpan hasil ke file? (y/n): {Colors.END}").strip().lower()
                    if save_choice == 'y':
                        save_results_to_file(results)

            elif cat_choice == '0':
                continue
            else:
                print(f"\n{Colors.RED}❌ Pilihan tidak valid.{Colors.END}")

            input(f"\n{Colors.BOLD}Tekan Enter untuk kembali...{Colors.END}")

        elif choice == '4':
            # Statistik
            clear_screen()
            print_banner()
            display_statistics()
            input(f"\n{Colors.BOLD}Tekan Enter untuk kembali...{Colors.END}")

        elif choice == '5':
            # Info GHS
            clear_screen()
            print_banner()
            show_ghs_info()
            input(f"\n{Colors.BOLD}Tekan Enter untuk kembali...{Colors.END}")

        else:
            print(f"\n{Colors.RED}❌ Pilihan tidak valid. Silakan coba lagi.{Colors.END}")
            input(f"\n{Colors.BOLD}Tekan Enter untuk melanjutkan...{Colors.END}")

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Aplikasi dihentikan oleh pengguna.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Terjadi kesalahan: {str(e)}{Colors.END}")
        sys.exit(1)
