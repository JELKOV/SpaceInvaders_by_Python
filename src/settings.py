import os

# 현재 파일 위치를 기준으로 assets 폴더 설정
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, "..", "assets", "sounds")

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# 초당 프레임 수
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 사운드 파일 절대 경로 설정
SOUND_BACKGROUND = os.path.join(ASSETS_PATH, "background.mp3")
SOUND_BULLET = os.path.join(ASSETS_PATH, "bullet.mp3")
SOUND_EXPLOSION = os.path.join(ASSETS_PATH, "explosion.mp3")
SOUND_UFO = os.path.join(ASSETS_PATH, "ufo.mp3")