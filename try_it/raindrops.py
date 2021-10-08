import pygame
from pygame.sprite import Sprite
import time
from random import randint
from rich import print

class Image(Sprite):
    """A class to represent a Sprite"""

    def __init__(self, screen):
        """Initialise the image and set its starting position"""
        super().__init__()
        self.screen = screen

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('try_it/raindrop.png')
        # self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

        # Start each new alien new the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)


screen_width = 800
screen_height = 800
pygame.display.set_caption("Rain")
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((200, 200, 200))
screen_rect = screen.get_rect()

image = Image(screen)
image.rect.topleft = image.rect.bottomright
image_width, image_height = image.rect.size
images = pygame.sprite.Group()


# Now create the group of images
number_images_x = (screen_width) // (2 * image_width)
number_images_y = (screen_height) // (2 * image_height) + 1

for row_number in range(number_images_y):
    for column_number in range(number_images_x):
        # without this here we just keep adding the same image to the group
        image = Image(screen) 
        # and there is only ever one image in the group

        image_x = image_width + 2 * image_width * column_number
        image_y = image_height + 2 * image_height * row_number

        rand_x = randint(-image_width // 2, +image_width // 2)
        rand_y = randint(-image_height // 2, +image_height // 2)

        image.rect.x = image_x + rand_x
        image.rect.y = image_y + rand_y
        images.add(image)
        # print(row_number, column_number , image_x, image_y, image, images)

images.draw(screen)

pygame.display.flip()

def update_images(self):
    for image in self:
        image.rect.y += 10
        if image.rect.y > screen_height:
            image.rect.y = -image_height

# now start animating them
loop = 0
while loop < 500:
    loop += 1
    screen.fill((200, 200, 200))
    update_images(images)
    images.draw(screen)
    pygame.display.flip()
    time.sleep(0.03)

time.sleep(1)