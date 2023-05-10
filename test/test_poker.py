from poker import PokerCard, PokerHand
from card import Deck, Suit


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
