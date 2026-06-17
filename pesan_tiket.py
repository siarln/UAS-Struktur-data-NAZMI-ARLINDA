import csv
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_CSV = os.path.join(BASE_DIR, "pesanan_tiket.csv")


# ==========================
# KELAS DATA PESANAN
# ==========================
class PesananTiket:
    def __init__(self, kode, nama, tujuan, jadwal, kursi):
        self.kode = kode
        self.nama = nama
        self.tujuan = tujuan
        self.jadwal = jadwal
        self.kursi = kursi


# ==========================
# STRUKTUR DATA
# Stack + Hash Map
# ==========================
class StackTiket:
    def __init__(self):
        self.tumpukan = []
        self.indeks_kode = {}

    # CREATE
    def pesan_tiket(self, pesanan):
        self.tumpukan.append(pesanan)
        self.indeks_kode[pesanan.kode] = pesanan

    # READ
    def semua_pesanan(self):
        return self.tumpukan.copy()

    # SEARCHING
    def cari_kode(self, kode):
        return self.indeks_kode.get(kode)

    # UPDATE
    def update_pesanan(self, kode, nama, tujuan, jadwal, kursi):
        pesanan = self.cari_kode(kode)

        if pesanan:
            pesanan.nama = nama
            pesanan.tujuan = tujuan
            pesanan.jadwal = jadwal
            pesanan.kursi = kursi
            return True

        return False

    # DELETE
    def hapus_pesanan(self, kode):
        pesanan = self.cari_kode(kode)

        if pesanan:
            self.tumpukan.remove(pesanan)
            del self.indeks_kode[kode]
            return True

        return False

    # SORTING
    def urutkan_jadwal(self):
        return sorted(
            self.tumpukan,
            key=lambda x: datetime.strptime(
                x.jadwal,
                "%d-%m-%Y %H:%M"
            )
        )


# ==========================
# CSV
# ==========================
def muat_dari_csv():
    data = StackTiket()

    try:
        with open(FILE_CSV, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:
                data.pesan_tiket(PesananTiket(*row))

    except FileNotFoundError:
        with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    "kode",
                    "nama",
                    "tujuan",
                    "jadwal",
                    "kursi"
                ]
            )

    return data


def simpan_ke_csv(data):
    with open(FILE_CSV, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "kode",
                "nama",
                "tujuan",
                "jadwal",
                "kursi"
            ]
        )

        for p in data.semua_pesanan():
            writer.writerow(
                [
                    p.kode,
                    p.nama,
                    p.tujuan,
                    p.jadwal,
                    p.kursi
                ]
            )


# ==========================
# GENERATOR KODE TIKET
# ==========================
def generate_kode(data):

    daftar = data.semua_pesanan()

    if not daftar:
        return "TKT0001"

    nomor_terbesar = max(
        int(p.kode[3:])
        for p in daftar
    )

    return f"TKT{nomor_terbesar + 1:04d}"


# ==========================
# MENU
# ==========================
def menu_sistem():

    data = muat_dari_csv()

    while True:

        print("\n")
        print("=" * 45)
        print(" SISTEM PEMESANAN TIKET TRANSPORTASI ")
        print("=" * 45)

        print("1. Tambah Pesanan")
        print("2. Lihat Semua Pesanan")
        print("3. Cari Tiket")
        print("4. Update Tiket")
        print("5. Hapus Tiket")
        print("6. Urutkan Jadwal")
        print("0. Keluar")

        pilihan = input("Pilih Menu : ")

        # CREATE
        if pilihan == "1":

            kode = generate_kode(data)

            nama = input("Nama Penumpang : ")
            tujuan = input("Tujuan : ")
            jadwal = input(
                "Jadwal (dd-mm-yyyy hh:mm) : "
            )
            kursi = input("Nomor Kursi : ")

            data.pesan_tiket(
                PesananTiket(
                    kode,
                    nama,
                    tujuan,
                    jadwal,
                    kursi
                )
            )

            simpan_ke_csv(data)

            print(f"\nTiket berhasil dibuat.")
            print(f"Kode Tiket : {kode}")

        # READ
        elif pilihan == "2":

            daftar = data.semua_pesanan()

            if not daftar:
                print("\nBelum ada pesanan.")

            else:
                print("\nDAFTAR PESANAN")

                for p in daftar:

                    print(
                        f"{p.kode} | "
                        f"{p.nama} | "
                        f"{p.tujuan} | "
                        f"{p.jadwal} | "
                        f"Kursi {p.kursi}"
                    )

        # SEARCH
        elif pilihan == "3":

            kode = input(
                "Masukkan kode tiket : "
            )

            hasil = data.cari_kode(kode)

            if hasil:

                print("\nDATA DITEMUKAN")
                print(f"Kode   : {hasil.kode}")
                print(f"Nama   : {hasil.nama}")
                print(f"Tujuan : {hasil.tujuan}")
                print(f"Jadwal : {hasil.jadwal}")
                print(f"Kursi  : {hasil.kursi}")

            else:
                print("Data tidak ditemukan.")

        # UPDATE
        elif pilihan == "4":

            kode = input(
                "Kode tiket yang diubah : "
            )

            tiket = data.cari_kode(kode)

            if tiket:

                nama = input("Nama Baru : ")
                tujuan = input("Tujuan Baru : ")
                jadwal = input(
                    "Jadwal Baru : "
                )
                kursi = input(
                    "Nomor Kursi Baru : "
                )

                data.update_pesanan(
                    kode,
                    nama,
                    tujuan,
                    jadwal,
                    kursi
                )

                simpan_ke_csv(data)

                print(
                    "Data berhasil diperbarui."
                )

            else:
                print("Data tidak ditemukan.")

        # DELETE
        elif pilihan == "5":

            kode = input(
                "Kode tiket yang dihapus : "
            )

            if data.hapus_pesanan(kode):

                simpan_ke_csv(data)

                print(
                    "Data berhasil dihapus."
                )

            else:
                print("Data tidak ditemukan.")

        # SORTING
        elif pilihan == "6":

            urut = data.urutkan_jadwal()

            if not urut:

                print("Belum ada data.")

            else:

                print(
                    "\nJADWAL KEBERANGKATAN"
                )

                for p in urut:

                    print(
                        f"{p.jadwal} | "
                        f"{p.nama} | "
                        f"{p.tujuan}"
                    )

        elif pilihan == "0":

            print(
                "\nTerima kasih telah menggunakan sistem."
            )

            break

        else:
            print(
                "\nPilihan tidak valid."
            )


# ==========================
# MAIN PROGRAM
# ==========================
if __name__ == "__main__":
    menu_sistem()