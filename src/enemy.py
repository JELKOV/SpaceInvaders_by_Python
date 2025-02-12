import pygame
import settings

class Enemy:
    def __init__(self, x, y, speed_x):
        """ 적 외계인 초기화 """
        self.x = x
        self.y = y
        self.speed_x = speed_x
        # 적 이미지 로드
        self.image = pygame.image.load("../assets/images/enemy.png")
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        """ 적 이동: 좌우로 움직이고, 벽에 닿으면 방향 변경 """
        self.rect.x += self.speed_x
        if self.rect.right >= settings.SCREEN_WIDTH or self.rect.left <= 0:
            self.speed_x *= -1  # 방향 반전

    def draw(self, screen):
        """ 적을 화면에 그림 """
        screen.blit(self.image, self.rect)
