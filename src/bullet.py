import pygame

class Bullet:
    def __init__(self, x, y, speed):
        """ 총알 초기화 """
        self.x = x
        self.y = y
        self.speed = speed
        # 총알 이미지 로드
        self.image = pygame.image.load("../assets/images/bullet.png")
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        """ 총알을 위쪽으로 이동 """
        self.rect.y -= self.speed

    def check_collision(self, enemy):
        """적과의 충돌여부 확인"""
        return self.rect.colliderect(enemy.rect)

    def draw(self, screen):
        """ 총알을 화면에 그림 """
        screen.blit(self.image, self.rect)