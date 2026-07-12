# CORPUS SHREDDER (Max / FluCoMa)

[English](#english) | [日本語](#日本語)

---

## English

A corpus (concatenative) system reproducing the core of SOUND SHREDDER in Max + FluCoMa.
Slice a sound → features → a 2D timbre map → click to audition. Adds **k-means cluster coloring** on top.

### Files
- `corpus_shredder.maxpat` … the main patch (based on FluCoMa's official corpus-explorer, with k-means coloring + a presentation UI added).
- `build_corpus_shredder.py` … the script that generates it (injects the coloring layer + lays out Presentation Mode in one pass).
- `inject_kmeans.py` … old version (coloring only; now merged into the build script).
- `maxctl.py` … (reference) a client that sends commands directly to the Max MCP socket.io server.

### Presentation mode
It launches in **Presentation Mode** automatically, showing just the control UI (Cmd+E, or the bottom-right icon, to enter patching mode).
- Left column: ① AUDIO ON (ezdac~) / ② ANALYZE (bang) / CLUSTERS (k) / GAIN / folder drop.
- Center–right: the 2D timbre map (color = k-means cluster). Click & drag to audition nearby slices.

### Requirements
- Max 8 or 9.
- The **FluCoMa** (Fluid Corpus Manipulation) package … installed.
- Bundled sounds like `Nicol-LoopE-M.wav` are found automatically from FluCoMa's media folder (search path).

### Usage
1. Open `corpus_shredder.maxpat` in Max.
2. Turn on **audio on** (①, bottom-right).
3. Click **click here** (③, the bang, top-left) → slice → MFCC features → normalize → UMAP 2D → point cloud in the plotter.
   - At the same time **k-means runs and auto-colors the points per cluster** (visualizing kick/snare/hat-like grouping).
4. **Click & drag** the plotter (④) → audition nearby slices (kdtree → play~).
5. To change the cluster count → the right-side **number box → `numclusters $1`** (applied on the next click here).
6. For another sound → drop a folder onto "Drag a folder containing valid AIFF/WAV files here", or swap the `buffer~ sound` filename (e.g. `Tremblay-BeatRemember.wav` for drums).

### Pipeline
| Function | FluCoMa |
|---|---|
| Slice | `fluid.bufonsetslice~ @metric 9 @threshold 0.01` |
| Features | `fluid.bufmfcc~` → `fluid.bufstats~` → `fluid.bufflatten~` → `fluid.dataset~ analysis` |
| Normalize | `fluid.normalize~` → `fluid.dataset~ normalised` |
| 2D projection | `fluid.umap~ @numdimensions 2` → `fluid.dataset~ reduction` |
| Nearest / audition | `fluid.kdtree~` → `play~ sound` |
| **Coloring (added)** | `fluid.kmeans~ @numclusters 4` → `fitpredict normalised clusters` → `fluid.labelset~ clusters` → plotter 2nd inlet |

### Notes
- If the Max 9 trial has expired you **can't save** (it still runs). The `.maxpat` in this repo is the master.
- The coloring layer is injected following the canonical wiring in FluCoMa's plotter help. The base core ①–④ is verified on-device up to the point cloud. **The coloring's rendering is not yet verified on-device** (open and click here to check).

### Not implemented (optional next steps)
- A beat-generation sequencer (pick slices from clusters, sequence steps).
- pfft~ spectral-morph integration (see `~/dev/max-spectral-morph`).

---

## 日本語

SOUND SHREDDER の中核を Max + FluCoMa で再現したコーパス（concatenative）システム。
音源をスライス→特徴量→2D音色マップ→クリックで試聴。さらに **k-means クラスタ色分け** を追加。

## ファイル
- `corpus_shredder.maxpat` … 本体（FluCoMa公式 corpus-explorer をベースに k-means色分け＋プレゼンUIを付与）
- `build_corpus_shredder.py` … 上記を生成するスクリプト（色分け層の注入＋Presentation Mode配置を一括）
- `inject_kmeans.py` … 旧版（色分けのみ。build スクリプトに統合済み）
- `maxctl.py` … （参考）Max MCP の socket.io サーバへ直接コマンドを送るクライアント

## プレゼンテーションモード
開くと自動で **Presentation Mode** で起動し、操作UIだけが並びます（編集したい時は Cmd+E / 右下のアイコンでパッチングモードへ）。
- 左列: ①AUDIO ON(ezdac~) / ②ANALYZE(bang) / CLUSTERS(k数) / GAIN / フォルダドロップ
- 中央〜右: 2D音色マップ（色=k-meansクラスタ）。クリック&ドラッグで近傍スライスを試聴

## 必要環境
- Max 8 または 9
- **FluCoMa**（Fluid Corpus Manipulation）パッケージ … インストール済み
- バンドル音源 `Nicol-LoopE-M.wav` 等は FluCoMa の media フォルダ（検索パス）から自動で見つかる

## 使い方
1. `corpus_shredder.maxpat` を Max で開く
2. 右下の **audio on**（①）をオン
3. 左上の **click here**（③ のbang）をクリック → スライス→MFCC特徴量→正規化→UMAP 2D→plotterに点群表示
   - 同時に **k-means が走り、クラスタごとに点が自動で色分け**される（kick/snare/hat 的なグルーピングの可視化）
4. plotter（④）を **クリック&ドラッグ** → 近傍スライスを試聴（kdtree→play~）
5. クラスタ数を変えたい → 右側の **number box → `numclusters $1`**（次回 click here で反映）
6. 別音源 → 「Drag a folder containing valid AIFF/WAV files here」にフォルダをドロップ、または
   `buffer~ sound` のファイル名を差し替え（例 `Tremblay-BeatRemember.wav` でドラム）

## パイプライン
| 機能 | FluCoMa |
|---|---|
| スライス | `fluid.bufonsetslice~ @metric 9 @threshold 0.01` |
| 特徴量 | `fluid.bufmfcc~` → `fluid.bufstats~` → `fluid.bufflatten~` → `fluid.dataset~ analysis` |
| 正規化 | `fluid.normalize~` → `fluid.dataset~ normalised` |
| 2D投影 | `fluid.umap~ @numdimensions 2` → `fluid.dataset~ reduction` |
| 近傍探索/試聴 | `fluid.kdtree~` → `play~ sound` |
| **色分け(追加)** | `fluid.kmeans~ @numclusters 4` →`fitpredict normalised clusters`→ `fluid.labelset~ clusters` → plotter第2インレット |

## 注意
- Max 9 がトライアル期限切れだと **保存不可**（動作はする）。このリポジトリの .maxpat がマスター。
- 色分け層は FluCoMa の plotter help の正準配線に準拠して注入。ベースのコア①〜④は実機で点群表示まで動作確認済み。**色分けの発色は未実機確認**（开いて click here で確認のこと）。

## 未実装（任意の次段階）
- ビート生成シーケンサ（クラスタからスライスを選んでステップ列で発音）
- pfft~ スペクトル・モーフィング統合（`~/dev/max-spectral-morph` を参照）
