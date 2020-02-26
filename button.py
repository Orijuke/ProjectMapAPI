from os import path

import pygame


def load_image(name):
    image = pygame.image.load(name)
    return image


class Mode_Button(pygame.sprite.Sprite):
    mode_btn_img = load_image("mode.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Mode_Button.mode_btn_img
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 20

        self.i = 0

    def get_click(self, pos):
        if self.rect.collidepoint(pos):
            self.i += 1

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.get_click(event.pos)
            return True

    def get_mode(self):
        return self.i