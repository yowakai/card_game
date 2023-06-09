from enum import IntEnum, auto
from collections import Counter
# from functools import reduce
from typing import TypeVar, Callable, NamedTuple, Any
from card import Card, Hand


class PokerCard(Card):
    """ポーカー用カード

    Cardクラスとの違いはカードの強さが以下のようになることである
        * スートを考慮しない
        * Aが最強(14)となる

    Attributes:
        strength: カードの強さ

    """
    @property
    def strength(self) -> int:
        # ポーカー固有のカードの強さ
        # Aが最強(14)、以下 K, Q, J, 10 ... 2
        # スートは無視する
        return 14 if self.number == 1 else self.number


class PokerHandEnum(IntEnum):
    """ポーカーの役を表す列挙型

    大小比較により役の強弱を判定できる
    """
    # 役を表す列挙型
    NO_PAIR = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_STRAIGHT_FLUSH = auto()


class Evaluator(NamedTuple):
    # 1つの役を判定する判定器をまとめた名前付きタプル
    #   tester(self) -> bool
    #       手札がチェックする役になっているか(true: なっている, false: なっていない)
    #   major(self) -> int
    #       役の強さを示す数値を返す関数
    #   minor(self) -> int
    #       同じ役の時の強弱を示す数値を返す関数
    #   name: str
    #       役名
    # 3.11以降では NamedTupleと Generic[T]が併用できるようになった
    # 互換性のため Anyで妥協する
    tester: Callable[[Any], bool]
    major: Callable[[Any], int]
    minor: Callable[[Any], int]
    name: str


