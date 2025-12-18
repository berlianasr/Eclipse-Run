import os
import pygame
import random
from src.core import settings
from src.entities.sun import Sun
from src.entities.moon import Moon
from src.systems.physics import move_with_collisions
from src.systems.pov import POVController
from src.environment.tiles import TILE_SIZE, T_EXIT, T_HOLE, T_AIR, T_GROUND, T_WALL
from .base_screen import BaseScreen
from ..ui.button import Button

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
OBSTACLE_DIR = os.path.join(BASE_DIR, "assets", "images", "obstacle")

# Entity kecil helper untuk Balok
class FallingBlock:
    def __init__(self, x, y, speed, is_spike_block=False):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = speed
        self.active = True
        self.is_spike_block = is_spike_block
        self.sprite = None
        self._load_sprite()
    
    def _load_sprite(self):
        """Load block sprite"""
        if self.is_spike_block:
            filepath = os.path.join(OBSTACLE_DIR, "block_spikes.png")
        else:
            filepath = os.path.join(OBSTACLE_DIR, "block_red.png")
        
        try:
            img = pygame.image.load(filepath).convert_alpha()
            self.sprite = pygame.transform.scale(img, (40, 40))
        except Exception as e:
            print(f"Warning: failed to load block sprite: {e}")
            self.sprite = None
    
    def update(self, is_side):
        if is_side:
            self.rect.y += self.speed
        if self.rect.y > settings.HEIGHT:
            self.active = False 

    def draw(self, surface, is_side):
        if self.sprite:
            surface.blit(self.sprite, self.rect)
        else:
            # Fallback drawing
            color = (180, 50, 50) if is_side else (100, 30, 30)
            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, (50, 0, 0), self.rect, 2)

