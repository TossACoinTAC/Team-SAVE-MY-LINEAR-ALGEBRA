import pygame


class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        # 用于缓存不同放大比例下的图像
        self.scaled_images = {}
        self.scale_factor = 1

    def scale(self, new_scale_factor):
        if new_scale_factor == self.scale_factor:
            return
        self.scale_factor = new_scale_factor
        if new_scale_factor in self.scaled_images:
            self.image = self.scaled_images[new_scale_factor]
        else:
            new_width = int(self.original_image.get_width() * new_scale_factor)
            new_height = int(self.original_image.get_height() * new_scale_factor)
            new_image = pygame.transform.scale(self.original_image, (new_width, new_height))
            self.scaled_images[new_scale_factor] = new_image
            self.image = new_image
        # 调整位置，以中心坐标放大
        original_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = original_center


# Get the center of the image
center_x, center_y = self.image.get_rect().center
# Scale the image
scaled_image = pygame.transform.scale(self.image, (new_width, new_height))

# Get the new rect of the scaled image
scaled_rect = scaled_image.get_rect()

# Set the center of the new rect to the original image's center
scaled_rect.center = (center_x, center_y)