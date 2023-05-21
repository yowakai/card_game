def key_down(e):
    key = e.keysym
    if key in '12345':
        n = int(key)-1
        players[1].cards[n].is_open = not players[1].cards[n].is_open


# モジュールを利用して実際のゲームを行う（メインプログラム）
if __name__ == "__main__":
    # 直接実行されたときにだけ動作させる
    # この部分は import時には実行しない
    from card import Deck
    from poker import PokerCard, PokerHand, PokerBoard
    from tkinter import Tk, Canvas

    # ルートウィンドウを作る
    root = Tk()
    root.title("The Poker")
    root.resizable(False, False)
    root.bind("<KeyPress>", key_down)
    # root.bind("<KeyRelease>", key_up)
    cvs = Canvas(root, width=800, height=640)
    cvs.pack()

    # ゲームボード(盤面)を作る
    board = PokerBoard(cvs, cls=PokerCard)

    # プレイヤー(手札の受け皿)を作る
    players = [PokerHand(str(i)) for i in range(1, 2+1)]

    # プレーヤーに自身の表示領域を設定する
    for n, holder in enumerate(board.holders):
        holder.cards = players[n].cards
        players[n].install_holder(holder)

    # デッキを作ってシャッフルする
    dk = Deck(card_cls=PokerCard, joker=False)
    dk.shuffle()

    # 各プレーヤーに 1枚ずつ 5枚のカードを配る
    for player in players:
        for _ in range(5):
            c = dk.draw()
            player.append(c)

    # 各プレーヤーの手札と役を表示する
    for player in players:
        player.sort()
        print(player, end="  ")
        print(player.evaluate(), end=" ")
        # print(player.score, end=" ")
        print()
        player.redraw()

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

    root.mainloop()
