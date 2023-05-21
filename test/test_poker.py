from poker import PokerCard, PokerHand
from card import Deck, Suit
from pytest import raises


class TestDeck:
    """Deckクラスのテスト
    """
    def setup_method(self):
        """セットアップ（何もしない）
        """
        pass

    def teardown_method(self):
        """後始末（何もしない）
        """
        pass

    def test_deck_creation_without_joker(self):
        """ジョーカーなしでデッキを作るとカードは 52枚
        """
        deck = Deck(card_cls=PokerCard, joker=False)
        assert deck.len == 52

    def test_deck_creation_with_joker(self):
        """ジョーカーありでデッキを作るとカードは 53枚
        """
        deck = Deck(card_cls=PokerCard, joker=True)
        assert deck.len == 53


class TestPokerScenario:
    """役判定のテスト
    """
    def setup_method(self):
        """セットアップ

            ２人分空の手札を用意する
        """
        self.hand1 = PokerHand()
        self.hand2 = PokerHand()

    def teardown_method(self):
        """後始末（何もしない）
        """
        pass

    def test_eval_hand1(self):
        """ワンペアのテスト
        """
        self.hand1.append(PokerCard(Suit.SPADE, 5))
        self.hand1.append(PokerCard(Suit.HEART, 5))
        self.hand1.append(PokerCard(Suit.CLUB, 1))
        self.hand1.append(PokerCard(Suit.SPADE, 13))
        self.hand1.append(PokerCard(Suit.SPADE, 12))
        assert self.hand1.evaluate() == "One pair"

    def test_eval_hand2(self):
        """スリーカードのテスト
        """
        self.hand1.append(PokerCard(Suit.SPADE, 5))
        self.hand1.append(PokerCard(Suit.DIAMOND, 5))
        self.hand1.append(PokerCard(Suit.CLUB, 5))
        self.hand1.append(PokerCard(Suit.SPADE, 13))
        self.hand1.append(PokerCard(Suit.SPADE, 12))
        assert self.hand1.evaluate() == "Three of a kind"

    def test_eval_hand3(self):
        """ロイヤルストレートフラッシュのテスト
        """
        self.hand1.append(PokerCard(Suit.SPADE, 10))
        self.hand1.append(PokerCard(Suit.SPADE, 1))
        self.hand1.append(PokerCard(Suit.SPADE, 11))
        self.hand1.append(PokerCard(Suit.SPADE, 13))
        self.hand1.append(PokerCard(Suit.SPADE, 12))
        assert self.hand1.evaluate() == "Royal straight flush"

    def test_eval_hand4(self):
        """フラッシュのテスト
        """
        self.hand1.append(PokerCard(Suit.SPADE, 5))
        self.hand1.append(PokerCard(Suit.SPADE, 7))
        self.hand1.append(PokerCard(Suit.SPADE, 11))
        self.hand1.append(PokerCard(Suit.SPADE, 13))
        self.hand1.append(PokerCard(Suit.SPADE, 12))
        assert self.hand1.evaluate() == "Flush"


class NewPokerHand(PokerHand):
    # PokerHandのサブクラス
    ...


class OtherClass:
    # PokerHandと継承関係にないクラス
    ...


class TestPokerHandComparator:
    """PokerHandクラスの比較メソッドのテスト
    同じ型同士、サブクラス間では比較可能
    """
    dk: Deck()

    def setup_method(self):
        # デッキを作ってシャッフルする
        self.dk = Deck(card_cls=PokerCard, joker=False)
        self.dk.shuffle()

    def test_comparator_1(self):
        """PokerHandクラス同士は比較可能
        """
        # プレイヤー(手札の受け皿)を作る
        player1 = PokerHand(str(1))
        player2 = PokerHand(str(2))

        try:
            player1 == player2
        except Exception:
            assert False

    def test_comparator_2(self):
        """サブクラスは比較不可
        """
        # プレイヤー(手札の受け皿)を作る
        player1 = PokerHand(str(1))
        player2 = NewPokerHand(str(2))

        with raises(NotImplementedError):
            player1 == player2

    def test_comparator_3(self):
        """継承関係にないクラスは比較不可
        """
        # プレイヤー(手札の受け皿)を作る
        player1 = PokerHand(str(1))

        with raises(NotImplementedError):
            player1 == 10

        with raises(NotImplementedError):
            player1 == 2.0

        with raises(NotImplementedError):
            player1 == "abc"

    def test_comparator_4(self):
        """継承関係にないクラスは比較不可
        """
        # プレイヤー(手札の受け皿)を作る
        player1 = PokerHand(str(1))
        player2 = OtherClass()

        with raises(NotImplementedError):
            player1 == player2
