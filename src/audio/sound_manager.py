import os
import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio", "sfx")


class SoundManager:
    """Manage sound effects for the game"""
    
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all sound effect files"""
        sound_files = {
            'pov': 'sfx_pov.ogg',
            'hurt': 'sfx_hurt.ogg',
            'select': 'sfx_select.ogg'
        }
        
        for key, filename in sound_files.items():
            filepath = os.path.join(AUDIO_DIR, filename)
            try:
                self.sounds[key] = pygame.mixer.Sound(filepath)
            except Exception as e:
                print(f"Warning: Failed to load sound '{filename}': {e}")
                self.sounds[key] = None
    
    def play_pov_change(self):
        """Play sound when POV changes (SIDE ↔ TOP)"""
        if self.sounds.get('pov'):
            self.sounds['pov'].play()
    
    def play_game_over(self):
        """Play sound when game over happens"""
        if self.sounds.get('hurt'):
            self.sounds['hurt'].play()
    
    def play_button_click(self):
        """Play sound when any button is clicked (menu, highscore, etc.)"""
        if self.sounds.get('select'):
            self.sounds['select'].play()
    
    def play_sound(self, key):
        """Play sound by key name"""
        if key in self.sounds and self.sounds[key]:
            self.sounds[key].play()


# Global instance
sound_manager = None


def init_sound_manager():
    """Initialize global sound manager"""
    global sound_manager
    sound_manager = SoundManager()
    return sound_manager


def get_sound_manager():
    """Get the global sound manager instance"""
    global sound_manager
    if sound_manager is None:
        sound_manager = init_sound_manager()
    return sound_manager
