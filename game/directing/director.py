from tokenize import group
from game.casting.cast import Cast
from game.casting.artifact import Artifact
from game.shared.point import Point
from game.shared.color import Color
import random


class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 600
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")

        #Added the Points:
        banner.set_text(f"Points: { self._score}")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        
        for artifact in artifacts:
            if robot.get_position().equals(artifact.get_position()):
                point = artifact.get_point()
                self._score += point
                banner.set_text(f"Points: { self._score}")
                cast.remove_actor("artifacts", artifact)
                stones = ['o', '*']

                text = random.choice(stones)
                if text == 'o':
                    points = -10
                else:
                    points = 10

                x = random.randint(1, 60 - 1)
                y = random.randint(-40, 1)
                position = Point(x, y)
                position = position.scale(15)

                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                color = Color(r, g, b)
                
                artifact = Artifact()
                artifact.set_text(text)
                artifact.set_font_size(32)
                artifact.set_color(color)
                artifact.set_position(position)
                artifact.set_point(points)
                cast.add_actor("artifacts", artifact)
            velocity = self._keyboard_service.artifact_direction()
            artifact.set_velocity(velocity)
            artifact.move_next(max_x, max_y)
        
        
        

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()