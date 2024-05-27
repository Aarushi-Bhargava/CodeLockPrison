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

level = 1
# newly added
num_internships = "100"
# newly added

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
        bullet = arcade.Sprite("CodeLockPrison/768px-Eo_circle_red_blank.svg.png", scale=0.04)
        bullet.center_x = self.center_x
        bullet.angle = -90
        bullet.top = self.bottom
        bullet.change_y = -2
        self.bullet_list.append(bullet)

#Setting up the arcade window where video game is displayed

class MyGameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)
        self.button = None


    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/final-welcome-screen-green.png")
        self.button_list = arcade.SpriteList()
        self.button = arcade.Sprite("CodeLockPrison/play-button-neww.png")
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
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)

# newly added
class GameOver(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)
        self.button = None
        self.button_list = None

    def setup(self):
        self.button_list = arcade.SpriteList()
        self.button = arcade.Sprite("CodeLockPrison/play-button-neww.png")
        self.button.center_x = SCREEN_WIDTH / 2
        self.button.center_y = SCREEN_HEIGHT / 2
        self.button_list.append(self.button)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT*0.9, arcade.color.WHITE, font_size=50, anchor_x="center")

        self.button_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.button_list)
        if len(buttons) > 0:
            global num_internships
            num_internships = "100"
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)
# newly added

class LevelOneView(arcade.View):
    def __init__(self):
        super().__init__()
        self.computer = None
        self.computer_list = None

        self.guard = None
        self.guard_list = None
        # newly added
        self.internships = None
        self.internships_list = None
        # newly added

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison\level 1 (bare).jpg")

        # newly added
        self.internships_list = arcade.SpriteList()
        self.internships = arcade.Sprite("CodeLockPrison/internship.png", scale=0.05)
        self.internships.center_x = SCREEN_WIDTH * 0.95
        self.internships.center_y = SCREEN_HEIGHT * 0.9
        self.internships_list.append(self.internships)
        # newly added
        
        self.computer_list = arcade.SpriteList()
        self.computer = arcade.Sprite("CodeLockPrison\IMG_3729.PNG", scale=1)
        self.computer.center_x = SCREEN_WIDTH / 2
        self.computer.center_y = SCREEN_HEIGHT / 2 + 100
        self.computer_list.append(self.computer)

        self.guard_list = arcade.SpriteList()
        self.guard = arcade.Sprite("CodeLockPrison\Idle.PNG", scale=0.3)
        self.guard.center_x = SCREEN_WIDTH / 2 + 200
        self.guard.center_y = SCREEN_HEIGHT / 2 + 100
        self.guard_list.append(self.guard)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background)
        # newly added
        # drawing internship count + icon
        self.internships_list.draw()
        arcade.draw_text(num_internships, self.internships.center_x * 0.98, self.internships.center_y * 0.99,
                         arcade.color.BLACK, font_size=15)
        # newly added

        self.computer_list.draw()
        self.guard_list.draw()

        # newly added
        if int(num_internships) <= 0:
            view = GameOver()
            view.setup()
            self.window.show_view(view)
        # newly added

    def on_mouse_press(self, x, y, button, key_modifiers):
        combat = arcade.get_sprites_at_point((x,y), self.guard_list)
        if len(combat) > 0:
            view = CombatView()
            view.setup()
            self.window.show_view(view)
        hacking = arcade.get_sprites_at_point((x,y), self.computer_list)
        if len(hacking) > 0:
            if level == 1:
                view = HackingView1()
                view.setup()
                self.window.show_view(view)
            elif level == 2:
                view = HackingView2()
                view.setup()
                self.window.show_view(view)
            elif level == 3:
                view = HackingView3()
                view.setup()
                self.window.show_view(view)


class HackingView1(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu = None
        self.menu_list = None

        # newly added
        self.internships = None
        self.internships_list = None
        # newly added

        self.user_input = None
        self.User_input_list = None

        self.sqrt = None
        self.sqrt_list = None

        self.check = None
        self.check_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison\IMG_3707.PNG")
        
        # menu button to get back
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison\menu icon.png", scale=1)
        self.menu.center_x = 100
        self.menu.center_y = 50
        self.menu_list.append(self.menu)

        # newly added
        self.internships_list = arcade.SpriteList()
        self.internships = arcade.Sprite("CodeLockPrison/internship.png", scale=0.05)
        self.internships.center_x = SCREEN_WIDTH*0.95
        self.internships.center_y = SCREEN_HEIGHT*0.9
        self.internships_list.append(self.internships)
        # newly added

        self.user_input_list = arcade.SpriteList()
        self.user_input = arcade.Sprite("CodeLockPrison\images__2_-removebg-preview.png", scale=0.5)
        self.user_input.center_x = SCREEN_WIDTH*0.65
        self.user_input.center_y = SCREEN_HEIGHT*0.5
        self.user_input_list.append(self.user_input)

        self.sqrt_list = arcade.SpriteList()
        self.sqrt = arcade.Sprite("CodeLockPrison\images__2_-removebg-preview.png", scale=0.5)
        self.sqrt.center_x = SCREEN_WIDTH*0.8
        self.sqrt.center_y = SCREEN_HEIGHT*0.5
        self.sqrt_list.append(self.sqrt)


    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background)
        arcade.draw_text("Write a program that asks the user for the number of tiles and then prints out the maximum side length. You may assume that the user will only type integers that are less than ten thousand. Once your program has read the user’s input and printed the largest square, your program stops executing", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.85, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)

        self.menu_list.draw()

        # newly added
        # drawing internship count + icon
        self.internships_list.draw()
        arcade.draw_text(num_internships, self.internships.center_x*0.98, self.internships.center_y*0.99, arcade.color.BLACK, font_size=15)
        # newly added

        self.user_input_list.draw()
        self.sqrt_list.draw()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x,y), self.menu_list)
        if len(buttons) > 0:
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)

