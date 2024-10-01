"""
    A class to represent a musical instrument.
    Attributes:
        name (str): The name of the instrument.
        id (int): The unique identifier for the instrument.
        scale (list[float]): A list of pitch frequencies associated with the instrument.
    Methods:
        __repr__(): Returns a string representation of the Instrument instance.
    """
class Instrument:
    def __init__(self, name: str, id: int, scale: list[float], wav_file: str):
        self.name = name
        self.id = id
        self.scale = scale
        self.wav_file = wav_file

    def __repr__(self):
        return f"Instrument(name={self.name}, id={self.id}, scale={self.scale}, pitch_file={self.wav_file})"
    
