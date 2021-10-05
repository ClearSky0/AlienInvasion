import pygame
import time

screen = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Sky")
screen.fill((0, 0, 255))

frog_image = pygame.image.load('try_it/frog.bmp')

screen_rect = screen.get_rect()

        # Load the ship image and get its rect
#        self.image = pygame.image.load('images/ship.bmp')
frog_rect = frog_image.get_rect()

        # Start each new ship at the bottom centre of the screen
frog_rect.midbottom = screen_rect.midbottom

"""Draw the ship at its current location"""
screen.blit(frog_image, frog_rect)
pygame.display.flip()


time.sleep(5)