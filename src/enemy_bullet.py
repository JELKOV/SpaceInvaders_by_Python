import pygame
import os

# 현재 파일 위치를 기준으로 assets 폴더 설정
base_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_path, "..", "assets", "images", "enemy-bullet.png")

class EnemyBullet:
    def __init__(self, x, y, speed):
        """적 미사일 초기화"""
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.destroyed = False  # 미사일이 삭제되었는지 여부

    def move(self):
        """미사일을 아래쪽으로 이동"""
        if self.destroyed:
            return  # 삭제된 미사일은 이동하지 않음
        self.rect.y += self.speed

    def check_collision(self, target):
        """ 충돌 감지 """
        return self.rect.colliderect(target.rect)

    def destroy(self, bullet_list):
        """ 미사일을 삭제하는 안전한 로직 """
        if self in bullet_list:
            bullet_list.remove(self)  # 리스트에서 안전하게 삭제
        self.destroyed = True  # 삭제된 상태로 변경
        self.rect.y = -100  # 화면 바깥으로 이동시켜 충돌 방지

    def draw(self, screen):
        """삭제된 미사일은 화면에 표시되지 않음"""
        if self.destroyed:
            return
        screen.blit(self.image, self.rect)