class HackingView2(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu = None
        self.menu_list = None

        self.user_input = None
        self.User_input_list = None

        self.sqrt = None
        self.sqrt_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison\IMG_3707.PNG")
        
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison\menu icon.png", scale=1)
        self.menu.center_x = 100
        self.menu.center_y = 50
        self.menu_list.append(self.menu)

        self.user_input_list = arcade.SpriteList()
        self.user_input = arcade.Sprite("CodeLockPrison\images__2_-removebg-preview.png", scale=0.5)
        self.user_input.center_x = SCREEN_WIDTH*0.65
        self.user_input.center_y = SCREEN_HEIGHT*0.5
        self.user_input_list.append(self.user_input)

        self.sqrt_list = arcade.SpriteList()
        self.sqrt = arcade.Sprite("CodeLockPrison\images__2_-removebg-preview.png", scale=0.5)
        self.sqrt.center_x = SCREEN_WIDTH*0.8
        self.sqrt.center_y = SCREEN_HEIGHT*0.5
        self.sqrt_list.append(self.sqrt)


    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background)
        arcade.draw_text("Each instruction is a sequence of five digits which represents a direction to turn and the number of steps to take to reach the top-secret safe. ", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.85, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)

        arcade.draw_text("The first two digits represent the direction to turn. If their sum is odd, then the direction to turn is left. If their sum is even and not zero, then the direction to turn is right. If their sum is zero, then the direction to turn is the same as the previous instruction.", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.80, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)
        
        arcade.draw_text("The remaining three digits represent the number of steps to take which will always be at least 100.", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.75, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)

        self.menu_list.draw()
        self.user_input_list.draw()
        self.sqrt_list.draw()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x,y), self.menu_list)
        if len(buttons) > 0:
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)

class HackingView3(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu = None
        self.menu_list = None

        self.user_input = None
        self.User_input_list = None

        self.sqrt = None
        self.sqrt_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison\IMG_3707.PNG")
        
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison\menu icon.png", scale=1)
        self.menu.center_x = 100
        self.menu.center_y = 50
        self.menu_list.append(self.menu)

        self.user_input_list = arcade.SpriteList()
        self.user_input = arcade.Sprite("CodeLockPrison\images__2_-removebg-preview.png", scale=0.5)
        self.user_input.center_x = SCREEN_WIDTH*0.65
        self.user_input.center_y = SCREEN_HEIGHT*0.5
        self.user_input_list.append(self.user_input)

        self.sqrt_list = arcade.SpriteList()
        self.sqrt = arcade.Sprite("CodeLockPrison\images__2_-removebg-preview.png", scale=0.5)
        self.sqrt.center_x = SCREEN_WIDTH*0.8
        self.sqrt.center_y = SCREEN_HEIGHT*0.5
        self.sqrt_list.append(self.sqrt)


    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background)
        arcade.draw_text("A password is encoded in a special encryption. The original letters of the password are shifted forward in the alphabet by a value of S = p^2, where p is the position of the letter.", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.85, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)
        arcade.draw_text("Example: ‘CODEZ’ → DSMUY", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.85, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)
        arcade.draw_text("The letter ‘C’ is in the first position, so p = 1. This means S = 1^2 = 1. Shifting ‘C’ forward by 1 gives you ‘D’, because ‘D’ is the letter one position after ‘C’ in the alphabet", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.85, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)
        arcade.draw_text("If you end up shifting positions beyond ‘Z’, continue shifting positions starting from ‘A’, as if ‘A’ was the letter that followed ‘Z’", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.85, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)
        arcade.draw_text("You must create a program that can decode all the passwords", 
                         SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.85, arcade.color.BLACK, font_size=15, multiline=True, width=SCREEN_WIDTH*0.75)

        self.menu_list.draw()
        self.user_input_list.draw()
        self.sqrt_list.draw()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x,y), self.menu_list)
        if len(buttons) > 0:
            view = LevelOneView()
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
            view = LevelOneView()
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
            view = LevelOneView()
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

        self.background = arcade.load_texture("CodeLockPrison\combat screen (background).jpg")

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()

        #Add healthbar
        for i in range(0, 101, 50):
            self.health = arcade.Sprite("CodeLockPrison/768px-Eo_circle_red_blank.svg.png", scale=0.04)
            self.health.center_x = self.health.width
            self.health.center_y = SCREEN_HEIGHT/2 + i
            
            self.health_list.append(self.health)

        # Add player ship
        self.player = arcade.Sprite("CodeLockPrison/images__2_-removebg-preview.png", scale=0.3)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 50
        self.player_list.append(self.player)

        # Add top-left enemy ship
        enemy = EnemySprite("CodeLockPrison/600px-Piste_Scandinavia_3_red_rectangle.svg.png",
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
        wall = arcade.Sprite("CodeLockPrison/600px-Piste_Scandinavia_3_red_rectangle.svg.png", scale=1)
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

        # newly added
        # if user loses combat game
        if len(self.health_list) <= 0:
            # lose 50 internships
            global num_internships
            num_internships = str(int(num_internships)-50)

            # change view to game over screen
            view = CombatGameOver()
            view.setup()
            self.window.show_view(view)

        # if user wins combat game
        elif self.bullet_num > 25:
            # gain 100 internships
            num_internships = str(int(num_internships) + 100)

            # change view to win screen
            view = CombatWinView()
            view.setup()
            self.window.show_view(view)

        # newly added
    

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