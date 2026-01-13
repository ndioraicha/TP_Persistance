import pygame
import random
import sys

pygame.init()

# --- Constantes ---
WIDTH, HEIGHT = 500, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter d'oiseaux")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --- Joueur ---
player_width = 60
player_height = 20
player_x = WIDTH // 2
player_y = HEIGHT - 40
player_speed = 5

# --- Balle ---
bullets = []
bullet_speed = 7

# --- Oiseaux ---
bird_width = 40
bird_height = 30
birds = []
bird_speed = 2

for _ in range(5):
    x = random.randint(0, WIDTH - bird_width)
    y = random.randint(-500, -40)
    birds.append([x, y])

score = 0

# --- Fonction pour afficher le texte ---
def draw_text(text, x, y):
    surface = font.render(text, True, BLACK)
    screen.blit(surface, (x, y))

# --- Main loop ---
while True:
    screen.fill(WHITE)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    # Mouvement du joueur
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Tir
    if keys[pygame.K_SPACE]:
        if len(bullets) == 0 or bullets[-1][1] < player_y - 40:
            bullets.append([player_x + player_width//2, player_y])

    # Mise à jour des balles
    for bullet in bullets:
        bullet[1] -= bullet_speed

    # Supprimer les balles sorties
    bullets = [b for b in bullets if b[1] > 0]

    # Mise à jour des oiseaux
    for bird in birds:
        bird[1] += bird_speed

        # Si l'oiseau atteint le sol → Game Over
        if bird[1] > HEIGHT:
            print("GAME OVER - Score :", score)
            pygame.quit()
            sys.exit()

    # Collision balle-oiseau
    for bird in birds:
        for bullet in bullets:
            if (bird[0] < bullet[0] < bird[0] + bird_width) and (bird[1] < bullet[1] < bird[1] + bird_height):
                score += 1
                bird[0] = random.randint(0, WIDTH - bird_width)
                bird[1] = random.randint(-500, -40)
                bullets.remove(bullet)
                break

    # --- Dessins ---
    # Joueur
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

    # Balles
    for bullet in bullets:
        pygame.draw.circle(screen, RED, (bullet[0], bullet[1]), 5)

    # Oiseaux
    for bird in birds:
        pygame.draw.rect(screen, (0, 200, 50), (bird[0], bird[1], bird_width, bird_height))

    # Score
    draw_text(f"Score : {score}", 10, 10)

    pygame.display.flip()
    clock.tick(60)
