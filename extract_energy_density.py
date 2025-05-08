from ase.io import read
import pandas as pd
import os
import re

data = []

for i in range(1, 3):
    filename = f"cage_crystal_2_units{i}-opt.extxyz"

    if not os.path.isfile(filename):
        print(f"Missing: {filename}")
        continue

    try:
        atoms = read(filename)

        # extract energy 
        with open(filename, 'r') as f:
            header = f.readline()  # number of atoms
            second_line = f.readline()  # metadata line

        match = re.search(r'energy=([-+]?\d*\.\d+|\d+)', second_line)
        if match:
            energy = float(match.group(1))
        else:
            print(f"⚠️ Energy not found in: {filename}")
            energy = None

        volume = atoms.get_volume()
        mass = atoms.get_masses().sum()

        mass_g = mass * 1.66054e-24
        volume_cm3 = volume * 1e-24
        density = mass_g / volume_cm3

        data.append({
            "System": i,
            "Energy (eV)": energy,
            "Volume (Å³)": volume,
            "Mass (amu)": mass,
            "Density (g/cm³)": density
        })

    except Exception as e:
        print(f"Error with {filename}: {e}")

df = pd.DataFrame(data)
df.to_csv("ran_crys_data.csv", index=False)

print("Table successfully saved as data.csv")
