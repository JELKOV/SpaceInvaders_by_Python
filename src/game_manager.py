import pygame
import settings
import random
import pygame.mixer
from player import Player
from enemy import Enemy
from bullet import Bullet
from src.barrier import Barrier
from src.explosion import Explosion
from src.ufo import UFO


class GameManager:
    def __init__(self, screen):
        """ 게임 매니저 초기화 """
        self.screen = screen
        self.player = Player(400, 550, 5)
        self.enemies = [Enemy(100 * i, 50, 2,0.5) for i in range(5)]
        self.bullets = []
        self.enemy_bullets = []
        self.explosions = []  # 폭발 효과 관리 리스트
        self.explosion_sprite = pygame.image.load("../assets/images/explode.png")  # 스프라이트 시트 로드
        self.barriers = [Barrier(200, 500), Barrier(400, 500), Barrier(600, 500)]  # 방어막 3개 생성
        self.running = True
        self.ufo = None  # 현재 활성화된 UFO
        self.ufo_count = 0
        self.ufo_timer = 0  # UFO 등장 간격을 관리하는 타이머
        self.wave = 1 # 초기웨이브 설정
        self.score = 0
        self.high_score = self.load_high_score()
        self.new_record_displayed = False
        self.font = pygame.font.Font('freesansbold.ttf', 36)
        self.spawn_enemies()

        #사운드 초기화
        pygame.mixer.init()
        pygame.mixer.music.load(settings.SOUND_BACKGROUND)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.sound_bullet = pygame.mixer.Sound(settings.SOUND_BULLET)
        self.sound_explosion = pygame.mixer.Sound(settings.SOUND_EXPLOSION)
        self.sound_ufo = pygame.mixer.Sound(settings.SOUND_UFO)
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
                    self.sound_bullet.play()

        # 키 상태 확인 (누르고 있는 동안 계속 이동)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()

    #################################################################################################################

    #################################################################################################################
    def update(self):
        """ 게임 상태 업데이트 """
        self.update_enemies()
        self.update_bullets()
        self.update_explosions()
        self.update_barriers()
        self.update_ufo()
        self.check_wave_progression()
        self.check_new_record()

    def update_enemies(self):
        """ 적 이동 및 미사일 발사 """
        self.enemy_bullets.clear()  # 기존 리스트 초기화
        for enemy in self.enemies:
            enemy.speed_x = 2 + (self.score // 50)  # 난이도 조절
            enemy.move()
            enemy.shoot(self.wave)
            enemy.update_bullets()

            # 적이 발사한 미사일을 GameManager의 enemy_bullets 리스트에 추가
            self.enemy_bullets.extend(enemy.bullets)

    def update_bullets(self):
        """ 플레이어 및 적 미사일 이동 & 충돌 처리 """

        # 플레이어 미사일 이동 & 적과 충돌 확인
        for bullet in self.bullets[:]:
            bullet.move()
            self.check_bullet_collision(bullet)

        """적 미사일을 업데이트하고 충돌을 체크"""
        for bullet in self.enemy_bullets[:]:  # 적 미사일 리스트 복사본을 사용하여 안전하게 순회
            bullet.move()  # 미사일 이동

            # 충돌 감지 및 삭제 처리
            if self.check_enemy_bullet_collision(bullet):  # 충돌 후 삭제된 경우, 다음 미사일로 넘어감
                continue

            # 화면 밖으로 나간 미사일 삭제
            if bullet.rect.top > settings.SCREEN_HEIGHT:
                bullet.destroy(self.enemy_bullets)

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
                self.sound_explosion.play()
                break

    def check_enemy_bullet_collision(self, bullet):
        """ 적 미사일이 방어막이나 플레이어와 충돌했는지 확인하고 처리 """

        # 방어막과 충돌 감지
        for barrier in self.barriers[:]:
            if bullet.rect.colliderect(barrier.rect):
                print(f"💥 적 미사일이 방어막과 충돌! 위치: {barrier.rect.x}, {barrier.rect.y}")

                # 방어막 체력 감소
                if barrier.take_damage():
                    self.barriers.remove(barrier)  # 체력이 0이면 방어막 제거

                # 미사일 즉시 삭제
                bullet.destroy(self.enemy_bullets)
                return True  #  충돌 후 삭제되었음을 알림

        # 플레이어와 충돌 감지
        if bullet.rect.colliderect(self.player.rect):
            print("🚀 플레이어 피격! 게임 오버 처리")

            # 폭발 효과 추가
            self.explosions.append(
                Explosion(self.player.rect.centerx, self.player.rect.centery, self.explosion_sprite, 64, 64, 14)
            )
            self.player.hit()

            # 미사일 즉시 삭제
            bullet.destroy(self.enemy_bullets)
            return True  #  충돌 후 삭제되었음을 알림

        return False  #  충돌하지 않은 경우

    def update_explosions(self):
        """ 폭발 애니메이션 업데이트 """
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.finished:
                self.explosions.remove(explosion)

                # 플레이어가 맞았던 경우, 폭발이 끝나면 게임 오버 실행
                if not self.player.alive:
                    self.game_over()

    def update_barriers(self):
        """ 방어막이 총알과 충돌할 경우 체력 감소 """
        for bullet in self.bullets[:]:
            for barrier in self.barriers[:]:
                if bullet.rect.colliderect(barrier.rect):
                    # 체력이 0이면 제거
                    if barrier.take_damage():
                        self.barriers.remove(barrier)
                    self.bullets.remove(bullet)
                    break

    def update_ufo(self):
        """ UFO 생성, 이동 및 충돌 처리 """

        # UFO 등장 가능 횟수 체크 (한 스테이지당 최대 3회)
        if self.ufo_count < 3:
            self.ufo_timer += 1
            if self.ufo is None and self.ufo_timer > 900:  # 약 15초(60FPS 기준)
                if random.randint(1, 3) == 1:  # 3번 중 1번 확률로 등장
                    self.ufo = UFO(settings.SCREEN_WIDTH, speed=2, points=100)
                    self.ufo_count += 1  # UFO 출현 횟수 증가
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
                    self.ufo_hit_effect(self.ufo.points)
                    self.ufo = None  # UFO 제거
                    self.bullets.remove(bullet)
                    self.sound_ufo.play()
                    break

    def ufo_hit_effect(self, score):
        """ UFO 격추 시 화면 반짝임 + 점수 표시 """
        for i in range(2):  # 두 번 깜빡이기
            self.screen.fill((255, 0, 0))  # 빨간색 화면
            pygame.display.flip()
            pygame.time.delay(100)
            self.screen.fill(settings.BLACK)
            pygame.display.flip()
            pygame.time.delay(100)

        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render(f"+{score} POINTS!", True, (255, 255, 0))
        text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))

        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  # 1초간 유지

    #################################################################################################################
    """
    스테이지 업그레이드 웨이브 초기화 함수들
    """
    #################################################################################################################
    # 스테이지 업그레이드

    def spawn_barriers(self):
        """ 방어막을 새롭게 배치 (스테이지 시작 시 리셋) """
        self.barriers = [Barrier(200, 500), Barrier(400, 500), Barrier(600, 500)]  # 방어막 3개 생성

    def spawn_enemies(self):
        """ 새로운 웨이브에서 적을 생성 (웨이브가 증가할수록 더 많은 적 등장) """

        enemy_count_per_row = 5 + (self.wave // 3)  # 기본 5마리 + 3스테이지마다 1마리 추가
        enemy_speed = min(2 + self.wave * 0.2, 3)  # 속도 증가 완화 (최대 3)

        # 🔹 스테이지에 따라 적 줄 수 증가 (최대 4줄)
        if self.wave >= 9:
            rows = 4
        elif self.wave >= 6:
            rows = 3
        elif self.wave >= 3:
            rows = 2
        else:
            rows = 1

        self.enemies = []
        for row in range(rows):
            for i in range(enemy_count_per_row):
                x_position = 50 + (i * 100)  # 적 간격 조정
                y_position = 50 + (row * 60)  # 줄마다 Y축 위치 조정
                self.enemies.append(Enemy(x_position, y_position, enemy_speed, 0.5))

        self.barriers = [Barrier(200, 500), Barrier(400, 500), Barrier(600, 500)]  # 방어막 3개 생성
        self.ufo_count = 0

        print(f"🌟 웨이브 {self.wave} 시작! 적 {len(self.enemies)}마리 등장, 속도 {enemy_speed}, 줄 수 {rows}")

    def check_wave_progression(self):
        """ 모든적이 제거되면  새로운 웨이브 시작"""
        if not self.enemies: # 모든적이 제거되었을 때
            # 웨이브 증가
            self.wave+=1
            # 스테이지 전환 효과 추가
            self.stage_transition_effect()
            # 새로운 적 스폰
            self.spawn_enemies()
            # 스테이지 변경 시 방어막 다시 배치
            self.spawn_barriers()

    #################################################################################################################
    '''
    최고 기록 관련 함수
    '''
    #################################################################################################################
    @staticmethod
    def load_high_score():
        """ 기존 최고 점수를 불러옴 (파일 저장 방식) """
        try:
            with open("../data/highscore.txt", "r") as file:
                data = file.read().strip()
                return int(data) if data.isdigit() else 0
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        """ 최고 점수 저장 (비어있을 경우 기본값 0 설정) """
        with open("../data/highscore.txt", "w") as file:
            file.write(str(self.high_score or 0))  #  None 또는 빈 값 방지

    def check_new_record(self):
        """ 신기록 여부 확인 및 시각적 효과 제공 """
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

            # 신기록을 한 번만 표시하도록 설정
            if not self.new_record_displayed:
                self.new_record_displayed = True  # 신기록 표시 플래그 활성화

                font = pygame.font.Font('freesansbold.ttf', 50)
                text = font.render("NEW RECORD!", True, (255, 215, 0))
                text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))

                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(1500)  # 1.5초간 표시

    #################################################################################################################
    '''
    화면 효과 관련 및 초기화
    '''
    #################################################################################################################

    def stage_transition_effect(self):
        """ 스테이지 변경 시 화면 깜빡임 + 메시지 출력 """
        for i in range(3):  # 3번 깜빡이기
            self.screen.fill((255, 255, 255))  # 흰색 화면
            pygame.display.flip()
            pygame.time.delay(150)
            self.screen.fill(settings.BLACK)  # 다시 검은색으로 복귀
            pygame.display.flip()
            pygame.time.delay(150)

        font = pygame.font.Font('freesansbold.ttf', 60)
        text = font.render(f"STAGE {self.wave}", True, (255, 255, 0))
        text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))

        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # 2초간 표시


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
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_text, restart_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # 정상 종료 코드
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # R 키로 게임 재시작
                        self.reset_game()
                        return  # 게임 루프로 돌아가기
                    elif event.key == pygame.K_ESCAPE:  # ESC 키로 종료
                        pygame.quit()
                        exit()  # 정상 종료 코드

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
        self.wave = 1  # 스테이지 초기화
        self.running = True  # 게임 루프 다시 실행 가능하게 설정
        self.new_record_displayed = False

    #################################################################################################################

    """
    랜더링 관련
    """
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

        # UFO를 화면에 그림
        if self.ufo:
            self.ufo.draw(self.screen)

        # 점수표시
        score_text = self.font.render("Score: %d" % self.score, True, settings.WHITE)
        self.screen.blit(score_text, (10, 10))

        # 최고 점수 표시
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, settings.YELLOW)
        self.screen.blit(high_score_text, (10, 50))

        pygame.display.flip()