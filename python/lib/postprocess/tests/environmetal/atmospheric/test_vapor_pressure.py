"""Tests for atmospheric vapour-pressure calculations."""

import math

import pytest

from postprocess.environmental.atmospheric import (
    partial_vapor_pressure,
    saturation_vapor_pressure,
    saturation_vapor_pressure_derivative,
)


# pylint: disable=missing-function-docstring


def test_saturation_vapor_pressure_at_zero_celsius():
    pressure = saturation_vapor_pressure(0.0)

    assert pressure == pytest.approx(611.0, rel=0.02)


def test_saturation_vapor_pressure_at_twenty_celsius():
    pressure = saturation_vapor_pressure(20.0)

    assert pressure == pytest.approx(2338.0, rel=0.01)


def test_saturation_vapor_pressure_at_thirty_celsius():
    pressure = saturation_vapor_pressure(30.0)

    assert pressure == pytest.approx(4243.0, rel=0.02)


def test_saturation_vapor_pressure_increases_with_temperature():
    values = [
        saturation_vapor_pressure(t)
        for t in [0.0, 10.0, 20.0, 30.0, 40.0]
    ]

    assert values == sorted(values)


@pytest.mark.parametrize(
    "temperature",
    [-20.0, 0.0, 10.0, 20.0, 30.0, 40.0],
)
def test_saturation_vapor_pressure_is_finite(temperature):
    result = saturation_vapor_pressure(temperature)

    assert math.isfinite(result)
    assert result > 0.0


def test_saturation_vapor_pressure_derivative_at_twenty_celsius():
    delta = saturation_vapor_pressure_derivative(20.0)

    assert delta == pytest.approx(145.0, rel=0.03)


def test_saturation_vapor_pressure_derivative_is_positive():
    for temperature in [-10.0, 0.0, 10.0, 20.0, 30.0, 40.0]:
        delta = saturation_vapor_pressure_derivative(temperature)

        assert delta > 0.0


@pytest.mark.parametrize(
    "rh",
    [0.0, 25.0, 50.0, 75.0, 100.0],
)
def test_partial_vapor_pressure_is_between_zero_and_saturation(rh):
    saturation = saturation_vapor_pressure(20.0)
    actual = partial_vapor_pressure(20.0, rh)

    assert 0.0 <= actual <= saturation
