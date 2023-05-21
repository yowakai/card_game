""" トランプゲーム用汎用モジュール

    * class Suit: トランプのスートを表す列挙型
    * class Card: トランプのカード 1枚を表すクラス
    * class CardImageBuilder: 1枚の大きな画像から
    *       カード 1枚の画像を切り出す Builder
    * class Deck: トランプ一式(山札)を表すクラス
    * class Hand: トランプの手札を表すクラス

"""
from enum import IntEnum, auto
from random import shuffle
from typing import TypeVar, Callable, Iterable
from PIL import Image, ImageTk
from board import Holder


class Suit(IntEnum):
    """トランプのスートを表す列挙型

    内部的にはスートの強さを表す整数値で表し
    __str__メソッドで表示名に変換する
    """
    CLUB = auto()
    DIAMOND = auto()
    HEART = auto()
    SPADE = auto()
    JOKER = auto()

    def __str__(self) -> str:
        # 左の[]はリストのリテラル、右の[]はインデックス指定
        return ["", "♣", "♦", "♥", "♠", "Joker"][self.value]


class CardImageBuilder:
    IMAGE_WIDTH: int
    IMAGE_HEIGHT: int
    __IMAGE_PATH: str = 'assets/images/trump.png'
    REVERSED: ImageTk

    def __init__(self):
        self.__IMAGE = Image.open(self.__IMAGE_PATH)
        self.IMAGE_WIDTH = self.__IMAGE.size[0] // 13
        self.IMAGE_HEIGHT = self.__IMAGE.size[1] // 4     # Number of suites
        self.REVERSED = self.__IMAGE.crop((0, 0, 100, 200))

    def GetPhotoImage(self, suit: Suit, number: int) -> Image:
        left = (number - 1) * self.IMAGE_WIDTH
        right = left + self.IMAGE_WIDTH - 1

        # Suitの並びと画像の並びが違うので読み替える
        x = [Suit.SPADE, Suit.HEART, Suit.CLUB, Suit.DIAMOND].index(suit)

        top = self.IMAGE_HEIGHT * x
        bottom = top + self.IMAGE_HEIGHT - 1

        return ImageTk.PhotoImage(
            self.__IMAGE.crop((left, top, right, bottom))
        )


class Card:
    """トランプのカード 1枚を表すクラス

    Attributes
        numbers: カードで使える値のレンジオブジェクト
        suit: スート
        number: 番号(1(A), 2, 3, ... , 10, 11(J), 12(Q), 13(K))
        strength: カードの強さ

    """
    Self = TypeVar('Self', bound='Card')

    IMAGE_WIDTH: int
    IMAGE_HEIGHT: int
    REVERSED: ImageTk
    __is_open: bool

    numbers = range(1, 13+1)
    # __NUM_DISP: カード番号の表示名のリスト
    __NUM_DISP = ["", "A", "J", "Q", "K"]
    __NUM_DISP[2:2] = [str(n) for n in range(2, 10+1)]

    # カードのイメージ
    cib = CardImageBuilder()
    IMAGE_WIDTH = cib.IMAGE_WIDTH
    IMAGE_HEIGHT = cib.IMAGE_HEIGHT
    REVERSED = cib.REVERSED

    def __init__(self, suit: Suit, number: int) -> None:
        self.__suit = suit
        self.__number = int(number)

        self.image = self.cib.GetPhotoImage(suit, number)
        self.is_open = True

    def __str__(self) -> str:
        if self.__suit == Suit.JOKER:
            return str(self.__suit)
        # __NUM_DISPはクラス変数だが、self.__NUM_DISPとすることで
        # サブクラスでオーバーライドしてもオーバーライド先を参照してくれる
        return "-".join([str(self.__suit), self.__NUM_DISP[self.__number]])

    @property
    def is_open(self) -> bool:
        return self.__is_open

    @is_open.setter
    def is_open(self, value: bool):
        self.__is_open = value

    # デコレータ
    @staticmethod
    def typecheck(func: Callable[[Self, Self], bool]) \
            -> Callable[[Self, Self], bool]:
        # 型チェックデコレータ
        # 比較演算で使用する
        # selfと otherの型が異なる場合、TypeErrorを上げる
        # なぜか型ヒントが書けないのでしかたなくデコレータで実装
        # 3.11 なら typing.Self が使える
        def _typecheck(self, other) -> bool:
            if not isinstance(other, type(self)):
                raise TypeError
            v = func(self, other)
            return v
        return _typecheck

    @property
    def strength(self) -> int:
        """カードの強さ

        デフォルトではスートを考慮し、Aを 1とする
        """
        return self.__suit * 100 + self.__number

    @property
    def suit(self) -> Suit:
        return self.__suit

    @property
    def number(self) -> int:
        return self.__number


