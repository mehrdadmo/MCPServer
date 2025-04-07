import clr
import json
import logging
from System import Array
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.Attributes import *
from revit_plugin.claude_integration import ClaudeIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

[Transaction(TransactionMode.Manual)]
class AIDesignCommand(IExternalCommand):
    def __init__(self):
        self.claude = ClaudeIntegration()
    
    def Execute(self, commandData):
        try:
            # Show input dialog
            description = self.show_input_dialog()
            if not description:
                return Result.Cancelled
            
            # Extract requirements
            requirements = self.claude.extract_requirements(description)
            
            # Generate design
            model_data = self.claude.generate_model(description, requirements)
            
            # Create floor plan
            doc = commandData.Application.ActiveUIDocument.Document
            with Transaction(doc, "Create AI Design") as t:
                t.Start()
                
                # Create level if needed
                level = self._get_or_create_level(doc, "Level 1")
                
                # Create rooms
                for room_data in model_data["rooms"]:
                    self._create_room(doc, room_data, level)
                
                # Create walls
                for wall_data in model_data["walls"]:
                    self._create_wall(doc, wall_data, level)
                
                # Add openings
                self._add_openings(doc, model_data["openings"])
                
                # Add dimensions
                self._add_dimensions(doc)
                
                # Add annotations
                self._add_annotations(doc)
                
                t.Commit()
            
            # Show completion dialog
            self.show_completion_dialog()
            return Result.Succeeded
            
        except Exception as e:
            logger.error(f"Error executing AI design command: {str(e)}")
            TaskDialog.Show("Error", f"An error occurred: {str(e)}")
            return Result.Failed
    
    def _get_or_create_level(self, doc, level_name):
        """Get existing level or create new one"""
        collector = FilteredElementCollector(doc)
        levels = collector.OfClass(Level).ToElements()
        
        for level in levels:
            if level.Name == level_name:
                return level
        
        # Create new level
        return Level.Create(doc, 0)
    
    def _create_room(self, doc, room_data, level):
        """Create a room with specified parameters"""
        # Create room boundary
        curve_loop = CurveLoop()
        
        # Create walls for room boundary
        points = []
        for element in room_data["elements"]:
            if element["type"] == "wall":
                start = XYZ(
                    element["parameters"]["Location"]["x"],
                    element["parameters"]["Location"]["y"],
                    level.Elevation
                )
                points.append(start)
        
        # Create room
        room = doc.Create.NewRoom(level, curve_loop)
        room.Number = room_data["name"]
        room.Area = room_data["area"]
        
        # Set room parameters
        for param_name, value in room_data.get("parameters", {}).items():
            param = room.LookupParameter(param_name)
            if param and not param.IsReadOnly:
                param.Set(value)
    
    def _create_wall(self, doc, wall_data, level):
        """Create a wall with specified parameters"""
        start_point = XYZ(
            wall_data["start_point"]["x"],
            wall_data["start_point"]["y"],
            level.Elevation
        )
        
        end_point = XYZ(
            wall_data["end_point"]["x"],
            wall_data["end_point"]["y"],
            level.Elevation
        )
        
        line = Line.CreateBound(start_point, end_point)
        
        # Get wall type
        wall_type = self._get_wall_type(doc, wall_data["type"])
        
        # Create wall
        wall = Wall.Create(
            doc,
            line,
            wall_type.Id,
            level.Id,
            wall_data["height"],
            0.0,
            False,
            False
        )
        
        # Set wall parameters
        for param_name, value in wall_data.get("parameters", {}).items():
            param = wall.LookupParameter(param_name)
            if param and not param.IsReadOnly:
                param.Set(value)
    
    def _get_wall_type(self, doc, wall_type_name):
        """Get wall type by name"""
        collector = FilteredElementCollector(doc)
        wall_types = collector.OfClass(WallType).ToElements()
        
        for wall_type in wall_types:
            if wall_type.Name == wall_type_name:
                return wall_type
        
        # Return default wall type if not found
        return wall_types.First()
    
    def _add_openings(self, doc, openings_data):
        """Add doors and windows"""
        for opening_data in openings_data:
            if opening_data["type"] == "door":
                self._create_door(doc, opening_data)
            elif opening_data["type"] == "window":
                self._create_window(doc, opening_data)
    
    def _create_door(self, doc, door_data):
        """Create a door"""
        # Get door family
        door_family = self._get_door_family(doc)
        
        # Create door instance
        location = XYZ(
            door_data["location"]["x"],
            door_data["location"]["y"],
            door_data["location"]["z"]
        )
        
        door = doc.Create.NewFamilyInstance(
            location,
            door_family,
            StructuralType.NonStructural
        )
        
        # Set door parameters
        door.LookupParameter("Width").Set(door_data["width"])
        door.LookupParameter("Height").Set(door_data["height"])
    
    def _create_window(self, doc, window_data):
        """Create a window"""
        # Get window family
        window_family = self._get_window_family(doc)
        
        # Create window instance
        location = XYZ(
            window_data["location"]["x"],
            window_data["location"]["y"],
            window_data["location"]["z"]
        )
        
        window = doc.Create.NewFamilyInstance(
            location,
            window_family,
            StructuralType.NonStructural
        )
        
        # Set window parameters
        window.LookupParameter("Width").Set(window_data["width"])
        window.LookupParameter("Height").Set(window_data["height"])
    
    def _get_door_family(self, doc):
        """Get door family"""
        collector = FilteredElementCollector(doc)
        door_families = collector.OfClass(Family).ToElements()
        
        for family in door_families:
            if family.FamilyCategory.Id.IntegerValue == int(BuiltInCategory.OST_Doors):
                return family
        return None
    
    def _get_window_family(self, doc):
        """Get window family"""
        collector = FilteredElementCollector(doc)
        window_families = collector.OfClass(Family).ToElements()
        
        for family in window_families:
            if family.FamilyCategory.Id.IntegerValue == int(BuiltInCategory.OST_Windows):
                return family
        return None
    
    def _add_dimensions(self, doc):
        """Add dimensions to the floor plan"""
        # Get all walls
        collector = FilteredElementCollector(doc)
        walls = collector.OfClass(Wall).ToElements()
        
        # Create dimension lines
        for wall in walls:
            location = wall.Location
            if isinstance(location, LocationCurve):
                line = location.Curve
                dimension = doc.Create.NewDimension(
                    doc.ActiveView,
                    line,
                    Array[ElementId]([wall.Id])
                )
    
    def _add_annotations(self, doc):
        """Add room tags and other annotations"""
        # Get all rooms
        collector = FilteredElementCollector(doc)
        rooms = collector.OfClass(SpatialElement).ToElements()
        
        # Add room tags
        for room in rooms:
            if room.Area > 0:
                tag = doc.Create.NewRoomTag(
                    LinkElementId(room.Id),
                    room.Location.Point,
                    doc.ActiveView.Id
                )
    
    def show_input_dialog(self):
        """Show dialog for user input"""
        dialog = TaskDialog("AI Design")
        dialog.Title = "Enter Design Requirements"
        dialog.MainContent = "Please describe the design you want to create:"
        dialog.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel
        
        # Add text input
        dialog.AddCommandLink(TaskDialogCommandLinkId.CommandLink1, "Enter description...")
        
        result = dialog.Show()
        
        if result == TaskDialogResult.CommandLink1:
            return dialog.MainContent
        return None
    
    def show_completion_dialog(self):
        """Show completion dialog"""
        dialog = TaskDialog("AI Design")
        dialog.Title = "Design Complete"
        dialog.MainContent = "The AI-generated design has been created successfully!"
        dialog.CommonButtons = TaskDialogCommonButtons.Ok
        dialog.Show() 