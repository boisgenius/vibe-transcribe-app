#!/usr/bin/env python3
"""
Create macOS icon from your logo
"""
import os
import subprocess

def create_icon():
    # Create iconset directory
    iconset_dir = "icon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)
    
    # We'll create a simple colored circle as placeholder since we can't process the uploaded image
    # Your friend can replace this with the actual logo later
    
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    for size in sizes:
        # Create a simple SVG placeholder
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="borderGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#e863b8;stop-opacity:1" />
      <stop offset="25%" style="stop-color:#879ee4;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#6bc0d1;stop-opacity:1" />
      <stop offset="75%" style="stop-color:#8cd1b0;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f0b06b;stop-opacity:1" />
    </linearGradient>
    <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feMorphology operator="dilate" radius="2"/>
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Outer gradient border -->
  <rect width="{size}" height="{size}" rx="{size//6}" fill="url(#borderGradient)" />
  
  <!-- Inner white background -->
  <rect x="{size//25}" y="{size//25}" width="{size - 2*size//25}" height="{size - 2*size//25}" rx="{size//6 - size//25}" fill="white" />
  
  <!-- Octopus body -->
  <g transform="translate({size//2}, {size//2 - size//10})">
    <!-- Tentacles -->
    <path d="M -{size//6} {size//15} Q -{size//5} {size//6} -{size//4} {size//3} Q -{size//5} {size//3} -{size//6} {size//4} Q -{size//8} {size//6} -{size//6} {size//15}" 
          fill="#8ca68c" stroke="#334d40" stroke-width="2"/>
    <path d="M -{size//12} {size//20} Q -{size//10} {size//8} -{size//8} {size//4} Q -{size//10} {size//4} -{size//12} {size//5} Q -{size//15} {size//8} -{size//12} {size//20}" 
          fill="#8ca68c" stroke="#334d40" stroke-width="2"/>
    <path d="M {size//12} {size//20} Q {size//10} {size//8} {size//8} {size//4} Q {size//10} {size//4} {size//12} {size//5} Q {size//15} {size//8} {size//12} {size//20}" 
          fill="#8ca68c" stroke="#334d40" stroke-width="2"/>
    <path d="M {size//6} {size//15} Q {size//5} {size//6} {size//4} {size//3} Q {size//5} {size//3} {size//6} {size//4} Q {size//8} {size//6} {size//6} {size//15}" 
          fill="#8ca68c" stroke="#334d40" stroke-width="2"/>
    <path d="M 0 {size//8} Q {size//100} {size//4} 0 {size//2.5} Q -{size//100} {size//4} 0 {size//8}" 
          fill="#8ca68c" stroke="#334d40" stroke-width="2"/>
    
    <!-- Tentacle circles -->
    <circle cx="-{size//5}" cy="{size//5}" r="{size//30}" fill="#e6bf66" stroke="#334d40" stroke-width="1"/>
    <circle cx="-{size//10}" cy="{size//6}" r="{size//35}" fill="#e6bf66" stroke="#334d40" stroke-width="1"/>
    <circle cx="{size//10}" cy="{size//6}" r="{size//35}" fill="#e6bf66" stroke="#334d40" stroke-width="1"/>
    <circle cx="{size//5}" cy="{size//5}" r="{size//30}" fill="#e6bf66" stroke="#334d40" stroke-width="1"/>
    <circle cx="0" cy="{size//4}" r="{size//35}" fill="#e6bf66" stroke="#334d40" stroke-width="1"/>
    
    <!-- Main body -->
    <circle cx="0" cy="0" r="{size//8}" fill="#8ca68c" stroke="#334d40" stroke-width="3"/>
    
    <!-- Eyes -->
    <circle cx="-{size//15}" cy="-{size//15}" r="{size//80}" fill="#334d40"/>
    <circle cx="{size//15}" cy="-{size//15}" r="{size//80}" fill="#334d40"/>
    
    <!-- Smile -->
    <path d="M -{size//20} {size//30} Q 0 {size//15} {size//20} {size//30}" 
          stroke="#334d40" stroke-width="{size//100}" fill="none" stroke-linecap="round"/>
  </g>
</svg>'''
        
        svg_file = f"temp_icon_{size}.svg"
        with open(svg_file, 'w') as f:
            f.write(svg_content)
        
        # Convert SVG to PNG using built-in tools
        png_file = f"{iconset_dir}/icon_{size}x{size}.png"
        
        # Try different conversion methods
        try:
            # Method 1: rsvg-convert (if available)
            subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg_file, '-o', png_file], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Method 2: ImageMagick convert (if available)
                subprocess.run(['convert', '-size', f'{size}x{size}', svg_file, png_file], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    # Method 3: Cairo (if available)
                    subprocess.run(['cairosvg', svg_file, '-o', png_file, '-W', str(size), '-H', str(size)], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback: create a simple colored rectangle using PIL
                    try:
                        from PIL import Image, ImageDraw, ImageFont
                        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(img)
                        
                        # Create gradient effect manually
                        for i in range(size):
                            for j in range(size):
                                # Simple gradient calculation
                                factor = (i + j) / (2 * size)
                                if factor < 0.25:
                                    r, g, b = int(102 + factor * 4 * (245 - 102)), int(126 + factor * 4 * (101 - 126)), int(234 + factor * 4 * (101 - 234))
                                elif factor < 0.5:
                                    factor = (factor - 0.25) * 4
                                    r, g, b = int(245 + factor * (72 - 245)), int(101 + factor * (187 - 101)), int(101 + factor * (120 - 101))
                                elif factor < 0.75:
                                    factor = (factor - 0.5) * 4
                                    r, g, b = int(72 + factor * (237 - 72)), int(187 + factor * (137 - 187)), int(120 + factor * (54 - 120))
                                else:
                                    factor = (factor - 0.75) * 4
                                    r, g, b = int(237 + factor * (102 - 237)), int(137 + factor * (126 - 137)), int(54 + factor * (234 - 54))
                                
                                img.putpixel((i, j), (r, g, b, 255))
                        
                        # Add emoji if font available
                        try:
                            font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", size//2)
                            draw.text((size//4, size//4), "🐙", font=font, fill=(255, 255, 255, 255))
                        except:
                            # Simple circle fallback
                            draw.ellipse([size//4, size//4, 3*size//4, 3*size//4], fill=(255, 255, 255, 255))
                        
                        img.save(png_file)
                    except ImportError:
                        # Ultimate fallback: just create an empty file
                        with open(png_file, 'w') as f:
                            f.write("")
        
        # Clean up
        try:
            os.remove(svg_file)
        except:
            pass
        
        # Also create @2x versions for retina
        if size <= 512:
            retina_file = f"{iconset_dir}/icon_{size}x{size}@2x.png"
            try:
                subprocess.run(['cp', png_file, retina_file], check=True)
            except:
                pass

    # Create the .icns file
    try:
        subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', 'Vibe Transcribe.app/Contents/Resources/icon.icns'], check=True)
        print("✅ Icon created successfully!")
    except subprocess.CalledProcessError:
        print("⚠️ Could not create .icns file, but app will still work")
    
    # Clean up
    import shutil
    try:
        shutil.rmtree(iconset_dir)
    except:
        pass

if __name__ == "__main__":
    create_icon()