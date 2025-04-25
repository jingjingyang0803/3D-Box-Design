import FreeCAD, Part

FreeCAD.newDocument('fingerHoleModule')
FreeCAD.Gui.runCommand('Std_DrawStyle', 6)

# ========================================================
# STEP 1: Dimensions
# ========================================================
# Bottom tab (for photodiode module clip)
bottom_width = 46.0-0.2
bottom_length = 30.0-0.2
bottom_height = 12.5

# Middle block (main body)
middle_width = 50.0
middle_length = 34.0
middle_height = 25.0

# Top tab (for LED module clip)
top_width = 46.0-0.2
top_length = 30.0-0.2
top_height = 10.0

# ========================================================
# STEP 2: Create Block Geometry (Bottom + Middle + Top)
# ========================================================
bottom_block = Part.makeBox(bottom_width, bottom_length, bottom_height,
                            FreeCAD.Vector(-bottom_width / 2, -bottom_length / 2, 0))

middle_block = Part.makeBox(middle_width, middle_length, middle_height,
                            FreeCAD.Vector(-middle_width / 2, -middle_length / 2, bottom_height))

top_block = Part.makeBox(top_width, top_length, top_height,
                         FreeCAD.Vector(-top_width / 2, -top_length / 2, bottom_height + middle_height))

block = bottom_block.fuse(middle_block).fuse(top_block)

# ========================================================
# STEP 3: Bottom Pocket (photodiode clip slot)
# ========================================================
bottom_cut_width = 30.0
bottom_cut_depth = 20.0
bottom_cut_height = bottom_height

bottom_cut = Part.makeBox(
    bottom_cut_width,
    bottom_cut_depth,
    bottom_cut_height,
    FreeCAD.Vector(-bottom_cut_width / 2, -bottom_cut_depth / 2, 0)
)

block = block.cut(bottom_cut)

# ========================================================
# STEP 4: Photodiode Light Hole (vertical hole in bottom)
# ========================================================
light_radius = 4.0
light_depth = 5.0  # cut through small gap below finger hole

light_hole = Part.makeCylinder(
    light_radius,
    light_depth,
    FreeCAD.Vector(0, 0, bottom_height),
    FreeCAD.Vector(0, 0, 1)
)

block = block.cut(light_hole)

# ========================================================
# STEP 5: Filter Pocket (below finger hole)
# ========================================================
filter_width = 18.0
filter_depth = 30.0
filter_height = 2.0

filter_origin = FreeCAD.Vector(
    -filter_width / 2,
    - filter_depth + middle_length / 2,
    bottom_height + 1  # centered in 4mm band
)

filter_cut = Part.makeBox(filter_width, filter_depth, filter_height, filter_origin)

block = block.cut(filter_cut)

# ========================================================
# STEP 6: Finger Hole (cylinder across Y-axis)
# ========================================================
finger_radius = 10.0
finger_length = middle_length
finger_center_z = bottom_height + 4 + finger_radius  # 4mm spacing above filter pocket

finger_hole = Part.makeCylinder(
    finger_radius,
    finger_length,
    FreeCAD.Vector(0, -finger_length / 2, finger_center_z),
    FreeCAD.Vector(0, 1, 0)  # horizontal cut
)

block = block.cut(finger_hole)

# ========================================================
# STEP 7: Humidity Sensor Pocket (slot cut on left side)
# ========================================================
side_pocket_width = 10.0
side_pocket_height = 18.0
side_pocket_depth = 27.0

side_pocket = Part.makeBox(
    side_pocket_width,
    side_pocket_depth,
    side_pocket_height,
    FreeCAD.Vector(
        - finger_radius - 1 - side_pocket_width,
        -middle_length / 2,
        finger_center_z - side_pocket_height / 2
    )
)

block = block.cut(side_pocket)

# ========================================================
# STEP 8: Humidity Sensor Window (left of finger hole)
# ========================================================
sensor_size = 7.0
sensor_depth = finger_radius + 1  # through wall thickness

sensor_cut = Part.makeBox(
    sensor_depth,
    sensor_size,
    sensor_size,
    FreeCAD.Vector(
        -sensor_depth,
        -sensor_depth / 2,
        finger_center_z - sensor_size / 2
    )
)

block = block.cut(sensor_cut)

# ========================================================
# STEP 9: Top Pocket (clip clearance)
# ========================================================
top_cut_width = top_width - 3.8
top_cut_depth = top_length - 3.8
top_cut_height = top_height

top_cut = Part.makeBox(
    top_cut_width,
    top_cut_depth,
    top_cut_height,
    FreeCAD.Vector(-top_cut_width / 2, -top_cut_depth / 2, bottom_height + middle_height)
)

block = block.cut(top_cut)

# ========================================================
# STEP 10: LED Light Window (top opening for 4 LEDs)
# ========================================================
led_window_width = 18.5
led_window_length = 18.5
led_window_height = 5.0  # vertical height

led_window = Part.makeBox(
    led_window_width,
    led_window_length,
    led_window_height,
    FreeCAD.Vector(
        -led_window_width / 2,
        -led_window_length / 2,
        bottom_height + middle_height - led_window_height # base of top tab
    )
)

block = block.cut(led_window)

# ========================================================
# STEP 11: Display the Final Model
# ========================================================
shape = Part.show(block, 'fingerHoleModule')
shape.ViewObject.Transparency = 20
shape.ViewObject.ShapeColor = (0.6, 0.6, 0.85)

FreeCAD.Gui.activeDocument().activeView().viewIsometric()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
