---
title: Alternative methods of predicting competitive events: An application in horserace betting markets
authors: Lessmann Stefan, Sung Ming-Chien, Johnson Johnnie E.V.
year: 2010
venue: International Journal of Forecasting 26(3) 518-536
url: https://ideas.repec.org/a/eee/intfor/v26yi3p518-536.html
doi: 10.1016/j.ijforecast.2009.12.013
topic: machine-learning
tags: random-forest, conditional-logit, hong-kong, kelly, ndcg, competitive-events
verified: abstract
importance: high
source: unavailable
source_version: none
---

# 競争構造に合わせて改造したランダムフォレストで勝率を推定（IJF 2010）

> 一言で: SVM 系の二段階モデル（[Lessmann 2009](./2009-lessmann-svm-classification-horserace.md)）の後継として、Breiman (2001) のランダムフォレストを「出走馬同士の競争」を扱えるように改造し、従来の統計手法より大きな賭けの利益が出たと報告する。

**原本未取得。** Elsevier は有料。Southampton ePrints（55125）の PDF は職員限定（取得時 401）、academia.edu はログインが必要で、他の無料版は見つからなかった。以下は IDEAS/RePEc の要旨・キーワード・参考文献一覧と、全文取得済みの他論文の記述に基づく。手法の詳細と数値は未確認。

## 要旨から分かること

- 問題設定: 選挙やスポーツのような競争的イベントでは、参加者の勝率は自分の能力だけでなく相手の能力にも依存する。標準的な回帰・分類の枠組みはこの「競争の要素」を扱えない。
- 方法: Breiman (2001) のランダムフォレスト分類器を、競馬の結果予測に合うよう改造する方法論を示す。
- 結果: 複数の実験で、予測から相当な賭けの利益が得られ、従来の統計手法を上回った。
- キーワード: Probability forecasting, Classification, Random forest, Sports forecasting。
- IDEAS の参考文献一覧には Bolton & Chapman (1986)、Edelman (2007)、Lessmann ら (2007, 2009)、Leitch & Tanner (1991、利益による予測評価) が含まれる。

## 二次資料が伝えること（未確認）

- [Galekwa 2024](./2024-galekwa-systematic-review-ml-sports-betting.md) のレビューは、香港の1,000レース（12,902頭）を使い、条件付きロジットや SVM より高い収益性と精度を示し、Kelly 方式の賭けで有意な利益が出たと要約する（同原本 p.33）。同レビューの表は NDCG を指標に挙げるが、どの研究の指標かが混ざっている可能性がある。香港データという点も、前作までの Goodwood データと違うので、原本での確認が必要。
- [Nakakita 2023](./2023-nakakita-hierarchical-bayes-horse-jockey.md) はランダムフォレストで勝ち馬を予測した研究として引く（同原本 p.4）。
- [Hubacek 2020](./2020-hubacek-beating-market-bad-model.md) は、本論文を「収益性と予測精度を混同している」研究の例の一つとして引いている（同原本 p.30, 文献[39]）。どの点を指しているかは本文で特定されていない。
- 後続の [Lessmann 2012](./2012-lessmann-stacking-competitive-event.md) の検索結果要約では、SVM をやめた理由の一つとして、SVM 系モデルの計算量が大きく、競馬の大きなデータを扱いにくいことが挙げられている（未確認）。

## 批判的に読む（未確認点）

- 「改造」の中身（レース内標準化した特徴量か、レース単位の抽出か、第2段の条件付きロジットか）は原本で確認が必要。前作の流れからすると二段階構成（RF の出力を市場確率と条件付きロジットで結合）が自然だが、推測にすぎない。
- 回収率の算出方法、評価期間の分割、レース数、統計的検定の有無は未確認。
- Hubacek らの批判が指す点（精度と利益の混同）は、keiba-ai で回収率を主張するときに避けるべき論点として意識しておく。

## keiba-ai での使い方

- **木系モデルとレース内相対化**: LightGBM を馬単位の独立分類として使うと、同じレースの他馬が見えない。レース内標準化特徴量（[Lessmann 2009](./2009-lessmann-svm-classification-horserace.md)）と、出力をレース内 softmax／条件付きロジットにかける第2段を組み合わせるのが基本形。
- **実験案**: LightGBM の binary 目的とレース内 softmax（lambdarank・独自の多クラス）を比べ、第2段の後の対数損失と回収率がどう変わるかを見る。本論文の主張（競争構造の考慮が効く）が JRA データで再現するかの検証になる。
- 原本未取得なので、設計の根拠として引くときは「要旨レベルの主張」として扱う。

## 関連ノート

- [Lessmann 2009](./2009-lessmann-svm-classification-horserace.md): 直前の SVM/CL。本論文の比較対象と思われる。
- [Lessmann 2007](./2007-lessmann-ls-svr-horserace-ndcg.md): LS-SVR と NDCG。
- [Lessmann 2012](./2012-lessmann-stacking-competitive-event.md): 本論文の後の、多数モデルの生成と結合。
- [Edelman 2007](./2007-edelman-svm-horserace-odds.md): 二段階モデルに機械学習を入れた先行研究。
- [Bolton 1986](./1986-bolton-conditional-logit.md): 条件付きロジット。
- [Hubacek 2020](./2020-hubacek-beating-market-bad-model.md): 本論文を精度と利益の混同の例に挙げる批判。
- [Galekwa 2024](./2024-galekwa-systematic-review-ml-sports-betting.md): 本論文のデータを香港と要約するレビュー。

## 検索語

ランダムフォレスト, 決定木アンサンブル, 競争的イベント, 出走馬間の競争, 勝率推定, 確率予測, 条件付きロジット, 二段階モデル, Kelly 基準, 香港競馬, random forest, competitive events, probability forecasting, sports forecasting, within-race competition, International Journal of Forecasting
