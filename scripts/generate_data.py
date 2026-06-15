"""生成合成 MVP 数据集的 CLI 脚本。"""

import argparse

from career_growth import config
from career_growth.data_generation.generator import generate_all_data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="生成 AI Career Growth Analytics MVP 的合成数据。"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=config.DEFAULT_USER_COUNT,
        help="要生成的合成用户数量。",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=config.RANDOM_SEED,
        help="用于可复现性的随机种子。",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data",
        help="写入生成数据的目录。",
    )
    args = parser.parse_args()

    data = generate_all_data(count=args.count, seed=args.seed, output_dir=args.output_dir)
    print(f"Generated {len(data['users'])} users and {len(data['events'])} events.")
    print(f"Churn rate: {data['labels']['is_churned'].mean():.2%}")


if __name__ == "__main__":
    main()
