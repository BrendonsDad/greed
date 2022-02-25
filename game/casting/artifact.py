from game.casting.actor import Actor


class Artifact(Actor):
    """
    An item of cultural or historical interest. 
    
    The responsibility of an Artifact is to provide a message about itself.

    Attributes:
        _message (string): A short description about the artifact.
    """
    def __init__(self):
        super().__init__()
        self._point = ""
        
    def get_point(self):
        """Gets the artifact's message.
        
        Returns:
            string: The message.
        """
        return self._point
    
    def set_point(self, point):
        """Updates the message to the given one.
        
        Args:
            message (string): The given message.
        """
        self._point = point

