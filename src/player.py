import pygame
import settings

class Player:
    def __init__(self, x, y, speed):
        """플레이어 초기화"""
        self.x = x
        self.y = y
        self.speed = speed

        """플레이어 이미지 로드"""
        self.image = pygame.image.load('../assets/images/player.png')
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move_left(self):
        """ 플레이어를 왼쪽으로 이동 (화면 밖으로 나가지 않도록 제한) """
        if self.rect.left > 0:
            self.rect.left -= self.speed

    def move_right(self):
        """ 플레이어를 오른쪽으로 이동 (화면 밖으로 나가지 않도록 제한) """
        if self.rect.right < settings.SCREEN_WIDTH:
            self.rect.right += self.speed

    def draw(self, screen):
        """ 플레이어를 화면에 그림 """
        screen.blit(self.image, self.rect)