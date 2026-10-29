from typing import Sequence, overload, Union

class Vector2(Sequence[tuple[float, float]]):
    """The Vector2 Class"""
    x:float|int
    y:float|int

    Values:tuple[float, float]

    def __init__(self, x:float, y:float):
        if not x or not y:
            self.x = 0.0
            self.y = 0.0
        else:
            self.x = x
            self.y = y

        self.Values = (x, y)

    def __iadd__(self, other:Vector2):
        tempV1, tempV2 = self.Values[0], self.Values[1]
        tempO1, tempO2 = other.Values[0], other.Values[1]

        return Vector2(tempV1+tempO1, tempV2+tempO2)

    def __isub__(self, other:Vector2):
        tempV1, tempV2 = self.Values[0], self.Values[1]
        tempO1, tempO2 = other.Values[0], other.Values[1]

        return Vector2(tempV1-tempO1, tempV2-tempO2)

    def __repr__(self):
        return f"Vector2({self.Values[0]}, {self.Values[1]})"

    def __call__(self):
        return self.Values

    @overload
    def __getitem__(self, index:int, /): # Converts to be usable as sequence like by pygame
        return tuple(self.Values)

    @overload
    def __getitem__(self, index:slice):
        return self.Values

    def __getitem__(self, index:Union[int, slice]) -> Union[float, 'tuple[float, float]']:
        return self.Values

    def __len__(self):
        return len(self.Values)