class Deck:
    """ トランプの 1セット

    イテラブルとして使用できる

    Attributes:
        len: 残りカード枚数

    """
    TCard = TypeVar('TCard', bound="Card")

    def __init__(self, *, card_cls: type[TCard] = Card, joker: bool = True) \
            -> None:
        # デッキを作る
        # Keyword parameters:
        #   joker(bool): ジョーカーを含むかどうか
        #   card_cls(Class): デッキで使うクラスを指定する(デフォルト Card)
        self.__cards = [card_cls(s, n)
                        for s in Suit
                        for n in card_cls.numbers if s != Suit.JOKER
                        ]
        if joker:
            self.__cards.append(card_cls(Suit.JOKER, 0))

    def __iter__(self) -> Iterable[Card]:
        # イテラブルとして参照されたときの動作
        # カードは取り除かれないことに注意
        yield from self.__cards

    def __str__(self) -> str:
        # デッキの内容をすべて表示する
        s = '\n'.join(map(str, self.__cards))
        return s

    def shuffle(self) -> None:
        """デッキをシャッフルする
        """
        shuffle(self.__cards)

    def draw(self) -> Card:
        """デッキからカードを 1枚取り出す

        Returns:
            カードオブジェクトを 1つ返す

        Raises:
            IndexError: デッキが空

        """
        return self.__cards.pop()

    def sort(self, *, reverse: bool = False):
        """デッキのカードを並べ替える

        Args:
            reverse: 並べ替える順序(True=降順, False=昇順)
        """
        self.__cards.sort(reverse=reverse)

    @property
    def len(self) -> int:
        """残りカード枚数
        """
        return len(self.__cards)


class Hand:
    """"手札クラス

    文字列化すると手札を順番に並べた文字列になる

    Attributes:
        cards: 手札のリスト
        suits: 手札に含まれるスートの集合
        name: プレーヤーの名前

    """
    THolder = TypeVar('THolder', bound='Holder')

    def __init__(self, name: str = "") -> None:
        self._cards: list[Card] = []
        self.name: str = name
        self._holder = None

    def __str__(self) -> str:
        # 手札を文字列化する
        # return " ".join([str(c) for c in self.__cards])
        return " ".join(map(str, self._cards))

    def install_holder(self, holder: THolder):
        self._holder = holder

    def append(self, card: Card) -> None:
        """カードを 1枚追加する

        """
        self._cards.append(card)

    @property
    def cards(self) -> list[Card]:
        """手札のリスト
        """
        return self._cards

    @cards.setter
    def cards(self, new_cards: list[Card]):
        self._cards = new_cards
        if self._holder is not None:
            self._holder.cards = new_cards

    @property
    def nums(self) -> list[int]:
        """手札の強さのリスト

        手札の番号ではないことに注意。
        """
        return [card.strength for card in self._cards]

    @property
    def suits(self) -> set[Suit]:
        """手札に含まれるスートの集合
        """
        self.__suits = {card.suit for card in self._cards}
        return self.__suits

    def redraw(self):
        self._holder.redraw()
