# importer libraries
import arcade
import random
import arcade.gui

PLAYER_MOVEMENT_SPEED = 5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shooting Game Scratch Code Version (2)"
SPRITE_SIZE = 64
SPRITE_SCALING = 0.5

num_internships = "100"
level = 1


# Prison guards
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
        # bullet image
        bullet = arcade.Sprite("CodeLockPrison/slippers.png", scale=0.1)
        bullet.center_x = self.center_x
        bullet.angle = -90
        bullet.top = self.bottom
        bullet.change_y = -2
        self.bullet_list.append(bullet)


# Setting up the arcade window where video game is displayed

class MyGameView(arcade.View):
    def __init__(self):
        super().__init__()

        # self.background = None
        arcade.set_background_color(arcade.color.BLACK)
        self.button = None
        # self.button_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/!!.png")
        self.button_list = arcade.SpriteList()
        self.button = arcade.Sprite("CodeLockPrison/play-button-neww.png")
        self.button.center_x = SCREEN_WIDTH / 2
        self.button.center_y = SCREEN_HEIGHT / 2
        self.button_list.append(self.button)

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.button_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.button_list)
        if len(buttons) > 0:
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)


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

        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.9, arcade.color.WHITE, font_size=50,
                         anchor_x="center")

        self.button_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.button_list)
        if len(buttons) > 0:
            global num_internships
            num_internships = "100"
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)


class LevelOneView(arcade.View):
    def __init__(self):
        super().__init__()

        # button to go to hacking view
        self.computer_list = None

        # button to go to combat view
        self.guard_list = None

        # internships tracker
        self.internships_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/level 1 (bare).jpg")

        # setting up internships count
        self.internships_list = arcade.SpriteList()
        self.internships = arcade.Sprite("CodeLockPrison/internship.png", scale=0.05)
        self.internships.center_x = SCREEN_WIDTH * 0.95
        self.internships.center_y = SCREEN_HEIGHT * 0.9
        self.internships_list.append(self.internships)

        # computer with word hack on it
        self.computer_list = arcade.SpriteList()
        self.computer = arcade.Sprite("CodeLockPrison/IMG_3729.PNG", scale=0.5)
        self.computer.center_x = SCREEN_WIDTH / 2 - 250
        self.computer.center_y = SCREEN_HEIGHT / 2 + 50
        self.computer_list.append(self.computer)

        # guard icon
        self.guard_list = arcade.SpriteList()
        self.guard = arcade.Sprite("CodeLockPrison/Idle.PNG", scale=0.1)
        self.guard.center_x = SCREEN_WIDTH / 2 + 300
        self.guard.center_y = SCREEN_HEIGHT / 2 + 100
        self.guard_list.append(self.guard)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # drawing internship count + icon
        self.internships_list.draw()
        arcade.draw_text(num_internships, self.internships.center_x * 0.98, self.internships.center_y * 0.99,
                         arcade.color.BLACK, font_size=15)

        # drawing other graphics
        self.computer_list.draw()
        self.guard_list.draw()

        # turn to game over screen if less than 0 internships
        if int(num_internships) <= 0:
            view = GameOver()
            view.setup()
            self.window.show_view(view)

    def on_mouse_press(self, x, y, button, key_modifiers):
        combat = arcade.get_sprites_at_point((x, y), self.guard_list)
        if len(combat) > 0:
            view = CombatView()
            view.setup()
            self.window.show_view(view)
        hacking = arcade.get_sprites_at_point((x, y), self.computer_list)
        if len(hacking) > 0:
            if level == 1:
                view = HackingView1()
                view.setup()
                self.window.show_view(view)
            elif level == 2:
                view = HackingView2()
                view.setup()
                self.window.show_view(view)


