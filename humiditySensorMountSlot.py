import FreeCAD, Part

# Create a new FreeCAD document and set visual style
FreeCAD.newDocument('HumiditySensorMountModule')
FreeCAD.Gui.runCommand('Std_DrawStyle', 6)

# -------------------------------
# 1. Base Plate (13 x 22 x 2 mm)
# -------------------------------
base_plate_width = 13.0               # 14.0 - 1 mm trimming
base_plate_length = 22.0
base_plate_thickness = 2.0

#  Positioned slightly offset to the left (X) and centered on Y, bottom at Z=0
base_plate_origin = FreeCAD.Vector(
    -(base_plate_width - 1) / 2,
    -base_plate_length / 2,
    0
)

base_plate = Part.makeBox(
    base_plate_width,
    base_plate_length,
    base_plate_thickness,
    base_plate_origin
)

# -----------------------------------------------
# 2. Mounting Block (9.6 x 17.6 x 5 mm) on top of base
# -----------------------------------------------
mount_block_width = 9.6
mount_block_length = 17.6
mount_block_height = 5.0

mount_block_origin = FreeCAD.Vector(
    -mount_block_width / 2,
    -mount_block_length / 2,
    base_plate_thickness  # starts on top of base plate
)

mount_block = Part.makeBox(
    mount_block_width,
    mount_block_length,
    mount_block_height,
    mount_block_origin
)

# ---------------------------------------------------------
# 3. Sensor Pocket (3 x 8 x 7 mm) subtracted from mounting block
# ---------------------------------------------------------
pocket_width = 3.0
pocket_length = 8.0
pocket_depth = 7.0  # goes through base plate + mounting block

# Positioned slightly offset to the left (X) and centered on Y
sensor_pocket_origin = FreeCAD.Vector(
    -pocket_width / 2 - 1,         # shifted -1mm on X
    -pocket_length / 2,            # centered on Y
    0                              # starts on bottom of the base plate
)

sensor_pocket = Part.makeBox(
    pocket_width,
    pocket_length,
    pocket_depth,
    sensor_pocket_origin
)

# -------------------------------
# Combine and apply the cut
# -------------------------------
model = base_plate.fuse(mount_block)
model = model.cut(sensor_pocket)

# -------------------------------
# Display the result in FreeCAD
# -------------------------------
shape = Part.show(model, 'HumiditySensorMountModule')
shape.ViewObject.Transparency = 40    # 0 = solid, 100 = fully transparent
shape.ViewObject.ShapeColor = (0.2, 0.6, 0.8)  # soft blue color

# Auto-fit and set to isometric view
FreeCAD.Gui.activeDocument().activeView().viewIsometric()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
