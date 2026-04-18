#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Memray stress test for config extraction hot paths.

Exercises extract_base_mkdocs and extract_python_wrknv_tasks — the core
shutil.copytree / file-copy chains that run on every docs setup.
"""

import os

os.environ.setdefault("LOG_LEVEL", "ERROR")

from pathlib import Path
import shutil
import tempfile

CYCLES = 50


def main() -> None:
    from provide.foundry.config import extract_base_mkdocs

    # Warmup — single cycle to prime imports / caches
    with tempfile.TemporaryDirectory() as tmp:
        extract_base_mkdocs(Path(tmp))

    # Stress: repeated extraction cycles into fresh temp dirs
    for _i in range(CYCLES):
        tmp = tempfile.mkdtemp(prefix="foundry_stress_")
        try:
            extract_base_mkdocs(Path(tmp))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    print(f"extract stress complete: {CYCLES} cycles")


if __name__ == "__main__":
    main()
