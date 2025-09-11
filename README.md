# catnip-image-gen

## 概要
catnip-image-gen は、テキストプロンプトや設定ファイルからAI画像生成を行うツールです。  
複数のAIプラットフォーム（OpenAI, Gemini, Stable Diffusion）に対応し、コマンドラインから簡単に画像生成・保存・ログ出力ができます。

## 主な機能
- テキストプロンプトやJSON設定ファイルから画像生成リクエストを作成
- OpenAI, Gemini, Stable Diffusion など複数のAI画像生成APIに対応
- 画像のバリエーション生成やシード値指定による再現性確保
- 生成画像の自動保存と出力ディレクトリ指定
- 生成結果やファイル保存のログ出力

### 実行ファイル・スクリプト
- `src/main.py`  
	コマンドラインから画像生成を実行するメインスクリプトです。  
	主なオプション例:
	- `--input` / `-i` : 入力JSONファイル指定
	- `--output-dir` / `-o` : 出力ディレクトリ指定
	- `--prompt` / `-p` : テキストプロンプト直接指定
	- `--variations` / `-v` : バリエーション数
	- `--seed` / `-s` : シード値
	- `--platform` : 画像生成AIプラットフォーム選択

## フォルダ構造

```
catnip-image-gen/
├── LICENSE                # ライセンスファイル
├── README.md              # このドキュメント
├── docs/                  # 仕様・設計などのドキュメント
│   ├── concept_notes.md
│   └── specification_document.md
├── src/                   # ソースコード
│   └── main.py            # 画像生成のメインスクリプト
└── catnip-image-gen.code-workspace # VSCode用ワークスペース設定
```

- `docs/` : プロジェクトの設計や仕様に関するドキュメントを格納
- `src/` : 画像生成処理のメインスクリプトを格納
- `LICENSE` : ライセンス情報
- `catnip-image-gen.code-workspace` : VSCode用のワークスペース設定

※ `.gitignore` で除外されたキャッシュ・ビルド・環境ファイル等は省略

## 利用方法

1. 必要な依存パッケージをインストール
2. コマンドラインから `main.py` を実行

例:
```sh
python src/main.py --prompt "猫のイラスト" --platform openai --output-dir output/
```
または
```sh
python src/main.py --input config.json
```

詳細な設定や依存関係については、`docs/` 内のドキュメントを参照してください。