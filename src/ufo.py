import pygame
import random


class UFO:
    def __init__(self, screen_width, speed=3, points=50):
        """ UFO 초기화 (보너스 적) """
        self.image = pygame.image.load("../assets/images/ufo.png")
        self.speed = speed  # UFO 이동 속도
        self.points = points  # 처치 시 보너스 점수

        # UFO가 왼쪽에서 오른쪽으로 등장할지, 반대 방향일지 결정
        if random.choice([True, False]):
            self.rect = self.image.get_rect(left=0, top=50)
            self.direction = 1
        else:
            self.rect = self.image.get_rect(right=screen_width, top=50)
            self.direction = -1

    def move(self):
        """ UFO 이동 """
        self.rect.x += self.speed * self.direction

    def draw(self, screen):
        """ UFO를 화면에 그림 """
        screen.blit(self.image, self.rect)

    def is_off_screen(self, screen_width):
        """ UFO가 화면을 벗어났는지 확인 """
        return self.rect.right < 0 or self.rect.left > screen_width
