# -*- coding: utf-8 -*-
"""Linux attach tests for the Qt5 backend.

Run from WSL/Linux under DBus/Xvfb, for example:
    PYTHONPATH=... dbus-run-session -- xvfb-run -a env QT_QPA_PLATFORM=xcb \
        python3 -m unittest pywinauto.unittests.test_qt5_linux_attach
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
    os.path.dirname(__file__), "..", "..", "apps", "Qt5_samples_linux"))
qt_styles_app = os.path.join(qt_samples_folder, "styles")
qt_interview_app = os.path.join(qt_samples_folder, "interview")


def _set_timings():
    """Setup timings for Qt related tests."""
    Timings.defaults()
    Timings.window_find_timeout = 20


class Qt5StylesLinuxTests(unittest.TestCase):
    """Tests for the Qt5 styles sample."""

    def setUp(self):
        """Start Qt5 styles sample application."""
        _set_timings()

        self.app = Application(backend="qt5")
        self.app = self.app.start(qt_styles_app)
        time.sleep(2)

    def tearDown(self):
        """Close application after tests."""
        self.app.kill()

    def test_explicit_pid_roots(self):
        root = self.app.window().find(timeout=15)
        self.assertEqual(root.element_info.process_id, self.app.process)
        self.assertEqual(root.window_text(), "Styles")
        self.assertGreater(len(root.children()), 0)

    def test_atspi_pid_discovery_by_title(self):
        windows = Desktop(backend="qt5").windows(name="Styles")
        self.assertEqual(len(windows), 1)
        self.assertEqual(windows[0].element_info.process_id, self.app.process)
        self.assertEqual(windows[0].window_text(), "Styles")

    def test_common_widget_actions(self):
        root = self.app.window().find(timeout=15)
        combo = root.by(control_type="ComboBox").find(timeout=10)
        self.assertGreaterEqual(combo.item_count(), 1)
        self.assertIn(combo.selected_text(), combo.texts())

        edit = root.by(control_type="Edit", class_name="QLineEdit", name="s3cRe7").find(timeout=10)
        edit.set_edit_text("linux")
        self.assertEqual(edit.window_text(), "linux")


class Qt5InterviewLinuxTests(unittest.TestCase):
    """Tests for the Qt5 interview sample."""

    def setUp(self):
        """Start Qt5 interview sample application."""
        _set_timings()

        self.app = Application(backend="qt5")
        self.app = self.app.start(qt_interview_app)
        time.sleep(2)

    def tearDown(self):
        """Close application after tests."""
        self.app.kill()

    def test_tree_and_table_models(self):
        root = self.app.window().find(timeout=15)
        tree = root.by(control_type="Tree", class_name="QTreeView").find(timeout=10)
        self.assertEqual(tree.item_text((0,)), "Item 0:0")
        tree.expand((0,))
        self.assertTrue(tree.is_expanded((0,)))

        table = root.by(control_type="Table", class_name="QTableView").find(timeout=10)
        self.assertGreater(table.row_count(), 0)
        self.assertGreater(table.column_count(), 0)


if __name__ == "__main__":
    unittest.main()
