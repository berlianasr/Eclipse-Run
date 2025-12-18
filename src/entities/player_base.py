import os
import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class PlayerBase:
    def __init__(self, x, y, color, character_name='moon'):
        self.x = x
        self.y = y
        self.w = 40  
        self.h = 40  
        self.color = color
        self.speed = 3
        self.character_name = character_name  # 'moon' atau 'sun'
        
        # Sprite system
        self.sprites = {}
        self.current_sprite = None
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.1  # seconds per frame
        self.facing_right = True
        self.last_dx = 0  
        self.is_hitting = False  #hit animation
        self.hit_timer = 0.0
        self.hit_duration = 0.2  # Duration to show hit animation
        
        # Load sprites
        self._load_sprites()
    
    def _load_sprites(self):
        """Load all 6 sprite images untuk character"""
        sprites_dir = os.path.join(BASE_DIR, "assets", "images", self.character_name)
        
        sprite_names = ['top_a', 'top_b', 'front', 'walk_a', 'walk_b', 'hit']
        
        for name in sprite_names:
            filename = f"{self.character_name}_{name}.png"
            filepath = os.path.join(sprites_dir, filename)
            try:
                img = pygame.image.load(filepath).convert_alpha()
                # Scale sprites to fit player size
                self.sprites[name] = pygame.transform.scale(img, (self.w, self.h))
            except Exception as e:
                print(f"Warning: failed to load sprite '{filename}': {e}")
                self.sprites[name] = None
    
    def _get_sprite(self, sprite_name):
        """Get sprite by name, return None if not loaded"""
        sprite = self.sprites.get(sprite_name)
        return sprite if sprite is not None else self._create_fallback_sprite()
    
    def _create_fallback_sprite(self):
        """Create fallback surface jika sprite tidak bisa diload"""
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.w, self.h), border_radius=4)
        return surf
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)
    
    def set_hitting(self):
        """Set character to hit animation (called before death)"""
        self.is_hitting = True
        self.hit_timer = 0.0
    
    def update(self, dt, pov_is_side):
        """Update animation state"""
        # Update hit animation
        if self.is_hitting:
            self.hit_timer += dt
            if self.hit_timer >= self.hit_duration:
                self.is_hitting = False
                self.hit_timer = 0.0
        
        # Update animation frames
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.animation_frame = (self.animation_frame + 1) % 2  # Cycle between 0 and 1 untuk walk animation
    
    def set_direction(self, dx):
        """Set character facing direction based on movement"""
        if dx != 0:
            self.last_dx = dx
            self.facing_right = dx > 0

    def draw_side(self, screen):
        """Draw character at SIDE POV dengan sprite"""
        if self.is_hitting:
            #hit animation
            sprite = self._get_sprite('hit')
        else:
            
            if self.animation_frame == 0:
                sprite = self._get_sprite('walk_a')
            else:
                sprite = self._get_sprite('walk_b')
        
        # Flip sprite based on facing direction
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        rect = sprite.get_rect(topleft=(int(self.x), int(self.y)))
        screen.blit(sprite, rect)

    def draw_top(self, screen):
        """Draw character at TOP POV dengan sprite - flip based on facing direction"""
        if self.is_hitting:
            #hit animation
            sprite = self._get_sprite('hit')
        else:
            if self.animation_frame == 0:
                sprite = self._get_sprite('top_a')
            else:
                sprite = self._get_sprite('top_b')
        
        # Flip sprite based on facing direction (only flip horizontally in TOP POV)
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        rect = sprite.get_rect(topleft=(int(self.x), int(self.y)))
        screen.blit(sprite, rect)
    
    def draw_side_fallback(self, screen):
        """Fallback drawing untuk SIDE POV jika sprites tidak available"""
        rect = self.get_rect()
        pygame.draw.rect(screen, self.color, rect, border_radius=4)
        pygame.draw.rect(screen, (40, 40, 40), rect, 2, border_radius=4)

    def draw_top_fallback(self, screen):
        """Fallback drawing untuk TOP POV jika sprites tidak available"""
        rect = self.get_rect()
        center_x = rect.centerx
        center_y = rect.centery
        radius = self.w // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
        pygame.draw.circle(screen, (40, 40, 40), (center_x, center_y), radius, 2)
        # Indikator arah
        pygame.draw.line(screen, (40, 40, 40), (center_x, center_y), (center_x, center_y - radius), 2)