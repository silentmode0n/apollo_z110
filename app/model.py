from .config import (
    CAP_NAME,
    CAP_UNITS,
    FENCE_NAME,
    LAMEL_NAME,
    LAMEL_UNITS,
    RAIL_NAME,
    RAIL_UNITS,
    SLAT_NAME,
    SLAT_UNITS,
    )


class Element:

    def __init__(self, name: str, size: int, color: str, colortype: str, unit: str):
        self.name = name
        self.size = size
        self.color = color
        self.colortype = colortype
        self.unit = unit

    def __repr__(self):
        return f"{self.__class__.__name__} <{self.name} {self.size} RAL{self.color} {self.colortype}>"

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, obj):
        if type(obj) is not type(self):
            return False
        if (
            self.name == obj.name
            and self.size == obj.size
            and self.color == obj.color
            and self.colortype == obj.colortype
        ):
            return True
        else:
            return False


class Counter():
    """Счетчик для количества идентичных элементов Element"""
    def __init__(self):
        self._map = {}

    def add(self, new_element: Element, num: int):
        if num > 0:
            if new_element in self._map.keys():
                self._map[new_element] += num
            else:
                self._map[new_element] = num

    def get(self) -> dict[Element, int]:
        return self._map.copy()


class Slat(Element):
	def __init__(self, size: int, color: str, colortype: str):
		super().__init__(name=SLAT_NAME, size=size, color=color, colortype=colortype, unit=SLAT_UNITS)


class Cap(Element):
	def __init__(self, size: int, color: str, colortype: str):
		super().__init__(name=CAP_NAME, size=size, color=color, colortype=colortype, unit=CAP_UNITS)


class Rail(Element):
	def __init__(self, size: int, color: str, colortype: str):
		super().__init__(name=RAIL_NAME, size=size, color=color, colortype=colortype, unit=RAIL_UNITS)


class Lamel(Element):
	def __init__(self, size: int, color: str, colortype: str):
		super().__init__(name=LAMEL_NAME, size=size, color=color, colortype=colortype, unit=LAMEL_UNITS)


class Fence:
    def __init__(self, width: int, height: int, color: str, colortype: str, num: int):
        self.name = FENCE_NAME
        self.width = width
        self.height = height
        self.color = color
        self.colortype = colortype
        self.slat_num = 2 if self.width >= 2500 else 1 if self.width >= 2000 else 0
        self.num = num

    def __repr__(self) -> str:
          return f'{self.__class__.__name__} <{self.name} {self.width}x{self.height} RAL{self.color} {self.colortype} {self.num}шт>'

    def get_lamels(self) -> tuple[Element, int]:
        num = (self.height // 110) * self.num
        return (Lamel(self.width - 15, self.color, self.colortype), num)

    def get_rails(self) -> tuple[Element, int]:
        num = self.num
        return (Rail(self.height, self.color, self.colortype), num)

    def get_caps(self) -> tuple[Element, int]:
        num = self.num
        return (Cap(self.width, self.color, self.colortype), num)

    def get_slats(self) -> tuple[Element, int]:
        num = self.slat_num * self.num
        return (Slat(self.height - 40, self.color, self.colortype), num)


class Model:
    """Класс описывающий главную модель"""

    def __init__(self, data: dict):
        self.data = data
        self.data['fences'] = [Fence(**fence) for fence in self.data['table']]
        self.data.update(self._count_elements(self.data['fences']))

    def _count_elements(self, fences: list) -> dict:
        lamels_counter = Counter()
        rails_counter = Counter()
        caps_counter = Counter()
        slats_counter = Counter()
        for fence in fences:
            lamels_counter.add(*fence.get_lamels())
            caps_counter.add(*fence.get_caps())
            rails_counter.add(*fence.get_rails())
            slats_counter.add(*fence.get_slats())
        return {
            'lamels': lamels_counter.get(),
            'rails': rails_counter.get(),
            'caps': caps_counter.get(),
            'slats': slats_counter.get(),
        }
