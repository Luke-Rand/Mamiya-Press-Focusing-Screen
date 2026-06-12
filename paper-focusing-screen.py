import cadquery as cq

# ==========================================
# PARAMETRIC PARAMETERS (All sizes in mm)
# ==========================================
# Mamiya Press M-Adapter reference dimensions
outer_width = 111.0       # Complete horizontal width of the insert
outer_height = 86.5       # Complete vertical height of the insert
plate_thickness = 6.5     # Depth required to seat securely in the locking grooves
body_thickness = 10.0     # Overall thickness of the center body to hold the glass

# Registration plane (distance from camera-facing <Z face to paper registration ledge)
registration_distance = 7.7   # Constant camera film-plane registration depth



# Light-Trap Groove Dimensions (on the camera-facing <Z face)
# Replicating the camera's silver lip of 106.0mm x 76.7mm outer dimensions
lip_outer_width = 106.0
lip_outer_height = 76.7
groove_clearance = 0.6        # Extra clearance around the lip
groove_width = 3.5            # Width of the groove channel
groove_depth = 1.5
groove_radius = 4.0           # Corner radius of the groove

# Paper / Drafting Film Specifications
paper_thickness = 0.1     # Heavy tracing paper or drafting film thickness
paper_tolerance = 0.5     # Clearance so the paper drops in easily without binding

# Viewing Window & Support Lip
lip_width = 4.5           # Increased to 4.5mm to maintain a thick, print-safe wall next to the groove

def generate_paper_focusing_screen(paper_width, paper_height):
    # Pocket dimensions (calculated dynamically to maintain registration_distance)
    pocket_width = paper_width + paper_tolerance
    pocket_height = paper_height + paper_tolerance
    pocket_depth = body_thickness - registration_distance
    retention_thickness = pocket_depth - paper_thickness

    view_width = paper_width - (lip_width * 2)
    view_height = paper_height - (lip_width * 2)

    # ==========================================
    # PART 1: MAIN FOCUSING SCREEN ADAPTER BODY
    # ==========================================
    body = (
        cq.Workplane("XY")
        .box(outer_width, outer_height, body_thickness)
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

    # Add standard Mamiya Press top/bottom registration lip steps for mounting alignment
    body = (
        body.faces(">Z")
        .workplane()
        .center(0, -outer_height / 2)
        .rect(outer_width, 6.0)
        .cutBlind(-(body_thickness - plate_thickness))
    )
    body = (
        body.center(0, outer_height)
        .rect(outer_width, 6.0)
        .cutBlind(-(body_thickness - plate_thickness))
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

    return body, retention_frame

# ==========================================
# EXPORT ASSEMBLY OR PARTS
# ==========================================
formats = [
    (45.0, 60.0, "60x45_vertical"),
    (60.0, 60.0, "60x60"),
    (70.0, 60.0, "60x70"),
    (90.0, 60.0, "60x90")
]

if "show_object" in locals() or "show_object" in globals():
    for i, (w, h, suffix) in enumerate(formats):
        body, frame = generate_paper_focusing_screen(w, h)
        x_offset = (i - 1.5) * 130.0
        show_object(body.translate((x_offset, 0, 0)), name=f"body_{suffix}", options={"color": "black", "alpha": 0.9})
        show_object(frame.translate((x_offset, 0, body_thickness * 2)), name=f"frame_{suffix}", options={"color": "lightgrey"})
else:
    import os
    os.makedirs("exports/paper", exist_ok=True)
    for w, h, suffix in formats:
        body, frame = generate_paper_focusing_screen(w, h)
        cq.exporters.export(body, f"exports/paper/mamiya_screen_body_{suffix}.stl")
        cq.exporters.export(body, f"exports/paper/mamiya_screen_body_{suffix}.step")
        cq.exporters.export(frame, f"exports/paper/paper_retention_ring_{suffix}.stl")
        cq.exporters.export(frame, f"exports/paper/paper_retention_ring_{suffix}.step")
    print("Exported all paper focusing screen bodies and retention frames to exports/paper/")

