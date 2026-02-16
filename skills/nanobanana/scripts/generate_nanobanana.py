#!/usr/bin/env python3
"""
Nano Banana 画像生成スクリプト
Gemini API を使ってテキストから画像を生成する
"""

import argparse
import base64
import os
import sys
from pathlib import Path


def get_api_key():
    """環境変数からAPIキーを取得"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # .envファイルからの読み込みを試行
        env_file = Path.home() / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"\'')
                        break

    if not api_key:
        print("エラー: GEMINI_API_KEY が設定されてへん！", file=sys.stderr)
        print("", file=sys.stderr)
        print("セットアップ方法:", file=sys.stderr)
        print("1. https://aistudio.google.com/apikey でAPIキーを取得", file=sys.stderr)
        print("2. export GEMINI_API_KEY='your-api-key' を実行", file=sys.stderr)
        print("   または ~/.env に GEMINI_API_KEY=xxx を追記", file=sys.stderr)
        sys.exit(1)

    return api_key


def load_image_as_base64(image_path: str) -> tuple[str, str]:
    """画像ファイルをbase64エンコードして返す"""
    path = Path(image_path)
    if not path.exists():
        print(f"エラー: 画像ファイルが見つからへん: {image_path}", file=sys.stderr)
        sys.exit(1)

    # MIMEタイプを判定
    suffix = path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime_type = mime_types.get(suffix, "image/png")

    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")

    return data, mime_type


def generate_image(
    prompt: str,
    model: str = "flash",
    output: str = "generated_image.png",
    input_image: str | None = None,
    aspect_ratio: str = "1:1",
    size: str = "1k",
):
    """画像を生成する"""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("エラー: google-genai パッケージがインストールされてへん！", file=sys.stderr)
        print("", file=sys.stderr)
        print("インストール方法:", file=sys.stderr)
        print("  pip install google-genai", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()

    # モデル名を解決
    model_map = {
        "flash": "gemini-2.0-flash-exp-image-generation",
        "pro": "imagen-4.0-generate-001",
        "pro-ultra": "imagen-4.0-ultra-generate-001",
        "pro-fast": "imagen-4.0-fast-generate-001",
    }
    model_name = model_map.get(model, model)

    # クライアント初期化
    client = genai.Client(api_key=api_key)

    print(f"画像生成中... (モデル: {model_name})")

    # Imagenモデル（pro系）はgenerate_imagesを使う
    if model.startswith("pro"):
        try:
            # アスペクト比のマッピング
            aspect_ratio_map = {
                "1:1": "1:1",
                "16:9": "16:9",
                "9:16": "9:16",
                "4:3": "4:3",
                "3:4": "3:4",
            }
            ar = aspect_ratio_map.get(aspect_ratio, "1:1")

            response = client.models.generate_images(
                model=model_name,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio=ar,
                )
            )

            # 最初の画像を保存
            if response.generated_images:
                image = response.generated_images[0]
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # 画像データを保存
                image.image.save(output_path)
                print(f"画像を保存したで: {output_path.absolute()}")
            else:
                print("警告: 画像が生成されへんかった", file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg:
                print("エラー: APIキーが無効やで", file=sys.stderr)
            elif "PERMISSION_DENIED" in error_msg:
                print("エラー: このAPIキーには画像生成の権限がないで", file=sys.stderr)
            elif "RESOURCE_EXHAUSTED" in error_msg:
                print("エラー: APIの利用制限に達したで。しばらく待ってから再試行してな", file=sys.stderr)
            elif "SAFETY" in error_msg.upper():
                print("エラー: プロンプトが安全性ポリシーに違反してるみたいやで", file=sys.stderr)
            else:
                print(f"エラー: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Gemini Flash系はgenerate_contentを使う
        # コンテンツを構築
        contents = []

        # 入力画像がある場合（編集モード）
        if input_image:
            image_data, mime_type = load_image_as_base64(input_image)
            contents.append(
                types.Part.from_bytes(
                    data=base64.standard_b64decode(image_data),
                    mime_type=mime_type,
                )
            )

        # プロンプトを追加
        contents.append(prompt)

        try:
            # 画像生成設定
            config = types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            )

            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )

            # レスポンスから画像を抽出
            image_saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    # 画像データをファイルに保存
                    image_data = part.inline_data.data
                    output_path = Path(output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(output_path, "wb") as f:
                        f.write(image_data)

                    print(f"画像を保存したで: {output_path.absolute()}")
                    image_saved = True
                    break
                elif part.text:
                    # テキストレスポンスがあれば表示
                    print(f"モデルからのメッセージ: {part.text}")

            if not image_saved:
                print("警告: 画像が生成されへんかった", file=sys.stderr)
                print("レスポンス:", response, file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg:
                print("エラー: APIキーが無効やで", file=sys.stderr)
            elif "PERMISSION_DENIED" in error_msg:
                print("エラー: このAPIキーには画像生成の権限がないで", file=sys.stderr)
            elif "RESOURCE_EXHAUSTED" in error_msg:
                print("エラー: APIの利用制限に達したで。しばらく待ってから再試行してな", file=sys.stderr)
            elif "SAFETY" in error_msg.upper():
                print("エラー: プロンプトが安全性ポリシーに違反してるみたいやで", file=sys.stderr)
            else:
                print(f"エラー: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Nano Banana - Gemini画像生成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s "富士山と桜の風景画"
  %(prog)s "サイバーパンクな東京" --model pro
  %(prog)s "海辺の夕日" --aspect-ratio 16:9
  %(prog)s "背景を変更" --input photo.jpg
        """,
    )

    parser.add_argument(
        "prompt",
        help="生成する画像の説明（日本語OK）",
    )
    parser.add_argument(
        "--model", "-m",
        choices=["flash", "pro"],
        default="flash",
        help="使用モデル: flash（高速・安価）or pro（高品質）[デフォルト: flash]",
    )
    # デフォルト出力先
    default_output_dir = Path.home() / "Pictures" / "ClaudeCode"
    default_output = default_output_dir / "generated_image.png"

    parser.add_argument(
        "--output", "-o",
        default=str(default_output),
        help=f"出力ファイルパス [デフォルト: {default_output}]",
    )
    parser.add_argument(
        "--input", "-i",
        dest="input_image",
        help="編集する元画像のパス（編集モード時のみ）",
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        default="1:1",
        help="アスペクト比 (1:1, 16:9, 9:16, 4:3, 3:4, 21:9 等) [デフォルト: 1:1]",
    )
    parser.add_argument(
        "--size", "-s",
        choices=["1k", "2k", "4k"],
        default="1k",
        help="解像度 [デフォルト: 1k]",
    )

    args = parser.parse_args()

    generate_image(
        prompt=args.prompt,
        model=args.model,
        output=args.output,
        input_image=args.input_image,
        aspect_ratio=args.aspect_ratio,
        size=args.size,
    )


if __name__ == "__main__":
    main()