class PokerHand(Hand):
    """ポーカー専用の手札

    比較により手札同士の強弱を判定可能
    """
    Self = TypeVar('Self', bound='PokerHand')

    def __init__(self, *args):
        super().__init__(*args)
        self.major: int
        self.minor: int

    # デコレータ
    @staticmethod
    def comparator(func: Callable[[Self, Self], bool]) \
            -> Callable[[Self, Self], bool]:
        # 比較演算用型チェックデコレータ
        # selfと otherの型が異なる場合、TypeErrorを上げる
        # なぜか型ヒントが書けないのでしかたなくデコレータで実装
        def _comparator(self, other) -> bool:
            if not isinstance(other, type(self)):
                raise TypeError
            v = func(self, other)
            return v
        return _comparator

    @comparator
    def __gt__(self: Self, other: Self) -> bool:
        return self.__score > other.__score

    @comparator
    def __eq__(self: Self, other: Self) -> bool:
        return self.__score == other.__score

    def sort(self) -> None:
        """カードを並べ替える

        枚数が多い番号のものが前に、番号が小さいものが前に来るよう並べ替える
        """
        # カードの強さのリストを作る
        nums = [c.strength for c in self.cards]
        # (強さが同じ枚数, カードそのもの)というタプルのリストを作る
        ordered_tuple = list(zip(
            [nums.count(c.strength) for c in self.cards],
            self.cards
            ))
        # 上記のタプルを (枚数, 番号の逆順) の降順に並べ替える
        # これにより枚数が多いカードが先に、番号が小さいものが先に並ぶ
        ordered_tuple.sort(key=lambda t: (t[0], 14 - t[1].number),
                           reverse=True)
        # 親クラスのカードリストを置き換える
        # 本来 privateなので直接操作できないが難読化した名前でアクセスしている
        self._Hand__cards = [t[1] for t in ordered_tuple]

    def __pre_evaluate(self) -> None:
        # 同じ番号の手札を数える
        # __c: (枚数, カードの強さ)の順に降順に並べたリスト
        # __g: 枚数だけを降順に並べたリスト、ペア系の役の判定に使う
        # __an: 最も弱い強さが 0になるよう調整したリスト(adjusted number)
        nums = [card.strength for card in self.cards]
        self.__c = sorted(Counter(nums).most_common(),
                          key=lambda t: (t[1], t[0]),
                          reverse=True)
        self.__g = list(Counter(nums).values())
        self.__g.sort(reverse=True)
        nums.sort()
        self.__an = [x - min(nums) for x in nums]

    def __calc_minor(self) -> int:
        # 手札が同じ役の時の強弱を計算する
        result = 0
        for strength, _ in self.__c:
            result = result * 100 + strength
        return result
        # return reduce(lambda a, b: a * 100 + b, [c[0] for c in self.__c])

    # -------------------------------------------------------
    # 役の判定器
    # -------------------------------------------------------
    def __is_onepair(self) -> bool:
        return self.__g == [2, 1, 1, 1]

    def __is_twopairs(self) -> bool:
        return self.__g == [2, 2, 1]

    def __is_threecards(self) -> bool:
        return self.__g == [3, 1, 1]

    def __is_fullhouse(self) -> bool:
        return self.__g == [3, 2]

    def __is_fourcards(self) -> bool:
        return self.__g == [4, 1]

    def __is_flush(self) -> bool:
        return len(self.suits) == 1

    def __is_straight(self) -> bool:
        return self.__an == [0, 1, 2, 3, 4]

    def __is_straightflush(self) -> bool:
        return self.__is_flush() and self.__is_straight()

    def __is_royalstraightflush(self) -> bool:
        # 枚数、番号(強さ)順に並べたリストの番号が Aだったら
        return self.__c[0][0] == 14 and self.__is_straightflush()

    # ------------------------------------------------------------
    # 役の評価
    # ------------------------------------------------------------
    # Evaluatorクラスを使ってすべての役の判定器を優先度順にまとめる
    __EVALUATORS = [
        Evaluator(__is_royalstraightflush,
                  lambda _: PokerHandEnum.ROYAL_STRAIGHT_FLUSH,
                  __calc_minor,
                  "Royal straight flush"),
        Evaluator(__is_straightflush,
                  lambda _: PokerHandEnum.STRAIGHT_FLUSH,
                  __calc_minor,
                  "Straight flush"),
        Evaluator(__is_fourcards,
                  lambda _: PokerHandEnum.FOUR_OF_A_KIND,
                  __calc_minor,
                  "Four of a kind"),
        Evaluator(__is_fullhouse,
                  lambda _: PokerHandEnum.FULL_HOUSE,
                  __calc_minor,
                  "Full house"),
        Evaluator(__is_flush,
                  lambda _: PokerHandEnum.FLUSH,
                  __calc_minor,
                  "Flush"),
        Evaluator(__is_straight,
                  lambda _: PokerHandEnum.STRAIGHT,
                  __calc_minor,
                  "Straight"),
        Evaluator(__is_threecards,
                  lambda _: PokerHandEnum.THREE_OF_A_KIND,
                  __calc_minor,
                  "Three of a kind"),
        Evaluator(__is_twopairs,
                  lambda _: PokerHandEnum.TWO_PAIR,
                  __calc_minor,
                  "Two pairs"),
        Evaluator(__is_onepair,
                  lambda _: PokerHandEnum.ONE_PAIR,
                  __calc_minor,
                  "One pair"),
        # 判定器が常に Trueを返すので必ず適用される
        Evaluator(lambda _: True,
                  lambda _: PokerHandEnum.NO_PAIR,
                  __calc_minor,
                  "No pair")
    ]

    def evaluate(self) -> str:
        """手札を評価する

            Returns:
                役の文字列
        """
        self.__pre_evaluate()

        for e in PokerHand.__EVALUATORS:
            if e.tester(self):
                self.major = e.major(self)
                self.minor = e.minor(self)
                return e.name

        return "Can't evaluate."

        """旧実装
        if self.is_royalstraightflush():
            self.major = PokerHandEnum.ROYAL_STRAIGHT_FLUSH
            return "Royal straight flush"
        if self.is_straightflush():
            self.major = PokerHandEnum.STRAIGHT_FLUSH
            return "Straight flush"
        if self.is_fourcards():
            self.major = PokerHandEnum.FOUR_OF_A_KIND
            return "Four of a kind"
        if self.is_fullhouse():
            self.major = PokerHandEnum.FULL_HOUSE
            return "Full house"
        if self.is_flush():
            self.major = PokerHandEnum.FLUSH
            return "flush"
        if self.is_straight():
            self.major = PokerHandEnum.STRAIGHT
            return "Straight"
        if self.is_threecards():
            self.major = PokerHandEnum.THREE_OF_A_KIND
            return "Three cards"
        if self.is_twopairs():
            self.major = PokerHandEnum.TWO_PAIR
            return "Two pairs"
        if self.is_onepair():
            self.major = PokerHandEnum.ONE_PAIR
            return "One pair"
        self.major = PokerHandEnum.NO_PAIR
        self.minor = self.__calc_minor()
        return "No pair"
        """

    @property
    def __score(self) -> int:
        self.evaluate()
        return self.major * 1_00_00_00_00_00 + self.minor
