# gpt-image API パラメータリファレンス（gpt-image-1 / gpt-image-1.5）

このドキュメントは、gpt-image 系モデル（特に gpt-image-1 と gpt-image-1.5）で使う主要なリクエストパラメータをまとめたものです。
アプリケーションコードやスクリプトから画像生成 API を呼び出すときのクイックリファレンスとして使えます。


## 画像生成（Generate image）

エンドポイント  
`POST /v1/images/generations`

テキストプロンプトから、1 枚以上の画像を新規生成します。


### リクエストボディのパラメータ

#### prompt

- 型: string  
- 必須: 必須  
- 説明: 生成したい画像の内容を表すテキスト。  
- 補足:  
  - gpt-image モデルでは最大 32,000 文字まで指定できます。  
  - スタイル、構図、ライティング、カメラアングルなどを 1 つのプロンプトにまとめて表現できます。  


#### background

- 型: string または null  
- 必須: 任意  
- デフォルト: `auto`  
- 説明: 生成される画像の背景の透過状態を制御します。  
- 設定値:  
  - `transparent`  
  - `opaque`  
  - `auto`  
- 補足:  
  - `transparent` を指定する場合、出力フォーマットは透過対応の `png` または `webp` にする必要があります。  
  - `auto` はモデル側に最適な背景の判断を任せます。  


#### model

- 型: string  
- 必須: 任意  
- 推奨値:  
  - `gpt-image-1`  
  - `gpt-image-1-mini`  
  - `gpt-image-1.5`  
- 説明: 使用する gpt-image モデルを指定します。  
- 補足:  
  - gpt-image モデルを使う場合は、明示的にこの値を指定することを推奨します。  
  - 最新モデルと機能を使いたい場合は `gpt-image-1.5` を指定します。  


#### moderation

- 型: string または null  
- 必須: 任意  
- デフォルト: `auto`  
- 説明: 生成される画像に対するコンテンツモデレーションのレベルを制御します。  
- 設定値:  
  - `auto`  
  - `low`  
- 補足:  
  - `low` はフィルタリングがやや緩くなり、境界線上のコンテンツが通りやすくなります。  


#### n

- 型: integer または null  
- 必須: 任意  
- デフォルト: `1`  
- 説明: 1 回のリクエストで生成する画像の枚数。  
- 制約:  
  - 最小 `1`  
  - 最大 `10`  


#### output_compression

- 型: integer または null  
- 必須: 任意  
- デフォルト: `100`  
- 説明: `webp` または `jpeg` 出力時の圧縮レベル（パーセント）。  
- 範囲:  
  - `0` から `100`  
- 補足:  
  - 値が大きいほど圧縮が弱くなり、ファイルサイズは大きくなります。  


#### output_format

- 型: string または null  
- 必須: 任意  
- デフォルト: `png`  
- 説明: 生成画像のファイルフォーマット。  
- 設定値:  
  - `png`  
  - `jpeg`  
  - `webp`  
- 補足:  
  - 透過背景が必要な場合は `png` か `webp` を選択します。  


#### partial_images

- 型: integer  
- 必須: 任意  
- デフォルト: `0`  
- 説明: ストリーミングレスポンスで、途中経過の画像を何枚送るかを指定します。  
- 制約:  
  - `0` から `3` の範囲  
- 補足:  
  - `0` の場合は、最終画像のみが 1 回のストリーミングイベントで返されます。  
  - 画像生成が速く完了した場合、指定枚数に達する前に最終画像が送られることがあります。  


#### quality

- 型: string または null  
- 必須: 任意  
- デフォルト: `auto`  
- 説明: 画像のクオリティと計算コストのバランスを制御します。  
- 設定値（gpt-image モデル）:  
  - `auto`  
  - `high`  
  - `medium`  
  - `low`  
- 補足:  
  - `high` はより多くの計算資源を使い、細部表現が向上する傾向があります。  
  - `low` はクオリティを多少落として速度とコストを優先します。  


#### size

- 型: string または null  
- 必須: 任意  
- デフォルト: `auto`  
- 説明: 生成される画像の解像度。  
- 設定値（gpt-image モデル）:  
  - `1024x1024`  
  - `1536x1024`（横長）  
  - `1024x1536`（縦長）  
  - `auto`  
- 補足:  
  - `auto` はプロンプトに応じてモデルが自動的にサイズを選びます。  


#### stream

- 型: boolean または null  
- 必須: 任意  
- デフォルト: `false`  
- 説明: 画像生成をストリーミングモードで行うかどうか。  
- 補足:  
  - `true` を指定すると、最終結果の前に途中経過の更新が届きます。  
  - `partial_images` と組み合わせて、途中経過画像の枚数を制御できます。  


#### user

- 型: string  
- 必須: 任意  
- 説明: アプリケーション側で定義するエンドユーザーを表す識別子。  
- 補足:  
  - 個人情報を含まない安定した ID を使うことを推奨します。  
  - OpenAI 側での不正検知やモニタリングに利用されます。  


### サンプルリクエスト（Python）

```python
import base64
from openai import OpenAI

client = OpenAI()

img = client.images.generate(
    model="gpt-image-1.5",
    prompt="A cute baby sea otter",
    background="transparent",
    moderation="auto",
    n=2,
    output_compression=90,
    output_format="png",
    partial_images=0,
    quality="high",
    size="1024x1024",
    stream=False,
    user="example-user-123"
)

for index, image in enumerate(img.data):
    image_bytes = base64.b64decode(image.b64_json)
    with open(f"output_{index}.png", "wb") as f:
        f.write(image_bytes)
```


