import pygame
import settings
import sys
import os
from game_manager import GameManager

# `src` 경로를 강제로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    # Pygame 초기화
    pygame.init()

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
    try:
        main()
    except KeyboardInterrupt:
        print("게임이 강제 종료되었습니다.")
    finally:
        pygame.quit()  # ⬅ 프로그램 종료 시 Pygame을 정리