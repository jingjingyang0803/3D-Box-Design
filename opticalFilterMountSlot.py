import FreeCAD, Part

# -------------------------------------------------------
# Create new FreeCAD document and set shaded wireframe
# -------------------------------------------------------
FreeCAD.newDocument('opticalFilterMountModule')
FreeCAD.Gui.runCommand('Std_DrawStyle', 6)

# -------------------------------------------------------
# 1. Filter Mount Block (17.8 x 1.9 x 29.8 mm)
#     - Centered at (0, 0), starts at Z = 0
# -------------------------------------------------------
mount_width =  17.8       # along X
mount_length = 1.9      # along Y
mount_height = 29.8      # along Z

mount_origin = FreeCAD.Vector(
    -mount_width / 2,
    -mount_length / 2,
    0
)


mount = Part.makeBox(
    mount_width,
    mount_length,
    mount_height,
    mount_origin
)

# -------------------------------------------------------
# 2. Base Plate (35 x 60.5 x 2 mm)
#     - Shifted so the base is offset at X = 7.5, Y = -13.75 from mount center
# -------------------------------------------------------
base_width = 35.0
base_length = 60.5
base_height = 2.0

plate_offset_x = 7.5
plate_offset_y = -13.75

plate_origin = FreeCAD.Vector(
    -base_width / 2 + plate_offset_x,
    -base_length / 2 + plate_offset_y,
    -base_height  # moved to be under the mount: Z = -2
)

plate = Part.makeBox(
    base_width,
    base_length,
    base_height,
    plate_origin
)

# Combine base and mount
model = plate.fuse(mount)

# -------------------------------------------------------
# 3. Horizontal Cylinder Hole (for optical filter)
#     - Centered on mount
#     - 17 mm up from base plate (Z=2)
# -------------------------------------------------------
hole_radius = 7.2
hole_length = mount_length + 0.2

hole_center_x = 0
hole_center_z = base_height + 17  # from bottom

hole_position = FreeCAD.Vector(
    hole_center_x,
    -1,  # slightly inside for guaranteed cut
    hole_center_z
)

hole_direction = FreeCAD.Vector(0, 1, 0)  # Y direction

hole_cylinder = Part.makeCylinder(hole_radius, hole_length, hole_position, hole_direction)
model = model.cut(hole_cylinder)

# -------------------------------------------------------
# 4. Show Result in FreeCAD
# -------------------------------------------------------
shape = Part.show(model, 'opticalFilterMountModule')
shape.ViewObject.Transparency = 0
shape.ViewObject.ShapeColor = (0.2, 0.6, 0.8)

FreeCAD.Gui.activeDocument().activeView().viewIsometric()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
