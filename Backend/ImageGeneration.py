"""
ImageGeneration.py
Advanced AI image generation for JARVIS using multiple backends.
"""

import os
import requests
import base64
import json
from typing import Optional, Dict, Any
from datetime import datetime
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()

class JarvisImageGen:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.stability_api_key = os.getenv("STABILITY_API_KEY")
        self.output_dir = "Frontend/Files"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Image generation parameters
        self.default_params = {
            'width': 1024,
            'height': 1024,
            'steps': 30,
            'cfg_scale': 7.0,
            'style': 'photographic'
        }
    
    def generate_image(self, prompt: str, style: str = "photographic", 
                      width: int = 1024, height: int = 1024) -> str:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt: Text description of the image
            style: Image style (photographic, digital-art, cinematic, etc.)
            width: Image width
            height: Image height
            
        Returns:
            str: Status message with file path or error
        """
        try:
            print(f"🎨 Generating image: {prompt}")
            
            # Try different image generation services
            if self.stability_api_key:
                return self._generate_with_stability_ai(prompt, style, width, height)
            elif self.openai_api_key:
                return self._generate_with_dalle(prompt)
            else:
                return self._generate_placeholder_image(prompt, width, height)
                
        except Exception as e:
            return f"❌ Image generation error: {str(e)}"
    
    def _generate_with_stability_ai(self, prompt: str, style: str, 
                                   width: int, height: int) -> str:
        """
        Generate image using Stability AI API.
        """
        try:
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.stability_api_key}"
            }
            
            body = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1
                    }
                ],
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": 1,
                "steps": 30,
                "style_preset": style
            }
            
            response = requests.post(url, headers=headers, json=body)
            
            if response.status_code == 200:
                data = response.json()
                
                # Save the generated image
                for i, image in enumerate(data["artifacts"]):
                    image_data = base64.b64decode(image["base64"])
                    
                    # Generate filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"jarvis_generated_{timestamp}.png"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(image_data)
                    
                    return f"✅ Image generated successfully!\n🖼️ Saved as: {filepath}\n📝 Prompt: {prompt}"
            else:
                return f"❌ Stability AI API error: {response.text}"
                
        except Exception as e:
            return f"❌ Stability AI generation error: {str(e)}"
    
    def _generate_with_dalle(self, prompt: str) -> str:
        """
        Generate image using OpenAI DALL-E API.
        """
        try:
            import openai
            
            openai.api_key = self.openai_api_key
            
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            image_url = response['data'][0]['url']
            
            # Download the image
            img_response = requests.get(image_url)
            
            if img_response.status_code == 200:
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"jarvis_dalle_{timestamp}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(img_response.content)
                
                return f"✅ Image generated with DALL-E!\n🖼️ Saved as: {filepath}\n📝 Prompt: {prompt}"
            else:
                return f"❌ Failed to download DALL-E image"
                
        except Exception as e:
            return f"❌ DALL-E generation error: {str(e)}"
    
    def _generate_placeholder_image(self, prompt: str, width: int, height: int) -> str:
        """
        Generate a placeholder image when no API is available.
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a new image with a gradient background
            img = Image.new('RGB', (width, height), color='lightblue')
            draw = ImageDraw.Draw(img)
            
            # Try to use a better font, fall back to default
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Add text
            text_lines = [
                "JARVIS Image Generation",
                "",
                f"Prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}",
                "",
                "Configure API keys for AI generation:",
                "- STABILITY_API_KEY (Stability AI)",
                "- OPENAI_API_KEY (DALL-E)",
            ]
            
            y_offset = height // 4
            for line in text_lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                draw.text((x, y_offset), line, fill='black', font=font)
                y_offset += 40
            
            # Save the placeholder image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jarvis_placeholder_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            img.save(filepath)
            
            return f"🖼️ Placeholder image created: {filepath}\n💡 Set up API keys for AI image generation!\n📝 Prompt: {prompt}"
            
        except Exception as e:
            return f"❌ Placeholder generation error: {str(e)}"
    
    def enhance_prompt(self, basic_prompt: str) -> str:
        """
        Enhance a basic prompt with artistic details.
        
        Args:
            basic_prompt: Simple prompt
            
        Returns:
            str: Enhanced prompt
        """
        enhancements = [
            "highly detailed",
            "professional photography",
            "8k resolution",
            "cinematic lighting",
            "masterpiece quality"
        ]
        
        enhanced = f"{basic_prompt}, {', '.join(enhancements)}"
        return enhanced
    
    def get_image_styles(self) -> Dict[str, str]:
        """
        Get available image styles.
        
        Returns:
            Dict: Available styles with descriptions
        """
        return {
            "photographic": "Realistic, photo-like images",
            "digital-art": "Digital artwork style",
            "cinematic": "Movie/film-like quality",
            "anime": "Anime/manga style",
            "fantasy-art": "Fantasy and magical themes",
            "line-art": "Clean line drawings",
            "comic-book": "Comic book illustration style",
            "3d-model": "3D rendered appearance",
            "pixel-art": "Retro pixel art style",
            "origami": "Paper folding art style"
        }
    
    def create_image_collage(self, image_paths: list, output_name: str = None) -> str:
        """
        Create a collage from multiple images.
        
        Args:
            image_paths: List of image file paths
            output_name: Output filename (optional)
            
        Returns:
            str: Status message
        """
        try:
            if not image_paths:
                return "❌ No images provided for collage"
            
            # Load images
            images = []
            for path in image_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    images.append(img)
            
            if not images:
                return "❌ No valid images found"
            
            # Create collage (simple 2x2 grid for up to 4 images)
            if len(images) == 1:
                collage = images[0]
            elif len(images) == 2:
                # Side by side
                width = images[0].width + images[1].width
                height = max(images[0].height, images[1].height)
                collage = Image.new('RGB', (width, height))
                collage.paste(images[0], (0, 0))
                collage.paste(images[1], (images[0].width, 0))
            else:
                # 2x2 grid
                img_width = max(img.width for img in images[:4])
                img_height = max(img.height for img in images[:4])
                
                collage = Image.new('RGB', (img_width * 2, img_height * 2))
                
                positions = [(0, 0), (img_width, 0), (0, img_height), (img_width, img_height)]
                for i, img in enumerate(images[:4]):
                    resized = img.resize((img_width, img_height))
                    collage.paste(resized, positions[i])
            
            # Save collage
            if not output_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_name = f"jarvis_collage_{timestamp}.png"
            
            output_path = os.path.join(self.output_dir, output_name)
            collage.save(output_path)
            
            return f"✅ Image collage created: {output_path}"
            
        except Exception as e:
            return f"❌ Collage creation error: {str(e)}"

# Convenience functions for backward compatibility
def generate_image(prompt: str, out_path: str = None):
    """Generate image using JARVIS image generator."""
    gen = JarvisImageGen()
    return gen.generate_image(prompt)

if __name__ == "__main__":
    # Test image generation
    generator = JarvisImageGen()
    
    print("Testing JARVIS Image Generation...")
    
    # Test image generation
    print("\n1. Image Generation Test:")
    result = generator.generate_image("a futuristic AI robot assistant", "photographic")
    print(result)
    
    # Test styles
    print("\n2. Available Styles:")
    styles = generator.get_image_styles()
    for style, description in styles.items():
        print(f"   {style}: {description}")
    
    print("\nImage generation testing complete!")
