import cadquery as cq

# ==========================================
# PARAMETRIC PARAMETERS (All sizes in mm)
# ==========================================
# Mamiya Press M-Adapter reference dimensions
outer_width = 111.0       # Complete horizontal width of the insert
outer_height = 86.5       # Complete vertical height of the insert
plate_thickness = 7.2     # Depth required to seat securely in the locking grooves

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

# Viewing Window & Support Lip
lip_width = 2.0           # Lip width around the edges to support the glass
view_width = glass_width - (lip_width * 2)
view_height = glass_height - (lip_width * 2)

# Pocket dimensions (Depth accounts for 2mm glass + 1.5mm retention ring)
pocket_width = glass_width + glass_tolerance
pocket_height = glass_height + glass_tolerance
retention_thickness = 1.5
pocket_depth = glass_thickness + retention_thickness

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

# Cut out the recessed pocket where the glass and retention frame seat
body = (
    body.faces(">Z")
    .workplane()
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
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
# PART 2: FRICTION-FIT RETENTION FRAME
# ==========================================
# Subtracting 0.15mm for a snug, snap-in friction fit against the pocket walls
wall_clearance = 0.15 
frame_width = pocket_width - wall_clearance
frame_height = pocket_height - wall_clearance

retention_frame = (
    cq.Workplane("XY")
    .box(frame_width, frame_height, retention_thickness)
    .faces(">Z")
    .workplane()
    .rect(view_width, view_height)
    .cutThruAll()
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