from firebase_admin import auth
from django.http import JsonResponse
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.core import Structure
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings
def get_graph(name):
    model_path = os.path.join(settings.BASE_DIR, "materials","static", "models", f"{name}.cif")  
    try:
        # Load structure
        structure = Structure.from_file(model_path)
        
        # Get standard pattern first
        calculator = XRDCalculator()
        pattern = calculator.get_pattern(structure)
        
        # Create a finer x-axis (2θ values)
        x_fine = np.linspace(0, 90, 1000)
        
        # Function to calculate peak shape (pseudo-Voigt profile)
        def peak_shape(x, center, intensity, fwhm=0.1):
            gamma = fwhm / 2
            return intensity * (gamma**2 / ((x - center)**2 + gamma**2))
        
        # Calculate smoother pattern by summing contributions from each peak
        y_fine = np.zeros_like(x_fine)
        for i in range(len(pattern.x)):
            y_fine += peak_shape(x_fine, pattern.x[i], pattern.y[i])
        
        # Plot result
        # plt.savefig(f"static/images/{name}.png", dpi=300)
        
        print("Alternative XRD pattern successfully generated!")
        return x_fine, y_fine
    except Exception as e:
        print(f"Alternative method also failed: {str(e)}")

if __name__ == "__main__":
    name = input("Enter the name of the CIF file: ")
    get_graph(name)