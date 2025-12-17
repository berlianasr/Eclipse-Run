import pygame
import random
from src.core import settings
from src.entities.sun import Sun
from src.entities.moon import Moon
from src.systems.physics import move_with_collisions
from src.environment.tiles import TILE_SIZE, T_EXIT, T_HOLE, T_AIR, T_GROUND, T_WALL

# Entity kecil helper untuk Balok
class FallingBlock:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = speed
        self.active = True
    
    def update(self, is_side):
        if is_side:
            self.rect.y += self.speed
        if self.rect.y > settings.HEIGHT:
            self.active = False 

    def draw(self, surface, is_side):
        color = (180, 50, 50) if is_side else (100, 30, 30)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (50, 0, 0), self.rect, 2)

class LevelBase:
    def __init__(self, game, arena, bridge=None):
        self.game = game
        self.arena = arena
        
        # setup player
        spawn_col, spawn_row = self.arena.start_pos
        cx = (spawn_col * TILE_SIZE) + (TILE_SIZE - 20) // 2
        cy = (spawn_row * TILE_SIZE) + (TILE_SIZE - 20) // 2
        self.spawn_pos_xy = (cx, cy)
        self.sun = Sun(cx, cy)
        self.moon = Moon(cx + 20, cy)

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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.running = False

    def _get_tile_under_feet(self, player):
        rect = player.get_rect()
        feet_y = rect.bottom + 2 
        col = rect.centerx // TILE_SIZE
        row = (feet_y - self.arena.origin_y) // TILE_SIZE
        if row < 0 or row >= self.arena.rows or col < 0 or col >= self.arena.cols: return None, -1, -1
        return self.arena.layout[row][col], row, col

    def update_mechanics(self):
        """Menjalankan Logika Rintangan (Tombol & Balok)"""
        is_side = self.game.pov.is_side()

        # lubang dihilangkan
        for key, coords in self.arena.hole_positions.items():
            for (hx, hy) in coords:
                self.arena.layout[hy][hx] = T_HOLE 
        
        # Cek penekanan tombol
        if is_side:
            _, r_sun, c_sun = self._get_tile_under_feet(self.sun)
            _, r_moon, c_moon = self._get_tile_under_feet(self.moon)
            
            for btn, pos_list in self.arena.button_positions.items():
                pressed = any((c_sun == bx and r_sun == by) or (c_moon == bx and r_moon == by) for bx, by in pos_list)
                if pressed:
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
                    self.blocks.append(FallingBlock(rx, -50, self.block_speed))
                    self.block_timer = 0
            
            # Update Gerak
            for b in self.blocks:
                b.update(is_side)
            
            # Hapus balok mati
            self.blocks = [b for b in self.blocks if b.active]

    def check_death_condition(self):
        # Cek Jatuh ke Lubang
        t_sun, _, _ = self._get_tile_under_feet(self.sun)
        t_moon, _, _ = self._get_tile_under_feet(self.moon)

        if t_sun == T_HOLE or t_moon == T_HOLE:
            print("MATI: Masuk Lubang!")
            self._reset_players()
            return True
        
        # Cek Tertimpa Balok
        if self.blocks_active and self.game.pov.is_side():
            for b in self.blocks:
                if b.rect.colliderect(self.sun.get_rect()) or b.rect.colliderect(self.moon.get_rect()):
                    print("MATI: Tertimpa Balok!")
                    self._reset_players()
                    return True
        return False

    def _reset_players(self):
        x, y = self.spawn_pos_xy
        self.sun = Sun(x, y)
        self.moon = Moon(x + 20, y)
        self.blocks = [] # Bersihkan balok saat reset

    def _on_exit(self, player) -> bool:
        tile, _, _ = self._get_tile_under_feet(player)
        return tile == T_EXIT

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx_sun, dy_sun = self.sun.get_desired_move(keys)
        dx_moon, dy_moon = self.moon.get_desired_move(keys)

        if self.game.pov.is_side():
            dy_sun = 0; dy_moon = 0
        
        # Logika Rintangan
        self.update_mechanics()

        # 2. Update Fisika Player
        sun_fell = move_with_collisions(self.sun, self.arena, dx_sun, dy_sun, apply_gravity=self.game.pov.is_side())
        moon_fell = move_with_collisions(self.moon, self.arena, dx_moon, dy_moon, apply_gravity=self.game.pov.is_side())

        # 3. Cek Mati / Menang
        if sun_fell or moon_fell or self.check_death_condition():
            self._reset_players()
            return

        if self._on_exit(self.sun) and self._on_exit(self.moon):
            print("LEVEL SELESAI!")
            self.game.next_level()

    def draw(self, surface):
        surface.fill(settings.BG_COLOR)
        is_side = self.game.pov.is_side()
        
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

        # HUD
        font = pygame.font.SysFont(None, 32)
        surface.blit(font.render(f"POV: {'SIDE' if is_side else 'TOP'}", True, (40,40,40)), (16, 16))