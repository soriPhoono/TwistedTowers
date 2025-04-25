import arcade

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Twisted Towers"

TILE_SCALE = 0.5

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 15


class GameView(arcade.Window):
    def __init__(self):
        """
        Initialize a new GameView object.

        Parameters:
        None
        """

        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.level = 1
        self.score_reset = False
        self.score = 0
        self.end_of_map = 0

        self.background_color = arcade.csscolor.SKY_BLUE

        self.collect_coin_sound = arcade.load_sound(
            ":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.gameover_sound = arcade.load_sound(
            ":resources:sounds/gameover1.wav")

        self.scene: arcade.Scene = None
        self.tile_map = None

        self.physics_engine = None

        self.camera = None
        self.gui_camera = None

        self.player_sprite = None

        self.score_text = None

    def setup(self):
        """
        Set up the game/level.

        This method is called once when the game starts. It is the place
        where you can initialize the variables and do all the setup that
        you need to do.

        Parameters:
        None
        """

        if self.score_reset:
            self.score = 0
        self.score_reset = True

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            }
        }

        self.tile_map = arcade.tilemap.load_tilemap(
            f":resources:tiled_maps/map2_level_{self.level}.json",
            scaling=TILE_SCALE,
            layer_options=layer_options,
            lazy=True,
        )

        self.end_of_map = (self.tile_map.width *
                           self.tile_map.tile_width) * self.tile_map.scaling

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite_list_after("Player", "Foreground")

        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.scene.get_sprite_list("Platforms")
        )

        self.camera = arcade.Camera2D()

        self.gui_camera = arcade.Camera2D()
        self.score_text = arcade.Text(
            text=f"Score: {self.score}",
            x=0,
            y=5,
        )

        pass

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        match key:
            case arcade.key.ESCAPE:
                self.setup()
            case arcade.key.UP | arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    arcade.play_sound(self.jump_sound)
            case arcade.key.LEFT | arcade.key.A:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            case arcade.key.RIGHT | arcade.key.D:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""

        match key:
            case arcade.key.UP | arcade.key.W:
                self.player_sprite.change_y = 0
            case arcade.key.LEFT | arcade.key.A:
                self.player_sprite.change_x = 0
            case arcade.key.RIGHT | arcade.key.D:
                self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Coins")
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"Score: {self.score}"

        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene.get_sprite_list("Don't Touch")
        ):
            arcade.play_sound(self.gameover_sound)
            self.setup()

        self.camera.position = self.player_sprite.position

        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1
            self.setup()

    def on_draw(self):
        """
        Render the screen.

        This method is called whenever the screen needs to be redrawn.
        It clears the screen and draws the necessary elements.
        """

        self.clear()

        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()
        self.score_text.draw()