class LevelBase(BaseScreen):
    def __init__(self, manager, screen_width: int, screen_height: int, arena, level_num=1):
        super().__init__(manager, screen_width, screen_height)
        self.arena = arena
        self.level_num = level_num
        self.pov = POVController()
        
        # setup player - spawn centered in tile, accounting for 40x40 player size
        spawn_col, spawn_row = self.arena.start_pos
        player_size = 40
        cx = (spawn_col * TILE_SIZE) + (TILE_SIZE - player_size) // 2
        cy = (spawn_row * TILE_SIZE) + (TILE_SIZE - player_size) // 2
        self.spawn_pos_xy = (cx, cy)
        self.sun = Sun(cx, cy)
        self.moon = Moon(cx + player_size, cy)

        # logika tombol
        self.mechanic_map = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'g': '6', 'h': '7', 'i': '8', 'j': '9'}

        # Balok jatuh
        self.blocks = []
        self.blocks_active = False
        
        # atifkan logika jika config ada
        if self.arena.falling_block_config:
            self.blocks_active = True
            self.block_timer = 0
            # Ambil data dari Arena
            self.block_interval = self.arena.falling_block_config.get('interval', 60)
            self.block_speed = self.arena.falling_block_config.get('speed', 3)
        
        # Timer untuk durasi level
        self.time_elapsed = 0.0
        
        # Exit button di level
        button_width = 100
        button_height = 40
        self.exit_button = Button(
            pygame.Rect(screen_width - button_width - 10, 10, button_width, button_height),
            "Exit",
            pygame.font.SysFont(None, 24),
            bg_color=(160, 100, 70),
            hover_color=(200, 150, 100)
        )

    def handle_event(self, event):
        # Handle exit button click
        if self.exit_button.handle_event(event):
            from .main_menu import MainMenuScreen
            self.manager.switch_to(MainMenuScreen(self.manager, self.screen_width, self.screen_height))
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Kembali ke menu
                from .main_menu import MainMenuScreen
                new_screen = MainMenuScreen(self.manager, self.screen_width, self.screen_height)
                self.manager.switch_to(new_screen)
            elif event.key == pygame.K_SPACE:
                self.pov.toggle()

    def _get_tile_under_feet(self, player):
        rect = player.get_rect()
        feet_y = rect.bottom + 2 
        col = rect.centerx // TILE_SIZE
        row = (feet_y - self.arena.origin_y) // TILE_SIZE
        if row < 0 or row >= self.arena.rows or col < 0 or col >= self.arena.cols: return None, -1, -1
        return self.arena.layout[row][col], row, col

    def update_mechanics(self):
        """Menjalankan Logika Rintangan (Tombol & Balok)"""
        is_side = self.pov.is_side()

        # lubang dihilangkan
        for key, coords in self.arena.hole_positions.items():
            for (hx, hy) in coords:
                self.arena.layout[hy][hx] = T_HOLE 
        
        # Clear pressed buttons dari frame sebelumnya
        self.arena.pressed_buttons.clear()
        
        # Cek penekanan tombol
        if is_side:
            _, r_sun, c_sun = self._get_tile_under_feet(self.sun)
            _, r_moon, c_moon = self._get_tile_under_feet(self.moon)
            
            for btn, pos_list in self.arena.button_positions.items():
                for bx, by in pos_list:
                    # Check jika salah satu player menginjak tombol ini
                    if (c_sun == bx and r_sun == by) or (c_moon == bx and r_moon == by):
                        # Track tombol ini sedang ditekan untuk sprite rendering
                        self.arena.pressed_buttons.add((bx, by))
                        
                        # Trigger hole logic
                        hole_id = self.mechanic_map.get(btn)
                        if hole_id in self.arena.hole_positions:
                            # Ubah T_HOLE jadi T_AIR
                            for (hx, hy) in self.arena.hole_positions[hole_id]:
                                self.arena.layout[hy][hx] = T_AIR

        # balok jatuh
        if self.blocks_active:
            # Spawn
            if is_side:
                self.block_timer += 1
                if self.block_timer >= self.block_interval:
                    rx = random.randint(50, settings.WIDTH - 50)
                    # Use spike blocks for level 2 and 3
                    is_spike = self.level_num in [2, 3]
                    self.blocks.append(FallingBlock(rx, -50, self.block_speed, is_spike_block=is_spike))
                    self.block_timer = 0
            
            # Update Gerak
            for b in self.blocks:
                b.update(is_side)
            
            # Hapus balok mati
            self.blocks = [b for b in self.blocks if b.active]

    def check_death_condition(self):
        """Return death type: None (alive), 'hole' (jatuh lubang), atau 'block' (tertimpa balok)"""
        # Cek Jatuh ke Lubang
        t_sun, _, _ = self._get_tile_under_feet(self.sun)
        t_moon, _, _ = self._get_tile_under_feet(self.moon)

        if t_sun == T_HOLE or t_moon == T_HOLE:
            print("MATI: Terkena Black Hole!")
            return 'hole'
        
        # Cek Tertimpa Balok (Black Hole)
        if self.blocks_active and self.pov.is_side():
            for b in self.blocks:
                if b.rect.colliderect(self.sun.get_rect()) or b.rect.colliderect(self.moon.get_rect()):
                    print("MATI: Tertimpa Balok!")
                    return 'block'
        
        return None

    def _reset_players(self):
        x, y = self.spawn_pos_xy
        self.sun = Sun(x, y)
        self.moon = Moon(x + 20, y)
        self.blocks = [] # Bersihkan balok saat reset

    def _get_player_grid_pos(self, player) -> tuple:
        """Get player's current grid position (col, row)"""
        player_rect = player.get_rect()
        col = player_rect.centerx // TILE_SIZE
        row = player_rect.centery // TILE_SIZE
        return (col, row)
    
    def _both_players_at_exit(self) -> bool:
        """Check if BOTH players are on the same grid as the finish tile"""
        exit_col, exit_row = self.arena.exit_pos
        
        sun_col, sun_row = self._get_player_grid_pos(self.sun)
        moon_col, moon_row = self._get_player_grid_pos(self.moon)
        
        # Kedua player harus berada di grid yang sama dengan finish
        sun_at_finish = (sun_col == exit_col and sun_row == exit_row)
        moon_at_finish = (moon_col == exit_col and moon_row == exit_row)
        
        return sun_at_finish and moon_at_finish

    def update(self, dt):
        # Update timer
        self.time_elapsed += dt
        
        keys = pygame.key.get_pressed()
        dx_sun, dy_sun = self.sun.get_desired_move(keys)
        dx_moon, dy_moon = self.moon.get_desired_move(keys)

        if self.pov.is_side():
            dy_sun = 0; dy_moon = 0
        
        # Logika Rintangan
        self.update_mechanics()

        # Update player animations
        self.sun.update(dt, self.pov.is_side())
        self.moon.update(dt, self.pov.is_side())

        # 2. Update Fisika Player
        sun_fell = move_with_collisions(self.sun, self.arena, dx_sun, dy_sun, apply_gravity=self.pov.is_side())
        moon_fell = move_with_collisions(self.moon, self.arena, dx_moon, dy_moon, apply_gravity=self.pov.is_side())

        # 3. Cek Mati / Menang
        death_type = self.check_death_condition()
        if sun_fell or moon_fell or death_type:
            # Show hit animation before death
            self.sun.set_hitting()
            self.moon.set_hitting()
            # Trigger game over screen untuk semua jenis kematian
            from .game_over import GameOverScreen
            game_over_screen = GameOverScreen(self.manager, self.screen_width, self.screen_height, 
                                            score=0, level_num=self.level_num)
            self.manager.switch_to(game_over_screen)
            return

        if self._both_players_at_exit():
            # Set finish sprite ke open state
            self.arena.is_finish_open = True
            
            print(f"LEVEL {self.level_num} SELESAI! Durasi: {self.time_elapsed:.2f} detik")
            # Go to finish screen
            from .level_finish import LevelFinishScreen
            next_screen = LevelFinishScreen(self.manager, self.screen_width, self.screen_height, 
                                           level_num=self.level_num, time_elapsed=self.time_elapsed)
            self.manager.switch_to(next_screen)

    def draw(self, surface):
        surface.fill(settings.BG_COLOR)
        is_side = self.pov.is_side()
        
        # Gambar Arena
        if is_side: self.arena.draw_side(surface)
        else: self.arena.draw_top(surface)
            
        # Gambar Balok
        for b in self.blocks:
            b.draw(surface, is_side)

        # Gambar Player
        if is_side:
            self.sun.draw_side(surface)
            self.moon.draw_side(surface)
        else:
            self.sun.draw_top(surface)
            self.moon.draw_top(surface)

        # HUD - white text color
        font = pygame.font.SysFont(None, 32)
        white_color = (255, 255, 255)
        
        # POV indicator
        surface.blit(font.render(f"POV: {'SIDE' if is_side else 'TOP'}", True, white_color), (5,5))
        
        # Timer display
        minutes = int(self.time_elapsed) // 60
        seconds = int(self.time_elapsed) % 60
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        surface.blit(font.render(time_text, True, white_color), (5, 40))
        
        # Level indicator
        surface.blit(font.render(f"Level: {self.level_num}", True, white_color), (5, 75))
        
        # ESC hint
        hint_font = pygame.font.SysFont(None, 24)
        surface.blit(hint_font.render("Press ESC for menu", True, (100,100,100)), (5, settings.HEIGHT - 30))
        
        # Draw exit button
        self.exit_button.draw(surface)