# モジュールを利用して実際のゲームを行う（メインプログラム）
if __name__ == "__main__":
    # 直接実行されたときにだけ動作させる
    # この部分は import時には実行しない
    from card import Deck
    from poker import PokerCard, PokerHand

    # プレイヤー(手札の受け皿)を作る
    players = [PokerHand(str(i)) for i in range(1, 5+1)]

    # デッキを作ってシャッフルする
    dk = Deck(card_cls=PokerCard, joker=False)
    dk.shuffle()

    # 各プレーヤーに 1枚ずつ 5枚のカードを配る
    for player in players:
        for _ in range(5):
            player.append(dk.draw())

    # 各プレーヤーの手札と役を表示する
    for player in players:
        player.sort()
        print(player, end="  ")
        print(player.evaluate(), end=" ")
        # print(player.score, end=" ")
        print()

    '''
    # プレーヤーごとに交換する手札を聞き、取り除く
    for i, p in enumerate(players):
        s = input("Which would you change, player " + str(i+1))
        # delするとインデックスがずれるので降順で後ろから削除する
        for n in sorted(list(map(int, s.split(","))), reverse=True):
            del p.cards[n - 1]

    # プレーヤーごとに不足するカードをドローする
    for player in players:
        while len(player.cards) < 5:
            player.append(dk.draw())

    # 各プレーヤーの手札と役を表示する
    for player in players:
        player.sort()
        print(player, end="  ")
        print(player.evaluate(), end=" ")
        # print(player.score, end=" ")
        print()
    '''

    # スコアが最大のプレーヤ番号を得る
    sorted_players = sorted(players, reverse=True)
    if sorted_players[0] == sorted_players[1]:
        print("Draw")
    else:
        print("Player " + sorted_players[0].name + " wins!")
