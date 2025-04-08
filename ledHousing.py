import FreeCAD, Part, math

FreeCAD.newDocument('ledHousingModule')
FreeCAD.Gui.runCommand('Std_DrawStyle', 6)

# ---------------------------------------
# 0. General Dimensions
# ---------------------------------------
box_width = 34.0          # Full width of outer housing
box_length = 50.0         # Full length of outer housing
box_height = 16.0         # Full height of outer housing

wall_thickness = 2.0      # Wall thickness on all sides
base_thickness = 6.0     # Internal platform starts at this height

# LED parameters
tilt_angle_deg = 12.4                          # LED tilt from vertical axis
tilt_angle_rad = math.radians(tilt_angle_deg)  # Tilt angle in radians
led_distance = 8.0                             # Distance from center to LED center
led_plane_z = 5.0                             # Height of LED plane center (before tilt)

# LED cylinder geometry
led_radius = 3.2
led_depth = 11.0

# LED pin geometry
pin_radius = 0.7
pin_spacing = 2.54                             # Distance between the two LED pins
pin_depth_actual = 8.0                        # Fixed pin hole depth

# Inner cavity dimensions
inner_width = box_width - 2 * wall_thickness
inner_length = box_length - 2 * wall_thickness
inner_height = box_height - base_thickness     # From platform top to housing top

# ---------------------------------------
# 1. Create outer shell and subtract inner cavity
# ---------------------------------------
outer_box = Part.makeBox(box_width, box_length, box_height,
                         FreeCAD.Vector(-box_width / 2, -box_length / 2, 0))

inner_box = Part.makeBox(inner_width, inner_length, inner_height,
                         FreeCAD.Vector(-inner_width / 2, -inner_length / 2, base_thickness))

housing = outer_box.cut(inner_box)

# ---------------------------------------
# 2. Create internal platform block inside cavity
# ---------------------------------------
platform_width = box_width - 8
platform_length = box_length - 8
platform_origin = FreeCAD.Vector(-platform_width / 2, -platform_length / 2, base_thickness)

inner_platform = Part.makeBox(platform_width, platform_length, inner_height, platform_origin)
housing = housing.fuse(inner_platform)

# ---------------------------------------
# 3. Create LED holes and pin holes (oriented with tilt)
# ---------------------------------------
holes = []
target_point = FreeCAD.Vector(0, 0, 36.5)  # All LEDs point to this top convergence point

for i in range(4):
    angle_deg = i * 90                      # 0°, 90°, 180°, 270°
    angle_rad = math.radians(angle_deg)

    # LED center in 3D space, positioned on tilted circular plane
    led_center = FreeCAD.Vector(
        led_distance * math.cos(angle_rad) * math.cos(tilt_angle_rad),
        led_distance * math.sin(angle_rad) * math.cos(tilt_angle_rad),
        led_plane_z + led_distance * math.sin(tilt_angle_rad)
    )

    # Direction of LED beam pointing to central target
    beam_direction = (target_point - led_center).normalize()

    # Create main LED beam hole (cylinder along beam direction)
    led_hole = Part.makeCylinder(led_radius, led_depth, led_center, beam_direction)
    holes.append(led_hole)

    # Determine the pin offset direction perpendicular to beam (in tilted plane)
    z_axis = FreeCAD.Vector(0, 0, 1)
    pin_line_direction = z_axis.cross(beam_direction).normalize()

    pin_offset = pin_spacing / 2  # Half spacing from center to each pin

    for offset in [-pin_offset, pin_offset]:
        # Position each pin center along the pin line (in tilted plane)
        pin_center = FreeCAD.Vector(
            led_center.x + offset * math.cos(tilt_angle_rad) * math.sin(angle_rad),
            led_center.y + offset * math.cos(tilt_angle_rad) * math.cos(angle_rad),
            led_center.z
        )

        # Flip the direction for one of the pins
        pin_direction = beam_direction.multiply(-1 if offset < 0 else 1)

        # Create pin hole as a cylinder from pin center along direction
        pin_hole = Part.makeCylinder(pin_radius, pin_depth_actual, pin_center, pin_direction)
        holes.append(pin_hole)

# ---------------------------------------
# 4. Subtract all LED and pin holes from the housing
# ---------------------------------------
for hole in holes:
    housing = housing.cut(hole)

# ---------------------------------------
# 5. Create visual debug planes at LED levels
# ---------------------------------------
plane_size = 50.0
plane_thickness = 0.1

# Plane at Z = base LED tilt origin
plane = Part.makeBox(plane_size, plane_size, plane_thickness,
                     FreeCAD.Vector(-plane_size / 2, -plane_size / 2, led_plane_z))

# Plane at actual LED hole height
plane2 = Part.makeBox(plane_size, plane_size, plane_thickness,
                      FreeCAD.Vector(-plane_size / 2, -plane_size / 2,
                                     led_plane_z + led_distance * math.sin(tilt_angle_rad)))

plane_shape = Part.show(plane, 'Z10Plane')
led_plane_shape = Part.show(plane2, 'Z_Top_Circle_Ref')
plane_shape.ViewObject.ShapeColor = (1.0, 0.3, 0.3)
plane_shape.ViewObject.Transparency = 85
led_plane_shape.ViewObject.ShapeColor = (0.6, 0.1, 0.7)
led_plane_shape.ViewObject.Transparency = 0

# ---------------------------------------
# 6. Display final housing model
# ---------------------------------------
shape = Part.show(housing, 'ledHousingModule')
shape.ViewObject.Transparency = 40
shape.ViewObject.ShapeColor = (0.8, 0.8, 0.4)

FreeCAD.Gui.activeDocument().activeView().viewIsometric()
FreeCAD.Gui.SendMsgToActiveView("ViewFit")
