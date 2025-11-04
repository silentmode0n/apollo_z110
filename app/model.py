from .config import (
    CAP_TITLE,
    CAP_UNITS,
    FENCE_TITLE,
    LAMEL_TITLE,
    LAMEL_UNITS,
    RAIL_TITLE,
    RAIL_UNITS,
    SLAT_TITLE,
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


class Counter:
    """Счетчик для количества идентичных элементов Element"""
    def __init__(self):
        self._map = {}

    def add(self, new_element: Element, num: int):
        if num > 0:
            if new_element in self._map.keys():
                self._map[new_element] += num
            else:
                self._map[new_element] = num

    def get_dict(self) -> dict[Element, int]:
        return self._map.copy()

    def get(self) -> list[dict]:
        list_of_elements = []
        for element, count in self._map.items():
            list_of_elements.append({
                'name': element.name,
                'size': str(element.size),
                'color': element.color,
                'colortype': element.colortype,
                'count': str(count),
                'unit': element.unit,
                })
        return list_of_elements



class Slat(Element):
	def __init__(self, size: int, color: str, colortype: str):
		super().__init__(name=SLAT_TITLE, size=size, color=color, colortype=colortype, unit=SLAT_UNITS)


class Cap(Element):
	def __init__(self, size: int, color: str, colortype: str):
		super().__init__(name=CAP_TITLE, size=size, color=color, colortype=colortype, unit=CAP_UNITS)


class Rail(Element):
	def __init__(self, size: int, color: str, colortype: str):
		super().__init__(name=RAIL_TITLE, size=size, color=color, colortype=colortype, unit=RAIL_UNITS)


class Lamel(Element):
	def __init__(self, size: int, color: str, colortype: str):
		super().__init__(name=LAMEL_TITLE, size=size, color=color, colortype=colortype, unit=LAMEL_UNITS)


class Fence:
    def __init__(self, width: int, height: int, color: str, colortype: str):
        self.name = FENCE_TITLE
        self.width = width
        self.height = height
        self.color = color
        self.colortype = colortype
        self.slat_num = 2 if self.width >= 2500 else 1 if self.width >= 2000 else 0

    def __repr__(self) -> str:
          return f'{self.__class__.__name__} <{self.name} {self.width}x{self.height} RAL{self.color} {self.colortype}>'

    def get_lamels(self) -> tuple[Element, int]:
        num = (self.height // 110)
        return (Lamel(self.width - 15, self.color, self.colortype), num)

    def get_rails(self) -> tuple[Element, int]:
        return (Rail(self.height, self.color, self.colortype), 1)

    def get_caps(self) -> tuple[Element, int]:
        return (Cap(self.width, self.color, self.colortype), 1)

    def get_slats(self) -> tuple[Element, int]:
        return (Slat(self.height - 40, self.color, self.colortype), self.slat_num)


class Model:
    """Класс описывающий главную модель"""

    def __init__(self, raw_table: list[dict]):
        self.fences = self._create_fences_from_tabel(raw_table)

    def _create_fences_from_tabel(self, raw_table: list) -> list[tuple[Fence, int]]:
        fences = []
        for row in raw_table:
            fences.append((
                Fence(row['width'], row['height'], row['color'], row['colortype']),
                row['count']
                ))
        return fences

    def export_fences(self) -> list[dict]:
        data = []
        for fence, count in self.fences:
            data.append({
                'name': fence.name,
                'width': str(fence.width),
                'height': str(fence.height),
                'color': fence.color,
                'colortype': fence.colortype,
                'slat_num': str(fence.slat_num),
                'count': str(count),
                })
        return data

    def export_lamels(self) -> list[dict]:
        counter = Counter()
        for fence, count in self.fences:
            element, num = fence.get_lamels()
            counter.add(element, num * count)
        return counter.get()

    def export_rails(self) -> list[dict]:
        counter = Counter()
        for fence, count in self.fences:
            element, num = fence.get_rails()
            counter.add(element, num * count)
        return counter.get()

    def export_caps(self) -> list[dict]:
        counter = Counter()
        for fence, count in self.fences:
            element, num = fence.get_caps()
            counter.add(element, num * count)
        return counter.get()

    def export_slats(self) -> list[dict]:
        counter = Counter()
        for fence, count in self.fences:
            element, num = fence.get_slats()
            counter.add(element, num * count)
        return counter.get()
