import pygame

class Barrier:
    def __init__(self, x, y, health=20):
        """ 방어막 초기화 """
        self.images = [
            pygame.image.load("../assets/images/barrier.png"),  # 초기 상태
            pygame.image.load("../assets/images/barrier_damaged1.png"),  # 1단계 손상
            pygame.image.load("../assets/images/barrier_damaged2.png"),  # 2단계 손상
            pygame.image.load("../assets/images/barrier_damaged3.png")   # 거의 파괴됨
        ]
        self.image = self.images[0]  # 초기 이미지
        self.rect = self.image.get_rect(center=(x, y))
        self.health = health  # 방어막의 체력

    def take_damage(self):
        """ 총알에 맞으면 체력이 감소하고, 이미지 변경 """
        if self.health > 0:  # 🔹 체력이 남아있을 때만 감소
            self.health -= 1
            print(f"🛡 방어막 체력 감소: {self.health}")  # 디버깅 메시지 추가

            # 체력 단계에 따라 이미지 변경
            if self.health > 15:
                self.image = self.images[0]  # 초기 상태
            elif 10 < self.health <= 15:
                self.image = self.images[1]  # 1단계 손상
            elif 5 < self.health <= 10:
                self.image = self.images[2]  # 2단계 손상
            elif 0 < self.health <= 5:
                self.image = self.images[3]  # 거의 파괴됨

        return self.health <= 0  # 체력이 0 이하이면 True 반환 (방어막 제거)

    def draw(self, screen):
        """ 방어막을 화면에 그림 """
        if self.health > 0:
            screen.blit(self.image, self.rect)
