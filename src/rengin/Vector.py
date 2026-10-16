class Vector2:
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
