---
title: JRA-VAN お試し期間（31日）の取得計画
date: 2026-11-13
status: 計画（未実行）
---

# JRA-VAN お試し期間（31日）の取得計画

> 一言で: JV-Link をインストールした日から 1 か月（依頼時の情報では 31 日）で、セットアップデータ全種別（1986 年〜）、時系列オッズ 0B41・0B42（直近 1 年を最優先に、取れる限り 2003 年 10 月まで）、開催日の速報（全券種オッズ・馬体重・天候馬場・変更情報）を取る。準備はインストール前に全部済ませる。最初に「お試し中の一括取得」が規約上許されるかを JRA-VAN に確かめ、だめなら 1 か月分（2,090 円）を払ってから同じ計画を実行する。

仕様の根拠は [JRA-VAN Data Lab.](./jra-van.md) にまとめた。ここでの [JVD]・[JVL]・[DG] などの略記もそのページと同じ。

## 前提と置き場所

- JV-Link は Windows の COM 部品なので、取得は Windows 側で行う。Windows 側の作業は Codex（Windows 上の AI エージェント）に任せる。この文書の「Windows で実行」の手順は、そのまま渡せる粒度で書く。
- 生データは Windows の E: ドライブ（NTFS、空き約 467GB、2026-11-13 確認）に置く。repo の `data/raw/jra-van/` にはコピーしない。

