import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = 0
        self.accel_timer = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_SPACE]:
            if self.shot_timer < 0:
                self.shoot()

        if keys[pygame.K_w]:
            self.thrust(dt)
        else:
            if self.accel_timer > 0:
                self.accel_timer -= dt
            else:
                self.accel_timer = 0
        
        self.position += self.velocity * dt

        self.shot_timer -= dt

    def thrust(self, dt):
        if self.accel_timer < PLAYER_SEC_TILL_MAX_ACCEL:
            self.accel_timer += dt
        else:
            self.accel_timer = PLAYER_SEC_TILL_MAX_ACCEL
            
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        percent_to_max_speed = self.accel_timer / PLAYER_SEC_TILL_MAX_ACCEL
        extra_backwards_vel = 0
        if self.velocity != pygame.Vector2(0,0):
            velocity_dot = pygame.Vector2.dot(forward, self.velocity)
            
            if velocity_dot < 0:
                extra_backwards_vel = -velocity_dot

        accel_on_curve = self.ease_out_quint(percent_to_max_speed) * (PLAYER_ACCEL_SPEED_PER_SEC + extra_backwards_vel)
        self.velocity += forward * accel_on_curve * dt

        if self.velocity.magnitude() >= PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED

    def shoot(self):
        temp_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        temp_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN
    
    def ease_out_quint(self, x):
        return 1.0 - (1.0-x)**5.0