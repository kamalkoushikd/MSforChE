from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Element(models.Model):
    atomic_number = models.IntegerField(primary_key=True)
    symbol = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    atomic_mass = models.FloatField()
    cpk_hex_color = models.CharField(max_length=6, null=True, blank=True)
    electron_configuration = models.TextField(null=True, blank=True)
    electronegativity = models.FloatField(null=True, blank=True)
    atomic_radius = models.FloatField(null=True, blank=True)
    ionization_energy = models.FloatField(null=True, blank=True)
    electron_affinity = models.FloatField(null=True, blank=True)
    oxidation_states = models.CharField(max_length=50, null=True, blank=True)
    standard_state = models.CharField(max_length=50, null=True, blank=True)
    melting_point = models.FloatField(null=True, blank=True)
    boiling_point = models.FloatField(null=True, blank=True)
    density = models.FloatField(null=True, blank=True)
    group_block = models.CharField(max_length=50, null=True, blank=True)
    year_discovered = models.CharField(max_length=10,   null=True, blank=True)
    
    # New fields for periodic table positioning
    group_number = models.IntegerField(null=True, blank=True)
    period_number = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Calculate group and period before saving
        if self.group_number is None:
            self.group_number = self.calculate_group_number()
        if self.period_number is None:
            self.period_number = self.calculate_period_number()
        super().save(*args, **kwargs)
    
    def calculate_period_number(self):
        """Calculate the period number based on atomic number."""
        # Period number mapping based on atomic number ranges
        if self.atomic_number <= 2:
            return 1
        elif self.atomic_number <= 10:
            return 2
        elif self.atomic_number <= 18:
            return 3
        elif self.atomic_number <= 36:
            return 4
        elif self.atomic_number <= 54:
            return 5
        elif self.atomic_number <= 86:
            return 6
        elif self.atomic_number <= 118:
            return 7
        return None
    
    def calculate_group_number(self):
        """Calculate the group number based on atomic number and group block."""
        # Special case for Hydrogen
        if self.atomic_number == 1:
            return 1
        
        # Special case for Helium
        if self.atomic_number == 2:
            return 18
        
        # Handle elements with fixed positions
        element_group_map = {
            # Group 1 (alkali metals)
            3: 1, 11: 1, 19: 1, 37: 1, 55: 1, 87: 1,
            
            # Group 2 (alkaline earth metals)
            4: 2, 12: 2, 20: 2, 38: 2, 56: 2, 88: 2,
            
            # Group 13-18
            5: 13, 13: 13, 31: 13, 49: 13, 81: 13, 113: 13,  # Group 13
            6: 14, 14: 14, 32: 14, 50: 14, 82: 14, 114: 14,  # Group 14
            7: 15, 15: 15, 33: 15, 51: 15, 83: 15, 115: 15,  # Group 15
            8: 16, 16: 16, 34: 16, 52: 16, 84: 16, 116: 16,  # Group 16
            9: 17, 17: 17, 35: 17, 53: 17, 85: 17, 117: 17,  # Group 17
            10: 18, 18: 18, 36: 18, 54: 18, 86: 18, 118: 18,  # Group 18
            
            # Transition metals (groups 3-12)
            # Period 4
            21: 3, 22: 4, 23: 5, 24: 6, 25: 7, 26: 8, 27: 9, 28: 10, 29: 11, 30: 12,
            # Period 5
            39: 3, 40: 4, 41: 5, 42: 6, 43: 7, 44: 8, 45: 9, 46: 10, 47: 11, 48: 12,
            # Period 6 (excluding lanthanides)
            57: 3, 72: 4, 73: 5, 74: 6, 75: 7, 76: 8, 77: 9, 78: 10, 79: 11, 80: 12,
            # Period 7 (excluding actinides)
            89: 3, 104: 4, 105: 5, 106: 6, 107: 7, 108: 8, 109: 9, 110: 10, 111: 11, 112: 12,
        }
        
        # Lanthanides (atomic numbers 58-71) - traditionally placed in group 3
        if 58 <= self.atomic_number <= 71:
            return 3
        
        # Actinides (atomic numbers 90-103) - traditionally placed in group 3
        if 90 <= self.atomic_number <= 103:
            return 3
        
        # Return the group number from the mapping if it exists
        return element_group_map.get(self.atomic_number)
    
    @property
    def display_position(self):
        """Return a dictionary with the display position for the periodic table."""
        # Handle special positioning for lanthanides and actinides
        if 57 < self.atomic_number <= 71:  # Lanthanides
            return {
                'row': 8,
                'column': self.atomic_number - 54  # Start at column 3 (57-54=3)
            }
        elif 89 < self.atomic_number <= 103:  # Actinides
            return {
                'row': 9,
                'column': self.atomic_number - 86  # Start at column 3 (89-86=3)
            }
        else:
            return {
                'row': self.period_number,
                'column': self.group_number
            }


def get_or_create_user(firebase_user):
    uid = firebase_user['uid']
    email = firebase_user.get('email')
    user, created = User.objects.get_or_create(username=uid, defaults={'email': email})
    return user