"""Run agchk as a module with `python -m agchk`."""

from __future__ import annotations

import sys

from agchk.cli import main


if __name__ == "__main__":
    sys.exit(main())
