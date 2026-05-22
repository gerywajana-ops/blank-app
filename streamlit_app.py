import streamlit as st
import random

def main():
    print("=== Welcome to the Number Guessing Game ===")
    print("Saya memikirkan angka antara 1 sampai 100.")
    
    # Komputer memilih angka acak
    angka_rahasia = random.randint(1, 100)
    percobaan = 0
    menang = False

    while not menang:
        try:
            tebakan = int(input("\nMasukkan tebakanmu: "))
            percobaan += 1

            if tebakan < angka_rahasia:
                print("Terlalu rendah! Coba lagi.")
            elif tebakan > angka_rahasia:
                print("Terlalu tinggi! Coba lagi.")
            else:
                print(f"SELAMAT! Kamu berhasil menebak angka {angka_rahasia} dalam {percobaan} percobaan.")
                menang = True
        except ValueError:
            print("Tolong masukkan angka yang valid!")

if __name__ == "__main__":
    main()
