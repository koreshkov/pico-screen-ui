"""Pong game screen."""
import time
import random
from machine import Timer
from screen.base import UIScreen


class UIPongScreen(UIScreen):
    """Pong game screen with AI opponent."""
    
    def __init__(self, name, ui):
        super().__init__(name, ui)
        # Game settings
        self.paddle_width = 4
        self.paddle_height = 30
        self.ball_size = 4
        self.paddle_speed = 5
        self.ai_speed = 3
        
        # Game state
        self.reset_game()
        
    def reset_game(self):
        """Reset game state."""
        # Paddle positions (y coordinate)
        self.player_y = (self.ui.height - self.paddle_height) // 2
        self.ai_y = (self.ui.height - self.paddle_height) // 2
        
        # Ball position and velocity
        self.ball_x = self.ui.width // 2
        self.ball_y = self.ui.height // 2
        self.ball_vx = random.choice([-3, 3])
        self.ball_vy = random.choice([-2, -1, 1, 2])
        
        # Scores
        self.player_score = 0
        self.ai_score = 0
        
        # Game state
        self.paused = False
        self.needs_update = True
        
    def init(self):
        """Called when screen becomes active."""
        self.reset_game()
        self.render()
        # Start game loop timer (run at ~60 FPS)
        self.game_timer = Timer(mode=Timer.PERIODIC, period=16, callback=self.game_tick)
    
    def deinit(self):
        """Called when screen becomes inactive."""
        if hasattr(self, 'game_timer'):
            self.game_timer.deinit()
    
    def game_tick(self, tim=None):
        """Timer callback - just sets flag for update."""
        self.needs_update = True
        
    def update(self):
        """Update game state - called by main loop."""
        if not self.needs_update or self.paused:
            return
        
        self.needs_update = False
        
        # Move ball
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        
        # Ball collision with top/bottom
        if self.ball_y <= 0 or self.ball_y >= self.ui.height - self.ball_size:
            self.ball_vy = -self.ball_vy
            self.ball_y = max(0, min(self.ball_y, self.ui.height - self.ball_size))
        
        # Ball collision with player paddle
        if (self.ball_x <= self.paddle_width and 
            self.player_y <= self.ball_y + self.ball_size and 
            self.ball_y <= self.player_y + self.paddle_height):
            self.ball_vx = abs(self.ball_vx)
            # Add some angle based on where it hit the paddle
            hit_pos = (self.ball_y - self.player_y) / self.paddle_height
            self.ball_vy = int((hit_pos - 0.5) * 4)
        
        # Ball collision with AI paddle
        if (self.ball_x >= self.ui.width - self.paddle_width - self.ball_size and 
            self.ai_y <= self.ball_y + self.ball_size and 
            self.ball_y <= self.ai_y + self.paddle_height):
            self.ball_vx = -abs(self.ball_vx)
            # Add some angle based on where it hit the paddle
            hit_pos = (self.ball_y - self.ai_y) / self.paddle_height
            self.ball_vy = int((hit_pos - 0.5) * 4)
        
        # Score points
        if self.ball_x < 0:
            self.ai_score += 1
            self.reset_ball()
        elif self.ball_x > self.ui.width:
            self.player_score += 1
            self.reset_ball()
        
        # AI movement (simple AI that follows the ball)
        ball_center = self.ball_y + self.ball_size // 2
        ai_center = self.ai_y + self.paddle_height // 2
        
        if ball_center < ai_center - 5:
            self.ai_y = max(0, self.ai_y - self.ai_speed)
        elif ball_center > ai_center + 5:
            self.ai_y = min(self.ui.height - self.paddle_height, self.ai_y + self.ai_speed)
        
        self.render()
    
    def reset_ball(self):
        """Reset ball to center with random direction."""
        self.ball_x = self.ui.width // 2
        self.ball_y = self.ui.height // 2
        self.ball_vx = random.choice([-3, 3])
        self.ball_vy = random.choice([-2, -1, 1, 2])
        
    def render(self):
        """Render the game."""
        self.clear()
        
        # Draw center line
        self.display.set_pen(self.palette.primary)
        for y in range(0, self.ui.height, 10):
            self.display.rectangle(self.ui.width // 2 - 1, y, 2, 5)
        
        # Draw paddles
        self.display.set_pen(self.palette.primary)
        self.display.rectangle(0, self.player_y, self.paddle_width, self.paddle_height)
        self.display.rectangle(self.ui.width - self.paddle_width, self.ai_y, 
                              self.paddle_width, self.paddle_height)
        
        # Draw ball
        self.display.rectangle(int(self.ball_x), int(self.ball_y), 
                              self.ball_size, self.ball_size)
        
        # Draw scores
        self.display.text(str(self.player_score), self.ui.width // 2 - 30, 10, scale=2)
        self.display.text(str(self.ai_score), self.ui.width // 2 + 20, 10, scale=2)
        
        # Draw pause indicator
        if self.paused:
            pause_text = "PAUSED"
            text_width = len(pause_text) * 6 * 2
            self.display.text(pause_text, 
                            (self.ui.width - text_width) // 2, 
                            self.ui.height // 2 - 10, scale=2)
        
        self.display.update()
    
    def btn_a_handler(self):
        """Move paddle up."""
        if not self.paused:
            self.player_y = max(0, self.player_y - self.paddle_speed)
    
    def btn_b_handler(self):
        """Move paddle down."""
        if not self.paused:
            self.player_y = min(self.ui.height - self.paddle_height, 
                              self.player_y + self.paddle_speed)
    
    def btn_x_handler(self):
        """Go back to home."""
        self.ui.set_active_screen('HOME')
    
    def btn_y_handler(self):
        """Toggle pause."""
        self.paused = not self.paused
        self.render()
