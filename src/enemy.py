import pygame
import settings
from enemy_bullet import EnemyBullet
import random

class Enemy:
    def __init__(self, x, y, speed_x, bullet_speed):
        """ 적 외계인 초기화 """
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.bullet_speed = bullet_speed # 미사일 속도 추가
        self.direction = 1  # 1: 오른쪽 이동, -1: 왼쪽 이동
        # 적 이미지 로드
        self.image = pygame.image.load("../assets/images/enemy.png")
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # 적이 발사한 미사일 리스트
        self.bullets = []

    def move(self):
        """ 적 이동: 좌우로 움직이고, 벽에 닿으면 방향 변경 """
        self.rect.x += self.speed_x * self.direction

        if self.rect.right > settings.SCREEN_WIDTH:
            self.direction = -1
            self.rect.right = settings.SCREEN_WIDTH - 1
        elif self.rect.left <= 0:
            self.direction = 1
            self.rect.left = 1

    def shoot(self):
        """ 일정 확률로 미사일 발사 """
        if random.randint (1, 100) < 1.05:
            self.bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom, self.bullet_speed))

    def update_bullets(self):
        """ 적이 발사한 미사일 업데이트 """
        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.top > settings.SCREEN_HEIGHT:  # 화면 아래로 나가면 제거
                self.bullets.remove(bullet)

    def draw(self, screen):
        """ 적을 화면에 그림 """
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)