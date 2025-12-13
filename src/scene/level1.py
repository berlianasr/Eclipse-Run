# src/scene/level1.py
import pygame
from src.core import settings
from src.entities.sun import Sun
from src.entities.moon import Moon
from src.environment.arena import create_level1_arena
from src.systems.physics import move_with_collisions
from src.environment.tiles import TILE_SIZE


class Level1:
    def __init__(self, game):
        self.game = game

        # arena + jembatan
        self.arena, self.bridge = create_level1_arena()
        self.ground_y = self.arena.ground_y()

        # posisi spawn awal
        self.spawn_sun = (200, self.ground_y - 40)
        self.spawn_moon = (260, self.ground_y - 40)

        self.sun = Sun(*self.spawn_sun)
        self.moon = Moon(*self.spawn_moon)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.running = False

    def _player_tile(self, player):
        """Hitung posisi tile (row,col) berdasarkan pusat player."""
        rect = player.get_rect()
        cx = rect.centerx
        cy = rect.centery
        col = cx // TILE_SIZE
        row = (cy - self.arena.origin_y) // TILE_SIZE
        return int(row), int(col)

    def _update_bridge_state(self):
        """Aktifkan jembatan jika salah satu player sedang di tombol."""
        row_sun, col_sun = self._player_tile(self.sun)
        row_moon, col_moon = self._player_tile(self.moon)

        sun_on_button = self.bridge.is_button_tile(row_sun, col_sun)
        moon_on_button = self.bridge.is_button_tile(row_moon, col_moon)

        active = sun_on_button or moon_on_button
        self.bridge.set_active(self.arena.layout, active)

    def _reset_players(self):
        """Untuk sementara: kalau jatuh ke lubang, respawn ke posisi awal."""
        self.sun = Sun(*self.spawn_sun)
        self.moon = Moon(*self.spawn_moon)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        dx_sun, dy_sun = self.sun.get_desired_move(keys)
        dx_moon, dy_moon = self.moon.get_desired_move(keys)

        # BEDAIN PERILAKU BERDASARKAN POV
        if self.game.pov.is_side():
            # Mode SIDE: gerak horizontal saja
            dy_sun = 0
            dy_moon = 0

        # Gerak + collision + cek jatuh ke lubang
        sun_fell = move_with_collisions(self.sun, self.arena, dx_sun, dy_sun)
        moon_fell = move_with_collisions(self.moon, self.arena, dx_moon, dy_moon)

        if sun_fell or moon_fell:
            print("Jatuh ke lubang! Respawn...")
            self._reset_players()
            return

        # Update ON/OFF jembatan (kalau ada yang berdiri di tombol)
        self._update_bridge_state()

        # Cek apakah dua-duanya sudah di exit
        sun_at_exit = self._on_exit(self.sun)
        moon_at_exit = self._on_exit(self.moon)

        if sun_at_exit and moon_at_exit:
            print("Level 1 CLEAR!")
            # sementara: reset saja dulu
            self._reset_players()
            # nanti dihubungkan ke scene level2 / game_over / dsb

    def draw(self, surface):
        surface.fill(settings.BG_COLOR)
        self.arena.draw_side(surface)
        self.sun.draw_side(surface)
        self.moon.draw_side(surface)

        # ---- HUD kecil: tampilkan mode POV ----
        font = pygame.font.SysFont(None, 32)
        if self.game.pov.is_side():
            text = font.render("POV: SIDE", True, (40, 40, 40))
        else:
            text = font.render("POV: TOP", True, (40, 40, 160))

        surface.blit(text, (16, 16))




    def _on_exit(self, player) -> bool:
        """True kalau player sedang berdiri di tile EXIT."""
        from src.environment.tiles import TILE_SIZE, T_EXIT

        rect = player.get_rect()
        cx = rect.centerx
        cy = rect.centery
        col = cx // TILE_SIZE

        row = (cy - self.arena.origin_y) // TILE_SIZE

        if row < 0 or row >= self.arena.rows or col < 0 or col >= self.arena.cols:
            return False

        tile_id = self.arena.layout[row][col]
        return tile_id == T_EXIT
