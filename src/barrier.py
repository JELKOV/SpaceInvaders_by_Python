import pygame

class Barrier:
    def __init__(self, x, y, health=3):
        """ 방어막 초기화 """
        self.image = pygame.image.load("../assets/images/barrier.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.health = health  # 방어막의 체력

    def take_damage(self):
        """ 총알에 맞으면 체력이 감소하고, 0이 되면 삭제됨 """
        self.health -= 1
        if self.health <= 0:
            return True  # 방어막이 파괴됨
        return False  # 아직 남아 있음

    def draw(self, screen):
        """ 방어막을 화면에 그림 """
        if self.health > 0:
            screen.blit(self.image, self.rect)
