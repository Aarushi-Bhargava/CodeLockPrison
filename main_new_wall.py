#importer libraries
import arcade
import random
import arcade.gui

PLAYER_MOVEMENT_SPEED = 5

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shooting Game Scratch Code Version (2)"
SPRITE_SIZE = 64
SPRITE_SCALING = 0.5

#Seperating different screens into rooms that the player could switch between (hacking, battle, etc)
class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = None

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None

#Room 1 => this code is the basic setup for every room you would create
def setup_room_1():
    """
    Create and return room 1.
    If your program gets large, you may want to separate this into different
    files.
    """
    room = Room()

    room.wall_list = arcade.SpriteList()


    # Load the background image for this level.
    room.background = arcade.load_texture(":resources:images/backgrounds/"
                                          "abstract_1.jpg")

    return room

#Room 2 => basic setup
def setup_room_2():
    """
    Create and return room 2.
    """
    room = Room()
    room.wall_list = arcade.SpriteList()

    # Load the background image for this level.
    room.background = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")

    return room

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
class MyGame(arcade.Window):
    """ Main application class """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        
        arcade.set_background_color(arcade.color.BLACK)

        self.player = None
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.wall_list = None
        self.physics_engine = None
        self.health = None

        
        #button start here
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()


        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200, height=100)
        start_button.on_click = self.swap_screens
        self.v_box.add(start_button.with_space_around(bottom=20))


        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )
        #button end here\
    
    #swap screen upon click
    def swap_screens(self, event):
        self.current_room = 1

    def setup(self):
        """ Setup the variables for the game. """

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


         # Our list of rooms
        self.rooms = []

        # Sprite lists
        self.current_room = 0

        # Create the rooms. Extend the pattern for each room.
        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2()
        self.rooms.append(room)

        # Our starting room number
        self.current_room = 0

        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.rooms[self.current_room].wall_list)

    def on_draw(self):
        """Render the screen. """

        self.clear()

        

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.rooms[self.current_room].background)

        # # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()
        if self.current_room == 1:
            self.enemy_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()
            self.health_list.draw()

            if len(self.health_list) <= 0:
                arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        
        if self.current_room == 0:
            self.manager.draw()

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

        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0


def main():
    """ Run the game """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()