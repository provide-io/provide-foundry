# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Documentation generation utilities."""

from __future__ import annotations

from provide.foundry.docs.gen_ref_pages import generate_reference_pages
from provide.foundry.docs.link_fixer import fix_md_links, process_file

__all__ = ["fix_md_links", "generate_reference_pages", "process_file"]
