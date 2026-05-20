import cv2
import pygame
import time
import math
from hand_gestures import HandDetector
from game_mechanics import Game, Bullet, Explosion, TARGET_ESCAPED_EVENT, Target

def main():
    # Initialize modules
    hand_detector = HandDetector()
    game = Game()
    cap = cv2.VideoCapture(0)  # Webcam

    # Timing/Cooldowns
    last_shot_time = 0
    shot_cooldown = 0.5
    last_cluster_time = pygame.time.get_ticks()
    cluster_interval = 5000  # 5 seconds between clusters
    target_respawn_cooldown = 1.5
    cluster_size = 3
    target_spacing = 100

    # Gesture buffer
    gesture_buffer = []
    buffer_size = 3

    while True:
        # Handle events (e.g., closing the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                return
            elif event.type == TARGET_ESCAPED_EVENT:
                game.lives -= 1
                if game.lives <= 0:
                    game.game_over = True

        # Game over screen
        if game.game_over:
            game.screen.fill((0, 0, 0))
            game.draw_game_over()
            pygame.display.flip()

            # Restart on pressing 'R'
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game = Game()
            continue

        # Capture webcam frame
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        # Detect gesture with visual feedback
        gesture, annotated_frame = hand_detector.get_gesture(frame)
        cv2.imshow('Hand Gesture', annotated_frame)

        # Calculate bullet direction
        bullet_angle = 0
        index_x, index_y = 0, 0
        if hand_detector.results and hand_detector.results.multi_hand_landmarks:
            hand_landmarks = hand_detector.results.multi_hand_landmarks[0].landmark
            screen_width = game.screen.get_width()
            screen_height = game.screen.get_height()
            
            index_x = hand_landmarks[8].x * screen_width
            index_y = hand_landmarks[8].y * screen_height
            
            center_x = screen_width // 2
            center_y = screen_height - 20
            rel_x = index_x - center_x
            rel_y = center_y - index_y  # Inverted Y-axis
            
            angle_radians = math.atan2(rel_y, rel_x)
            bullet_angle = math.degrees(angle_radians)

        # Shooting logic (with ammo check)
        gesture_buffer.append(gesture)
        if len(gesture_buffer) > buffer_size:
            gesture_buffer.pop(0)
        
        current_time = time.time()
        if all(g == "fist" for g in gesture_buffer[-buffer_size:]) and game.ammo > 0:
            if current_time - last_shot_time > shot_cooldown:
                bullet = Bullet(
                    x=game.screen.get_width() // 2,
                    y=game.screen.get_height() - 20,
                    angle=bullet_angle
                )
                game.all_bullets.add(bullet)
                game.shoot_sound.play()
                game.ammo -= 1
                last_shot_time = current_time

        # Target cluster spawning logic
        current_ticks = pygame.time.get_ticks()
        time_since_last_hit = current_ticks - game.last_hit_time
        
        if (current_ticks - last_cluster_time > cluster_interval) and \
           (time_since_last_hit > target_respawn_cooldown * 1000):
            # Spawn a cluster of targets
            for i in range(cluster_size):
                offset = (i - cluster_size // 2) * target_spacing
                target = Target(game.screen.get_width(), game.screen.get_height(), offset)
                game.all_targets.add(target)
            last_cluster_time = current_ticks

        # Update game state
        game.all_targets.update()
        game.all_bullets.update()
        game.all_explosions.update()

        # Collision detection
        for bullet in game.all_bullets:
            hits = pygame.sprite.spritecollide(bullet, game.all_targets, True)
            for target in hits:
                explosion = Explosion(target.rect.centerx, target.rect.centery)
                game.all_explosions.add(explosion)
                game.score += 100
                game.explosion_sound.play()
                game.last_hit_time = pygame.time.get_ticks()

        # Game over conditions
        if game.lives <= 0 or (game.ammo <= 0 and len(game.all_bullets) == 0):
            game.game_over = True

        # Draw everything
        game.screen.fill((0, 0, 0))
        game.all_targets.draw(game.screen)
        game.all_bullets.draw(game.screen)
        game.all_explosions.draw(game.screen)
        
        # UI elements
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
        game.screen.blit(score_text, (10, 10))
        game.draw_lives()
        game.draw_ammo()

        # Debug trajectory line
        if hand_detector.results and hand_detector.results.multi_hand_landmarks:
            pygame.draw.line(game.screen, (0, 255, 0), 
                            (game.screen.get_width()//2, game.screen.get_height()-20),
                            (int(index_x), int(index_y)), 2)

        pygame.display.flip()
        game.clock.tick(30)

        if cv2.waitKey(1) == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()