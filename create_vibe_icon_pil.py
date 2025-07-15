#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math

def create_gradient(width, height):
    """Create a gradient image"""
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Create diagonal gradient
    for i in range(width + height):
        progress = i / (width + height)
        
        # Interpolate between colors
        if progress < 0.25:
            # Pink to blue
            t = progress / 0.25
            r = int(232 + (135 - 232) * t)
            g = int(100 + (156 - 100) * t)
            b = int(184 + (227 - 184) * t)
        elif progress < 0.5:
            # Blue to teal
            t = (progress - 0.25) / 0.25
            r = int(135 + (107 - 135) * t)
            g = int(156 + (191 - 156) * t)
            b = int(227 + (209 - 227) * t)
        elif progress < 0.75:
            # Teal to light green
            t = (progress - 0.5) / 0.25
            r = int(107 + (140 - 107) * t)
            g = int(191 + (209 - 191) * t)
            b = int(209 + (176 - 209) * t)
        else:
            # Light green to yellow/orange
            t = (progress - 0.75) / 0.25
            r = int(140 + (240 - 140) * t)
            g = int(209 + (176 - 209) * t)
            b = int(176 + (107 - 176) * t)
        
        # Draw diagonal line
        for j in range(3):
            draw.line([(i - j, 0), (0, i - j)], fill=(r, g, b, 255), width=2)
    
    return img

