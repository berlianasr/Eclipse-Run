from src.scene.level_base import LevelBase
from src.environment.arena import create_arena_from_layout

class Level2(LevelBase):
    def __init__(self, game):
        level_map = [
                    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
                    "T7777777777777777777777777777T",
                    "T...888......................T",
                    "T...888.TTTTTTTTTTTTTTTTTTTT.T",
                    "TF..888.T....................T",
                    "TTThTTThT..TTTTTTTTTTTTTTTTTTT",
                    "TS..111TTT.....9...9...9...9.T",
                    "TTT.111TTTT..9...9...9...9...T",
                    "TTT.111TTTTT...9...9...9...9.T",
                    "TTT.111TTTTTTTTTTTTTTTTTTTTT.T",
                    "TTT.111TTTTT..3..44444..5....T",
                    "TTT.111TTTT..333..444..555...T",
                    "TTT.111TTT..33333..4..55555..T",
                    "TTT.111....cTTTTTcdTdeTTTTTeTT",
                    "TTTaTTTTT....................T",
                    "TTTTTTTTTa2222222222222222222T",
                    "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"
                ]

        arena = create_arena_from_layout(
            level_map, 
            falling_block_config={'interval': 150, 'speed': 1}
        )
        
        super().__init__(game, arena)