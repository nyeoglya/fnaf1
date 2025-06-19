import pygame

class AudioManager:
    # Mixer 초기화 플래그 및 채널 설정
    _initialized = False
    channel_count = 32
    next_channel = 0
    channels = []

    @classmethod
    def init_mixer(cls, channel_count=32):
        """
        pygame 믹서 초기화 (최초 1회 호출)
        """
        if not cls._initialized:
            pygame.mixer.init()
            cls.channel_count = channel_count
            pygame.mixer.set_num_channels(cls.channel_count)
            cls.channels = [pygame.mixer.Channel(i) for i in range(cls.channel_count)]
            cls._initialized = True

    @classmethod
    def get_free_channel(cls):
        """
        사용 가능한 채널 반환, 모두 사용 중이면 라운드로빈
        """
        for ch in cls.channels:
            if not ch.get_busy():
                return ch
        ch = cls.channels[cls.next_channel % cls.channel_count]
        cls.next_channel += 1
        return ch

    def __init__(self, path, repeated=False, volume=1.0):
        """
        :param path: 오디오 파일 경로
        :param repeated: True일 경우 무한 반복
        :param volume: 0.0 ~ 1.0 사이의 초기 볼륨
        """
        AudioManager.init_mixer()
        self.sound = pygame.mixer.Sound(path)
        self.repeated = repeated
        self.volume = max(0.0, min(volume, 1.0))
        # Sound 객체 자체 볼륨 세팅
        self.sound.set_volume(self.volume)
        self._played_channels = []

    def play(self):
        """
        사운드를 설정된 볼륨으로 재생
        """
        '''
        for ch in self._played_channels:
            if ch.get_busy():
                return
        '''

        loops = -1 if self.repeated else 0
        ch = AudioManager.get_free_channel()
        ch.set_volume(self.volume)
        ch.play(self.sound, loops=loops)
        self._played_channels.append(ch)

    def stop(self):
        """
        이 인스턴스로 재생된 모든 채널 정지
        """
        for ch in self._played_channels:
            ch.stop()
        self._played_channels.clear()

    def set_volume(self, volume):
        """
        인스턴스 볼륨 조절 (0.0 ~ 1.0)
        현재 재생 중인 채널에도 즉시 적용
        """
        self.volume = max(0.0, min(volume, 1.0))
        # Sound 객체 볼륨 업데이트
        self.sound.set_volume(self.volume)
        # 이미 재생 중인 채널 볼륨 변경
        for ch in self._played_channels:
            ch.set_volume(self.volume)

    def get_volume(self):
        """
        현재 볼륨 반환
        """
        return self.volume
