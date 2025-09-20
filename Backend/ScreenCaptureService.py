"""
ScreenCaptureService.py
Screen capture and annotation service for JARVIS.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import threading

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL not available. Install with: pip install Pillow")

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ pyautogui not available. Install with: pip install pyautogui")

class JarvisScreenCaptureService:
    """
    Screen capture and annotation service with:
    - Full screen capture
    - Window capture
    - Region capture
    - Image annotation
    - Screenshot management
    - Image editing tools
    """
    
    def __init__(self, data_dir: str = "Data/screenshots"):
        self.data_dir = data_dir
        self.screenshots_file = os.path.join(data_dir, "screenshots.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.screenshots = self._load_screenshots()
        
        # Default settings
        self.default_format = 'PNG'
        self.default_quality = 95
        self.auto_save = True
        
        # Annotation settings
        self.annotation_font_size = 24
        self.annotation_color = (255, 0, 0)  # Red
        self.annotation_thickness = 3
    
    def _load_screenshots(self) -> List[Dict[str, Any]]:
        """Load screenshots metadata from file."""
        try:
            if os.path.exists(self.screenshots_file):
                with open(self.screenshots_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Error loading screenshots: {e}")
            return []
    
    def _save_screenshots(self):
        """Save screenshots metadata to file."""
        try:
            with open(self.screenshots_file, 'w') as f:
                json.dump(self.screenshots, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving screenshots: {e}")
    
    def capture_screen(self, filename: str = None, region: Tuple[int, int, int, int] = None) -> str:
        """
        Capture screen or screen region.
        
        Args:
            filename: Custom filename (optional)
            region: (x, y, width, height) for region capture (optional)
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                return "❌ Screen capture not available. Install pyautogui: pip install pyautogui"
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            # Ensure filename has extension
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filename += '.png'
            
            filepath = os.path.join(self.data_dir, filename)
            
            # Capture screen
            if region:
                # Region capture
                screenshot = pyautogui.screenshot(region=region)
                capture_type = f"region ({region[0]}, {region[1]}, {region[2]}, {region[3]})"
            else:
                # Full screen capture
                screenshot = pyautogui.screenshot()
                capture_type = "full screen"
            
            # Save screenshot
            screenshot.save(filepath, self.default_format, quality=self.default_quality)
            
            # Add to metadata
            screenshot_info = {
                'filename': filename,
                'filepath': filepath,
                'timestamp': datetime.now().isoformat(),
                'type': capture_type,
                'size': screenshot.size,
                'format': self.default_format,
                'file_size': os.path.getsize(filepath)
            }
            
            self.screenshots.append(screenshot_info)
            self._save_screenshots()
            
            return f"✅ Screenshot captured: {filename}\n📏 Size: {screenshot.size[0]}x{screenshot.size[1]}\n📍 Type: {capture_type}"
            
        except Exception as e:
            return f"❌ Error capturing screen: {str(e)}"
    
    def capture_window(self, window_title: str = None) -> str:
        """
        Capture a specific window.
        
        Args:
            window_title: Title of the window to capture (optional)
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                return "❌ Window capture not available. Install pyautogui: pip install pyautogui"
            
            # For now, we'll capture full screen since window-specific capture
            # requires additional libraries on Windows
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"window_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            filepath = os.path.join(self.data_dir, filename)
            screenshot.save(filepath, self.default_format, quality=self.default_quality)
            
            # Add to metadata
            screenshot_info = {
                'filename': filename,
                'filepath': filepath,
                'timestamp': datetime.now().isoformat(),
                'type': f"window ({window_title or 'active'})",
                'size': screenshot.size,
                'format': self.default_format,
                'file_size': os.path.getsize(filepath)
            }
            
            self.screenshots.append(screenshot_info)
            self._save_screenshots()
            
            return f"✅ Window captured: {filename}\n📏 Size: {screenshot.size[0]}x{screenshot.size[1]}"
            
        except Exception as e:
            return f"❌ Error capturing window: {str(e)}"
    
    def annotate_image(self, filename: str, annotations: List[Dict[str, Any]]) -> str:
        """
        Annotate an image with text, shapes, and highlights.
        
        Args:
            filename: Name of the screenshot to annotate
            annotations: List of annotation objects
        """
        try:
            if not PIL_AVAILABLE:
                return "❌ Image annotation not available. Install Pillow: pip install Pillow"
            
            # Find the screenshot
            screenshot_info = next((s for s in self.screenshots if s['filename'] == filename), None)
            if not screenshot_info:
                return f"❌ Screenshot '{filename}' not found"
            
            filepath = screenshot_info['filepath']
            
            # Load image
            image = Image.open(filepath)
            draw = ImageDraw.Draw(image)
            
            # Apply annotations
            for annotation in annotations:
                annotation_type = annotation.get('type', 'text')
                
                if annotation_type == 'text':
                    self._add_text_annotation(draw, annotation)
                elif annotation_type == 'rectangle':
                    self._add_rectangle_annotation(draw, annotation)
                elif annotation_type == 'circle':
                    self._add_circle_annotation(draw, annotation)
                elif annotation_type == 'line':
                    self._add_line_annotation(draw, annotation)
                elif annotation_type == 'arrow':
                    self._add_arrow_annotation(draw, annotation)
                elif annotation_type == 'highlight':
                    self._add_highlight_annotation(draw, annotation)
            
            # Save annotated image
            annotated_filename = f"annotated_{filename}"
            annotated_filepath = os.path.join(self.data_dir, annotated_filename)
            image.save(annotated_filepath, self.default_format, quality=self.default_quality)
            
            # Add to metadata
            annotated_info = {
                'filename': annotated_filename,
                'filepath': annotated_filepath,
                'timestamp': datetime.now().isoformat(),
                'type': f"annotated ({filename})",
                'size': image.size,
                'format': self.default_format,
                'file_size': os.path.getsize(annotated_filepath),
                'original': filename,
                'annotations': annotations
            }
            
            self.screenshots.append(annotated_info)
            self._save_screenshots()
            
            return f"✅ Image annotated: {annotated_filename}\n📝 Annotations: {len(annotations)}"
            
        except Exception as e:
            return f"❌ Error annotating image: {str(e)}"
    
    def _add_text_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """Add text annotation to image."""
        text = annotation.get('text', '')
        position = annotation.get('position', (10, 10))
        color = tuple(annotation.get('color', self.annotation_color))
        font_size = annotation.get('font_size', self.annotation_font_size)
        
        try:
            # Try to load a font
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        draw.text(position, text, fill=color, font=font)
    
    def _add_rectangle_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """Add rectangle annotation to image."""
        position = annotation.get('position', (10, 10, 100, 100))  # (x1, y1, x2, y2)
        color = tuple(annotation.get('color', self.annotation_color))
        thickness = annotation.get('thickness', self.annotation_thickness)
        
        draw.rectangle(position, outline=color, width=thickness)
    
    def _add_circle_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """Add circle annotation to image."""
        center = annotation.get('center', (50, 50))
        radius = annotation.get('radius', 25)
        color = tuple(annotation.get('color', self.annotation_color))
        thickness = annotation.get('thickness', self.annotation_thickness)
        
        # Calculate bounding box
        x1 = center[0] - radius
        y1 = center[1] - radius
        x2 = center[0] + radius
        y2 = center[1] + radius
        
        draw.ellipse([x1, y1, x2, y2], outline=color, width=thickness)
    
    def _add_line_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """Add line annotation to image."""
        start = annotation.get('start', (10, 10))
        end = annotation.get('end', (100, 100))
        color = tuple(annotation.get('color', self.annotation_color))
        thickness = annotation.get('thickness', self.annotation_thickness)
        
        draw.line([start, end], fill=color, width=thickness)
    
    def _add_arrow_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """Add arrow annotation to image."""
        start = annotation.get('start', (10, 10))
        end = annotation.get('end', (100, 100))
        color = tuple(annotation.get('color', self.annotation_color))
        thickness = annotation.get('thickness', self.annotation_thickness)
        
        # Draw line
        draw.line([start, end], fill=color, width=thickness)
        
        # Draw arrowhead (simplified)
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = (dx**2 + dy**2)**0.5
        
        if length > 0:
            # Arrowhead points
            arrow_size = 10
            arrow_angle = 0.5  # radians
            
            # Calculate arrowhead points
            angle = -arrow_angle
            arrow_x1 = end[0] - arrow_size * (dx * (1 + arrow_angle) - dy * arrow_angle) / length
            arrow_y1 = end[1] - arrow_size * (dy * (1 + arrow_angle) + dx * arrow_angle) / length
            
            angle = arrow_angle
            arrow_x2 = end[0] - arrow_size * (dx * (1 - arrow_angle) - dy * arrow_angle) / length
            arrow_y2 = end[1] - arrow_size * (dy * (1 - arrow_angle) + dx * arrow_angle) / length
            
            # Draw arrowhead
            draw.polygon([end, (int(arrow_x1), int(arrow_y1)), (int(arrow_x2), int(arrow_y2))], fill=color)
    
    def _add_highlight_annotation(self, draw: ImageDraw.Draw, annotation: Dict[str, Any]):
        """Add highlight annotation to image."""
        position = annotation.get('position', (10, 10, 100, 100))  # (x1, y1, x2, y2)
        color = tuple(annotation.get('color', (255, 255, 0)))  # Yellow highlight
        opacity = annotation.get('opacity', 128)
        
        # Create a semi-transparent overlay
        overlay = Image.new('RGBA', draw._image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(position, fill=(*color, opacity))
        
        # Composite the overlay
        draw._image.paste(overlay, (0, 0), overlay)
    
    def list_screenshots(self, limit: int = 10) -> str:
        """List recent screenshots."""
        try:
            if not self.screenshots:
                return "📸 No screenshots found"
            
            # Get recent screenshots
            recent_screenshots = self.screenshots[-limit:]
            recent_screenshots.reverse()  # Show newest first
            
            response = f"📸 **Recent Screenshots** ({len(recent_screenshots)} entries)\n\n"
            
            for screenshot in recent_screenshots:
                timestamp = datetime.fromisoformat(screenshot['timestamp'])
                file_size_kb = screenshot['file_size'] / 1024
                
                response += f"📷 **{screenshot['filename']}**\n"
                response += f"   🕒 {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                response += f"   📏 {screenshot['size'][0]}x{screenshot['size'][1]}\n"
                response += f"   📊 {file_size_kb:.1f} KB\n"
                response += f"   📝 {screenshot['type']}\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error listing screenshots: {str(e)}"
    
    def delete_screenshot(self, filename: str) -> str:
        """Delete a screenshot."""
        try:
            screenshot_info = next((s for s in self.screenshots if s['filename'] == filename), None)
            if not screenshot_info:
                return f"❌ Screenshot '{filename}' not found"
            
            # Delete file
            if os.path.exists(screenshot_info['filepath']):
                os.remove(screenshot_info['filepath'])
            
            # Remove from metadata
            self.screenshots = [s for s in self.screenshots if s['filename'] != filename]
            self._save_screenshots()
            
            return f"✅ Deleted screenshot: {filename}"
            
        except Exception as e:
            return f"❌ Error deleting screenshot: {str(e)}"
    
    def get_screenshot_info(self, filename: str) -> str:
        """Get detailed information about a screenshot."""
        try:
            screenshot_info = next((s for s in self.screenshots if s['filename'] == filename), None)
            if not screenshot_info:
                return f"❌ Screenshot '{filename}' not found"
            
            timestamp = datetime.fromisoformat(screenshot_info['timestamp'])
            file_size_kb = screenshot_info['file_size'] / 1024
            
            response = f"📷 **Screenshot Details: {filename}**\n\n"
            response += f"🕒 **Created:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            response += f"📏 **Size:** {screenshot_info['size'][0]}x{screenshot_info['size'][1]} pixels\n"
            response += f"📊 **File Size:** {file_size_kb:.1f} KB\n"
            response += f"📝 **Type:** {screenshot_info['type']}\n"
            response += f"🎨 **Format:** {screenshot_info['format']}\n"
            response += f"📁 **Path:** {screenshot_info['filepath']}\n"
            
            if 'original' in screenshot_info:
                response += f"🔄 **Original:** {screenshot_info['original']}\n"
            
            if 'annotations' in screenshot_info:
                response += f"📝 **Annotations:** {len(screenshot_info['annotations'])} items\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting screenshot info: {str(e)}"
    
    def quick_capture_with_annotation(self, text: str = "", position: Tuple[int, int] = (10, 10)) -> str:
        """Quick capture with text annotation."""
        try:
            # Capture screen
            capture_result = self.capture_screen()
            if capture_result.startswith("❌"):
                return capture_result
            
            # Extract filename from result
            filename = capture_result.split(": ")[1].split("\n")[0]
            
            # Add text annotation
            if text:
                annotations = [{
                    'type': 'text',
                    'text': text,
                    'position': position,
                    'color': self.annotation_color,
                    'font_size': self.annotation_font_size
                }]
                
                annotate_result = self.annotate_image(filename, annotations)
                return f"{capture_result}\n{annotate_result}"
            else:
                return capture_result
                
        except Exception as e:
            return f"❌ Error in quick capture: {str(e)}"
    
    def get_screen_capture_help(self) -> str:
        """Get help information for screen capture features."""
        return """📸 **Screen Capture & Annotation Help**