### サンプルレスポンス（簡略版）

```json
{
  "created": 1713833628,
  "data": [
    {
      "b64_json": "..."
    }
  ],
  "usage": {
    "total_tokens": 100,
    "input_tokens": 50,
    "output_tokens": 50,
    "input_tokens_details": {
      "text_tokens": 10,
      "image_tokens": 40
    }
  }
}
```


## 画像編集（Create image edit）

エンドポイント  
`POST /v1/images/edits`

既存の画像（複数可）とプロンプトを入力として、画像の編集や拡張を行います。

注意  
執筆時点では、gpt-image 系モデルの中では `gpt-image-1` のみがこのエンドポイントをサポートしています。  
gpt-image-1.5 はまだ編集エンドポイントに対応していません。


### リクエストボディのパラメータ

#### image

- 型: string または配列  
- 必須: 必須  
- 説明: 編集や拡張の対象となる入力画像。複数指定も可能です。  
- 制約（gpt-image モデル）:  
  - 各画像は `png` `webp` `jpg` のいずれか。  
  - 1 枚あたり最大 50 MB。  
  - 1 リクエストあたり最大 16 枚まで。  


#### prompt

- 型: string  
- 必須: 必須  
- 説明: 編集後に得たい画像の内容を説明するテキスト。  
- 補足:  
  - gpt-image モデルでは最大 32,000 文字まで指定できます。  
  - どの部分を変更し、どの部分を元画像に近いまま残したいかを、できるだけ具体的に書くと制御しやすくなります。  


#### background

- 型: string または null  
- 必須: 任意  
- デフォルト: `auto`  
- 説明: 編集後の画像の背景の透過状態を制御します。  
- 設定値:  
  - `transparent`  
  - `opaque`  
  - `auto`  
- 補足:  
  - `transparent` を指定する場合、`output_format` は `png` か `webp` にします。  


#### input_fidelity

- 型: string  
- 必須: 任意  
- デフォルト: `low`  
- 説明: 入力画像のスタイルや特徴（特に顔など）を、どの程度厳密に維持するかを制御します。  
- 設定値:  
  - `high`  
  - `low`  
- 補足:  
  - `gpt-image-1` のみでサポートされています。  
  - 顔の類似度や全体のスタイルをどこまで保つかに影響します。  


#### mask

- 型: file  
- 必須: 任意  
- 説明: どの領域を編集対象とするかを示すマスク画像。  
- 制約:  
  - `png` 形式で、4 MB 未満。  
  - メインの `image` と同じ解像度である必要があります。  
  - 完全に透過（alpha 0）の領域が「編集する部分」です。  
  - 透過していない領域はそのまま保持されます。  


#### model

- 型: string  
- 必須: 任意  
- 推奨値:  
  - `gpt-image-1`  
  - `gpt-image-1-mini`  
- 説明: 画像編集に使用する gpt-image モデル。  
- 補足:  
  - 現時点では、編集用途には `gpt-image-1` が主な選択肢です。  


#### n

- 型: integer または null  
- 必須: 任意  
- デフォルト: `1`  
- 説明: 生成する編集済み画像の枚数。  
- 制約:  
  - 最小 `1`  
  - 最大 `10`  


#### output_compression

- 型: integer または null  
- 必須: 任意  
- デフォルト: `100`  
- 説明: `webp` または `jpeg` 出力時の圧縮レベル。  
- 範囲:  
  - `0` から `100`  


#### output_format

- 型: string または null  
- 必須: 任意  
- デフォルト: `png`  
- 説明: 編集後の画像のファイルフォーマット。  
- 設定値:  
  - `png`  
  - `jpeg`  
  - `webp`  


#### partial_images

- 型: integer  
- 必須: 任意  
- デフォルト: `0`  
- 説明: ストリーミング時に途中経過の画像を何枚送るか。  
- 制約:  
  - `0` から `3` の範囲  
- 補足:  
  - `0` の場合は最終画像のみが返されます。  


#### quality

- 型: string または null  
- 必須: 任意  
- デフォルト: `auto`  
- 説明: 編集処理のクオリティとコストのバランスを制御します。  
- 設定値（gpt-image モデル）:  
  - `auto`  
  - `high`  
  - `medium`  
  - `low`  


#### size

- 型: string または null  
- 必須: 任意  
- デフォルト: `1024x1024`  
- 説明: 編集後の画像の解像度。  
- 設定値（gpt-image モデル）:  
  - `1024x1024`  
  - `1536x1024`（横長）  
  - `1024x1536`（縦長）  
  - `auto`  


#### stream

- 型: boolean または null  
- 必須: 任意  
- デフォルト: `false`  
- 説明: 画像編集をストリーミングモードで行うかどうか。  


#### user

- 型: string  
- 必須: 任意  
- 説明: 画像生成エンドポイントと同じく、アプリケーション側のエンドユーザー識別子。  


### サンプルリクエスト（Python）

```python
import base64
from openai import OpenAI

client = OpenAI()

with open("input.png", "rb") as image_file, open("mask.png", "rb") as mask_file:
    result = client.images.edits(
        model="gpt-image-1",
        image=image_file,
        mask=mask_file,
        prompt="A brighter living room with more plants",
        background="transparent",
        input_fidelity="high",
        n=2,
        output_compression=90,
        output_format="png",
        partial_images=0,
        quality="high",
        size="1024x1024",
        stream=False,
        user="example-user-123"
    )

for index, image in enumerate(result.data):
    image_bytes = base64.b64decode(image.b64_json)
    with open(f"edit_output_{index}.png", "wb") as f:
        f.write(image_bytes)
```

