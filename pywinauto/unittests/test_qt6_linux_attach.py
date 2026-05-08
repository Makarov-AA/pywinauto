# -*- coding: utf-8 -*-
"""Linux attach tests for the Qt6 backend.

Run from WSL/Linux under DBus/Xvfb, for example:
    PYTHONPATH=... dbus-run-session -- xvfb-run -a env QT_QPA_PLATFORM=xcb \
        python3 -m unittest pywinauto.unittests.test_qt6_linux_attach
"""

from __future__ import unicode_literals

import os
import sys
import time
import unittest


if sys.platform == "win32":
    raise unittest.SkipTest("Linux Qt attach tests require Linux")

sys.path.append(".")
from pywinauto import Application, Desktop  # noqa: E402
from pywinauto.timings import Timings  # noqa: E402


qt_samples_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "apps", "Qt6_samples_linux"))
qt_tree_app = os.path.join(qt_samples_folder, "editabletreemodel")
qt_spreadsheet_app = os.path.join(qt_samples_folder, "spreadsheet")


def _set_timings():
    """Setup timings for Qt related tests."""
    Timings.defaults()
    Timings.window_find_timeout = 20


class Qt6EditableTreeLinuxTests(unittest.TestCase):
    """Tests for the Qt6 editable tree model sample."""

    def setUp(self):
        """Start Qt6 editable tree model sample application."""
        _set_timings()

        self.app = Application(backend="qt6")
        self.app = self.app.start(qt_tree_app)
        time.sleep(2)

    def tearDown(self):
        """Close application after tests."""
        self.app.kill()

    def test_explicit_pid_roots(self):
        root = self.app.window().find(timeout=15)
        self.assertEqual(root.element_info.process_id, self.app.process)
        self.assertEqual(root.window_text(), "Editable Tree Model")
        self.assertGreater(len(root.children()), 0)

    def test_atspi_pid_discovery_by_title(self):
        windows = Desktop(backend="qt6").windows(name="Editable Tree Model")
        self.assertEqual(len(windows), 1)
        self.assertEqual(windows[0].element_info.process_id, self.app.process)
        self.assertEqual(windows[0].window_text(), "Editable Tree Model")

    def test_tree_path_actions(self):
        root = self.app.window().find(timeout=15)
        tree = root.by(control_type="Tree", class_name="QTreeView").find(timeout=10)
        self.assertEqual(tree.item_text((0,)), "Getting Started")
        tree.collapse((0,))
        self.assertTrue(tree.is_collapsed((0,)))
        tree.expand((0,))
        self.assertTrue(tree.is_expanded((0,)))


class Qt6SpreadsheetLinuxTests(unittest.TestCase):
    """Tests for the Qt6 spreadsheet sample."""

    def setUp(self):
        """Start Qt6 spreadsheet sample application."""
        _set_timings()

        self.app = Application(backend="qt6")
        self.app = self.app.start(qt_spreadsheet_app)
        time.sleep(2)

    def tearDown(self):
        """Close application after tests."""
        self.app.kill()

    def test_table_cell_actions(self):
        root = self.app.window().find(timeout=15)
        table = root.by(control_type="Table", class_name="QTableWidget").find(timeout=10)
        self.assertEqual(table.cell_text(0, 0), "Item")
        table.select(0, 0)
        self.assertTrue(table.is_cell_selected(0, 0))
        table.set_cell_value(0, 0, "changed")
        self.assertEqual(table.cell_text(0, 0), "changed")


if __name__ == "__main__":
    unittest.main()
