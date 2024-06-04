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
        global level
        bullet.change_y = -(level*5)
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
            view = LevelView()
            view.setup()
            self.window.show_view(view)

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.back_list = None

        self.story_list = None
        self.instructions_list = None

        self.view_mode = 0

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/menu_background.PNG")

        self.story_list = arcade.SpriteList()
        self.story = arcade.Sprite("CodeLockPrison/pixelated button bg.png")
        self.story.center_x = SCREEN_WIDTH / 4
        self.story.center_y = SCREEN_HEIGHT / 2
        self.story_list.append(self.story)

        self.instructions_list = arcade.SpriteList()
        self.instructions = arcade.Sprite("CodeLockPrison/pixelated button bg.png")
        self.instructions.center_x = SCREEN_WIDTH * 0.75
        self.instructions.center_y = SCREEN_HEIGHT / 2
        self.instructions_list.append(self.instructions)

        self.hacking_list = arcade.SpriteList()
        self.hacking = arcade.Sprite("CodeLockPrison/pixelated button bg.png")
        self.hacking.center_x = SCREEN_WIDTH * 0.25
        self.hacking.center_y = SCREEN_HEIGHT * 0.4
        self.hacking_list.append(self.hacking)

        self.combat_list = arcade.SpriteList()
        self.combat = arcade.Sprite("CodeLockPrison/pixelated button bg.png")
        self.combat.center_x = SCREEN_WIDTH * 0.75
        self.combat.center_y = SCREEN_HEIGHT * 0.4
        self.combat_list.append(self.combat)

        self.internship_list = arcade.SpriteList()
        self.internship = arcade.Sprite("CodeLockPrison/pixelated button bg.png")
        self.internship.center_x = SCREEN_WIDTH * 0.5
        self.internship.center_y = SCREEN_HEIGHT * 0.2
        self.internship_list.append(self.internship)

        # button to return to homepage
        self.back_list = arcade.SpriteList()
        self.back = arcade.Sprite("CodeLockPrison/back button.png", scale=0.2)
        self.back.center_x = 100
        self.back.center_y = 550
        self.back_list.append(self.back)

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        # main menu page view
        if self.view_mode == 0:
            self.story_list.draw()
            self.instructions_list.draw()
            arcade.draw_text("Game Story", self.story.center_x, self.story.center_y, arcade.color.BLACK, font_size=40, anchor_y="center",
                             anchor_x="center", font_name="Consolas")
            arcade.draw_text("How To Play", self.instructions.center_x, self.instructions.center_y, arcade.color.BLACK, font_size=40,
                             anchor_y="center",
                             anchor_x="center", font_name="Consolas")
        # view for game story page
        if self.view_mode == 1:
            arcade.draw_text("You are a prisoner with exceptional coding skills, and your goal is to escape from jail. To succeed, you'll need to hack into systems and outsmart prison guards. Each hacking problem you solve brings you closer to freedom. Are you ready to embark on this epic escape?",
                             SCREEN_WIDTH*0.2, SCREEN_HEIGHT/2, arcade.color.WHITE, font_size=20, anchor_y="center",
                             multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")
        # view for intructions page
        if self.view_mode == 2:
            arcade.draw_text(
                "You will be switching between two other scenes to escape: the hacking scene and the combat scene. You can access the hacking scene by clicking the computer icon that says, “HACK.” You can access the combat scene by clicking on the guard (the cute looking robot).",
                SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.75, arcade.color.WHITE, font_size=20, anchor_y="center",
                multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")

            self.hacking_list.draw()
            self.combat_list.draw()
            self.internship_list.draw()

            arcade.draw_text("Hacking", self.hacking.center_x, self.hacking.center_y, arcade.color.BLACK,
                             font_size=40,
                             anchor_y="center",
                             anchor_x="center", font_name="Consolas")
            arcade.draw_text("Combat", self.combat.center_x, self.combat.center_y, arcade.color.BLACK,
                             font_size=40,
                             anchor_y="center",
                             anchor_x="center", font_name="Consolas")
            arcade.draw_text("Internships", self.internship.center_x, self.internship.center_y, arcade.color.BLACK,
                             font_size=40,
                             anchor_y="center",
                             anchor_x="center", font_name="Consolas")

        # menu view about block code game
        if self.view_mode == 3:
            arcade.draw_text(
                "Use the code blocks provided on the screen to solve the displayed coding problem. If you click on a code block, its corresponding code will display on the whiteboard. Click on the code blocks in the correct order to solve the question and pass the level! Press the red 'HACK' button to submit your code once you think you have the right solution!",
                SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.5, arcade.color.WHITE, font_size=20, anchor_y="center",
                multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")

        # menu view about combat game
        if self.view_mode == 4:
            arcade.draw_text(
                "You can earn internships if you dodge all the projectiles thrown by the guard. If you get hit, you lose a life. You have 3 lives, dodge all the projectiles within the time constraint and without losing all your lives to earn internships!",
                SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.5, arcade.color.WHITE, font_size=20, anchor_y="center",
                multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")

        # menu view about internships
        if self.view_mode == 5:
            arcade.draw_text(
                "You will need internships to purchase code blocks to use in your blockcode solution. You can gain internships in two ways: ",
                SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.8, arcade.color.WHITE, font_size=20, anchor_y="center",
                multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")
            arcade.draw_text(
                "1) Passing a level (solving the level’s question) --- # of internships you gain depends on the level’s difficulty",
                SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.8 - 100, arcade.color.WHITE, font_size=20, anchor_y="center",
                multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")
            arcade.draw_text(
                "2) Winning a combat challenge --- 100 internships. You can also lose 50 internships if you lose the combat challenge.",
                SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.8 - 200, arcade.color.WHITE, font_size=20, anchor_y="center",
                multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")
            arcade.draw_text(
                "If your internship count reaches zero, you lose the game and will have to start over. You will start off with 100 internships.",
                SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.8 - 300, arcade.color.WHITE, font_size=20, anchor_y="center",
                multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")


        self.back_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):

        story = arcade.get_sprites_at_point((x, y), self.story_list)
        instructions = arcade.get_sprites_at_point((x, y), self.instructions_list)
        hacking = arcade.get_sprites_at_point((x, y), self.hacking_list)
        combat = arcade.get_sprites_at_point((x, y), self.combat_list)
        internships = arcade.get_sprites_at_point((x, y), self.internship_list)
        back = arcade.get_sprites_at_point((x, y), self.back_list)

        if story and self.view_mode == 0:
            self.view_mode = 1
        elif instructions and self.view_mode == 0:
            self.view_mode = 2
        elif hacking and self.view_mode == 2:
            self.view_mode = 3
        elif combat and self.view_mode == 2:
            self.view_mode = 4
        elif internships and self.view_mode == 2:
            self.view_mode = 5
        elif back:
            if self.view_mode == 0:
                view = LevelView()
                view.setup()
                self.window.show_view(view)
            elif self.view_mode > 2:
                self.view_mode = 2
            else:
                self.view_mode = 0


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
                         anchor_x="center", font_name="Consolas")
        arcade.draw_text("You have no more internships", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8, arcade.color.WHITE, font_size=50,
                         anchor_x="center", font_name="Consolas")

        self.button_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.button_list)
        if len(buttons) > 0:
            global num_internships
            num_internships = "100"
            view = LevelView()
            view.setup()
            self.window.show_view(view)


class LevelView(arcade.View):
    def __init__(self):
        super().__init__()

        # menu button
        self.menu_list = None

        # button to go to hacking view
        self.computer_list = None

        # button to go to combat view
        self.guard_list = None

        # internships tracker
        self.internships_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/level 1 (bare).jpg")

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.4)
        self.menu.center_x = 100
        self.menu.center_y = 550
        self.menu_list.append(self.menu)

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
                         arcade.color.BLACK, font_size=15, font_name="Consolas")

        arcade.draw_text("Level "+str(level), SCREEN_WIDTH*0.9, SCREEN_HEIGHT * 0.04,
                         arcade.color.BLACK, font_size=15, font_name="Consolas")

        # drawing other graphics
        self.menu_list.draw()
        self.computer_list.draw()
        self.guard_list.draw()

        # turn to game over screen if less than 0 internships
        if int(num_internships) <= 0:
            view = GameOver()
            view.setup()
            self.window.show_view(view)

    def on_mouse_press(self, x, y, button, key_modifiers):
        menus = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(menus) > 0:
            view = MenuView()
            view.setup()
            self.window.show_view(view)
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

        # menu button
        self.menu_list = None

        # (returns to homepage)
        self.back_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/!!.png")

        self.back_list = arcade.SpriteList()
        self.back = arcade.Sprite("CodeLockPrison/back button.png", scale=0.25)
        self.back.center_x = SCREEN_WIDTH / 2
        self.back.center_y = SCREEN_HEIGHT / 2 + 100
        self.back_list.append(self.back)

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.4)
        self.menu.center_x = 100
        self.menu.center_y = 550
        self.menu_list.append(self.menu)

        # key
        self.key_list = arcade.SpriteList()
        self.key = arcade.Sprite("CodeLockPrison/pixel-old-key-for-games-free-vector-removebg-preview.png", scale=0.4)
        self.key.center_x = SCREEN_WIDTH/2
        self.key.center_y = SCREEN_HEIGHT/2
        self.key_list.append(self.key)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Successful Hacking!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200, arcade.color.WHITE,
                         font_size=50, anchor_x="center", font_name="Consolas")
        arcade.draw_text("Level Up!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150, arcade.color.WHITE,
                         font_size=50, anchor_x="center", font_name="Consolas")
        self.menu_list.draw()
        self.back_list.draw()
        self.key_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.back_list)
        if len(buttons) > 0:
            view = LevelView()
            view.setup()
            self.window.show_view(view)
        menu = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(menu) > 0:
            view = MenuView()
            view.setup()
            self.window.show_view(view)


