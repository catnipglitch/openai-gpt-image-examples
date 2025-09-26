# Catnip Image Generator

## 概要
Catnip Image GeneratorはOpenAIのgpt-image-1モデルを活用した画像生成ツールです。  
テキストプロンプトやJSON設定ファイルから簡単にAI画像生成を行い、複数のバリエーション画像を同時に生成できます。

## 主な機能
- **テキストから画像生成（Text to Image）**: プロンプトから画像を生成
- **画像から画像生成（Image to Image）**: 既存画像を基に新しい画像を生成
- **画像編集（Edit）**: 既存画像の一部を編集・変更
- **複数バリエーション生成**: 一度に複数の画像バリエーションを生成
- **シード値管理**: 再現性を確保するためのシード値指定・再利用
- **多様な出力形式**: PNG、JPEG、SVG形式での画像出力
- **詳細ログ出力**: JSON/CSV形式でのログ出力（生成料金情報含む）

## 必要環境
- **OS**: Windows 11
- **Python**: 3.8以上
- **APIキー**: OpenAIのAPIキーが必要（環境変数 `OPENAI_API_KEY` で設定）

## インストール・セットアップ
1. このリポジトリをクローン
2. 必要な依存パッケージをインストール:
   ```powershell
   pip install -r requirements.txt
   ```
3. OpenAI APIキーを環境変数に設定:
   ```powershell
   $env:OPENAI_API_KEY = "your-openai-api-key-here"
   ```

## 使用方法

### コマンドラインオプション
- `--input` / `-i` : 入力JSONファイル指定
- `--output-dir` / `-o` : 出力ディレクトリ指定
- `--prompt` / `-p` : テキストプロンプト直接指定
- `--variations` / `-v` : バリエーション数（デフォルト: 1）
- `--seed` / `-s` : シード値
- `--platform` : 画像生成プラットフォーム選択（openai, gemini, stable_diffusion）

### 実行例

#### プロンプトからの直接生成
```powershell
python src/main.py --prompt "可愛い猫のイラスト" --variations 3 --output-dir output/
```

#### JSON設定ファイルを使用した生成
```powershell
python src/main.py --input config.json --output-dir output/
```

#### シード値を指定した再現可能な生成
```powershell
python src/main.py --prompt "夕日と海の風景" --seed 12345 --platform openai
```

### JSON設定ファイル形式

```json
{
  "mode": "t2i",
  "prompt": "美しい山の風景画",
  "variations": 2,
  "seed": 12345,
  "platform": "openai",
  "output_format": "png"
}
```

## プロジェクト構造

```
catnip-image-gen/
├── LICENSE                # ライセンスファイル
├── README.md              # このドキュメント
├── docs/                  # 仕様・設計などのドキュメント
│   ├── concept_notes.md           # プロジェクトコンセプト
│   ├── specification_document.md  # 詳細仕様書
│   └── openai/                    # OpenAI関連ドキュメント
├── src/                   # ソースコード
│   └── main.py            # 画像生成のメインスクリプト
└── catnip-image-gen.code-workspace # VS Code用ワークスペース設定
```

- `docs/` : プロジェクトの設計や仕様に関するドキュメントを格納
- `src/` : 画像生成処理のメインスクリプトを格納  
- `LICENSE` : ライセンス情報
- `catnip-image-gen.code-workspace` : VS Code用のワークスペース設定

## 出力とログ

### 生成画像
- デフォルト出力先: `output/` ディレクトリ
- サポート形式: PNG、JPEG、SVG
- ファイル名には自動的にタイムスタンプが付与されます

### ログ情報
生成結果のログには以下の情報が含まれます：
- 生成パラメーター（プロンプト、シード値、バリエーション数）
- 生成料金（USD/JPY表示）
- 生成時刻とファイルパス
- エラー情報（該当する場合）

ログはJSON・CSV形式で出力され、再現性を確保するためのシード値情報も記録されます。

## 開発状況

⚠️ **注意**: このプロジェクトは現在開発中です。
- `main.py` で参照されているモジュール（`input_parser`、`image_request_manager`等）は未実装
- 実際の動作には追加の実装が必要です

## ドキュメント

詳細な仕様や設計については、`docs/` ディレクトリ内のドキュメントを参照してください：
- [`docs/concept_notes.md`](docs/concept_notes.md) - プロジェクトのコンセプトと要件
- [`docs/specification_document.md`](docs/specification_document.md) - 詳細な技術仕様
- [`docs/openai/`](docs/openai/) - OpenAI関連の情報とドキュメント

## ライセンス

このプロジェクトは[LICENSE](LICENSE)ファイルに記載されたライセンスの下で公開されています。