# gpt-image API parameters (gpt-image-1 / gpt-image-1.5)

This document summarizes the core request parameters for the gpt-image models, focusing on gpt-image-1 and gpt-image-1.5.
Use it as a quick reference when calling the image generation APIs from application code or scripts.


## Generate image

Endpoint: `POST /v1/images/generations`

Generates one or more new images from a text prompt.


### Request body parameters

#### prompt

- Type: string  
- Required: yes  
- Description: Text description of the desired image or images.  
- Notes:  
  - Maximum length is 32,000 characters for gpt-image models.  
  - You can combine style, composition, lighting, camera angle, and other constraints in a single prompt.  


#### background

- Type: string or null  
- Required: no  
- Default: `auto`  
- Description: Controls background transparency for generated images.  
- Allowed values:  
  - `transparent`  
  - `opaque`  
  - `auto`  
- Notes:  
  - When `transparent` is used, the output format must support transparency (`png` or `webp`).  
  - `auto` lets the model choose the background automatically.  


#### model

- Type: string  
- Required: no  
- Recommended values:  
  - `gpt-image-1`  
  - `gpt-image-1-mini`  
  - `gpt-image-1.5`  
- Description: Selects which gpt-image model to use.  
- Notes:  
  - Always set this explicitly when using gpt-image models.  
  - Use `gpt-image-1.5` when you want the latest image model and features.  


#### moderation

- Type: string or null  
- Required: no  
- Default: `auto`  
- Description: Controls content moderation level for generated images.  
- Allowed values:  
  - `auto`  
  - `low`  
- Notes:  
  - `low` applies less restrictive filtering and may allow more borderline content.  


#### n

- Type: integer or null  
- Required: no  
- Default: `1`  
- Description: Number of images to generate for a single request.  
- Constraints:  
  - Minimum `1`  
  - Maximum `10`  


#### output_compression

- Type: integer or null  
- Required: no  
- Default: `100`  
- Description: Compression level for generated images when using `webp` or `jpeg` output formats.  
- Range:  
  - `0` to `100` (percent)  
- Notes:  
  - Higher values mean less compression and larger files.  


#### output_format

- Type: string or null  
- Required: no  
- Default: `png`  
- Description: File format for generated images.  
- Allowed values:  
  - `png`  
  - `jpeg`  
  - `webp`  
- Notes:  
  - Use `png` or `webp` if you need transparent backgrounds.  


#### partial_images

- Type: integer  
- Required: no  
- Default: `0`  
- Description: Number of partial images to send when using streaming responses.  
- Constraints:  
  - Range `0` to `3`  
- Notes:  
  - `0` means only a single final image is sent in one streaming event.  
  - If the full image finishes quickly, the final image may be sent before all partial images.  


#### quality

- Type: string or null  
- Required: no  
- Default: `auto`  
- Description: Controls overall image quality and compute cost.  
- Allowed values for gpt-image models:  
  - `auto`  
  - `high`  
  - `medium`  
  - `low`  
- Notes:  
  - `high` generally uses more compute and may give better detail.  
  - `low` trades some quality for speed and cost.  


#### size

- Type: string or null  
- Required: no  
- Default: `auto`  
- Description: Sets the resolution of generated images.  
- Allowed values for gpt-image models:  
  - `1024x1024`  
  - `1536x1024` (landscape)  
  - `1024x1536` (portrait)  
  - `auto`  
- Notes:  
  - `auto` lets the model choose the most suitable size based on the prompt.  


#### stream

- Type: boolean or null  
- Required: no  
- Default: `false`  
- Description: Enables streaming image generation.  
- Notes:  
  - When `true`, the API returns partial updates before sending the final image.  
  - Pair with `partial_images` to control how many intermediate images you want.  


#### user

- Type: string  
- Required: no  
- Description: Application-specific end user identifier.  
- Notes:  
  - Use a stable, non-PII identifier if you set this.  
  - Helps OpenAI monitor and detect abuse at the user level.  


### Example request (Python)

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


### Example response (simplified)

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


## Create image edit

Endpoint: `POST /v1/images/edits`

Creates an edited or extended image given one or more source images plus a prompt.

Note: At the time of writing, this endpoint only supports `gpt-image-1` among the gpt-image models.
gpt-image-1.5 is not yet supported for edits.


### Request body parameters

#### image

- Type: string or array  
- Required: yes  
- Description: One or more input images to edit or extend.  
- Constraints for gpt-image models:  
  - Each image must be `png`, `webp`, or `jpg`.  
  - Maximum file size is 50 MB per image.  
  - Up to 16 images per request.  


#### prompt

- Type: string  
- Required: yes  
- Description: Text description of the desired result after editing.  
- Notes:  
  - Maximum length is 32,000 characters for gpt-image models.  
  - Describe which parts should change and which should stay similar to the input image.  


#### background

- Type: string or null  
- Required: no  
- Default: `auto`  
- Description: Controls background transparency of the edited image.  
- Allowed values:  
  - `transparent`  
  - `opaque`  
  - `auto`  
- Notes:  
  - For `transparent`, set `output_format` to `png` or `webp`.  


#### input_fidelity

- Type: string  
- Required: no  
- Default: `low`  
- Description: Controls how closely the model should match the style and features of the input images.  
- Allowed values:  
  - `high`  
  - `low`  
- Notes:  
  - Supported only for `gpt-image-1`.  
  - Affects details like facial similarity and overall style preservation.  


#### mask

- Type: file  
- Required: no  
- Description: Mask image specifying which regions to edit.  
- Constraints:  
  - Must be a `png` file less than 4 MB.  
  - Must have the same dimensions as the main `image`.  
  - Fully transparent areas (alpha 0) indicate regions to edit.  
  - Non-transparent areas are left unchanged.  


#### model

- Type: string  
- Required: no  
- Recommended values:  
  - `gpt-image-1`  
  - `gpt-image-1-mini`  
- Description: gpt-image model used for the edit.  
- Notes:  
  - At present, `gpt-image-1` is the main choice for edits.  


#### n

- Type: integer or null  
- Required: no  
- Default: `1`  
- Description: Number of edited images to generate.  
- Constraints:  
  - Minimum `1`  
  - Maximum `10`  


#### output_compression

- Type: integer or null  
- Required: no  
- Default: `100`  
- Description: Compression level for edited images when using `webp` or `jpeg`.  
- Range:  
  - `0` to `100`  


#### output_format

- Type: string or null  
- Required: no  
- Default: `png`  
- Description: File format for edited images.  
- Allowed values:  
  - `png`  
  - `jpeg`  
  - `webp`  


#### partial_images

- Type: integer  
- Required: no  
- Default: `0`  
- Description: Number of partial images to send when streaming.  
- Constraints:  
  - Range `0` to `3`  
- Notes:  
  - `0` means only the final edited image is sent.  


#### quality

- Type: string or null  
- Required: no  
- Default: `auto`  
- Description: Controls quality and cost for image edits.  
- Allowed values for gpt-image models:  
  - `auto`  
  - `high`  
  - `medium`  
  - `low`  


#### size

- Type: string or null  
- Required: no  
- Default: `1024x1024`  
- Description: Output size of edited images.  
- Allowed values for gpt-image models:  
  - `1024x1024`  
  - `1536x1024` (landscape)  
  - `1024x1536` (portrait)  
  - `auto`  


#### stream

- Type: boolean or null  
- Required: no  
- Default: `false`  
- Description: Enables streaming for image edits.  


#### user

- Type: string  
- Required: no  
- Description: Application-specific end user identifier, same as in the generate endpoint.  


### Example request (Python)

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

