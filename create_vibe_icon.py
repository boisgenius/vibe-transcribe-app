#!/usr/bin/env python3
import cairo
import math

def create_gradient_rounded_rect(ctx, x, y, width, height, radius, gradient_stops):
    """Create a rounded rectangle with gradient border"""
    # Create gradient
    pattern = cairo.LinearGradient(x, y, x + width, y + height)
    for stop, color in gradient_stops:
        pattern.add_color_stop_rgba(stop, *color)
    
    # Draw rounded rectangle path
    ctx.new_path()
    ctx.arc(x + width - radius, y + radius, radius, -math.pi/2, 0)
    ctx.arc(x + width - radius, y + height - radius, radius, 0, math.pi/2)
    ctx.arc(x + radius, y + height - radius, radius, math.pi/2, math.pi)
    ctx.arc(x + radius, y + radius, radius, math.pi, 3*math.pi/2)
    ctx.close_path()
    
    return pattern

def draw_octopus(ctx, cx, cy, size):
    """Draw the octopus-like creature"""
    # Set octopus color (sage green)
    ctx.set_source_rgba(0.55, 0.65, 0.55, 1.0)
    
    # Draw main body
    body_radius = size * 0.25
    ctx.arc(cx, cy - size * 0.1, body_radius, 0, 2 * math.pi)
    ctx.fill()
    
    # Draw tentacles
    tentacle_positions = [
        (-0.3, 0.1, -0.4, 0.4),   # Left tentacle
        (-0.15, 0.05, -0.2, 0.35), # Left-middle tentacle
        (0.15, 0.05, 0.2, 0.35),   # Right-middle tentacle
        (0.3, 0.1, 0.4, 0.4),      # Right tentacle
        (0, 0.15, 0, 0.45),        # Center tentacle
    ]
    
    for tx1, ty1, tx2, ty2 in tentacle_positions:
        ctx.new_path()
        ctx.move_to(cx + tx1 * size, cy + ty1 * size)
        ctx.curve_to(
            cx + tx1 * size * 1.2, cy + ty1 * size + size * 0.15,
            cx + tx2 * size * 0.8, cy + ty2 * size - size * 0.05,
            cx + tx2 * size, cy + ty2 * size
        )
        ctx.line_to(cx + tx2 * size * 0.8, cy + ty2 * size)
        ctx.curve_to(
            cx + tx2 * size * 0.6, cy + ty2 * size - size * 0.05,
            cx + tx1 * size * 0.8, cy + ty1 * size + size * 0.1,
            cx + tx1 * size * 0.6, cy + ty1 * size
        )
        ctx.close_path()
        ctx.fill()
    
    # Draw yellow circles on tentacles
    ctx.set_source_rgba(0.9, 0.75, 0.4, 1.0)
    circle_positions = [
        (-0.35, 0.25, 0.06),
        (-0.18, 0.22, 0.05),
        (0.18, 0.22, 0.05),
        (0.35, 0.25, 0.06),
        (0, 0.32, 0.05),
    ]
    
    for cx_off, cy_off, radius in circle_positions:
        ctx.arc(cx + cx_off * size, cy + cy_off * size, radius * size, 0, 2 * math.pi)
        ctx.fill()
    
    # Draw face on main body
    ctx.set_source_rgba(0.2, 0.3, 0.25, 1.0)
    
    # Eyes
    eye_radius = size * 0.02
    ctx.arc(cx - size * 0.08, cy - size * 0.12, eye_radius, 0, 2 * math.pi)
    ctx.fill()
    ctx.arc(cx + size * 0.08, cy - size * 0.12, eye_radius, 0, 2 * math.pi)
    ctx.fill()
    
    # Smile
    ctx.new_path()
    ctx.arc(cx, cy - size * 0.08, size * 0.08, 0.2 * math.pi, 0.8 * math.pi)
    ctx.set_line_width(size * 0.015)
    ctx.stroke()

def create_vibe_icon(filename, size=1024):
    """Create the Vibe Transcribe icon"""
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surface)
    
    # Clear background
    ctx.set_source_rgba(1, 1, 1, 0)
    ctx.paint()
    
    # Define gradient colors (pink -> blue -> teal -> yellow/orange)
    gradient_stops = [
        (0.0, (0.91, 0.39, 0.72, 1.0)),   # Pink
        (0.25, (0.53, 0.61, 0.89, 1.0)),  # Blue
        (0.5, (0.42, 0.75, 0.82, 1.0)),   # Teal
        (0.75, (0.55, 0.82, 0.69, 1.0)),  # Light teal/green
        (1.0, (0.94, 0.69, 0.42, 1.0)),   # Yellow/orange
    ]
    
    # Draw outer gradient border
    border_width = size * 0.04
    radius = size * 0.15
    pattern = create_gradient_rounded_rect(ctx, 0, 0, size, size, radius, gradient_stops)
    ctx.set_source(pattern)
    ctx.fill()
    
    # Draw inner white background
    inner_margin = border_width
    ctx.set_source_rgba(1, 1, 1, 1)
    create_gradient_rounded_rect(
        ctx, 
        inner_margin, 
        inner_margin, 
        size - 2 * inner_margin, 
        size - 2 * inner_margin, 
        radius - inner_margin,
        []
    )
    ctx.fill()
    
    # Draw octopus in center
    draw_octopus(ctx, size/2, size/2, size * 0.35)
    
    # Save the image
    surface.write_to_png(filename)
    print(f"Icon saved as {filename}")

if __name__ == "__main__":
    # Create icon in multiple sizes
    sizes = {
        "icon_1024.png": 1024,
        "icon_512.png": 512,
        "icon_256.png": 256,
        "icon_128.png": 128,
    }
    
    for filename, size in sizes.items():
        create_vibe_icon(filename, size)