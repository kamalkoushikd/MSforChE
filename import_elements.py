import json
import os
import django
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSforChE.settings')
django.setup()

# Import your Element model - adjust the import path as needed
from materials.models import Element

def import_elements():
    # Path to the JSON file
    json_file_path = 'materials/static/data/elements.json'
    
    # Load the JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Extract the rows from the JSON structure
    rows = data['Table']['Row']
    
    # Clear existing elements (optional)
    Element.objects.all().delete()
    
    # Process each element
    for row in rows:
        cells = row['Cell']
        
        # Create a new Element object
        element = Element(
            atomic_number=int(cells[0]),
            symbol=cells[1],
            name=cells[2],
            atomic_mass=cells[3],
            cpk_hex_color=cells[4] if cells[4] else None,
            electron_configuration=cells[5] if cells[5] else None,
            electronegativity=cells[6] if cells[6] else None,
            atomic_radius=cells[7] if cells[7] else None,
            ionization_energy=cells[8] if cells[8] else None,
            electron_affinity=cells[9] if cells[9] else None,
            oxidation_states=cells[10] if cells[10] else None,
            standard_state=cells[11] if cells[11] else None,
            melting_point=cells[12] if cells[12] else None,
            boiling_point=cells[13] if cells[13] else None,
            density=cells[14] if cells[14] else None,
            group_block=cells[15] if cells[15] else None,
            year_discovered=cells[16] if cells[16] else None
        )
        
        # Save the element to the database
        element.save()
        
        print(f"Imported element: {element.symbol} - {element.name}")
    
    print(f"Successfully imported {len(rows)} elements to the database.")

if __name__ == "__main__":
    import_elements()
