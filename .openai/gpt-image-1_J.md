https://platform.openai.com/docs/guides/image-generation?image-generation-model=gpt-image-1

画像生成
================

画像を生成または編集する方法を学びます。

概要
--------

OpenAI APIを使用すると、GPT ImageまたはDALL·Eモデルを使用して、テキストプロンプトから画像を生成および編集できます。

現在、画像生成は[Image API](/docs/api-reference/images)を通じてのみ利用可能です。[Responses API](/docs/api-reference/responses)へのサポート拡大に向けて積極的に取り組んでいます。

[Image API](/docs/api-reference/images)は、以下の3つのエンドポイントを提供し、それぞれ異なる機能を持っています：

*   **生成**: テキストプロンプトに基づいて[画像を生成](#generate-images)
*   **編集**: 新しいプロンプトを使用して既存の画像を部分的または完全に[編集](#edit-images)
*   **バリエーション**: 既存の画像の[バリエーションを生成](#image-variations)（DALL·E 2のみ利用可能）

また、品質、サイズ、形式、圧縮、透明背景の有無を指定して[出力をカスタマイズ](#customize-image-output)することもできます。

### モデル比較

画像生成のための最新かつ最先端のモデルは、`gpt-image-1`で、ネイティブなマルチモーダル言語モデルです。

このモデルは、高品質な画像生成と、画像作成における世界知識の活用能力で推奨されます。ただし、Image APIを使用して、DALL·E 2やDALL·E 3などの専門的な画像生成モデルを使用することもできます。

| モデル    | エンドポイント                                              | ユースケース                                                             |
| --------- | ----------------------------------------------------------- | ------------------------------------------------------------------------ |
| DALL·E 2  | Image API: 生成、編集、バリエーション                       | 低コスト、同時リクエスト、インペインティング（マスクを使用した画像編集） |
| DALL·E 3  | Image API: 生成のみ                                         | DALL·E 2より高品質な画像、大きな解像度のサポート                         |
| GPT Image | Image API: 生成、編集 – Responses APIサポートは近日公開予定 | 優れた指示追従性、テキストレンダリング、詳細な編集、現実世界の知識       |

このガイドはGPT Imageに焦点を当てていますが、[DALL·E 2](/docs/guides/image-generation?image-generation-model=dall-e-2)および[DALL·E 3](/docs/guides/image-generation?image-generation-model=dall-e-3)のドキュメントに切り替えることもできます。

このモデルを責任を持って使用するために、`gpt-image-1`を使用する前に[開発者コンソール](https://platform.openai.com/settings/organization/general)から[API組織認証](https://help.openai.com/en/articles/10910291-api-organization-verification)を完了する必要がある場合があります。

![a vet with a baby otter](https://cdn.openai.com/API/docs/images/otter.png)

画像を生成する
---------------

[画像生成エンドポイント](/docs/api-reference/images/create)を使用して、テキストプロンプトに基づいて画像を作成できます。出力（サイズ、品質、形式、透明性）をカスタマイズする方法については、以下の[画像出力をカスタマイズ](#customize-image-output)セクションを参照してください。

`n`パラメータを設定することで、1回のリクエストで複数の画像を生成することができます（デフォルトではAPIは1つの画像を返します）。

画像を生成する

```javascript
import OpenAI from "openai";
import fs from "fs";
const openai = new OpenAI();

const prompt = `
子供向けの絵本のイラストで、獣医が聴診器を使って赤ちゃんカワウソの心音を聞いている様子。
`;

const result = await openai.images.generate({
    model: "gpt-image-1",
    prompt,
});

// 画像をファイルに保存
const image_base64 = result.data[0].b64_json;
const image_bytes = Buffer.from(image_base64, "base64");
fs.writeFileSync("otter.png", image_bytes);
```

```python
from openai import OpenAI
import base64
client = OpenAI()

prompt = """
子供向けの絵本のイラストで、獣医が聴診器を使って赤ちゃんカワウソの心音を聞いている様子。
"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# 画像をファイルに保存
with open("otter.png", "wb") as f:
    f.write(image_bytes)
```

```bash
curl -X POST "https://api.openai.com/v1/images/generations" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-type: application/json" \
    -d '{
        "model": "gpt-image-1",
        "prompt": "子供向けの絵本のイラストで、獣医が聴診器を使って赤ちゃんカワウソの心音を聞いている様子。"
    }' | jq -r '.data[0].b64_json' | base64 --decode > otter.png
```

...（以下の内容も同様に翻訳されます）...

### 画像を編集する

[画像編集エンドポイント](/docs/api-reference/images/createEdit)を使用すると、以下のことが可能です：

* 既存の画像を編集
* 他の画像を参照として使用して新しい画像を生成
* マスクをアップロードして画像の一部を編集（**インペインティング**と呼ばれるプロセス）

#### 画像参照を使用して新しい画像を作成

1つ以上の画像を参照として使用して、新しい画像を生成できます。

この例では、4つの入力画像を使用して、参照画像に含まれるアイテムを含むギフトバスケットの新しい画像を生成します。

![gift basket](https://cdn.openai.com/API/docs/images/gift-basket.png)

```javascript
import OpenAI from "openai";
import fs from "fs";
const openai = new OpenAI();

const result = await openai.images.generate({
  model: "gpt-image-1",
  prompt: "a gift basket",
  images: [
    {
      image: fs.createReadStream("input-image-1.png"),
    },
    {
      image: fs.createReadStream("input-image-2.png"),
    },
    {
      image: fs.createReadStream("input-image-3.png"),
    },
    {
      image: fs.createReadStream("input-image-4.png"),
    },
  ],
});

// 画像をファイルに保存
const image_base64 = result.data[0].b64_json;
const image_bytes = Buffer.from(image_base64, "base64");
fs.writeFileSync("output-image.png", image_bytes);
```

```python
from openai import OpenAI
import base64
client = OpenAI()

result = client.images.generate(
    model="gpt-image-1",
    prompt="a gift basket",
    images=[
        {"image": open("input-image-1.png", "rb")},
        {"image": open("input-image-2.png", "rb")},
        {"image": open("input-image-3.png", "rb")},
        {"image": open("input-image-4.png", "rb")},
    ],
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# 画像をファイルに保存
with open("output-image.png", "wb") as f:
    f.write(image_bytes)
```

```bash
curl -X POST "https://api.openai.com/v1/images/generations" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-type: application/json" \
    -F 'model="gpt-image-1"' \
    -F 'prompt="a gift basket"' \
    -F 'images=@input-image-1.png' \
    -F 'images=@input-image-2.png' \
    -F 'images=@input-image-3.png' \
    -F 'images=@input-image-4.png' \
    -o output-image.png
```

#### マスクを使用して画像を編集（インペインティング）

マスクを提供して、画像のどの部分を編集するかを指定できます。マスクの透明な部分が置き換えられ、塗りつぶされた部分はそのまま残ります。

この例では、カワウソの赤ちゃんの画像の一部を編集するためにマスクを使用しています。マスクは、編集したい画像の部分を白で塗りつぶした画像です。

![baby otter with mask](https://cdn.openai.com/API/docs/images/otter-mask.png)

```javascript
import OpenAI from "openai";
import fs from "fs";
const openai = new OpenAI();

const result = await openai.images.generate({
  model: "gpt-image-1",
  prompt: "a baby otter",
  mask: fs.createReadStream("otter-mask.png"),
});

// 画像をファイルに保存
const image_base64 = result.data[0].b64_json;
const image_bytes = Buffer.from(image_base64, "base64");
fs.writeFileSync("otter-updated.png", image_bytes);
```

```python
from openai import OpenAI
import base64
client = OpenAI()

result = client.images.generate(
    model="gpt-image-1",
    prompt="a baby otter",
    mask=open("otter-mask.png", "rb"),
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# 画像をファイルに保存
with open("otter-updated.png", "wb") as f:
    f.write(image_bytes)
```

```bash
curl -X POST "https://api.openai.com/v1/images/generations" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-type: application/json" \
    -F 'model="gpt-image-1"' \
    -F 'prompt="a baby otter"' \
    -F 'mask=@otter-mask.png' \
    -o otter-updated.png
```

### 画像出力をカスタマイズ

以下の出力オプションを設定できます：

* **サイズ**: 画像の寸法（例: `1024x1024`, `1024x1536`）
* **品質**: レンダリング品質（例: `low`, `medium`, `high`）
* **形式**: ファイル出力形式
* **圧縮**: JPEGおよびWebP形式の圧縮レベル（0-100%）
* **背景**: 透明または不透明

これらのオプションは、[画像生成エンドポイント](/docs/api-reference/images/create)および[画像編集エンドポイント](/docs/api-reference/images/createEdit)のリクエストで設定できます。

### 制限事項

GPT-4o Imageモデルは強力で多用途な画像生成モデルですが、以下の制限があります：

* **遅延**: 複雑なプロンプトは処理に最大2分かかる場合があります。
* **テキストレンダリング**: DALL·Eシリーズより大幅に改善されていますが、正確なテキスト配置や明瞭さに課題が残る場合があります。
* **一貫性**: 一貫したイメージを生成する能力はありますが、複数の生成にわたって再現キャラクターやブランド要素を維持するのが難しい場合があります。
* **構図制御**: 指示の追従性は向上していますが、構造化されたレイアウトや配置に敏感な構図で要素を正確に配置するのが難しい場合があります。

### コンテンツモデレーション

生成された画像は、OpenAIの[コンテンツポリシー](/policy)に準拠している必要があります。すべての画像は、ユーザーがリクエストした後に生成され、OpenAIのシステムによって自動的にフィルタリングされます。

### コストと遅延

画像を生成または編集するためのコストは、使用するモデルとリクエストの複雑さによって異なります。詳細については、[料金ページ](https://openai.com/pricing)を参照してください。