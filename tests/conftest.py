"""共享的 pytest fixtures。"""

import pytest

from career_growth.data_generation.generator import generate_all_data


@pytest.fixture(scope="session")
def synthetic_data(tmp_path_factory):
    """在临时目录中每个测试会话生成一次共享的合成数据集。"""
    output_dir = tmp_path_factory.mktemp("synthetic")
    return generate_all_data(count=1500, seed=42, output_dir=str(output_dir))
