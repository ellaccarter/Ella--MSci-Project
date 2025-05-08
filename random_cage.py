from pyxtal import pyxtal
from pyxtal.molecule import pyxtal_molecule
from pyxtal.lattice import Lattice
import os

# Load two cage molecules
my_crystal_1 = pyxtal_molecule('/Users/ella/Desktop/final_opt_sulf_cage.xyz')
my_crystal_2 = pyxtal_molecule('/Users/ella/Desktop/final_opt_me_cage.xyz')

# create output folder on Desktop
output_folder = "/Users/ella/Desktop/1000_pyxtal_structures"
os.makedirs(output_folder, exist_ok=True)

# Create a PyXtal object for molecular crystal generation
c1 = pyxtal(molecular=True)

# Define a cubic unit cell with 45 Å sides
l2 = Lattice.from_para(45, 45, 45, 90, 90, 90)

# Generate 10 random packings
x = 1
while x <= 1000:
    try:
        # Generate a 3D molecular crystal in space group 1
        c1.from_random(3, 1, [my_crystal_1, my_crystal_2], [2, 1], lattice=l2)

        # Convert to ASE object
        ase_c1 = c1.to_ase()

        # Save as both .xyz and .cif in the Desktop folder
        xyz_filename = os.path.join(output_folder, f'cage_crystal_sys1_{x}.xyz')
        cif_filename = os.path.join(output_folder, f'cage_crystal_sys1_{x}.cif')
        ase_c1.write(xyz_filename, format='extxyz')
        ase_c1.write(cif_filename, format='cif')

        print(f"Saved structure {x} to Desktop.")
        x += 1
    except Exception as e:
        print(f"Structure {x} failed: {e}")

