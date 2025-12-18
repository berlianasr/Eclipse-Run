from src.scene.level_base import LevelBase
from src.environment.arena import create_arena_from_layout

class Level1(LevelBase):
    def __init__(self, manager, screen_width: int, screen_height: int):
        level_map = [
            "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",
            "T..............TTT..4..TTT...T",
            "T..........TTT.TTT.TTT.TTT...T",
            "TTTTTTTTTT.TTT.TTT.TTT.TTT...T",
            "T...3......TTT.....TTT.......T",
            "TF..3......TTTTTTTdTTTdTTTT..T",
            "TTTcTT..TTTTTTTTTTTTTTTTTTT..T",
            "TTTTTT..T....................T",
            "TTTTTTcTTTTT.TTTTTTTTTTTTTTTTT",
            "TTTTTTTTTTTT..........222....T",
            "TTTTTTTTTTTTTTTTTT....222....T",
            "TTTTTTTTTTTTTTTTTTbTTTTTTTTb.T",
            "T.....111..........TTT.....T.T",
            "T.....111....TTTTT...........T",
            "T..TaTTTTTaTTTTTTTTTTTTTTTT..T",
            "TS.T.........................T",
            "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"
        ]
        
        arena = create_arena_from_layout(level_map, falling_block_config=None)
        super().__init__(manager, screen_width, screen_height, arena, level_num=1)