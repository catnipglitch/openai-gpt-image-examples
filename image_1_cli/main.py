import os
import argparse
from typing import Dict, Any
import json

from input_parser import InputParser
from image_request_manager import ImageRequestManager
from output_manager import OutputManager
from logging_manager import LoggingManager

def main():
    parser = argparse.ArgumentParser(description="Catnip Image Generator")
    parser.add_argument("--input", "-i", type=str, help="Input JSON file")
    parser.add_argument("--output-dir", "-o", type=str, help="Output directory")
    parser.add_argument("--prompt", "-p", type=str, help="Text prompt for image generation")
    parser.add_argument("--variations", "-v", type=int, default=1, help="Number of variations to generate")
    parser.add_argument("--seed", "-s", type=int, help="Seed value for reproducibility")
    parser.add_argument("--platform", type=str, default="openai", choices=["openai", "gemini", "stable_diffusion"], 
                       help="AI platform to use for generation")
    args = parser.parse_args()
    
    # 入力の解析
    input_parser = InputParser()
    if args.input:
        config = input_parser.parse_file(args.input)
    else:
        config = input_parser.parse_args(args)
    
    # 画像生成リクエスト
    request_manager = ImageRequestManager()
    generation_results = request_manager.generate_images(config)
    
    # 出力処理
    output_dir = args.output_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    output_manager = OutputManager(output_dir=output_dir)
    saved_files = output_manager.save_images(generation_results)
    
    # ログ出力
    logging_manager = LoggingManager()
    logging_manager.log_generation_results(generation_results, saved_files, config)
    
    print(f"Generated {len(generation_results)} image(s). See logs for details.")

if __name__ == "__main__":
    main()
