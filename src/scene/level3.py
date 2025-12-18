from src.scene.level_base import LevelBase
from src.environment.arena import create_arena_from_layout

class Level3(LevelBase):
    def __init__(self, manager, screen_width: int, screen_height: int):
        level_map = [
            "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "T............................T",
            "T...TTTTTTTTTTTTTTTTTTTTTT...T",
            "T...T....................T...T",
            "T...T.TTTTTTTTTTTTTTTTT..T...T",
            "T...T.T...4.......5...T..T...T",
            "T...T.T.TdTdTT.TTeTeT.T..T...T",
            "T...T.T.T....T.T....T.T..T...T",
            "T...T.T.T....T.T....T.T..T...T",
            "T...T.T.T....T.T.F..T.T..T...T",
            "T...T.T.TTTT.T.T.TTTT.T..T...T",
            "T...T.T......T.T......T..T...T",
            "T...T.TTTTTTTT.TTTTTTTT..T...T",
            "T...T....................T...T",
            "T...TTTTTTTTTT.TTTTTTTTTTT...T",
            "TS...1..................3....T",
            "TTTTaTaTTTTTTb2bTTTTTTTcTcTTTT"
        ]

        arena = create_arena_from_layout(
            level_map, 
            falling_block_config={'interval': 30, 'speed': 3}
        )
        super().__init__(manager, screen_width, screen_height, arena, level_num=3)