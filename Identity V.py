import pygame as pg
import random

# Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH = 1280  # Pixels
HEIGHT = 720
SCREEN_SIZE = (WIDTH, HEIGHT)
NUM_ENEMIES = 10
NUM_CIPHER = 5

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load("./enemy.png")

        self.image = pg.transform.scale(self.image, (self.image.get_width() // 5, self.image.get_height() // 5))

        self.rect = self.image.get_rect()   
        self.rect.x = WIDTH
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

    def update(self):
        """Make the enermy go from right to left"""
        self.rect.x -= random.randrange(1, 4)
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

class CipherMachine(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load("./Cipher.png")

        self.image = pg.transform.scale(self.image, (self.image.get_width() // 5, self.image.get_height() // 5))

        self.rect = self.image.get_rect()   
        self.rect.x = WIDTH
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

    def update(self):
        """Make the Cipher Machiens go from right to left"""
        self.rect.x -= random.randrange(1, 4)
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

class Player(pg.sprite.Sprite):
 
    def __init__(self):
        super().__init__()

        self.image = pg.image.load("./player.png")
        self.image = pg.transform.scale(self.image, (self.image.get_width() // 10, self.image.get_height() // 10))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height
        self.lives = 25

 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        self.rect.x += self.change_x

 
        # Move up/down
        self.rect.y += self.change_y
 
        # Keep the player on the ground
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.rect.bottom <= HEIGHT:
            self.change_y += .35
        else:
            self.change_y = 0

    def jump(self):
        """ Called when user hits 'jump' button. """
        if self.rect.bottom >= HEIGHT / 3:
            self.change_y = -10

    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

def display_message(screen, message):
    """Function to display a message on the screen"""
    font = pg.font.SysFont("Futura", 48)
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)

def start():
    """ Main Program """
    pg.init()

    game_over = False  

    score = 0
    
    font = pg.font.SysFont("Futura", 24)

    # Set the height and width of the screen
    size = [WIDTH, HEIGHT]
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Identity V")

    all_sprites = pg.sprite.Group()
    enemies = pg.sprite.Group()

    # Create the player
    player = Player()
    all_sprites.add(player)

    # Create enemies
    for _ in range(NUM_ENEMIES):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Create cipher machines
    ciphers = pg.sprite.Group()
    for _ in range (NUM_CIPHER):
        cipher = CipherMachine()
        all_sprites.add(cipher)
        ciphers.add(cipher)
    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pg.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.go_left()
                if event.key == pg.K_RIGHT:
                    player.go_right()
                if event.key == pg.K_UP:
                    player.jump()
                if game_over and event.key == pg.K_r:
                    start()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pg.K_RIGHT and player.change_x > 0:
                    player.stop()
        if not game_over:
            all_sprites.update()

        # Check for collision between the cipher machines and the player
        ciphers_collided = pg.sprite.spritecollide(player, ciphers, True)
        for cipher in ciphers_collided:
           score += 1
        print(f"Score: {score}")

        # Check for collisions between player and enemies
        enemies_collided = pg.sprite.spritecollide(player, enemies, False)
        # If Player is collided with an enemy, player's lives -1
        
        if player.lives > 0:
            for enemy in enemies_collided:
                player.lives -= 1
                print(int(player.lives))
            
                
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0


        screen.fill(WHITE)
        all_sprites.draw(screen)
        if player.lives <= 0:
            game_over = True
            display_message(screen, "You lose! Press \"R\" to restart.")

        if score >= 5:  # Added this block
            game_over = True
            display_message(screen, "You win! Press \"R\" to restart.")
        # Create a surface for the score
        score_image = font.render(f"Score: {score}", True, BLACK)

        player.lives_image = font.render(f"Player Lives: {player.lives}", True, BLACK)
        # "Blit" the surface on the screen
        screen.blit(score_image, (5, 5))
        screen.blit(player.lives_image, (5, 50))


        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pg.display.flip()


    pg.quit()

if __name__ == "__main__":
    start()