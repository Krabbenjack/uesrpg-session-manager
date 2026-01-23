"""
Mechanics module for UESRPG Session Manager.

This module contains game mechanics engines for computing derived stats,
applying rules, and processing character data according to game rules.
"""

from .derived_engine import apply_derived_stats

__all__ = ['apply_derived_stats']
