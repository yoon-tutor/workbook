"""Run the existing, unmodified tests with the deployed workspace adapter."""
import argparse
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--runtime', type=Path, default=ROOT)
args = parser.parse_args()
sys.dont_write_bytecode = True
sys.path.insert(0, str(args.runtime.resolve()))
from workbook_mcp.runtime_entry import bind_workspace
bind_workspace(ROOT)
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