class HackWinView(arcade.View):
    def __init__(self):
        super().__init__()

        # menu button (returns to homepage)
        self.menu_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/!!.png")

        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.5)
        self.menu.center_x = SCREEN_WIDTH / 2
        self.menu.center_y = SCREEN_HEIGHT / 2 + 100
        self.menu_list.append(self.menu)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Successful Hacking!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150, arcade.color.WHITE,
                         font_size=50, anchor_x="center")
        self.menu_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(buttons) > 0:
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)


class HackLoseView(arcade.View):
    def __init__(self):
        super().__init__()
        # menu button
        self.menu_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/!!.png")

        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.5)
        self.menu.center_x = SCREEN_WIDTH / 2
        self.menu.center_y = SCREEN_HEIGHT / 2 + 100
        self.menu_list.append(self.menu)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Unsuccessful Hacking :/ ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150, arcade.color.WHITE,
                         font_size=50, anchor_x="center")
        self.menu_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(buttons) > 0:
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)


class HackingView1(arcade.View):
    def __init__(self):
        super().__init__()

        # button to return to homepage
        self.menu_list = None

        # internships tracker
        self.internships_list = None

        # submitting code button
        self.submit_button_list = None

        # code blocks
        self.blocks = []
        self.block_texts = [
            "num_tiles = int(input())",  # User Input
            "max_side_length = math.sqrt(num_tiles)",  # Square Root Function
            "max_side_length = math.floor(max_side_length)",  # Round Down Function
            "print(max_side_length)"  # Output
        ]

        # checking order of code blocks
        self.correct_order = [0, 1, 2, 3]
        self.current_order = []

        # displaying the written code
        self.code_display = ""

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/IMG_3707.PNG")

        # button to return to homepage
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=1)
        self.menu.center_x = 100
        self.menu.center_y = 50
        self.menu_list.append(self.menu)

        # setting up internships count
        self.internships_list = arcade.SpriteList()
        self.internships = arcade.Sprite("CodeLockPrison/internship.png", scale=0.05)
        self.internships.center_x = SCREEN_WIDTH * 0.95
        self.internships.center_y = SCREEN_HEIGHT * 0.9
        self.internships_list.append(self.internships)

        # submit code button
        self.submit_list = arcade.SpriteList()
        self.submit = arcade.Sprite("CodeLockPrison/submit.PNG", scale=0.04)
        self.submit.center_x = SCREEN_WIDTH * 0.48
        self.submit.center_y = SCREEN_HEIGHT * 0.21
        self.submit_list.append(self.submit)

        # code blocks
        self.blocks = arcade.SpriteList()
        for i, text in enumerate(self.block_texts):
            block = arcade.Sprite("CodeLockPrison/images__2_-removebg-preview.png", scale=0.5)
            block.width = 300  # Set your desired width
            block.height = 100  # Set your desired height
            block.center_x = SCREEN_WIDTH * 0.3 + (i % 2) * 350
            block.center_y = SCREEN_HEIGHT * 0.6 - (i // 2) * 150
            block.index = i
            block.text = text
            self.blocks.append(block)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # drawing internship count + icon
        self.internships_list.draw()
        arcade.draw_text(num_internships, self.internships.center_x * 0.98, self.internships.center_y * 0.99,
                         arcade.color.BLACK, font_size=15)

        # drawing programming question
        question_text = "Write a program that asks the user for the number of tiles and then prints out the maximum side length. You may assume that the user will only type integers that are less than ten thousand. Once your program has read the user’s input and printed the largest square, your program stops executing."
        arcade.draw_text(question_text, SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.85, arcade.color.BLACK, font_size=15,
                         multiline=True, width=SCREEN_WIDTH * 0.75)

        # drawing home button
        self.menu_list.draw()

        # drawing submit button
        self.submit_list.draw()

        # drawing code blocks
        self.blocks.draw()

        # drawing text onto code blocks
        for block in self.blocks:
            arcade.draw_text(block.text, block.center_x, block.center_y, arcade.color.WHITE, font_size=10,
                             anchor_x="center", anchor_y="center")

        # drawing actual code
        arcade.draw_text(self.code_display, SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.4, arcade.color.BLACK, font_size=15,
                         multiline=True, width=SCREEN_WIDTH * 0.75)

    def on_mouse_press(self, x, y, button, key_modifiers):

        # if user clicks on menu button
        menu_buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
        if menu_buttons:
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)

        # if user clicks on code blocks
        clicked_blocks = arcade.get_sprites_at_point((x, y), self.blocks)
        if clicked_blocks:
            clicked_block = clicked_blocks[0]
            if clicked_block.index not in self.current_order:
                # each block costs 20 internships
                global num_internships
                num_internships = str(int(num_internships) - 20)

                # appending clicked code block to user's order
                self.current_order.append(clicked_block.index)

                # displaying the code of the clock clicked
                self.code_display += clicked_block.text + "\n"

        # checking answers
        submit_option = arcade.get_sprites_at_point((x, y), self.submit_list)
        if submit_option:
            if self.current_order == self.correct_order:
                view = HackWinView()
                view.setup()
                self.window.show_view(view)
                arcade.draw_text("Correct", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, font_size=50,
                                 anchor_x="center")
                global level
                # gain internships for beating level
                num_internships = str(int(num_internships) + (level * 100))

                #switching levels
                level = 2

            else:
                view = HackLoseView()
                view.setup()
                self.window.show_view(view)


