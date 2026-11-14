"""A deliberately small module for IPSELIA M1 coding runs (the code under change)."""

from __future__ import annotations


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean of an empty list")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    """Return the median of values without modifying the input list."""
    if not values:
        raise ValueError("median of an empty list")
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def clamp(value: float, low: float, high: float) -> float:
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(value, high))
