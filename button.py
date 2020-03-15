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


class Clear_Button(pygame.sprite.Sprite):
    clear_btn_img = load_image("clear.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Clear_Button.clear_btn_img
        self.rect = self.image.get_rect()
        self.rect.x = 420
        self.rect.y = 20
        self.i = False

    def get_click(self, pos):
        if self.rect.collidepoint(pos):
            self.i = True

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.get_click(event.pos)
            return True

    def get_mode(self):
        return self.i


class Index_Button(pygame.sprite.Sprite):
    on_index_btn_img = load_image("index_on.png")
    ffo_index_btn_img = load_image("index_off.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Index_Button.ffo_index_btn_img
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 60
        self.i = False

    def get_click(self, pos):
        if self.rect.collidepoint(pos):
            self.i = not self.i
            if self.i:
                self.image = Index_Button.on_index_btn_img
            else:
                self.image = Index_Button.ffo_index_btn_img

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.get_click(event.pos)
            return True

    def get_mode(self):
        return self.i