class HackingView2(arcade.View):
    def __init__(self):
        super().__init__()

        # button to return to homepage
        self.menu_list = None

        # internships tracker
        self.internships_list = None

        # submitting code button
        self.submit_button_list = None

        # code blocks
        self.blocks = []
        self.block_texts = [
            "secret_code = input()",  # User input
            "secret_code[0]",  # Slice array function
            "secret_code[1]",  # Slice array function
            "direction_sum = int(secret_code[0]) + int(secret_code[1])",  # Variable block
            "if direction_sum % 2 == 1:",  # If statement
            "direction = 'left'",  # Variable block (direction)
            "else:",  # Else statement
            "direction = 'right'",  # Variable block (direction)
            "secret_code[2:]",  # Slice array function (3rd to 5th digit)
            "num_steps = secret_code[2:]",  # Variable block (num_steps)
            "print(direction + num_steps)"  # Output
        ]

        # checking answers
        self.correct_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.current_order = []

        # text on blocks
        self.code_display = ""

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/IMG_3707.PNG")

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=1)
        self.menu.center_x = 100
        self.menu.center_y = 50
        self.menu_list.append(self.menu)

        # setting up internships count
        self.internships_list = arcade.SpriteList()
        self.internships = arcade.Sprite("CodeLockPrison/internship.png", scale=0.05)
        self.internships.center_x = SCREEN_WIDTH * 0.95
        self.internships.center_y = SCREEN_HEIGHT * 0.9
        self.internships_list.append(self.internships)

        # submit code button
        self.submit_list = arcade.SpriteList()
        self.submit = arcade.Sprite("CodeLockPrison/submit.PNG", scale=0.04)
        self.submit.center_x = SCREEN_WIDTH * 0.48
        self.submit.center_y = SCREEN_HEIGHT * 0.21
        self.submit_list.append(self.submit)

        # code blocks
        self.blocks = arcade.SpriteList()
        for i, text in enumerate(self.block_texts):
            block = arcade.Sprite("CodeLockPrison/images__2_-removebg-preview.png", scale=0.5)
            block.width = 300  # Set your desired width
            block.height = 100  # Set your desired height
            block.center_x = SCREEN_WIDTH * 0.3 + (i % 2) * 350
            block.center_y = SCREEN_HEIGHT * 0.6 - (i // 2) * 150
            block.index = i
            block.text = text
            self.blocks.append(block)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # drawing internship count + icon
        self.internships_list.draw()
        arcade.draw_text(num_internships, self.internships.center_x * 0.98, self.internships.center_y * 0.99,
                         arcade.color.BLACK, font_size=15)

        # drawing hacking question
        question_text = "Each instruction is a sequence of five digits which represents a direction to turn and the number of steps to take to reach the top-secret safe."
        arcade.draw_text(question_text, SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.85, arcade.color.BLACK, font_size=15,
                         multiline=True, width=SCREEN_WIDTH * 0.75)

        # drawing menu button
        self.menu_list.draw()

        # drawing submit button
        self.submit_list.draw()

        # drawing code blocks
        self.blocks.draw()

        # drawing text on code blocks
        for block in self.blocks:
            arcade.draw_text(block.text, block.center_x, block.center_y, arcade.color.WHITE, font_size=10,
                             anchor_x="center", anchor_y="center")

        arcade.draw_text(self.code_display, SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.4, arcade.color.BLACK, font_size=15,
                         multiline=True, width=SCREEN_WIDTH * 0.75)

    def on_mouse_press(self, x, y, button, key_modifiers):

        # if menu button is clicked
        menu_buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(menu_buttons) > 0:
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)
        # if user clicks on code blocks
        clicked_blocks = arcade.get_sprites_at_point((x, y), self.blocks)
        if clicked_blocks:
            clicked_block = clicked_blocks[0]
            if clicked_block.index not in self.current_order:
                # each block costs 20 internships
                global num_internships
                num_internships = str(int(num_internships) - 20)

                # appending clicked code block to user's order
                self.current_order.append(clicked_block.index)

                # displaying the code of the clock clicked
                self.code_display += clicked_block.text + "\n"

        # checking answers
        submit_option = arcade.get_sprites_at_point((x, y), self.submit_list)
        if submit_option:
            if self.current_order == self.correct_order:
                view = HackWinView()
                view.setup()
                self.window.show_view(view)
                arcade.draw_text("Correct", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, font_size=50,
                                 anchor_x="center")
                global level
                level = 3
            else:
                view = HackLoseView()
                view.setup()
                self.window.show_view(view)


