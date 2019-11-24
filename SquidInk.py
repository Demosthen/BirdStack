class SquidInk(pygame.sprite.Sprite):
    """docstring for SquidInk."""

    def __init__(self, game, rounds):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image, self.rect = Load.load_image("squidink.png", None, Game.screensize)
        self.initial_round = self.game.turns
        self.rounds = rounds
        self.groups = [game.allsprites]

    def update(self):
        if self.game.turns == self.initial_round + self.rounds:
            self.kill()