| 用途 | Windows のパス | WSL から |
|---|---|---|
| JV-Link の保存パス（JV-Link が `cache`・`data` を作る） | `E:\keiba-ai\jra-van\jvlink-data\` | `/mnt/e/keiba-ai/jra-van/jvlink-data/` |
| 取得スクリプトが書き出す生レコード | `E:\keiba-ai\jra-van\raw\<dataspec>\<年>.txt` など（下に詳細） | `/mnt/e/keiba-ai/jra-van/raw/` |
| ログ・進捗の状態ファイル・マニフェスト | `E:\keiba-ai\jra-van\logs\` | `/mnt/e/keiba-ai/jra-van/logs/` |
| SDK・仕様書の作業用コピー | `E:\keiba-ai\jra-van\sdk\`、`E:\keiba-ai\jra-van\specs\` | — |
| 取得スクリプトの実行用コピー | `E:\keiba-ai\jra-van\scripts\` | — |
| SDK・仕様書の原本（今の置き場所） | `\\wsl.localhost\Ubuntu\home\wogikaze\keiba-ai\data\raw\jra-van\sdk\`、`...\specs\` | `/home/wogikaze/keiba-ai/data/raw/jra-van/sdk/`、`.../specs/` |
| 加工後のテーブル（parquet など） | — | `/home/wogikaze/keiba-ai/data/processed/jra-van/` |

- WSL からは `/mnt/e/keiba-ai/jra-van/` を直接読む。repo から参照しやすいように、`data/raw/jra-van/e-drive` を `/mnt/e/keiba-ai/jra-van` へのシンボリックリンクにする。`data/raw/*` は `.gitignore` 済みなので、リンクも中身も git に入らない（2026-11-13 に `git check-ignore` で確認）。
- 取得スクリプトのソースは repo の `scripts/jravan/`（データを含まない。git 管理）に置き、実行するときに `E:\keiba-ai\jra-van\scripts\` へコピーする。`\\wsl.localhost` 上のパスから直接実行すると、タスクスケジューラや COM と相性が悪い可能性があるため（推測）。
- `E:\keiba-ai\jra-van\` の下は、`sdk`・`specs`・`scripts` を除いてすべて JRA-VAN 由来のデータで、解約したら消す（[JRA-VAN のページ](./jra-van.md)の「利用規約上の制約」）。

## 0. インストールより前に決めること: お試し中の一括取得

開発者コミュニティで、利用者がサポートデスクから「無料期間中におけるデータの一括取得は禁止」と回答されたと書いている（[topic 1230](https://developer.jra-van.jp/t/topic/1230)、2026-10-31）。公式スタッフはこの点に答えておらず、利用規約にもお試し中の一括取得を名指しで禁じる条文は見つからなかった。一方で公式の無料体験ページは「過去データを取得する」ことを案内している。

この計画はセットアップ全種別と時系列オッズの過去分をまとめて取るので、「一括取得」に当たる可能性がある。

- **JV-Link をインストールする前に**、JRA-VAN のお問い合わせ窓口に次を聞く: 「無料体験中に、JV-Link のセットアップ（option 3/4）で全データ種別を取得すること、時系列オッズ（0B41/0B42）を過去のレースについて JVRTOpen で順に取得することは、禁止される『一括取得』に当たりますか」。回答は日付つきでこのページに追記する。
- 当たるなら、お試しを使わずに最初の 1 か月を購入（2,090 円）し、契約期間中に同じ計画を実行する。日程（Day 0〜30）はそのまま使える。
- 当たらないなら、お試しで実行する。

## 1. Day 0 より前にやること（Windows で実行）

JV-Link をインストールした瞬間からお試し期間が始まる（公式の無料体験ページ「インストールしてから１か月間」）。インストール以外は全部先に済ませる。

### 1.1 フォルダと SDK のコピー

PowerShell で:

```powershell
$root = 'E:\keiba-ai\jra-van'
'jvlink-data','raw','logs','sdk','specs','scripts' | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $root $_) | Out-Null }
$src = '\\wsl.localhost\Ubuntu\home\wogikaze\keiba-ai\data\raw\jra-van'
Copy-Item -Recurse -Force "$src\sdk\*"   "$root\sdk\"
Copy-Item -Recurse -Force "$src\specs\*" "$root\specs\"
Get-ChildItem "$root\sdk" -Recurse -Filter 'JV-Link.exe' | Select-Object FullName, Length
```

- インストーラは `E:\keiba-ai\jra-van\sdk\JRA-VAN Data Lab. SDK Ver5.0.0_64bit\JV-Link\JV-Link.exe`（約 19MB）。**Day 0 まで実行しない。**
- 仕様書の PDF は `E:\keiba-ai\jra-van\sdk\JRA-VAN Data Lab. SDK Ver5.0.0_64bit\ドキュメント\`、テキスト化した版は `E:\keiba-ai\jra-van\specs\text\`。
- Python のサンプルは `...\サンプルプログラム\sample1_Python3.14\Form1.py`・`Form2.py`、レコードの構造体は `...\JV-Data構造体\Python版\JVData_Struct.py`。

### 1.2 Python 環境

- 64bit の Python 3.12 以上（SDK のサンプルは 3.14。SDK は 64bit 版なので 32bit の Python からは呼べない）。
- 例: `winget install astral-sh.uv` のあと、`E:\keiba-ai\jra-van\scripts\` で `uv venv --python 3.12` と `uv pip install pywin32`。
- COM の生成は `win32com.client.Dispatch("JVDTLab.JVLink")`（SDK の `Form1.py` と同じ）。インストール前は COM が登録されていないので失敗するのが正常。

### 1.3 Windows の設定

- スリープしない: `powercfg /change standby-timeout-ac 0`、`powercfg /change hibernate-timeout-ac 0`。
- Windows Update の再起動を、Day 0〜7 の間は止める（アクティブ時間の設定か一時停止）。
- 長時間の取得はタスクスケジューラから `cmd` で動かし、`python -u`、環境変数 `PYTHONIOENCODING=utf-8`、終了コードをログに残す。対話セッションの裏で走らせた取得が止まった報告がある（[crossclub_lab 2026](../literature/2026-crossclublab-jvlink-python.md) の失敗 6）。
- 利用キーは 1 台でしか使えない（同じキーを複数マシンで使うと -301）。取得はこの PC だけで行う。

### 1.4 取得スクリプトを書いて、偽の JV-Link で試す

インストール前は本物の JV-Link が無いので、JVOpen・JVStatus・JVRead・JVRTOpen・JVClose の戻り値を真似る偽オブジェクト（合成レコードを返す）で一通り動かしておく。[jvdata-store](https://github.com/ht-0328/jvdata-store) は同じ方法でテストしている。使えるならこのツール自体を使う選択肢もある（ライセンスと規約上の扱いは未確認）。

共通の作り:

- `JVInit("UNKNOWN")` を起動時に 1 回。
- 読み出しは **JVRead**（JVGets は pywin32 でメモリが漏れる報告がある）。返ってきた文字列を `cp932` でバイト列に戻し、末尾の `\r\n` と NUL を落としてから、1 行 1 レコードで追記する。固定長の位置はバイト単位なので、ファイルは cp932 のまま保存する。
- JVRead の戻り値で分岐: 正 → 書く、-1 → 次のファイル（続ける）、0 → 終わり、-3 → 1 秒待って再試行、-402/-403 → `JVFiledelete(filename)` して JVOpen からやり直し（3 回まで）、-502/-503 → JVClose して JVOpen からやり直し。
- JVOpen が -1 のとき、**「0 件で取得済み」と記録しない**。期間指定で -1 になる種別（DIFN など）がある。
- 1 単位（dataspec × 年、レース key など）が終わるたびに、マニフェストに 1 行（JSON Lines）追記する: dataspec、option、fromtime、readcount、downloadcount、lastfiletimestamp、レコード種別ごとの件数、飛ばした件数、戻り値、開始・終了時刻、出力ファイル名とバイト数・SHA-256。再開時はマニフェストを見て済んだ単位を飛ばす。
- 5 万件ごとに進捗をログに出す。

スクリプトは 4 本に分ける。

| スクリプト | 何をするか | 出力 |
|---|---|---|
| `jv_setup.py` | セットアップ（option 4）を dataspec × 年で回す。引数で dataspec・開始年・終了年 | `raw\<dataspec>\<年>.txt`（DIFN など期間指定できない種別は `raw\<dataspec>\all.txt`） |
| `jv_update.py` | 通常データ（option 1）の差分取得。前回の lastfiletimestamp を `logs\state_<dataspec>.json` に保存し、次の fromtime に使う | `raw\<dataspec>\update\<取得日時>.txt` |
| `jv_timeseries.py` | RA から JRA のレース key の一覧を作り、0B41・0B42 を 1 レースずつ JVRTOpen で取る。引数で期間。新しい年から古い年へ | `raw\0B41\<年>\<YYYYMMDDJJKKHHRR>.txt`、`raw\0B42\...` |
| `jv_realtime.py` | 開催日の速報を記録する。JVWatchEvent のイベントと定期取得 | `raw\realtime\<dataspec>\<YYYYMMDD>\<key>_<取得時刻>.txt` |

`jv_timeseries.py` のレース key は、RA の開催年・開催月日・競馬場コード・開催回・開催日目・レース番号をつないだ 16 桁（`YYYYMMDDJJKKHHRR`、[JVL] JVRTOpen, p.22）。地方・海外（データ区分 A/B、競馬場コード 01〜10 以外）は除く。

### 1.5 ディスクの見積もり

| 対象 | 見積もり | 根拠 |
|---|---|---|
| セットアップの生レコード | 25〜30GB | RACE 1999〜2026 年で 16.3GB（[crossclub_lab 2026](../literature/2026-crossclublab-jvlink-python.md)）に 1986〜1998 年と他の種別を足した概算 |
| JV-Link の保存パス（圧縮ファイル） | 未確認。生レコードと同程度以下と推測 | — |
| 0B41・0B42（2003 年 10 月〜） | 約 25GB | 1 レース約 0.3MB × 年 3,500 レース × 23 年（[JRA-VAN のページ](./jra-van.md)の「データ量と取得時間の目安」） |
| 開催日の速報記録（4〜5 週末） | 数 GB | O6 は 1 レコード 83KB。全券種を数分おきに取ると 1 日数百 MB（推測） |
| 合計 | 100GB 未満 | E: の空き約 467GB で足りる |

## 2. 日程

Day 0 は**月曜か火曜**にする。セットアップと時系列オッズの直近 1 年分を最初の週末までに終わらせ、週末は速報の記録に専念するため。どの曜日に始めても、31 日の中に週末は 4 回ある（5 回入ることもある）。

### Day 0（インストール日）

Windows で、上から順に:

1. `E:\keiba-ai\jra-van\sdk\JRA-VAN Data Lab. SDK Ver5.0.0_64bit\JV-Link\JV-Link.exe` を実行し、使用許諾に同意してインストールする（[DG] 3.2, p.14–17）。お試しの手続きとして JRA-VAN のサイトからダウンロードした JV-Link を使う必要があるかは未確認。必要ならそちらを使う。
2. スクリプトから `JVInit("UNKNOWN")` → `JVSetUIProperties()` を呼んでダイアログを出し、次を設定する（[JVL] p.11–13）:
   - 保存パス: `E:\keiba-ai\jra-van\jvlink-data`（フォルダが無いと JVOpen が -211 になる。1.1 で作成済み）
   - 保存フラグ: 保存する（2 回目以降の JVOpen でダウンロードを省ける）
   - 利用キー: 持っていれば入れる。お試し中に利用キーが要るかは未確認。JVOpen が -303 を返したら要る
   - 払戻ダイアログ: 表示しない（無人実行の邪魔になるため）

   ダイアログを使わない場合は `JVSetSavePath('E:\\keiba-ai\\jra-van\\jvlink-data')`、`JVSetSaveFlag(1)`、`JVSetServiceKey(...)` でも設定できる（[JVL] p.14–16）。
3. JVOpen が -305 を返したら、利用規約の同意画面で同意する（[JVL] コード表 p.55）。
4. 動作確認（各 1〜2 分）:
   - `JVOpen("RACE", <7日前の日時>, 1, ...)` → JVStatus で完了を待って JVRead → RA・SE が読めること。
   - 先週日曜の 1 レースについて `JVRTOpen("0B41", "<16桁key>")` → O1 が複数行返ること。**発表月日時分の間隔と行数を記録する**（刻みの確認。下のチェックリスト）。
   - 同じレースで 0B42 も。
5. セットアップの最初の 1 回（`jv_setup.py RACE 1986 1986`）を**画面の前で**実行し、スタートキットのダイアログが出たら「持っていない」を選ぶ（[JVL] p.20–21）。option 4 では 2 回目以降ダイアログが出ないはず（[JVL] p.18）だが、出た例がある（crossclub_lab）。出なくなったことを確かめてから無人実行に移る。

### Day 0〜2: セットアップ（全種別）

option 4、dataspec ごとに開く。期間指定できる種別は 1 年ずつ開く（1 回で開くファイル数が多いと極端に遅くなるため。crossclub_lab）。期間指定のときは、自分で決めた年の境目を次の開始にし、**最後の 1 回は終了時刻なしで開く**（[DG] p.23）。

| 順 | dataspec | 期間の切り方 | 対象 | 予想時間 | 備考 |
|---|---|---|---|---|---|
| 1 | RACE | 1986 年〜今年を 1 年ずつ（`19860101000000-19870101000000` …、最後は `20260101000000` で終了なし） | RA, SE, HR, H1, H6, O1〜O6, WF, JG | 1 時間未満（1999〜2026 年で 14 分の報告）＋ 1986〜1998 年分 | 本体。年ごとの件数をマニフェストで確認 |
| 2 | DIFN | 期間指定なし（`19860101000000`） | UM, KS, CH, BR, BN, RC, 地方・海外の RA/SE | 未確認 | 期間指定すると -1 になる |
| 3 | DIFF | 期間指定なし | 同上（旧形式） | 未確認 | DIFN で 1986 年からの全件が取れるか未確認なので両方取る |
| 4 | BLDN、BLOD | 期間指定なし | HN, SK, BT | 未確認 | 同上 |
| 5 | SNPN、SNAP | 2004 年〜を 1 年ずつ | CK | 未確認 | 出走時点の着度数。リークしない累積成績 |
| 6 | SLOP | 2003 年〜を 1 年ずつ | HC | 未確認 | — |
| 7 | WOOD | 2021 年〜（`20210701000000`） | WC | 短い | option 4 で -301 になったら option 1 で同じ fromtime（crossclub_lab の回避策） |
| 8 | MING | 2001 年〜を 1 年ずつ | DM, TM | 未確認 | — |
| 9 | YSCH | 2000 年〜 | YS | 短い | — |
| 10 | HOSN、HOSE | 期間指定なし | HS | 短い | 終了時刻を付けられない |
| 11 | HOYU | 期間指定なし | HY | 短い | 同上 |
| 12 | COMM | 期間指定なし | CS | 短い | 同上 |
| 13 | TOKU | option 1、fromtime を 1 年前に | TK | 短い | セットアップでは当週＋翌週しか取れない（[JVL] p.21） |

TCOV・RCOV・TCVN・RCVN は option 2（今週データ）専用で、過去分は無い。セットアップの後は不要（RA・SE・マスタで足りる）。

終わったら、セットアップで返った lastfiletimestamp を種別ごとに `logs\state_<dataspec>.json` に保存する。以降の差分取得（option 1）の起点になる（[DG] p.22–23）。

### Day 1〜6: 時系列オッズ 0B41・0B42 の過去分

1. **直近 1 年分を最優先**（保証期間。約 3,500 レース × 2 種別で 2〜4 時間）。
2. 次に、1 年前より古い年を新しい順に 1 年ずつ、2003 年 10 月 4 日まで。1 年あたり 2〜4 時間、23 年で 2〜4 日の連続実行（jvdata-store の 1 回約 1 秒からの見積もり）。
3. 年ごとに「取れたレース数 / RA のレース数」をマニフェストに残す。取れなくなった年で止める（-1 が続いたら、その年の数レースを手で確かめてから打ち切る）。
4. 同じ key を何度も開かない（同じ key の 2 回目以降に古い版が返る報告がある。jrvltsql #288）。終わったレースを 1 回だけ開く。

週末の開催日は、速報の記録とぶつからないように止める（JV-Link は 1 つの Open しか同時に扱えない。前の Open を JVClose しないと -202）。

### 週末（4〜5 回）: 速報の記録

時系列オッズが無いワイド・馬単・3連複・3連単の発走前オッズと、発走前の馬体重・天候馬場・変更情報は、**その場で記録しないと残らない**（保持 1 週間）。`jv_realtime.py` をタスクスケジューラで、金曜 19:00〜（PAT の金曜発売があるとき）と土日の 8:00〜17:30 に動かす。

| 何を | dataspec | いつ・どの頻度 | key |
|---|---|---|---|
| 出走表・確定成績 | 0B15 | 金・土の夕方と開催日の朝に 1 回 | `YYYYMMDD` |
| 天候馬場・取消除外・騎手変更・発走時刻変更・コース変更 | 0B14 | 開催日 5 分おき。**毎回前回分を捨てて全体を取り直す**（取り消された変更は消えるため。[JVD]「データ提供タイミング･提供単位」※1） | `YYYYMMDD` |
| 同上（イベント） | 0B16 | JVWatchEvent のイベントごと | イベントの引数 |
| 馬体重 | 0B11 | 馬体重発表のイベントごと（発走約 1 時間前） | イベントの引数 |
| 全券種オッズ | 0B30 または 0B31〜0B36 | 各レースの発走 60 分前から 5 分おき、15 分前から 1 分おき（仮）。取得時刻を必ず付ける | レースの 16 桁 key |
| 票数 | 0B20 | 前日売最終の後に 1 回、確定後に 1 回 | レース key |
| 払戻確定 | 0B12 | 払戻確定のイベントごと | イベントの引数 |
| マイニング予想 | 0B13, 0B17 | 前日・当日・直前の発表後 | `YYYYMMDD` |
| WIN5 | 0B51 | 開催日に 2 回 | 未確認 |
| 当日分の時系列オッズ | 0B41, 0B42 | **全レース終了後（19:00 以降か翌朝）に 1 回だけ** | レース key |

**1 回目の週末は試運転**にして、次を確かめる（jrvltsql #288 の問題の確認）。

- 同じレース key で 0B31 を 5 分おきに開いたとき、版（発表月日時分）が進むか。
- 夜に取った 0B41 の版の一覧と、日中に取った 0B31 の版を突き合わせる。
- 版が進まないときは、JVFiledelete で保存済みファイルを消してから開く、保存フラグを 0 にする、の 2 つを試す（#288 で提案されているが未検証の案）。どれも効かなければ、ワイド・馬単・3連系の発走前オッズの記録はあきらめ、単複・馬連は夜の 0B41・0B42 だけで済ませる。

### 毎週月曜・木曜の夜: 差分取得

`jv_update.py` で option 1 の差分を取る。対象は RACE、DIFN、BLDN、SNPN、SLOP、WOOD、YSCH、HOSN、HOYU、MING、COMM、TOKU。月曜 14:00 頃に確定成績、木曜 20:00 頃に出走馬名表とマスタの差分が出る（[JVD]「データ提供タイミング･提供単位」）。速報の記録と時間が重ならないようにする。

### Day 7〜24: WSL 側での確認と、足りない分の取り直し

WSL で `/mnt/e/keiba-ai/jra-van/` を読み、下のチェックリストを埋める。欠けが見つかったら、まだ期間内のうちに取り直す。

```sh
ln -s /mnt/e/keiba-ai/jra-van /home/wogikaze/keiba-ai/data/raw/jra-van/e-drive
```

- `/mnt/e` は WSL から読むと遅いので、パースした結果は `data/processed/jra-van/` に parquet で置く。パーサは `src/keiba_ai/` に置き、`JVData_Struct.py` と [JVD]「フォーマット」でオフセットを確かめる。
- `data_version` は、マニフェスト（`logs\manifest.jsonl`）のハッシュと取得日で決める。

### Day 25〜30: 判断と後始末

下の「契約を続けるかの判断」で決める。解約するなら、お試し（または契約）の終了後に削除する。

## 3. お試し期間中のチェックリスト

| # | 確認すること | いつ | 結果 |
|---|---|---|---|
| 1 | お試し中のセットアップ・時系列オッズ過去分の取得が「一括取得」に当たらないか（JRA-VAN に問い合わせ） | インストール前 | |
| 2 | お試し中に利用キーが要るか、JVOpen の戻り値 | Day 0 | |
| 3 | option 4 でダイアログが 2 回目以降出ないか | Day 0 | |
| 4 | 0B41 の発表月日時分の間隔（何分刻みか、締切前に細かくなるか）と 1 レースあたりの版数 | Day 0 | |
| 5 | 0B41・0B42 が何年前まで取れたか（年ごとの取得率） | Day 1〜6 | |
| 6 | 年ごとのレース数（RA、データ区分 7）が平年並み（年約 3,450 レース）か。SE の件数、RA と SE のキーの整合 | Day 2〜 | |
| 7 | 1 年ずつ開いた合計件数と、まとめて開いた件数の差（crossclub_lab は 348 ファイルの差が未解決） | Day 2〜 | |
| 8 | DIFN と DIFF、BLDN と BLOD、SNPN と SNAP の件数と期間の違い | Day 2〜 | |
| 9 | O1 の確定オッズと SE の単勝オッズ、HR の単勝払戻が一致するか | Day 7〜 | |
| 10 | 0B41 の最終版と O1 の確定オッズの関係（最終版が確定と一致するか） | Day 7〜 | |
| 11 | 同じ key の JVRTOpen で版が進むか（jrvltsql #288） | 1 回目の週末 | |
| 12 | JVWatchEvent のイベントが Python で受けられるか（[DGPy]） | 1 回目の週末 | |
| 13 | 0B14 の取り直しで、取り消された変更が消えることの確認 | 週末 | |
| 14 | JV-Link 保存パスの容量と、生レコードの容量 | Day 2、Day 25 | |
| 15 | 集計値（回収率など）を公開リポジトリに載せることが投稿ガイドライン上問題ないか | 期間中 | |

## 4. 契約を続けるかの判断

前提として、**解約したら保存データ・コピー・学習データを消す必要がある**（公式スタッフ回答、[topic 1230](https://developer.jra-van.jp/t/topic/1230)、2026-11-08）。お試しで取ったデータを使い続けるには、契約を続けるしかない。

続ける（月 2,090 円）条件。どれか 1 つでも当てはまれば続ける:

- keiba-ai の実験で JRA-VAN のデータを使い続ける（主データ源にする予定なので、基本はこれに当たる）。
- ワイド・馬単・3連系の発走前オッズを研究に使いたい。過去分はどこにも無く、毎週末記録し続けるしかない。
- 0B41・0B42 の 1 年より前の分が取れた。解約すると消すことになり、次に取り直せる保証は無い。

やめる条件:

- チェックリストの 5・6・9 で、データの欠けや不整合が大きく、研究に使えないと分かった。
- 別のデータ源に切り替えると決めた（[データ源](./index.md)）。

やめる場合の後始末:

1. Windows で `E:\keiba-ai\jra-van\jvlink-data\`、`raw\`、`logs\`（レコードを含むもの）を消す。
2. WSL で `data/processed/jra-van/` と、JRA-VAN 由来の中間ファイル・特徴量・学習データを消す。`data/raw/jra-van/e-drive` のリンクも消す。
3. 学習済みモデルなど元データを復元できない作成物は、公開しない前提で残してよい（公式回答の範囲。モデルが該当するかは明示されていないので、残すなら JRA-VAN に確認する）。
4. JV-Link はアンインストールしてよい（必須ではない）。
5. 削除した日と対象を、このページに追記する。

## 関連

- [JRA-VAN Data Lab.](./jra-van.md) — 仕様の要約、時系列オッズ、リーク表。
- [crossclub_lab 2026](../literature/2026-crossclublab-jvlink-python.md) — 無人実行の失敗と対策 8 つ。取得スクリプトはこれを前提に書く。
- [jvdata-store](https://github.com/ht-0328/jvdata-store) — JV-Link からの取得・時系列オッズの取り込みを実装した Python ツール。
