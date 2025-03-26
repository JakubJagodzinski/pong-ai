import pygame

FPS = 60

BOARD_WIDTH = 800
BOARD_HEIGHT = 400


class PongGame:

    def __init__(self, player1, player2):
        pygame.init()
        from board import Board
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        self.fps_clock = pygame.time.Clock()

        from ball import Ball
        self.ball = Ball(BOARD_WIDTH // 2, BOARD_HEIGHT // 2)

        from racket import Racket
        self.opponent_paddle = Racket(x=BOARD_WIDTH // 2, y=0)
        self.opponent = player1(self.opponent_paddle, self.ball, self.board)

        self.player_paddle = Racket(x=BOARD_WIDTH // 2, y=BOARD_HEIGHT - 20)
        self.player = player2(self.player_paddle, self.ball, self.board)

    def run(self) -> None:
        while not self.handle_events():
            self.ball.move(self.board, self.player_paddle, self.opponent_paddle)
            self.board.draw(self.ball, self.player_paddle, self.opponent_paddle, )
            self.opponent.act(
                self.opponent.racket.rect.centerx - self.ball.rect.centerx,
                self.opponent.racket.rect.centery - self.ball.rect.centery,
            )
            self.player.act(
                self.player.racket.rect.centerx - self.ball.rect.centerx,
                self.player.racket.rect.centery - self.ball.rect.centery,
            )
            self.fps_clock.tick(FPS)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return True
        keys = pygame.key.get_pressed()
        if keys[pygame.constants.K_LEFT]:
            self.player.move_manual(0)
        elif keys[pygame.constants.K_RIGHT]:
            self.player.move_manual(self.board.surface.get_width())
        return False