def draw_rounded_rectangle(draw, coords, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = coords
    diameter = 2 * radius
    
    # Draw the rectangles and circles that make up the rounded rectangle
    if fill:
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        draw.ellipse([x1, y1, x1 + diameter, y1 + diameter], fill=fill)
        draw.ellipse([x2 - diameter, y1, x2, y1 + diameter], fill=fill)
        draw.ellipse([x1, y2 - diameter, x1 + diameter, y2], fill=fill)
        draw.ellipse([x2 - diameter, y2 - diameter, x2, y2], fill=fill)
    
    if outline:
        draw.arc([x1, y1, x1 + diameter, y1 + diameter], 180, 270, fill=outline, width=width)
        draw.arc([x2 - diameter, y1, x2, y1 + diameter], 270, 0, fill=outline, width=width)
        draw.arc([x1, y2 - diameter, x1 + diameter, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - diameter, y2 - diameter, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([x1 + radius, y1, x2 - radius, y1], fill=outline, width=width)
        draw.line([x1 + radius, y2, x2 - radius, y2], fill=outline, width=width)
        draw.line([x1, y1 + radius, x1, y2 - radius], fill=outline, width=width)
        draw.line([x2, y1 + radius, x2, y2 - radius], fill=outline, width=width)

def draw_octopus(draw, cx, cy, size):
    """Draw the octopus creature"""
    # Octopus color (sage green)
    octopus_color = (140, 166, 140, 255)
    dark_green = (51, 77, 64, 255)
    yellow_color = (230, 191, 102, 255)
    
    # Draw tentacles
    tentacle_data = [
        # (start_x, start_y, control1_x, control1_y, control2_x, control2_y, end_x, end_y)
        (-0.3, 0.1, -0.35, 0.25, -0.38, 0.35, -0.4, 0.4),
        (-0.15, 0.05, -0.18, 0.2, -0.19, 0.3, -0.2, 0.35),
        (0.15, 0.05, 0.18, 0.2, 0.19, 0.3, 0.2, 0.35),
        (0.3, 0.1, 0.35, 0.25, 0.38, 0.35, 0.4, 0.4),
        (0, 0.15, 0.02, 0.3, 0.01, 0.4, 0, 0.45),
    ]
    
    for i, (sx, sy, c1x, c1y, c2x, c2y, ex, ey) in enumerate(tentacle_data):
        # Draw tentacle shape
        points = []
        for t in range(21):
            t = t / 20.0
            # Bezier curve calculation
            x = (1-t)**3 * (cx + sx*size) + 3*(1-t)**2*t * (cx + c1x*size) + 3*(1-t)*t**2 * (cx + c2x*size) + t**3 * (cx + ex*size)
            y = (1-t)**3 * (cy + sy*size) + 3*(1-t)**2*t * (cy + c1y*size) + 3*(1-t)*t**2 * (cy + c2y*size) + t**3 * (cy + ey*size)
            
            # Vary width along tentacle
            width = size * 0.08 * (1 - t * 0.5)
            points.append((x - width/2, y))
        
        # Add points for the other side
        for t in range(20, -1, -1):
            t = t / 20.0
            x = (1-t)**3 * (cx + sx*size) + 3*(1-t)**2*t * (cx + c1x*size) + 3*(1-t)*t**2 * (cx + c2x*size) + t**3 * (cx + ex*size)
            y = (1-t)**3 * (cy + sy*size) + 3*(1-t)**2*t * (cy + c1y*size) + 3*(1-t)*t**2 * (cy + c2y*size) + t**3 * (cy + ey*size)
            width = size * 0.08 * (1 - t * 0.5)
            points.append((x + width/2, y))
        
        draw.polygon(points, fill=octopus_color, outline=dark_green, width=2)
    
    # Draw main body
    body_radius = size * 0.25
    body_bbox = [cx - body_radius, cy - size * 0.1 - body_radius, 
                 cx + body_radius, cy - size * 0.1 + body_radius]
    draw.ellipse(body_bbox, fill=octopus_color, outline=dark_green, width=2)
    
    # Draw yellow circles on tentacles
    circle_positions = [
        (-0.35, 0.25, 0.06),
        (-0.18, 0.22, 0.05),
        (0.18, 0.22, 0.05),
        (0.35, 0.25, 0.06),
        (0, 0.32, 0.05),
    ]
    
    for cx_off, cy_off, radius in circle_positions:
        circle_x = cx + cx_off * size
        circle_y = cy + cy_off * size
        circle_r = radius * size
        draw.ellipse([circle_x - circle_r, circle_y - circle_r, 
                     circle_x + circle_r, circle_y + circle_r], 
                    fill=yellow_color, outline=dark_green, width=1)
    
    # Draw face
    # Eyes
    eye_radius = size * 0.02
    draw.ellipse([cx - size * 0.08 - eye_radius, cy - size * 0.12 - eye_radius,
                  cx - size * 0.08 + eye_radius, cy - size * 0.12 + eye_radius],
                 fill=dark_green)
    draw.ellipse([cx + size * 0.08 - eye_radius, cy - size * 0.12 - eye_radius,
                  cx + size * 0.08 + eye_radius, cy - size * 0.12 + eye_radius],
                 fill=dark_green)
    
    # Smile
    smile_bbox = [cx - size * 0.08, cy - size * 0.16, 
                  cx + size * 0.08, cy]
    draw.arc(smile_bbox, 0, 180, fill=dark_green, width=int(size * 0.015))

def create_vibe_icon(filename, size=1024):
    """Create the Vibe Transcribe icon"""
    # Create base image with transparent background
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient for border
    gradient = create_gradient(size, size)
    
    # Create mask for rounded rectangle border
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    border_width = int(size * 0.04)
    radius = int(size * 0.15)
    
    # Draw outer rounded rectangle on mask
    draw_rounded_rectangle(mask_draw, [0, 0, size-1, size-1], radius, fill=255)
    
    # Draw inner rounded rectangle (to create border effect)
    draw_rounded_rectangle(mask_draw, 
                          [border_width, border_width, 
                           size-1-border_width, size-1-border_width], 
                          radius - border_width, fill=0)
    
    # Apply gradient through mask
    img.paste(gradient, (0, 0), mask)
    
    # Draw white background inside border
    draw_rounded_rectangle(draw, 
                          [border_width, border_width, 
                           size-1-border_width, size-1-border_width], 
                          radius - border_width, fill=(255, 255, 255, 255))
    
    # Draw octopus
    draw_octopus(draw, size/2, size/2, size * 0.35)
    
    # Save the image
    img.save(filename, 'PNG')
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