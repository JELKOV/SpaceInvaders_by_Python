import pygame
import settings
from player import Player
from enemy import Enemy
from bullet import Bullet

class GameManager:
    def __init__(self, screen):
        """ 게임 매니저 초기화 """
        self.screen = screen
        self.player = Player(400, 550, 5)
        self.enemies = [Enemy(100 * i, 50, 2) for i in range(5)]
        self.bullets = []
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 36)

    def handle_events(self):
        """ 게임 매니저 초기화 """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(self.player.rect.centerx, self.player.rect.top, 5))

    def update(self):
        """ 게임 상태 업데이트 """
        for enemy in self.enemies:
            # 점수가 올라갈수록 속도 증가 (난이도 조절)
            enemy.speed_x = 2 + (self.score // 50)
            enemy.move()

        for bullet in self.bullets:
            bullet.move()

            # 총알이 적과 충돌했는지 확인
            for enemy in self.enemies:
                if bullet.check_collision(enemy):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.score += 10 # 점수 증가
                    break # 충돌 확인한후 반복종료

    def render(self):
        """ 화면을 새로 그리는 함수 """
        self.screen.fill(settings.BLACK) # 배경을 검은색으로 채움
        self.player.draw(self.screen) # 플레이어 그림
        for enemy in self.enemies:
            enemy.draw(self.screen) # 적 그림
        for bullet in self.bullets:
            bullet.draw(self.screen) # 총알 그림

        # 점수표시
        score_text = self.font.render("Score: %d" % self.score, True, settings.WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()