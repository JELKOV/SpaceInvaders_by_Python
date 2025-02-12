import pygame

class EnemyBullet:
    def __init__(self, x, y, speed):
        """적 미사일 초기화"""
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load('../assets/images/enemy-bullet.png')
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        """미사일을 아래쪽으로 이동"""
        self.rect.y += self.speed

    def draw(self, screen):
        """화면에 미사일을 그림"""
        screen.blit(self.image, self.rect)