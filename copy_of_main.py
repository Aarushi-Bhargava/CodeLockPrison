#importer libraries
import arcade
import random
import arcade.gui

PLAYER_MOVEMENT_SPEED = 5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shooting Game Scratch Code Version (2)"
SPRITE_SIZE = 64
SPRITE_SCALING = 0.5

#Prison guards
class EnemySprite(arcade.Sprite):
    """ Enemy ship class that tracks how long it has been since firing and moves left and right.
    It fires at random intervals. """

    def __init__(self, image_file, scale, bullet_list, min_time_between_firing, max_time_between_firing, movement_speed,
                 boundary_left, boundary_right):
        """ Set up the enemy """
        super().__init__(image_file, scale)
        self.time_since_last_firing = 0.0
        self.min_time_between_firing = min_time_between_firing
        self.max_time_between_firing = max_time_between_firing
        self.time_between_firing = random.uniform(min_time_between_firing, max_time_between_firing)
        self.bullet_list = bullet_list
        self.movement_speed = movement_speed
        self.boundary_left = boundary_left
        self.boundary_right = boundary_right
        self.movement_direction = 1  # 1 for right, -1 for left

    def on_update(self, delta_time: float = 1 / 60):
        """ Update this sprite. """
        # Update position
        self.center_x += self.movement_speed * self.movement_direction

        # Check if we hit a boundary and need to reverse
        if self.right >= self.boundary_right or self.left <= self.boundary_left:
            self.movement_direction *= -1

        # Track time since we last fired
        self.time_since_last_firing += delta_time

        # If we are past the firing time, then fire
        if self.time_since_last_firing >= self.time_between_firing:
            self.fire_bullet()

    def fire_bullet(self):
        """ Fire a bullet and reset the firing timer to a random interval. """
        self.time_since_last_firing = 0
        self.time_between_firing = random.uniform(self.min_time_between_firing, self.max_time_between_firing)
        #bullet image
        bullet = arcade.Sprite("768px-Eo_circle_red_blank.svg.png", scale=0.04)
        bullet.center_x = self.center_x
        bullet.angle = -90
        bullet.top = self.bottom
        bullet.change_y = -2
        self.bullet_list.append(bullet)

#Setting up the arcade window where video game is displayed

class MyGameView(arcade.View):
    def __init__(self):
        super().__init__()

        # self.background = None
        arcade.set_background_color(arcade.color.BLACK)
        self.button = None
        # self.button_list = None


    def setup(self):
        self.background = arcade.load_texture("home screen.png")
        self.button_list = arcade.SpriteList()
        self.button = arcade.Sprite("play-button-neww.png")
        self.button.center_x = SCREEN_WIDTH / 2
        self.button.center_y = SCREEN_HEIGHT/2
        self.button_list.append(self.button)
    
    
    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.button_list.draw()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x,y), self.button_list)
        if len(buttons) > 0:
            view = CombatView()
            view.setup()
            self.window.show_view(view)

class CombatGameOver(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu = None
        self.menu_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison\combat screen (background).jpg")
        
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison\menu icon.png", scale=1)
        self.menu.center_x = SCREEN_WIDTH / 2
        self.menu.center_y = SCREEN_HEIGHT / 2 + 100
        self.menu_list.append(self.menu)


    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background)
        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        self.menu_list.draw()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x,y), self.menu_list)
        if len(buttons) > 0:
            view = MyGameView()
            view.setup()
            self.window.show_view(view)

class CombatWinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu = None
        self.menu_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison\combat screen (background).jpg")
        
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison\menu icon.png", scale=1)
        self.menu.center_x = SCREEN_WIDTH / 2
        self.menu.center_y = SCREEN_HEIGHT / 2 + 100
        self.menu_list.append(self.menu)


    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background)
        arcade.draw_text("You Win!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        self.menu_list.draw()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x,y), self.menu_list)
        if len(buttons) > 0:
            view = MyGameView()
            view.setup()
            self.window.show_view(view)

class CombatView(arcade.View):
    """ Main application class """

    def __init__(self):
        super().__init__()

        
        arcade.set_background_color(arcade.color.BLACK)

        self.player = None
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.wall_list = None
        self.physics_engine = None
        self.health = None
        self.bullet_num = 0
        self.play_mode = 0
      

    def setup(self):
        """ Setup the variables for the game. """

        self.background = arcade.load_texture("combat screen (background).jpg")

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()

        #Add healthbar
        for i in range(0, 101, 50):
            self.health = arcade.Sprite("heart (single).png", scale=0.5)
            # self.health.center_x = self.health.width
            self.health.center_x = 70
            # self.health.center_y = SCREEN_HEIGHT/2 + i
            self.health.center_y = SCREEN_HEIGHT/2 + i
            
            self.health_list.append(self.health)

        # Add player ship
        self.player = arcade.Sprite("images__2_-removebg-preview.png", scale=0.3)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 50
        self.player_list.append(self.player)

        # Add top-left enemy ship
        enemy = EnemySprite("600px-Piste_Scandinavia_3_red_rectangle.svg.png",
                            scale=0.1,
                            bullet_list=self.bullet_list,
                            min_time_between_firing=0.5,  # Minimum time between shots
                            max_time_between_firing=2.0,  # Maximum time between shots
                            movement_speed=2,
                            boundary_left=0,
                            boundary_right=SCREEN_WIDTH)
        enemy.center_x = SCREEN_WIDTH / 2
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add a crate on the ground (not visible, example placeholder)
        wall = arcade.Sprite("600px-Piste_Scandinavia_3_red_rectangle.svg.png", scale=1)
        wall.position = [-100, -500]
        self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)


    def on_draw(self):
        """Render the screen. """

        self.clear()

        

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.health_list.draw()

        if len(self.health_list) <= 0:
            # self.play_mode = 1
            view = CombatGameOver()
            view.setup()
            self.window.show_view(view)
        elif self.bullet_num > 25:
            view = CombatWinView()
            view.setup()
            self.window.show_view(view)
 
    

    def on_update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """

        self.enemy_list.on_update(delta_time)

        bullet_hit = arcade.check_for_collision_with_list(
            self.player, self.bullet_list
        )      
        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists() 
                self.bullet_num += 1
            if bullet in bullet_hit:
                if len(self.health_list) > 0:
                    self.health_list[0].remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()          
       
        self.bullet_list.update()
        self.player_list.update()

        # Constrain the player to stay within the screen boundaries
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH

        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if self.play_mode == 0:
            if key == arcade.key.LEFT:
                self.player.change_x = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if self.play_mode == 0:
            if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player.change_x = 0


def main():
    """ Run the game """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MyGameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()