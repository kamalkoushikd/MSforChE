# your_app/management/commands/update_grid_positions.py
from django.core.management.base import BaseCommand
from materials.models import Element

class Command(BaseCommand):
    help = 'Updates grid positions for all elements'

    def handle(self, *args, **options):
        elements = Element.objects.all()
        
        for element in elements:
            # Default positioning
            element.grid_row = element.period_number
            element.grid_column = element.group_number
            
            # Special case for Lanthanides (57-71)
            if 57 <= element.atomic_number <= 71:
                element.grid_row = 8
                element.grid_column = element.atomic_number - 54
            
            # Special case for Actinides (89-103)
            elif 89 <= element.atomic_number <= 103:
                element.grid_row = 9
                element.grid_column = element.atomic_number - 86
                
            element.save(update_fields=['grid_row', 'grid_column'])
            
        self.stdout.write(self.style.SUCCESS(f'Updated grid positions for {elements.count()} elements'))