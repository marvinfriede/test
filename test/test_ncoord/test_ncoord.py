"""
Test calculation of DFT-D4 coordination number.
"""

import pytest
import torch

from tad_dftd4.data import cov_rad_d3
from tad_dftd4.ncoord import erf_count, get_coordination_number
from tad_dftd4.utils import pack

from .samples import samples

sample_list = ["SiH4", "MB16_43_01", "MB16_43_02"]


@pytest.mark.parametrize("dtype", [torch.float, torch.double])
@pytest.mark.parametrize("name", sample_list)
def test_single(dtype: torch.dtype, name: str) -> None:
    sample = samples[name]
    numbers = sample["numbers"]
    positions = sample["positions"].type(dtype)

    rcov = cov_rad_d3[numbers]
    ref = sample["cn"].type(dtype)

    cn = get_coordination_number(numbers, positions, erf_count, rcov)
    assert pytest.approx(cn) == ref


@pytest.mark.parametrize("dtype", [torch.float, torch.double])
@pytest.mark.parametrize("name1", sample_list)
@pytest.mark.parametrize("name2", sample_list)
def test_cn_batch(dtype: torch.dtype, name1: str, name2: str) -> None:
    sample1, sample2 = samples[name1], samples[name2]
    numbers = pack(
        (
            sample1["numbers"],
            sample2["numbers"],
        )
    )
    positions = pack(
        (
            sample1["positions"].type(dtype),
            sample2["positions"].type(dtype),
        )
    )
    ref = pack(
        (
            sample1["cn"].type(dtype),
            sample2["cn"].type(dtype),
        )
    )

    cn = get_coordination_number(numbers, positions)
    assert pytest.approx(cn) == ref
