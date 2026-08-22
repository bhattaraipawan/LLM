"""Run the complete four-model benchmark in separate subprocesses.

This is the easiest entry point for Google Colab. Each LLM is loaded in a fresh
Python process, so GPU memory is released when that model finishes.

Default workflow:
    1. validate/freeze the reconciled expert reference;
    2. run Llama;
    3. run Qwen;
    4. run DeepSeek;
    5. run Mistral; and
    6. combine the four Excel result workbooks.

Examples
--------
Full benchmark::

    python scripts/run_four_llm_benchmark.py

Quick smoke test of all four models::

    python scripts/run_four_llm_benchmark.py --smoke

Resume after an interrupted session and skip completed model workbooks::

    python scripts/run_four_llm_benchmark.py --resume
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PREPARE_SCRIPT = REPO_ROOT / "scripts" / "prepare_benchmark_reference.py"
BENCHMARK_SCRIPT = REPO_ROOT / "scripts" / "benchmark_four_llms.py"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "Four_Models" / "Output"
MODEL_ORDER = ["llama", "qwen", "deepseek", "mistral"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Freeze the expert reference, benchmark four LLMs, and combine results."
    )
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--candidate-pool-size", type=int, default=20)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--max-new-tokens", type=int, default=384)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument(
        "--no-4bit", action="store_true", help="Disable 4-bit NF4 loading."
    )
    parser.add_argument(
        "--skip-prepare",
        action="store_true",
        help="Use the already-frozen Four_Models/Input reference workbook.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip a model if its benchmark_results.xlsx already exists.",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run 2 materials x 1 repeat per model instead of the full experiment.",
    )
    return parser.parse_args()


def run(command: list[str]) -> None:
    print("\n$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def main() -> None:
    args = parse_args()
    output_root = args.output_root.expanduser().resolve()

    if not args.skip_prepare:
        run([sys.executable, str(PREPARE_SCRIPT)])

    run([
        sys.executable,
        str(BENCHMARK_SCRIPT),
        "--check-inputs",
        "--candidate-pool-size",
        str(args.candidate_pool_size),
        "--top-k",
        str(args.top_k),
    ])

    runs = 1 if args.smoke else args.runs
    limit_args = ["--limit", "2"] if args.smoke else []

    for model_key in MODEL_ORDER:
        result_path = output_root / model_key / "benchmark_results.xlsx"
        if args.resume and result_path.exists():
            print(f"Skipping {model_key}: result already exists at {result_path}")
            continue

        command = [
            sys.executable,
            str(BENCHMARK_SCRIPT),
            "--model",
            model_key,
            "--runs",
            str(runs),
            "--candidate-pool-size",
            str(args.candidate_pool_size),
            "--top-k",
            str(args.top_k),
            "--max-new-tokens",
            str(args.max_new_tokens),
            "--temperature",
            str(args.temperature),
            "--output-root",
            str(output_root),
            *limit_args,
        ]
        if args.no_4bit:
            command.append("--no-4bit")
        run(command)

    run(
        [
            sys.executable,
            str(BENCHMARK_SCRIPT),
            "--combine-results",
            "--output-root",
            str(output_root),
        ]
    )

    print("\nFour-model benchmark completed successfully.")
    print(
        "Combined workbook: "
        + str(output_root / "combined" / "four_model_comparison.xlsx")
    )


if __name__ == "__main__":
    main()
