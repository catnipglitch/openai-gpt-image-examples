# Catnip Image Generator 仕様書

## 1. はじめに

### 1.1 目的
このドキュメントは、Catnip Image Generator（以下、CIG）の詳細な仕様を記述するものです。CIGはOpenAIのgpt-image-1モデルを活用した画像生成ツールで、テキストから画像生成（t2i）、画像から画像生成（i2i）、画像編集（edit）機能を提供します。

### 1.2 対象読者
- 開発チーム
- テスター
- エンドユーザー（技術的な知識を持つユーザー）

### 1.3 参考資料
- OpenAI API ドキュメント（gpt-image-1）
- Catnip Image Generator コンセプトノート

## 2. システム概要

### 2.1 アプリケーション構成
CIGは以下の主要コンポーネントで構成されます：
- **CLIインターフェース**: JSON形式でのコマンド入力を受け付け
- **画像生成エンジン**: OpenAI gpt-image-1 APIとの連携
- **ファイル管理**: 画像の保存と変換
- **ログ管理**: JSON/CSV形式でのログ出力

### 2.2 機能概要
- テキストから画像生成（Text to Image）
- 画像から画像生成（Image to Image）
- 画像編集（Edit）
- プリセットテンプレートの提供
- 複数のファイル形式での出力（PNG、JPEG、SVG）

### 2.3 実行環境
- **OS**: Windows 11のみサポート
- **依存ライブラリ**: Python 3.8以上
- **APIキー**: 環境変数「OPENAI_API_KEY」で設定

## 3. 詳細仕様

### 3.1 CLIインターフェース

#### 3.1.1 基本コマンド構造
```
catnip <command> [options] <input-file>
```

#### 3.1.2 JSON入力形式
```json
{
  "mode": "t2i|i2i|edit",
  "prompt": "画像生成のためのプロンプト",
  "model": "gpt-image-1",
  "options": {
    "size": "1024x1024|1536x1024|1024x1536",
    "quality": "low|medium|high",
    "format": "png|jpeg|webp",
    "background": "transparent|opaque"
  },
  "output": {
    "filename": "出力ファイル名",
    "directory": "出力ディレクトリ"
  }
}
```

#### 3.1.3 テストモードでのコマンドライン引数
```
catnip test --mode=t2i --prompt="A cat sitting on a chair" --size=1024x1024 --output=cat.png
```

### 3.2 画像生成機能

#### 3.2.1 Text to Image (t2i)
- **入力**: テキストプロンプト
- **出力**: 生成された画像（PNG/JPEG/SVG）
- **オプション**: 
  - サイズ（デフォルト: 1024x1024）
  - 品質（低/中/高、デフォルト: 中）
  - 透明背景サポート（PNGのみ）

#### 3.2.2 Image to Image (i2i)
- **入力**: 参照画像 + テキストプロンプト
- **出力**: 生成された新しい画像
- **制限**: 参照画像のサイズと形式に関する制約あり

#### 3.2.3 Edit機能
- **入力**: 元画像 + マスク画像（オプション） + テキストプロンプト
- **出力**: 編集された画像
- **制限**: マスク画像は元画像と同じサイズである必要あり

### 3.3 ファイル管理

#### 3.3.1 サポートする出力形式
- PNG（デフォルト）- 透明背景サポート
- JPEG - 圧縮レベル調整可能
- WebP - 圧縮レベル調整可能
- SVG - ベクター形式出力

#### 3.3.2 ファイル命名規則
```
{prefix}_{timestamp}_{hash}.{extension}
```

#### 3.3.3 出力先ディレクトリ
- **デフォルト**: 実行ファイルと同じフォルダの下に`output`ディレクトリを作成
- **カスタム**: JSONの`output.directory`プロパティで指定可能

#### 3.3.4 ファイルパス指定の優先順位
1. JSONで`output.filename`にフルパスが指定されている場合、そのパスを優先
2. JSONで`output.filename`（ファイル名のみ）と`output.directory`の両方が指定されている場合、両者を結合
3. JSONで`output.filename`のみが指定されている場合、デフォルトディレクトリ内にそのファイル名で保存
4. ファイル名未指定の場合、自動生成されたファイル名をデフォルトディレクトリまたは指定ディレクトリに保存

### 3.4 ログ管理

#### 3.4.1 JSONログ形式
```json
{
  "timestamp": "YYYY-MM-DDThh:mm:ss.sssZ",
  "operation": "t2i|i2i|edit",
  "prompt": "使用されたプロンプト",
  "options": {
    "size": "使用サイズ",
    "quality": "使用品質"
  },
  "output": "出力ファイルパス",
  "status": "success|error",
  "processingTime": "処理時間（ミリ秒）",
  "estimatedCost": {
    "usd": "米ドルでの推定コスト（例: $0.042）",
    "jpy": "日本円での推定コスト（例: ¥6.72）",
    "model": "使用したモデル",
    "note": "テキストプロンプト料金は含まれていません"
  }
}
```

#### 3.4.2 CSVログ形式
```
timestamp,operation,prompt,size,quality,output_file,status,processing_time,estimated_cost_usd,estimated_cost_jpy,model
```

#### 3.4.3 推定料金の計算
画像生成時の推定料金は以下のモデル、品質、サイズに基づいて計算されます：

##### GPT Image 1

| 品質   | 1024x1024 | 1024x1536 | 1536x1024 |
| ------ | --------- | --------- | --------- |
| Low    | $0.011    | $0.016    | $0.016    |
| Medium | $0.042    | $0.063    | $0.063    |
| High   | $0.167    | $0.25     | $0.25     |

日本円は1米ドル＝160円で計算されます。
※テキストプロンプトトークン料金は含まれていません。

## 4. エラーハンドリング

### 4.1 エラーコード
- **E001**: API接続エラー
- **E002**: 無効なJSONフォーマット
- **E003**: 不正なパラメータ
- **E004**: ファイル書き込みエラー
- **E005**: 画像生成エラー

### 4.2 エラーレスポンス
```json
{
  "status": "error",
  "code": "エラーコード",
  "message": "エラーメッセージ",
  "timestamp": "エラー発生時刻"
}
```

## 5. 制限事項と注意点

### 5.1 APIの制限
- OpenAI APIのレート制限に従います
- 高品質の画像生成には時間がかかる場合があります（最大2分程度）

### 5.2 セキュリティ上の注意点
- APIキーは環境変数「OPENAI_API_KEY」で管理し、ソースコードには記述しないでください
- センシティブな内容を含むプロンプトはOpenAIのコンテンツポリシーに従って制限される場合があります

### 5.3 実行環境の制限
- 本ツールはWindows 11のみで動作を保証します
- 他のOS（Linux、macOS等）はサポート対象外となります

## 6. 今後の拡張計画
- GUI実装
- 追加の画像生成モデルのサポート
- バッチ処理機能
- 自動プロンプト最適化機能

## 7. 技術スタック
- **開発言語**: Python
- **依存関係**: 
  - OpenAI API
  - JSON処理ライブラリ
  - 画像処理ライブラリ

## 8. 付録

### 8.1 環境変数設定例
```
# OpenAI APIキー（必須）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ログ出力レベル（オプション、デフォルト: INFO）
CATNIP_LOG_LEVEL=DEBUG
```

### 8.2 用語集
- **t2i**: Text to Image - テキストプロンプトから画像を生成
- **i2i**: Image to Image - 参照画像を基に新しい画像を生成
- **edit**: 既存画像の編集機能