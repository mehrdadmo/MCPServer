try:
    from src.main import app
    print("Successfully imported app from src.main")
except Exception as e:
    print(f"Error importing: {str(e)}")

class ClaudeIntegration:
    async def generate_revit_design(self, prompt: str):
        system_prompt = """
        You are an expert architectural designer working with Revit.
        Convert the following natural language description into detailed Revit elements.
        Include:
        - Room layouts and dimensions
        - Wall placements and properties
        - Door and window positions
        - Furniture placement
        - MEP systems basic layout
        Output the design in a structured format that can be processed by Revit.
        """
        
        try:
            response = await self.client.messages.create(
                model="claude-3-sonnet",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000
            )
            return self._parse_design_response(response)
        except Exception as e:
            raise Exception(f"Failed to generate design: {str(e)}") 

class RevitDesignCommand:
    def __init__(self):
        self.doc = __revit__.ActiveUIDocument.Document
        self.uidoc = __revit__.ActiveUIDocument
        self.api_client = APIClient()

    def create_floor_plan(self, design_data):
        with Transaction(self.doc, "Create AI Generated Design") as t:
            t.Start()
            try:
                # Create levels
                level = self._create_level(0.0, "Level 1")
                
                # Create rooms
                for room in design_data["rooms"]:
                    self._create_room(
                        level,
                        room["location"],
                        room["dimensions"],
                        room["name"]
                    )
                
                # Create walls
                for wall in design_data["walls"]:
                    self._create_wall(
                        level,
                        wall["start_point"],
                        wall["end_point"],
                        wall["height"],
                        wall["type"]
                    )
                
                # Add doors and windows
                self._add_openings(design_data["openings"])
                
                t.Commit()
            except Exception as e:
                t.RollBack()
                raise Exception(f"Failed to create design: {str(e)}") 

# User interaction in Revit
class AIDesignCommand:
    def Execute(self, commandData):
        try:
            # Show input dialog
            prompt = self.show_input_dialog()
            
            # Generate design
            design_data = await self.api_client.generate_design(prompt)
            
            # Create progress bar
            with ProgressBar("Creating Design") as pb:
                # Create floor plan
                self.create_floor_plan(design_data)
                
                # Add dimensions
                self.add_dimensions(design_data)
                
                # Add annotations
                self.add_annotations(design_data)
            
            # Show completion dialog
            self.show_completion_dialog()
            
        except Exception as e:
            self.show_error_dialog(str(e)) 

def process_natural_language(prompt: str):
    return {
        "rooms": extract_rooms(prompt),
        "dimensions": extract_dimensions(prompt),
        "style": extract_style(prompt),
        "relationships": extract_relationships(prompt)
    } 

def generate_design_specs(processed_data: Dict):
    return {
        "layout": generate_layout(processed_data),
        "elements": generate_elements(processed_data),
        "dimensions": calculate_dimensions(processed_data),
        "constraints": generate_constraints(processed_data)
    } 

def create_revit_elements(design_specs: Dict):
    with Transaction(doc, "Create AI Design") as t:
        t.Start()
        create_rooms(design_specs["layout"])
        create_walls(design_specs["elements"])
        create_openings(design_specs["elements"])
        add_furniture(design_specs["furniture"])
        t.Commit()