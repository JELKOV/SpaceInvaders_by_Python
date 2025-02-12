import pygame

class Explosion:
    def __init__(self, x, y, sprite_sheet, frame_width, frame_height, num_frames):
        """
        폭발 애니메이션 초기화
        :param x: 폭발의 x 좌표 (화면에서의 위치)
        :param y: 폭발의 y 좌표
        :param sprite_sheet: 폭발 스프라이트 시트 (이미지 파일)
        :param frame_width: 개별 프레임의 가로 길이 (픽셀 단위)
        :param frame_height: 개별 프레임의 세로 길이 (픽셀 단위)
        :param num_frames: 폭발 애니메이션 프레임 개수
        """
        # 현재 애니메이션 프레임 인덱스( 처음에는 0번 프레임부터 시작)
        self.index = 0

        # 폭발 애니메이션의 위치를 설정(첫번째 프레임 기준)
        self.rect = self.images[0].get_rect(centerx=x, centery=y)

        # 애니메이션이 끝났는지 여부를 확인하는 변수
        self.finished = False

        # 스프라이트 시트에서 개별 프레임을 추출하여 리스트로 저장
        self.images = self.load_frames(sprite_sheet, frame_width, frame_height, num_frames)

    @staticmethod
    def load_frames(sprite_sheet, frame_width, frame_height, num_frames):
        """
        스프라이트 시트에서 개별 프레임을 추출하여 리스트로 저장하는 함수
        :param sprite_sheet: 폭발 애니메이션이 포함된 스프라이트 시트 이미지
        :param frame_width: 개별 프레임의 가로 길이 (픽셀 단위)
        :param frame_height: 개별 프레임의 세로 길이 (픽셀 단위)
        :param num_frames: 총 프레임 개수
        :return: 개별 프레임 리스트
        """
        frames = []

        # 스프라이트 시트에서 개별 프레임을 잘라서 리스트에 추가
        for i in range(num_frames):
            # (i * frame_width, 0) 위치에서 frame_width x frame_height 크기만큼 잘라서 저장
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)

        return frames  # 추출한 프레임 리스트 반환

    def update(self):
        """
        폭발 애니메이션의 다음 프레임으로 변경하는 함수
        - 현재 프레임 인덱스를 증가시켜 다음 프레임을 표시
        - 마지막 프레임까지 진행되면 애니메이션이 종료되었다고 표시
        """
        if self.index < len(self.images) - 1:
            # 다음 프레임으로 변경
            self.index += 1
        else:
            # 마지막 프레임에 도달하면 애니메이션 종료
            self.finished = True

    def draw(self, screen):
        """
        현재 폭발 프레임을 화면에 그리는 함수
        :param screen: 게임 화면 Surface (Pygame에서 제공)
        """
        if not self.finished:
            # 현재 인덱스의 프레임을 화면에 그림
            screen.blit(self.images[self.index], self.rect)