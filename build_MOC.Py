from pathlib import Path
import numpy as np
import stk
import os

def main() -> None:

    # Produce a Fe+2 atom with 6 functional groups.
    iron_atom = stk.BuildingBlock(
        smiles="[Fe+2]",
        functional_groups=(
            stk.SingleAtom(stk.Fe(0, charge=2)) for _ in range(6)
        ),
        position_matrix=np.array([[0, 0, 0]]),
    )

    # Define coordinating ligand with dummy bromine groups and
    # metal coordinating functional groups.
    oct_bb = stk.BuildingBlock(
        smiles="Br/N=C/C1=NC=C(OCCCS(=O)([O-])=O)C=C1",
        functional_groups=[
            stk.SmartsFunctionalGroupFactory(
                smarts="[#6]~[#7X2]~[#35]",
                bonders=(1,),
                deleters=(),
            ),
            stk.SmartsFunctionalGroupFactory(
                smarts="[#6]~[#7X2]~[#6]",
                bonders=(1,),
                deleters=(),
            ),
        ],
    )

    # Build iron complex with delta stereochemistry.
    iron_oct_delta_bb = stk.ConstructedMolecule(
        topology_graph=stk.metal_complex.OctahedralDelta(
            metals=iron_atom,
            ligands=oct_bb,
            optimizer=stk.MCHammer(),
        ),
    )

    # Assign Bromo functional groups to the metal complex.
    iron_oct_delta = stk.BuildingBlock.init_from_molecule(
        molecule=iron_oct_delta_bb,
        functional_groups=[stk.BromoFactory()],
    )

    # Define building block.
    bb3 = stk.BuildingBlock(
        smiles=("BrC1=CC=C(C(C)=C1)C2=CC=C(C=C2C)Br"),
        functional_groups=[stk.BromoFactory()],
    )

    # Build an M4L6 Tetrahedron
    cage10 = stk.ConstructedMolecule(
        topology_graph=stk.cage.M4L6TetrahedronSpacer(
            building_blocks=(
                iron_oct_delta,
                bb3,
            ),
            optimizer=stk.MCHammer(),
        ),
    )
    # Save the cage as an .xyz file on the desktop.
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, "cage10.xyz")
    cage10.write(file_path)

    print(f"Cage saved to {file_path}")

if __name__ == "__main__":
    main()