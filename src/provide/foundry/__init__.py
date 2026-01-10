# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Shared documentation infrastructure for provide.io ecosystem."""

from __future__ import annotations

from provide.foundation.utils.versioning import get_version

__version__ = get_version("provide-foundry", caller_file=__file__)

__all__ = ["__version__"]
