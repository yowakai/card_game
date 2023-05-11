# card_game
トランプを使ったゲームのサンプルです。ポーカーの手役を判定するロジックのサンプルプログラムですが、遊ぶことはできません。

# Prerequisite
- python 3.10以上推奨
- 自動テストを試すには自動テストモジュールが必要(pytest推奨)

# 実行例
src/game.pyを右クリックして「ターミナルでPythonファイルを実行します」を選びます。
```
PS C:\card_game> python c:/card_game/src/game.py
♥-K ♣-K ♥-7 ♣-J ♠-Q  One pair 
♣-2 ♥-3 ♠-6 ♥-10 ♠-K  No pair 
♥-A ♣-3 ♥-5 ♠-7 ♣-9  No pair 
♦-A ♠-5 ♣-7 ♠-J ♥-Q  No pair 
♠-A ♥-2 ♠-4 ♥-6 ♥-J  No pair
Player 1 wins!
PS C:\card_game>
```

# 注意事項
クローン直後に実行する前には、以下が必要になる場合があります。
- 必要な拡張機能のインストール
- pythonインタプリタの選択

# フォルダ構成
```
CARD_GAME
  + src     // ソースディレクトリ
  + test    // テストディレクトリ
```

# Modules
## card.py
トランプの基本機能を実装したモジュールです。

### card.Suitクラス
トランプのスートを扱う列挙型です。

### card.Cardクラス
トランプ 1枚を表すクラスです。

### card.Deckクラス
トランプ 1組(1デッキ)を表すクラスです。

## poker.py
ポーカーのルールを実装したモジュールです。

## game.py
ゲームを実行するモジュールです。
