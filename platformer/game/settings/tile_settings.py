import general_settings

NORMAL          = 0
RIGHT_SLOPE_1   = 1
LEFT_SLOPE_1    = 2
RIGHT_SLOPE_2_1 = 3
RIGHT_SLOPE_2_2 = 4
LEFT_SLOPE_2_1  = 5
LEFT_SLOPE_2_2  = 6
TOP_LEFT_SLOPE_1    = 7

# 1 tile rightward slopes
RIGHT_SLOPE_1_LEFT_Y  = 0
RIGHT_SLOPE_1_RIGHT_Y = general_settings.TILE_SIZE

# 1 tile leftward slopes
LEFT_SLOPE_1_LEFT_Y  = general_settings.TILE_SIZE
LEFT_SLOPE_1_RIGHT_Y = 0

# 1 tile upper leftward slopes
TOP_LEFT_SLOPE_1_LEFT_Y  = 0
TOP_LEFT_SLOPE_1_RIGHT_Y = general_settings.TILE_SIZE

# 2 tile rightward slopes
RIGHT_SLOPE_2_1_LEFT_Y  = 0
RIGHT_SLOPE_2_1_RIGHT_Y = 16
RIGHT_SLOPE_2_2_LEFT_Y  = 17
RIGHT_SLOPE_2_2_RIGHT_Y = general_settings.TILE_SIZE

# 2 tile leftward slopes
LEFT_SLOPE_2_1_LEFT_Y  = general_settings.TILE_SIZE
LEFT_SLOPE_2_1_RIGHT_Y = 17
LEFT_SLOPE_2_2_LEFT_Y  = 16
LEFT_SLOPE_2_2_RIGHT_Y = 0