""" トランプゲーム用汎用モジュール

    * class Size: 幅(IMAGE_WIDTH)と高さ(IMAGE_HEIGHT)をもつプロトコル
    * class Rectangle: 矩形領域を示すデータ型
    * class Holder: ボード上の場(カードを表示する領域)
    * class Board: トランプゲームの盤面を表すクラス

"""
from typing import NamedTuple, TypeVar, Callable, Generic, Protocol
from tkinter import Canvas
from PIL import ImageTk

T = TypeVar('T', bound='Size')


class Size(Protocol):
    @property
    def IMAGE_WIDTH(self) -> int:
        ...

    @property
    def IMAGE_HEIGHT(self) -> int:
        ...


class Rectangle(NamedTuple):
    """矩形領域を示すデータ型
    """
    top: int
    left: int
    botom: int
    right: int


class Holder(Generic[T]):
    """盤上の表示領域を表すクラス
    """
    TBoard = TypeVar('TBoard', bound='Board')

    cards: list[T]
    rect: Rectangle
    _parent: TBoard
    func_pos: Callable[[T], tuple[int, int]]

    def __init__(self, top, left, bottom, right,
                 parent: TBoard,
                 func: Callable[[T], tuple[int, int]] = lambda _: (0, 0)):
        self.rect = Rectangle(top, left, bottom, right)
        self._parent = parent
        self.cards = []
        self.func_pos = func

    def redraw(self):
        for c in self.cards:
            x, y = self.func_pos(self, c)
            self._parent.draw(self, x, y, c.image)

    def holizontal(self, elem: T) -> tuple[int, int]:
        index = self.cards.index(elem)
        return (index * elem.IMAGE_WIDTH, 0)


class Board(Generic[T]):
    """盤面を表すクラス
    """
    card_class: T

    def __init__(self, canvas: Canvas, *, cls: T) -> None:
        self.__canvas = canvas
        self.holders = []
        self.card_class = cls

    def create_holder(self,
                      top: int, left: int, bottom: int, right: int,
                      func: Callable[[T], tuple[int, int]]
                      ) -> Holder:
        """表示領域を作る

        Args:
            top (int): 盤上での表示領域上端の位置
            left (int): 盤上での表示領域左端の位置
            bottom (int): 盤上での表示領域下端の位置
            right (int): 盤上での表示領域右端の位置

        Returns:
            Holder: 表示領域を示すオブジェクト
        """
        holder = Holder(top, left, bottom, right, self, func)
        self.holders.append(holder)
        return holder

    def get_holder(self, n: int) -> Holder:
        """番号を基準に表示領域を返す

        Args:
            n (int): 表示領域の番号

        Returns:
            Holder: 表示領域のオブジェクト
        """
        return self.holders[n]

    def draw(self, holder: Holder, x, y, img: ImageTk) -> None:
        """盤面の指定した領域の指定した場所にイメージを表示する
        """
        top = holder.rect.top + y
        left = holder.rect.left + x

        self.__canvas.create_image(left, top, anchor='nw', image=img)

    def redraw(self) -> None:
        for holder in self.holders:
            holder.redraw()