class HackLoseView(arcade.View):
    def __init__(self):
        super().__init__()
        # menu button
        self.menu_list = None
        self.back_list = None


    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/!!.png")

        self.back_list = arcade.SpriteList()
        self.back = arcade.Sprite("CodeLockPrison/back button.png", scale=0.25)
        self.back.center_x = SCREEN_WIDTH / 2
        self.back.center_y = SCREEN_HEIGHT / 2 + 100
        self.back_list.append(self.back)

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.4)
        self.menu.center_x = 100
        self.menu.center_y = 550
        self.menu_list.append(self.menu)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Unsuccessful Hacking :/ ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150, arcade.color.WHITE,
                         font_size=50, anchor_x="center", font_name="Consolas")
        self.menu_list.draw()
        self.back_list.draw()


    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.back_list)
        if len(buttons) > 0:
            view = LevelView()
            view.setup()
            self.window.show_view(view)
        menu = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(menu) > 0:
            view = MenuView()
            view.setup()
            self.window.show_view(view)


class HackingView1(arcade.View):
    def __init__(self):
        super().__init__()

        # button to return to homepage
        self.menu_list = None

        # button to return to homepage
        self.back_list = None

        # internships tracker
        self.internships_list = None

        # submitting code button
        self.submit_button_list = None

        # code blocks
        self.blocks = []
        self.block_texts = [
            "num_tiles = int(input())",  # User Input
            "print(max_side_length)",  # Output
            "max_side_length = math.sqrt(num_tiles)",  # Square Root Function
            "max_side_length = math.floor(max_side_length)",  # Round Down Function
        ]

        # checking order of code blocks
        self.correct_order = [0, 2, 3, 1]
        self.current_order = []

        # displaying the written code
        self.code_display = ""

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/IMG_3707.PNG")

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.4)
        self.menu.center_x = 100
        self.menu.center_y = 550
        self.menu_list.append(self.menu)

        # button to return to homepage
        self.back_list = arcade.SpriteList()
        self.back = arcade.Sprite("CodeLockPrison/back button.png", scale=0.2)
        self.back.center_x = 220
        self.back.center_y = 550
        self.back_list.append(self.back)

        # setting up internships count
        self.internships_list = arcade.SpriteList()
        self.internships = arcade.Sprite("CodeLockPrison/internship.png", scale=0.05)
        self.internships.center_x = SCREEN_WIDTH * 0.95
        self.internships.center_y = SCREEN_HEIGHT * 0.9
        self.internships_list.append(self.internships)

        # submit code button
        self.submit_list = arcade.SpriteList()
        self.submit = arcade.Sprite("CodeLockPrison/submit.PNG", scale=0.04)
        self.submit.center_x = SCREEN_WIDTH * 0.75
        self.submit.center_y = SCREEN_HEIGHT * 0.7
        self.submit_list.append(self.submit)

        # code blocks
        self.blocks = arcade.SpriteList()
        for i, text in enumerate(self.block_texts):
            block = arcade.Sprite("CodeLockPrison/pixelated button bg.png", scale=1)
            block.width = 500  # Set your desired width
            block.height = 200  # Set your desired height
            block.center_x = SCREEN_WIDTH * 0.75
            block.center_y = SCREEN_HEIGHT * 0.6 - (i / 2) * 150
            block.index = i
            block.text = text
            self.blocks.append(block)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # drawing internship count + icon
        self.internships_list.draw()
        arcade.draw_text(num_internships, self.internships.center_x * 0.98, self.internships.center_y * 0.99,
                         arcade.color.BLACK, font_size=15, font_name="Consolas")

        # drawing programming question
        question_text = "Write a program that asks the user for the number of tiles, and then prints out the side length of the largest possible square built with the tiles. You may assume that the user will only type integers that are less than ten thousand."
        arcade.draw_text(question_text, SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.85, arcade.color.BLACK, font_size=15,
                         multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")

        # drawing home button
        self.menu_list.draw()

        # drawing home button
        self.back_list.draw()

        # drawing submit button
        self.submit_list.draw()

        # drawing code blocks
        self.blocks.draw()

        # drawing text onto code blocks
        for block in self.blocks:
            arcade.draw_text(block.text, block.center_x, block.center_y, arcade.color.WHITE, font_size=10,
                             anchor_x="center", anchor_y="center", font_name="Consolas")

        # drawing actual code
        arcade.draw_text("Program", SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.65, arcade.color.BLACK, font_size=25,
                         multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")
        arcade.draw_text(self.code_display, SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.5, arcade.color.BLACK, font_size=10,
                         multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")

    def on_mouse_press(self, x, y, button, key_modifiers):

        # if user clicks on menu button
        back_buttons = arcade.get_sprites_at_point((x, y), self.back_list)
        if back_buttons:
            view = LevelView()
            view.setup()
            self.window.show_view(view)

        # if user clicks on menu button
        menu_buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
        if menu_buttons:
            view = MenuView()
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
                global level
                # gain internships for beating level
                num_internships = str(int(num_internships) + (level * 100))

                view = HackWinView()
                view.setup()
                self.window.show_view(view)
                arcade.draw_text("Correct", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, font_size=50,
                                 anchor_x="center", font_name="Consolas")

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
        self.back_list = None

        # internships tracker
        self.internships_list = None

        # submitting code button
        self.submit_button_list = None

        # code blocks
        self.blocks = []
        self.block_texts = [
            "direction_sum = secret_code[0]+secret_code[1]",  # Variable block
            "if direction_sum % 2 == 1:",  # If statement
            "num_steps = secret_code[2:]",  # Variable block (num_steps)
            "direction = 'right'",  # Variable block (direction)
            "direction = 'left'",  # Variable block (direction)
            "else:",  # Else statement
            "print(direction + num_steps)",  # Output
            "secret_code = input()",  # User input
        ]

        # checking answers
        self.correct_order = [7, 0, 1, 4, 5, 3, 2, 6]
        self.current_order = []

        # text on blocks
        self.code_display = ""

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/IMG_3707.PNG")

        # button to return to homepage
        self.back_list = arcade.SpriteList()
        self.back = arcade.Sprite("CodeLockPrison/back button.png", scale=0.2)
        self.back.center_x = 220
        self.back.center_y = 550
        self.back_list.append(self.back)

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.4)
        self.menu.center_x = 100
        self.menu.center_y = 550
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
            block = arcade.Sprite("CodeLockPrison/pixelated button bg.png", scale=1)
            block.width = 450  # Set your desired width
            block.height = 200  # Set your desired height
            block.center_x = SCREEN_WIDTH * 0.55 + (i % 2) * 350
            block.center_y = SCREEN_HEIGHT * 0.65 - (i // 2) * 50
            block.index = i
            block.text = text
            self.blocks.append(block)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # drawing internship count + icon
        self.internships_list.draw()
        arcade.draw_text(num_internships, self.internships.center_x * 0.98, self.internships.center_y * 0.99,
                         arcade.color.BLACK, font_size=15, font_name="Consolas")

        # drawing hacking question
        question_text = "Decode an instruction that is a sequence of five digits which represents a direction to turn and the number of steps to take. The first two digits represent the direction: if their sum is odd, turn left. If their sum is even, turn right. The last 3 digits represent the number of steps."
        arcade.draw_text(question_text, SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.85, arcade.color.BLACK, font_size=15,
                         multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")

        # drawing menu button
        self.menu_list.draw()
        self.back_list.draw()

        # drawing submit button
        self.submit_list.draw()

        # drawing code blocks
        self.blocks.draw()

        # drawing text on code blocks
        for block in self.blocks:
            arcade.draw_text(block.text, block.center_x, block.center_y, arcade.color.WHITE, font_size=10,
                             anchor_x="center", anchor_y="center", font_name="Consolas")
        # drawing actual code
        arcade.draw_text("Program", SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.65, arcade.color.BLACK, font_size=25,
                         multiline=True, width=SCREEN_WIDTH * 0.75, font_name="Consolas")
        arcade.draw_text(self.code_display, SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.55, arcade.color.BLACK,
                         font_size=5, multiline=True, width=SCREEN_WIDTH * 0.3, font_name="Consolas")

    def on_mouse_press(self, x, y, button, key_modifiers):

        # if menu button is clicked
        back_buttons = arcade.get_sprites_at_point((x, y), self.back_list)
        if len(back_buttons) > 0:
            view = LevelView()
            view.setup()
            self.window.show_view(view)
        # if menu button is clicked
        menu_buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(menu_buttons) > 0:
            view = MenuView()
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
                global level
                # gain internships for beating level
                num_internships = str(int(num_internships) + (level * 100))

                view = HackWinView()
                view.setup()
                self.window.show_view(view)
                arcade.draw_text("Correct", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, font_size=50,
                                 anchor_x="center", font_name="Consolas")
                level = 3
            else:
                view = HackLoseView()
                view.setup()
                self.window.show_view(view)


class CombatGameOver(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_list = None
        self.back_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/combat screen (background).jpg")

        self.back_list = arcade.SpriteList()
        self.back = arcade.Sprite("CodeLockPrison/back button.png", scale=0.5)
        self.back.center_x = SCREEN_WIDTH / 2
        self.back.center_y = SCREEN_HEIGHT / 2 + 100
        self.back_list.append(self.back)

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.4)
        self.menu.center_x = 100
        self.menu.center_y = 550
        self.menu_list.append(self.menu)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50,
                         anchor_x="center", font_name="Consolas")
        self.menu_list.draw()
        self.back_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        back = arcade.get_sprites_at_point((x, y), self.back_list)
        if back:
            view = LevelView()
            view.setup()
            self.window.show_view(view)
        menu = arcade.get_sprites_at_point((x, y), self.menu_list)
        if menu:
            view = MenuView()
            view.setup()
            self.window.show_view(view)


class CombatWinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_list = None
        self.back_list = None

    def setup(self):
        self.background = arcade.load_texture("CodeLockPrison/combat screen (background).jpg")

        self.back_list = arcade.SpriteList()
        self.back = arcade.Sprite("CodeLockPrison/back button.png", scale=0.25)
        self.back.center_x = SCREEN_WIDTH / 2
        self.back.center_y = SCREEN_HEIGHT / 2 + 100
        self.back_list.append(self.back)

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.4)
        self.menu.center_x = 100
        self.menu.center_y = 550
        self.menu_list.append(self.menu)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_text("You Win!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50,
                         anchor_x="center", font_name="Consolas")
        self.menu_list.draw()
        self.back_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.back_list)
        if len(buttons) > 0:
            view = LevelView()
            view.setup()
            self.window.show_view(view)
        menu = arcade.get_sprites_at_point((x, y), self.menu_list)
        if menu:
            view = MenuView()
            view.setup()
            self.window.show_view(view)


class CombatView(arcade.View):
    """ Main application class """

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.menu_list = None

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

        # menu button
        self.menu_list = arcade.SpriteList()
        self.menu = arcade.Sprite("CodeLockPrison/menu icon.png", scale=0.4)
        self.menu.center_x = 100
        self.menu.center_y = 550
        self.menu_list.append(self.menu)

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
        self.player = arcade.Sprite("CodeLockPrison/girl walking2.png", scale=0.3)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 50
        self.player_list.append(self.player)

        # Add top-left enemy ship
        enemy = EnemySprite("CodeLockPrison/robot shooting.PNG",
                            scale=0.1,
                            bullet_list=self.bullet_list,
                            min_time_between_firing=0.2,  # Minimum time between shots
                            max_time_between_firing=1,  # Maximum time between shots
                            movement_speed=4,
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

        self.menu_list.draw()

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.health_list.draw()

        global num_internships
        # if user loses combat game
        if len(self.health_list) <= 0:
            # lose 50 internships
            num_internships = str(int(num_internships) - (level*50))

            # change view to game over screen
            view = CombatGameOver()
            view.setup()
            self.window.show_view(view)

        # if user wins combat game
        elif self.bullet_num > level*15:
            # gain internships
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

    def on_mouse_press(self, x, y, button, key_modifiers):
        buttons = arcade.get_sprites_at_point((x, y), self.menu_list)
        if len(buttons) > 0:
            view = MenuView()
            view.setup()
            self.window.show_view(view)


def main():
    """ Run the game """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MyGameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()