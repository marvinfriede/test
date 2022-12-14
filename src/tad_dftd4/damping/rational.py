"""
Rational (Becke-Johnson) damping. Default damping scheme.
"""

import torch

from ..typing import Tensor


def rational_damping(
    order: int,
    distances: Tensor,
    qq: Tensor,
    a1: float = 0.4,
    a2: float = 5.0,
) -> Tensor:
    """
    Rational damped dispersion interaction between pairs
    Parameters
    ----------
    order : int
        Order of the dispersion interaction, e.g.
        6 for dipole-dipole, 8 for dipole-quadrupole and so on.
    distances : Tensor
        Pairwise distances between atoms in the system.
    rvdw : Tensor
        Van der Waals radii of the atoms in the system.
    qq : Tensor
        Quotient of C8 and C6 dispersion coefficients.
    a1 : float
        Scaling for the C8 / C6 ratio in the critical radius.
    a2 : float
        Offset parameter for the critical radius.
    """

    return 1.0 / (distances.pow(order) + (a1 * torch.sqrt(qq) + a2).pow(order))
