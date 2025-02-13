import pygame
import settings
import os
from game_manager import GameManager

def main():
    # Pygame 초기화
    pygame.init()

    # 현재 스크립트가 있는 디렉토리로 작업 디렉토리 변경
    os.chdir(os.path.dirname(__file__))

    # 게임화면 생성( 설정에서 불러옴
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")

    # FPS 조절을 위한 Clock 객체
    clock=pygame.time.Clock()

    # 게임 매니저 새성
    game = GameManager(screen)

    while game.running:
        # 이벤트 처리 키 입력
        game.handle_events()
        # 게임 상태 업데이트 (플레이어, 적, 총알 움직임)
        game.update()
        # 화면에 요소 그리기
        game.render()
        # FPS 유지
        clock.tick(settings.FPS)
    # 게임 오버 시 게임 오버 화면 실행
    game.game_over_screen()

    # 게임 종료
    pygame.quit()

if __name__ == "__main__":
    main()