from pathlib import PurePosixPath, PureWindowsPath
import unittest
from workbook_mcp.bundle import runtime_path_key


class RuntimeOrderingTests(unittest.TestCase):
    def test_linux_and_windows_manifest_order_is_identical(self):
        names = ['workbook_engine/templates/README.md',
                 'workbook_engine/templates/preview.html',
                 'workbook_engine/templates/preview-data.js',
                 'workbook_engine/templates/renderer.js']
        expected = sorted(names, key=str.casefold)
        for path_type in (PurePosixPath, PureWindowsPath):
            result = sorted(map(path_type, names), key=runtime_path_key)
            self.assertEqual(expected, [path.as_posix() for path in result])
