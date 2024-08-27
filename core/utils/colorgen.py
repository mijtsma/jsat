import distinctipy as dp
from typing import Tuple

class ColorGenerator:
    ''' A static class for generating distinct colors which are matched to and 
        retriveable by an ID string.
    '''

    __num_generated: int = 0
    # Blue, Red, Cyan, Green, Orange, Purple, Yellow, Magenta
    __basic_colors: list[Tuple[float,float,float]] = [
        (0.0, 0.0, 1.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 1.0),
        (0.0, 1.0, 0.0), 
        (1.0, 0.5, 0.0), 
        (0.5, 0.0, 1.0), 
        (1.0, 1.0, 0.0), 
        (1.0, 0.0, 1.0)
    ]
    __blacklisted_colors: list[Tuple[float,float,float]] = [
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0)
    ]
    generated_colors: dict[str, list[Tuple[float,float,float]]] = {}

    @staticmethod
    def get_color(id: str) -> str:
        ''' Gets a hex code from generated colors matching the given string.
            If a color has not been made for the given string, a new
            visually distinct color is generated.
        '''
        return dp.get_hex(ColorGenerator.find_color(id))

    @staticmethod
    def get_pastel_tikz_color(id:str) -> str:
        ''' Gets a tikz color from generated colors matching the given string.
            If a color has not been made for the given string, a new
            visually distinct color is generated.
        '''
        color = dp.get_rgb256(ColorGenerator.find_pastel_color(id))
        return ("{" + str(color[0]) + "," + 
            str(color[1]) + "," + 
            str(color[2]) + "}")

    @staticmethod
    def find_pastel_color(
        id: str, 
        factor: float = 0.6
    ) -> Tuple[float,float,float]:
        ''' Does the same as find_color, but pastelizes the color by
            mixing with white (determined by factor).
        '''
        color = ColorGenerator.find_color(id)
        return (
            factor + ((1 -factor) * color[0]),
            factor + ((1 -factor) * color[1]),
            factor + ((1 -factor) * color[2])
        )

    @staticmethod
    def find_color(id: str) -> Tuple[float,float,float]:
        ''' Method which handles color generation/distinctipy interactions
            for the methods which get colors.
        '''
        #already exists
        if id in ColorGenerator.generated_colors:
            return ColorGenerator.generated_colors[id]
        #basic colors remain
        if ColorGenerator.__num_generated < len(ColorGenerator.__basic_colors):
            index = ColorGenerator.__num_generated 
            tuple_basic = ColorGenerator.__basic_colors[index]
            ColorGenerator.generated_colors[id] = tuple_basic
            ColorGenerator.__num_generated += 1
            return tuple_basic
        #need to generate color with distinctipy
        tuple_new = dp.distinct_color(
            list(ColorGenerator.generated_colors.values())
            .extend(ColorGenerator.__blacklisted_colors)
        )
        ColorGenerator.generated_colors[id] = tuple_new
        ColorGenerator.__num_generated += 1
        return tuple_new


        
        

