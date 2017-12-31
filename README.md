# lovelive-wordcloud
ラブライブの歌詞からワードクラウドを作成するプログラムです。

## はじめに
多分使う人はいないと思ってるので適当に書きます。
使いたいけどよくわからないという場合には [@darsein](https://twitter.com/darsein) に直接連絡してください。
問い合わせに返答するととも、併せてこの README を更新します。

## 準備
python: 3.6.3 での動作を確認しています。
beautiful soup: [PythonとBeautiful Soupでスクレイピング](https://qiita.com/itkr/items/513318a9b5b92bd56185)を参考にしてインストールしてください。
mecab, wordcloud: [Word Cloudで文章の単語出現頻度を可視化する。](https://qiita.com/kenmatsu4/items/9b6ac74f831443d29074)を参考にしてインストールしてください。

## 使い方
とりあえず `run.sh` を動かすと全楽曲に基づくワードクラウドが `word_clouds/test.png` として作成されます。

  sh run.sh

この中を見ればどういう流れで使えばいいのかわかるかと思いますが、
一度 `run.sh` を実行した後は曲データを更新しない限りは `word_cloud.py` を実行するだけで大丈夫です。

word_cloud.py の実行例は以下の通りです。

  python word_cloud.py -t [出力画像の名前] -n -b [ベースにする歌詞のグループ] -d [ベースにする歌詞のグループ]

- `-n` オプションをつけると1楽曲に複数回現れる単語も1回の出現と数えます。
- `-b` オプションをつけると、指定したグループの歌詞の頻度に基づいてワードクラウドを作ります。
- `-d` オプションをつけると、指定したグループの単語頻度に楽曲数補正を掛けて、`-b` オプションで指定したグループの単語頻度から引きます。

僕たちはひとつの光のワードクラウドは

  python word_cloud_bokuhika.py

すればできます。
