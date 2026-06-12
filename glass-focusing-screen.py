import cadquery as cq
import math

# ==========================================
# PARAMETRIC PARAMETERS (All sizes in mm)
# ==========================================
# Mamiya Press M-Adapter reference dimensions
outer_width = 111.0       # Complete horizontal width of the insert
outer_height = 86.5       # Complete vertical height of the insert
plate_thickness = 7.0     # Depth required to seat securely in the locking grooves


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
glass_thickness = 2.0
glass_tolerance = 0.5     # Clearance so the glass drops in easily without binding

# Retention Frame (Pressure Plate) Specifications
frame_tolerance = 0.3     # Clearance for 3D printed frame

# Screw Retention Specifications (Option C - Integrated Corners)
screw_hole_dia = 2.0          # M2 pilot hole
screw_clearance_dia = 2.2     # M2 pass-through clearance hole
screw_head_dia = 3.8          # M2 counter-sunk head diameter
screw_head_depth = 1.6        # M2 counter-sunk depth
nut_flat_to_flat = 4.3        # M2 hex nut flat-to-flat with tolerance
nut_depth = 1.8               # M2 hex nut depth

# Viewing Window & Support Lip
lip_width = 2.0           # Lip width around the edges to support the glass
retention_thickness = 3.5

def generate_glass_focusing_screen(glass_width, glass_height):
    # Pocket dimensions (calculated dynamically to maintain registration_distance)
    glass_pocket_w = glass_width + glass_tolerance
    glass_pocket_h = glass_height + glass_tolerance
    glass_pocket_depth = plate_thickness - registration_distance

    frame_pocket_w = glass_width + 10.0
    frame_pocket_h = glass_height + 10.0
    frame_pocket_depth = glass_pocket_depth - glass_thickness

    view_width = glass_width - (lip_width * 2)
    view_height = glass_height - (lip_width * 2)

    screw_offset_x = (frame_pocket_w - 5.0) / 2
    screw_offset_y = (frame_pocket_h - 5.0) / 2

    # Corner centers for screw holes (drilled through the frame pocket shelf)
    screw_centers = [
        (screw_offset_x, screw_offset_y),
        (-screw_offset_x, screw_offset_y),
        (screw_offset_x, -screw_offset_y),
        (-screw_offset_x, -screw_offset_y)
    ]

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
        body, frame = generate_glass_focusing_screen(w, h)
        x_offset = (i - 1.5) * 130.0
        show_object(body.translate((x_offset, 0, 0)), name=f"body_{suffix}", options={"color": "black", "alpha": 0.9})
        show_object(frame.translate((x_offset, 0, plate_thickness * 2)), name=f"frame_{suffix}", options={"color": "lightgrey"})
else:
    import os
    os.makedirs("exports/glass", exist_ok=True)
    for w, h, suffix in formats:
        body, frame = generate_glass_focusing_screen(w, h)
        cq.exporters.export(body, f"exports/glass/mamiya_screen_body_{suffix}.stl")
        cq.exporters.export(body, f"exports/glass/mamiya_screen_body_{suffix}.step")
        cq.exporters.export(frame, f"exports/glass/glass_retention_ring_{suffix}.stl")
        cq.exporters.export(frame, f"exports/glass/glass_retention_ring_{suffix}.step")
    print("Exported all glass focusing screen bodies and retention frames to exports/glass/")