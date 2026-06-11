import cadquery as cq

# ==========================================
# PARAMETRIC PARAMETERS (All sizes in mm)
# ==========================================
# Mamiya Press M-Adapter reference dimensions
outer_width = 114.0       # Complete horizontal width of the insert
outer_height = 98.0       # Complete vertical height of the insert
plate_thickness = 5.0     # Depth required to seat securely in the locking grooves

# Paper / Drafting Film Specifications
paper_width = 95.0
paper_height = 72.0
paper_thickness = 0.1     # Heavy tracing paper or drafting film thickness
paper_tolerance = 0.5     # Clearance so the paper drops in easily without binding

# Viewing Window & Support Lip
lip_width = 2.0           # Lip width around the edges to support the paper
view_width = paper_width - (lip_width * 2)
view_height = paper_height - (lip_width * 2)

# Pocket dimensions (Depth is kept at 3.5mm to match the glass version's registration plane)
pocket_width = paper_width + paper_tolerance
pocket_height = paper_height + paper_tolerance
pocket_depth = 3.5        # Keep registration plane identical to glass model (Z = -1.0)
retention_thickness = pocket_depth - paper_thickness

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

# Cut out the recessed pocket where the paper and retention frame seat
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

# Output to CadQuery environment if running in GUI editor, otherwise export files
if "show_object" in locals() or "show_object" in globals():
    show_object(body, name="mamiya_screen_body", options={"color": "black", "alpha": 0.9})
    show_object(retention_frame_display, name="paper_retention_ring", options={"color": "lightgrey"})
else:
    # Standalone execution
    import os
    os.makedirs("exports/paper", exist_ok=True)
    cq.exporters.export(body, "exports/paper/mamiya_screen_body.stl")
    cq.exporters.export(body, "exports/paper/mamiya_screen_body.step")
    cq.exporters.export(retention_frame, "exports/paper/paper_retention_ring.stl")
    cq.exporters.export(retention_frame, "exports/paper/paper_retention_ring.step")
    print("Exported paper focusing screen body and retention frame to exports/paper/")
