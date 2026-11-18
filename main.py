import random
import tkinter as tk
from tkinter import messagebox


# 1. Načítanie a kontrola vstupných dát z poľa Text (ošetrenie chýb)
def nacitaj_a_over_pole():
    surovy_text = vstup_pole.get("1.0", "end-1c").strip()

    if not surovy_text:
        messagebox.showwarning("Chyba vstupu", "Pole je prázdne! Zadajte čísla alebo kliknite na Random.")
        return None

    casti = surovy_text.split()
    cisla = []

    for prvok in casti:
        try:
            hodnota = float(prvok.replace(",", "."))
            cisla.append(hodnota)
        except ValueError:
            messagebox.showerror("Neplatný znak", f"Hodnota '{prvok}' nie je číslo!")
            return None

    return cisla


# 2. Generovanie náhodného poľa (tlačidlo Random)
def vygeneruj_nahodne():
    try:
        pocet = int(vstup_pocet.get())
        minimum = int(vstup_min.get())
        maximum = int(vstup_max.get())
    except ValueError:
        messagebox.showerror("Chyba", "Počet, Min a Max musia byť celé čísla!")
        return

    if pocet <= 0 or pocet > 100:
        messagebox.showwarning("Upozornenie", "Počet prvkov musí byť od 1 do 100.")
        return

    if minimum >= maximum:
        messagebox.showwarning("Upozornenie", "Minimum musí byť menšie ako Maximum.")
        return

    nahodne_pole = [random.randint(minimum, maximum) for _ in range(pocet)]
    vstup_pole.delete("1.0", tk.END)
    vstup_pole.insert("1.0", " ".join(str(x) for x in nahodne_pole))


# 3. Vlastný algoritmus triedenia poľa (Bubble Sort / Bublinkové triedenie)
def utried_pole_bubble(pole, vzostupne=True):
    arr = pole.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if vzostupne:
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            else:
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# 4. Hlavné spracovanie dát z poľa (štatistika + triedenie + filtrovanie)
def spracuj_data():
    pole = nacitaj_a_over_pole()
    if pole is None:
        return

    minimum = min(pole)
    maximum = max(pole)
    sucet = sum(pole)
    priemer = sucet / len(pole)

    # Triedenie poľa vzostupne (od najmenšieho) a zostupne (od najväčšieho)
    vzostupne = utried_pole_bubble(pole, vzostupne=True)
    zostupne = utried_pole_bubble(pole, vzostupne=False)

    # Rozdelenie prvkov nad priemer a pod priemer
    nad_priemerom = [x for x in pole if x > priemer]
    pod_priemerom = [x for x in pole if x < priemer]

    # Formátovanie výsledkov
    vystup = [
        f"Počet prvkov v poli: {len(pole)}",
        f"Súčet prvkov:        {sucet:.2f}",
        f"Minimum:             {minimum:.2f}",
        f"Maximum:             {maximum:.2f}",
        f"Priemer:             {priemer:.2f}",
        "-" * 55,
        f"Utriedené vzostupne: {vzostupne}",
        f"Utriedené zostupne:  {zostupne}",
        "-" * 55,
        f"Prvky nad priemerom ({len(nad_priemerom)}): {nad_priemerom}",
        f"Prvky pod priemerom ({len(pod_priemerom)}): {pod_priemerom}",
    ]

    vysledok_text.config(state="normal")
    vysledok_text.delete("1.0", tk.END)
    vysledok_text.insert(tk.END, "\n".join(vystup))
    vysledok_text.config(state="disabled")


# 5. Vymazanie polí
def vymaz_vsetko():
    vstup_pole.delete("1.0", tk.END)
    vysledok_text.config(state="normal")
    vysledok_text.delete("1.0", tk.END)
    vysledok_text.config(state="disabled")


# ================= GRAFICKÉ ROZHRANIE (GUI - Tkinter) =================
root = tk.Tk()
root.title("Spracovanie a triedenie poľa dát – Programovacie techniky")
root.geometry("680x560")
root.resizable(False, False)

# Nadpis
tk.Label(root, text="Spracovanie a triedenie číselného poľa", font=("Arial", 15, "bold")).pack(pady=10)

# Rám pre nastavenie generátora Random
frame_gen = tk.Frame(root)
frame_gen.pack(pady=5)

tk.Label(frame_gen, text="Počet:").grid(row=0, column=0, padx=5)
vstup_pocet = tk.Entry(frame_gen, width=6)
vstup_pocet.insert(0, "10")
vstup_pocet.grid(row=0, column=1, padx=5)

tk.Label(frame_gen, text="Min:").grid(row=0, column=2, padx=5)
vstup_min = tk.Entry(frame_gen, width=6)
vstup_min.insert(0, "1")
vstup_min.grid(row=0, column=3, padx=5)

tk.Label(frame_gen, text="Max:").grid(row=0, column=4, padx=5)
vstup_max = tk.Entry(frame_gen, width=6)
vstup_max.insert(0, "100")
vstup_max.grid(row=0, column=5, padx=5)

tk.Button(frame_gen, text="Random (Generovať)", command=vygeneruj_nahodne, bg="#e0e0e0").grid(row=0, column=6, padx=10)

# Vstupné pole Text
tk.Label(root, text="Zadajte čísla oddelené medzerou:").pack(anchor="w", padx=30, pady=(10, 2))
vstup_pole = tk.Text(root, height=4, width=75, font=("Consolas", 10))
vstup_pole.pack(padx=30)

# Tlačidlá akcií
frame_btns = tk.Frame(root)
frame_btns.pack(pady=12)

tk.Button(
    frame_btns, text="Spracovať a utriediť pole", command=spracuj_data,
    font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=24
).grid(row=0, column=0, padx=10)

tk.Button(
    frame_btns, text="Vymazať", command=vymaz_vsetko, width=12
).grid(row=0, column=1, padx=10)

# Výstupné pole Text
tk.Label(root, text="Výsledky spracovania a triedenia:").pack(anchor="w", padx=30, pady=(5, 2))
vysledok_text = tk.Text(root, height=13, width=75, font=("Consolas", 10), state="disabled", bg="#f7f7f7")
vysledok_text.pack(padx=30)

root.mainloop()