class CombatGameOver(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/combat screen (background).jpg")

        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.5)
        self.menu.center_x = SCREEN_WIDTH / 2
        self.menu.center_y = SCREEN_HEIGHT / 2 + 100
        self.menu_list.append(self.menu)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50,
                         anchor_x="center")
        self.menu_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(buttons) > 0:
            view = LevelOneView()
            view.setup()
            self.window.show_view(view)


class CombatWinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/combat screen (background).jpg")

        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.5)
        self.menu.center_x = SCREEN_WIDTH / 2
        self.menu.center_y = SCREEN_HEIGHT / 2 + 100
        self.menu_list.append(self.menu)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("You Win!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50,
                         anchor_x="center")
        self.menu_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
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

        self.background = arcade.load_texture("CodeLockPrison/combat screen (background).jpg")

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()

        # Add healthbar
        for i in range(0, 101, 50):
            self.health = arcade.Sprite("CodeLockPrison/heart (single).png", scale=0.5)
            self.health.center_x = self.health.width - 10
            self.health.center_y = SCREEN_HEIGHT / 2 + i - 160

            self.health_list.append(self.health)

        # Add player ship
        self.player = arcade.Sprite("CodeLockPrison/girl sliding.gif", scale=0.3)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 50
        self.player_list.append(self.player)

        # Add top-left enemy ship
        enemy = EnemySprite("CodeLockPrison/robot shooting.PNG",
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

        if len(self.health_list) <= 0:
            view = CombatGameOver()
            view.setup()
            self.window.show_view(view)
        elif self.bullet_num > 25:
            view = CombatWinView()
            view.setup()
            self.window.show_view(view)

        # if user loses combat game
        if len(self.health_list) <= 0:
            # lose 50 internships
            global num_internships
            num_internships = str(int(num_internships) - 50)

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