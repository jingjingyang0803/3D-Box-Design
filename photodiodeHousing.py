import FreeCAD, Part
import math

# -------------------------------------------------------
# Create new document and set shaded wireframe view
# -------------------------------------------------------
FreeCAD.newDocument('photodiodeHousingModule')
FreeCAD.Gui.runCommand('Std_DrawStyle', 6)

# -------------------------------------------------------
# 1. Outer Housing Box (34 x 50 x 14.5 mm)
# -------------------------------------------------------
housing_width = 34.0
housing_length = 50.0
housing_height = 14.5

housing_origin = FreeCAD.Vector(-housing_width / 2, -housing_length / 2, 0)
outer_housing = Part.makeBox(housing_width, housing_length, housing_height, housing_origin)

# -------------------------------------------------------
# 2. Internal Pocket (30.6 x 46.6 x 12.5 mm)
#     - Positioned inside the outer housing
#     - Wall thickness = 1.7 mm on each side:
#         -> pocket_width = 34.0 - 1.7*2 = 30.6
#         -> pocket_length = 50.0 - 1.7*2 = 46.6
#     - pocket_height = 14.5 housing height - 2 mm bottom plate thickness = 12.5 mm
# -------------------------------------------------------
pocket_width = 30.6
pocket_length = 46.6
pocket_height = 12.5


pocket_origin = FreeCAD.Vector(
    -pocket_width / 2,
    -pocket_length / 2,
    housing_height - pocket_height  # pocket starts below top
)

internal_pocket = Part.makeBox(pocket_width, pocket_length, pocket_height, pocket_origin)

# Subtract pocket from outer housing
model = outer_housing.cut(internal_pocket)

# -------------------------------------------------------
# 3. Photodiode Mounting Cylinder (Ø12 x 12.5 mm)
# -------------------------------------------------------
mount_radius = 6.0
mount_height = 12.5

mount_base = FreeCAD.Vector(0, 0, housing_height - pocket_height)
mount_cylinder = Part.makeCylinder(mount_radius, mount_height, mount_base)

model = model.fuse(mount_cylinder)

# -------------------------------------------------------
# 4. Photodiode Hole (Ø10.2 x 4.5 mm), cut from top
# -------------------------------------------------------
hole_radius = 5.1
hole_depth = 4.5

hole_top_z = housing_height - pocket_height + mount_height - hole_depth
hole_position = FreeCAD.Vector(0, 0, hole_top_z)

photodiode_hole = Part.makeCylinder(hole_radius, hole_depth, hole_position)

model = model.cut(photodiode_hole)

# -------------------------------------------------------
# 5. Photodiode Pin Holes (Ø1.2 mm, 2.54 mm from center)
# -------------------------------------------------------
pin_radius = 0.6
pin_spacing = 2.54
pin_depth = housing_height - hole_depth  # full depth

# Positions of two pins (same X, Y offset)
pin1_position = FreeCAD.Vector(0, pin_spacing, 0)
pin2_position = FreeCAD.Vector(0, -pin_spacing, 0)

pin1 = Part.makeCylinder(pin_radius, pin_depth, pin1_position)
pin2 = Part.makeCylinder(pin_radius, pin_depth, pin2_position)

model = model.cut(pin1)
model = model.cut(pin2)

# -------------------------------------------------------
# 6. Bump Pocket (rectangular notch at 135°, top-down)
# -------------------------------------------------------
bump_depth = 2.0          # depth into cylinder wall
bump_width = 1.5          # width along circumference
bump_height = 4.5         # height (cut from top down)
bump_angle_deg = 45      # angle around Z
bump_angle_rad = math.radians(bump_angle_deg)

# Calculate bump center on outer cylinder wall
bump_center_x = mount_radius * math.cos(bump_angle_rad)
bump_center_y = mount_radius * math.sin(bump_angle_rad)
bump_z = housing_height - pocket_height + mount_height - bump_height

bump_center = FreeCAD.Vector(bump_center_x, bump_center_y, bump_z)

# Position cutter box centered at bump
bump_origin = FreeCAD.Vector(
    bump_center_x - bump_depth / 2,
    bump_center_y - bump_width / 2,
    bump_z
)

bump_cutter = Part.makeBox(
    bump_depth,
    bump_width,
    bump_height,
    bump_origin
)

# Rotate around Z axis about its own center
bump_cutter.rotate(
    bump_center,
    FreeCAD.Vector(0, 0, 1),
    bump_angle_deg
)

model = model.cut(bump_cutter)

# -------------------------------------------------------
# 7. Show final model with color and transparency
# -------------------------------------------------------
shape = Part.show(model, 'photodiodeHousingModule')
shape.ViewObject.Transparency = 40
shape.ViewObject.ShapeColor = (0.2, 0.6, 0.8)

# View setup
FreeCAD.Gui.activeDocument().activeView().viewIsometric()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
