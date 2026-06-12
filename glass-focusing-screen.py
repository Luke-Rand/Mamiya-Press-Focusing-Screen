import cadquery as cq
import math

# ==========================================
# PARAMETRIC PARAMETERS (All sizes in mm)
# ==========================================
# Mamiya Press M-Adapter reference dimensions
outer_width = 111.0       # Complete horizontal width of the insert
outer_height = 86.5       # Complete vertical height of the insert
plate_thickness = 6.0     # Depth required to seat securely in the locking grooves

# Registration plane (distance from camera-facing <Z face to glass registration ledge)
registration_distance = 0.5   # Constant camera film-plane registration depth



# Light-Trap Groove Dimensions (on the camera-facing <Z face)
# Replicating the camera's silver lip of 106.0mm x 76.7mm outer dimensions
lip_outer_width = 106.0
lip_outer_height = 76.7
groove_clearance = 0.6        # Extra clearance around the lip
groove_width = 3.5            # Width of the groove channel
groove_depth = 1.5
groove_radius = 4.0           # Corner radius of the groove

# Glass Sheet Specifications
glass_width = 60.0
glass_height = 60.0
glass_thickness = 2.0
glass_tolerance = 0.5     # Clearance so the glass drops in easily without binding

# Retention Frame (Pressure Plate) Specifications
frame_pocket_width = 70.0
frame_pocket_height = 70.0
frame_tolerance = 0.3     # Clearance for 3D printed frame

# Screw Retention Specifications (Option C - Integrated Corners)
screw_offset_x = 32.5
screw_offset_y = 32.5
screw_hole_dia = 2.0          # M2 pilot hole
screw_clearance_dia = 2.2     # M2 pass-through clearance hole
screw_head_dia = 3.8          # M2 counter-sunk head diameter
screw_head_depth = 1.6        # M2 counter-sunk depth
nut_flat_to_flat = 4.3        # M2 hex nut flat-to-flat with tolerance
nut_depth = 1.8               # M2 hex nut depth



# Viewing Window & Support Lip
lip_width = 2.0           # Lip width around the edges to support the glass
view_width = glass_width - (lip_width * 2)
view_height = glass_height - (lip_width * 2)

# Pocket dimensions (calculated dynamically to maintain registration_distance)
glass_pocket_w = glass_width + glass_tolerance
glass_pocket_h = glass_height + glass_tolerance
glass_pocket_depth = plate_thickness - registration_distance

frame_pocket_w = frame_pocket_width
frame_pocket_h = frame_pocket_height
frame_pocket_depth = glass_pocket_depth - glass_thickness
retention_thickness = 3.5



# ==========================================
# PART 1: MAIN FOCUSING SCREEN ADAPTER BODY
# ==========================================
body = (
    cq.Workplane("XY")
    .box(outer_width, outer_height, plate_thickness)
    .edges("|Z")
    .chamfer(2.0)  # Eases slide-in mounting capability
)

# Cut out the main viewing window through the center
body = body.faces(">Z").workplane().rect(view_width, view_height).cutThruAll()

# Cut out the wider frame pocket where the retention frame seats
body = (
    body.faces(">Z")
    .workplane()
    .rect(frame_pocket_w, frame_pocket_h)
    .cutBlind(-frame_pocket_depth)
)

# Cut out the deeper glass pocket in the center
body = (
    body.faces(">Z")
    .workplane()
    .rect(glass_pocket_w, glass_pocket_h)
    .cutBlind(-glass_pocket_depth)
)

# Corner centers for screw holes (drilled through the frame pocket shelf)
screw_centers = [
    (screw_offset_x, screw_offset_y),
    (-screw_offset_x, screw_offset_y),
    (screw_offset_x, -screw_offset_y),
    (-screw_offset_x, -screw_offset_y)
]

# Drill screw pilot holes
body = (
    body.faces(">Z")
    .workplane()
    .pushPoints(screw_centers)
    .circle(screw_hole_dia / 2)
    .cutThruAll()
)

# Add standard Mamiya Press side registration lip steps for mounting alignment
body = (
    body.faces(">Z")
    .workplane()
    .center(-outer_width / 2, 0)
    .rect(6.0, outer_height)
    .cutBlind(-1.5)
)
body = (
    body.center(outer_width, 0)
    .rect(6.0, outer_height)
    .cutBlind(-1.5)
)

# Cut the hex nut pockets on the camera-facing back face (<Z)
body = (
    cq.Workplane("XY")
    .add(body.val())
    .faces("<Z")
    .workplane()
    .pushPoints(screw_centers)
    .polygon(6, nut_flat_to_flat / math.cos(math.pi / 6), circumscribed=False)
    .cutBlind(-nut_depth)
)



# ==========================================
# PART 1.5: LIGHT-TRAP GROOVE
# ==========================================
# Concentric rounded rectangles sketch for the light-trap channel
groove_outer_w = lip_outer_width + (2 * groove_clearance)
groove_outer_h = lip_outer_height + (2 * groove_clearance)
groove_inner_w = groove_outer_w - (2 * groove_width)
groove_inner_h = groove_outer_h - (2 * groove_width)

groove_sketch = (
    cq.Sketch()
    .rect(groove_outer_w, groove_outer_h)
    .rect(groove_inner_w, groove_inner_h, mode="s")
    .vertices()
    .fillet(groove_radius)
)

body = (
    cq.Workplane("XY")
    .add(body.val())
    .faces("<Z")
    .workplane()
    .placeSketch(groove_sketch)
    .cutBlind(-groove_depth)
)

# ==========================================
# PART 2: SCREW-RETAINED PRESSURE PLATE
# ==========================================
# Subtracting frame_tolerance for a snug clearance fit against the pocket walls
frame_width = frame_pocket_w - frame_tolerance
frame_height = frame_pocket_h - frame_tolerance

retention_frame = (
    cq.Workplane("XY")
    .box(frame_width, frame_height, retention_thickness)
)

# Cut viewing window through the center
retention_frame = (
    retention_frame.faces(">Z")
    .workplane()
    .rect(view_width, view_height)
    .cutThruAll()
)

# Cut counter-sunk screw holes in pressure plate
retention_frame = (
    retention_frame.faces(">Z")
    .workplane()
    .pushPoints(screw_centers)
    .circle(screw_clearance_dia / 2)
    .cutThruAll()
)
retention_frame = (
    retention_frame.faces(">Z")
    .workplane()
    .pushPoints(screw_centers)
    .circle(screw_head_dia / 2)
    .cutBlind(-screw_head_depth)
)

# ==========================================
# EXPORT ASSEMBLY OR PARTS
# ==========================================
# Move frame visually clear of the body for assembly layout inspection (if rendering)
retention_frame_display = retention_frame.translate((0, 0, plate_thickness * 2))

# Output both objects to your CadQuery environment if running in GUI editor, otherwise export files
if "show_object" in locals() or "show_object" in globals():
    show_object(body, name="mamiya_screen_body", options={"color": "black", "alpha": 0.9})
    show_object(retention_frame_display, name="glass_retention_ring", options={"color": "lightgrey"})
else:
    # Standalone execution
    import os
    os.makedirs("exports/glass", exist_ok=True)
    cq.exporters.export(body, "exports/glass/mamiya_screen_body.stl")
    cq.exporters.export(body, "exports/glass/mamiya_screen_body.step")
    cq.exporters.export(retention_frame, "exports/glass/glass_retention_ring.stl")
    cq.exporters.export(retention_frame, "exports/glass/glass_retention_ring.step")
    print("Exported glass focusing screen body and retention frame to exports/glass/")