🔧 **Basic Capture:**
   • 'capture screen' - Capture full screen
   • 'capture screen filename.png' - Capture with custom filename
   • 'capture window' - Capture active window
   • 'quick capture [text]' - Capture with text annotation

📝 **Image Annotation:**
   • 'annotate image filename.png' - Annotate existing screenshot
   • Add text, rectangles, circles, lines, arrows, highlights
   • Customize colors, sizes, and positions

📋 **Screenshot Management:**
   • 'list screenshots' - Show recent screenshots
   • 'screenshot info filename.png' - Get detailed info
   • 'delete screenshot filename.png' - Remove screenshot

🎨 **Annotation Types:**
   • Text annotations with custom fonts and colors
   • Rectangle and circle shapes
   • Lines and arrows
   • Highlight overlays
   • Custom positioning and sizing

💡 **Examples:**
   • 'capture screen meeting_notes.png'
   • 'quick capture "Important Update"'
   • 'capture window "Calculator"'
   • 'annotate image screenshot_20241201_143022.png'

📊 **Features:**
   • Automatic filename generation with timestamps
   • Multiple image formats (PNG, JPG)
   • Metadata tracking and management
   • High-quality image capture
   • Batch annotation support

⚠️ **Requirements:**
   • pyautogui for screen capture
   • Pillow (PIL) for image editing
   • Install with: pip install pyautogui Pillow
"""
