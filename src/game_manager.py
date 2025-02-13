import pygame
import settings
import random
from player import Player
from enemy import Enemy
from bullet import Bullet
from src.barrier import Barrier
from src.explosion import Explosion
from src.ufo import UFO


class GameManager:
    def __init__(self, screen):
        """ 게임 매니저 초기화 """
        self.player_hit = False
        self.running = True
        self.screen = screen
        self.player = Player(400, 550, 5)
        self.enemies = [Enemy(100 * i, 50, 2,0.5) for i in range(5)]
        self.bullets = []
        self.enemy_bullets = []
        self.explosions = []  # 폭발 효과 관리 리스트
        self.explosion_sprite = pygame.image.load("../assets/images/explode.png")  # 스프라이트 시트 로드
        self.barriers = [Barrier(200, 500), Barrier(400, 500), Barrier(600, 500)]  # 방어막 3개 생성
        self.ufo = None  # 현재 활성화된 UFO
        self.ufo_timer = 0  # UFO 등장 간격을 관리하는 타이머
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 36)

    #################################################################################################################
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
        # 🔹 키 상태 확인 (누르고 있는 동안 계속 이동)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()

    #################################################################################################################

    #################################################################################################################
    def update(self):
        """ 게임 상태 업데이트 (각 기능별로 분리 리팩토링 실행) """
        self.update_enemies()
        self.update_bullets()
        self.update_explosions()
        self.update_barriers()
        self.update_ufo()

    def update_enemies(self):
        """ 적 이동 및 미사일 발사 """
        self.enemy_bullets.clear()  # 🔹 기존 리스트 초기화
        for enemy in self.enemies:
            enemy.speed_x = 2 + (self.score // 50)  # 난이도 조절
            enemy.move()
            enemy.shoot()
            enemy.update_bullets()

            # 🔹 적이 발사한 미사일을 GameManager의 enemy_bullets 리스트에 추가
            self.enemy_bullets.extend(enemy.bullets)

    def update_bullets(self):
        """ 플레이어 및 적 미사일 이동 & 충돌 처리 """

        # 플레이어 미사일 이동 & 적과 충돌 확인
        for bullet in self.bullets[:]:
            bullet.move()
            self.check_bullet_collision(bullet)

        # 적 미사일 이동 & 방어막 또는 플레이어 충돌 확인
        for bullet in self.enemy_bullets[:]:
            bullet.move()
            self.check_enemy_bullet_collision(bullet)

    def check_bullet_collision(self, bullet):
        """ 플레이어 미사일과 적 충돌 감지 """
        for enemy in self.enemies[:]:
            if bullet.check_collision(enemy):
                self.explosions.append(
                    Explosion(enemy.rect.centerx, enemy.rect.centery, self.explosion_sprite, 64, 64, 14)
                )
                self.enemies.remove(enemy)
                self.bullets.remove(bullet)
                self.score += 10
                break

    def check_enemy_bullet_collision(self, bullet):
        """ 적 미사일이 방어막이나 플레이어와 충돌했는지 확인하고 처리 """

        # 🔹 방어막과 충돌 감지
        for barrier in self.barriers[:]:  # 방어막 리스트 순회
            if bullet.rect.colliderect(barrier.rect):  # 미사일이 방어막과 충돌하면
                print(f"💥 적 미사일이 방어막과 충돌! 위치: {barrier.rect.x}, {barrier.rect.y}")  # 🔍 디버깅
                if barrier.take_damage():  # 방어막 체력이 0이 되면 제거
                    self.barriers.remove(barrier)
                self.enemy_bullets.remove(bullet)  # 적 미사일 삭제
                return  # 방어막과 충돌했으면 더 이상 검사하지 않음

        # 🔹 플레이어와 충돌 감지
        if bullet.rect.colliderect(self.player.rect):  # 플레이어와 충돌 확인
            print("🚀 플레이어 피격! 게임 오버 처리")  # 게임 오버 디버깅 메시지

            # 플레이어 위치에서 폭발 효과 추가
            self.explosions.append(
                Explosion(self.player.rect.centerx, self.player.rect.centery, self.explosion_sprite, 64, 64, 14)
            )
            self.enemy_bullets.remove(bullet)  # 미사일 삭제
            self.player_hit = True # 게임 오버 플래그 설정 (폭발 후 실행)

    def update_explosions(self):
        """ 폭발 애니메이션 업데이트 """
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.finished:
                self.explosions.remove(explosion)

                # 플레이어가 맞았던 경우, 폭발이 끝나면 게임 오버 실행
                if self.player_hit:
                    self.game_over()

    def update_barriers(self):
        """ 방어막이 총알과 충돌할 경우 체력 감소 """
        for bullet in self.bullets[:]:
            for barrier in self.barriers[:]:
                if bullet.rect.colliderect(barrier.rect):
                    if barrier.take_damage():  # 체력이 0이면 제거
                        self.barriers.remove(barrier)
                    self.bullets.remove(bullet)
                    break

    def update_ufo(self):
        """ UFO 생성, 이동 및 충돌 처리 """

        # UFO 생성 (15초마다 등장, 3번 중 1번 확률)
        self.ufo_timer += 1
        if self.ufo is None and self.ufo_timer > 900:
            if random.randint(1, 3) == 1:
                self.ufo = UFO(settings.SCREEN_WIDTH, speed=2, points=100)
            self.ufo_timer = 0  # 타이머 초기화

        # UFO 이동 및 화면에서 사라질 경우 제거
        if self.ufo:
            self.ufo.move()
            if self.ufo.is_off_screen(settings.SCREEN_WIDTH):
                self.ufo = None

        # UFO와 플레이어 미사일 충돌 처리
        if self.ufo:
            for bullet in self.bullets[:]:
                if bullet.rect.colliderect(self.ufo.rect):
                    print("🚀 UFO 격추! 보너스 점수 획득!")
                    self.score += self.ufo.points
                    self.ufo = None  # UFO 제거
                    self.bullets.remove(bullet)
                    break
    #################################################################################################################

    def game_over(self):
        """ 게임 오버 시 실행할 로직 """
        print("💀 게임 오버! 플레이어가 적 미사일에 맞았습니다.")
        self.running = False  # 게임 루프 중지
        self.game_over_screen()  # 🔹 게임 오버 화면 표시

    def game_over_screen(self):
        """ 게임 오버 화면을 표시하고, 사용자의 입력을 기다림 """
        font = pygame.font.Font('freesansbold.ttf', 48)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))

        restart_font = pygame.font.Font('freesansbold.ttf', 30)
        restart_text = restart_font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))

        while True:
            self.screen.fill((0, 0, 0))  # 화면을 검은색으로 초기화
            self.screen.blit(text, text_rect)  # "GAME OVER" 메시지 표시
            self.screen.blit(restart_text, restart_rect)  # "재시작" 메시지 표시
            pygame.display.flip()  # 화면 갱신

            # 키보드 입력 대기
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 🔹 'R' 키를 누르면 게임 재시작
                        self.reset_game()
                        return  # 게임 루프로 돌아가기
                    elif event.key == pygame.K_ESCAPE:  # 🔹 'ESC' 키를 누르면 게임 종료
                        pygame.quit()
                        exit()

    def reset_game(self):
        """ 게임을 초기 상태로 재설정 """
        self.player = Player(400, 550, 5)
        self.enemies = [Enemy(100 * i, 50, 2, 0.5) for i in range(5)]
        self.bullets = []
        self.enemy_bullets = []
        self.explosions = []
        self.barriers = [Barrier(200, 500), Barrier(400, 500), Barrier(600, 500)]
        self.ufo = None
        self.ufo_timer = 0
        self.score = 0
        self.running = True  # 게임 루프 다시 실행 가능하게 설정

    #################################################################################################################
    def render(self):
        """ 화면을 새로 그리는 함수 """
        self.screen.fill(settings.BLACK) # 배경을 검은색으로 채움
        self.player.draw(self.screen) # 플레이어 그림
        for enemy in self.enemies:
            enemy.draw(self.screen) # 적 그림
        for bullet in self.bullets:
            bullet.draw(self.screen) # 총알 그림
        for bullet in self.enemy_bullets: 
            bullet.draw(self.screen) # 적 총알 그림
        for explosion in self.explosions:
            explosion.draw(self.screen) # 폭발 효과 표시
        for barrier in self.barriers:
            barrier.draw(self.screen) # 방어막 그림

        # 🔹 UFO를 화면에 그림
        if self.ufo:
            self.ufo.draw(self.screen)

        # 점수표시
        score_text = self.font.render("Score: %d" % self.score, True, settings.WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()