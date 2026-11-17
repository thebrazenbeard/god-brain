"""Offline negative tests for untrusted workspace start-up source."""
from __future__ import annotations

import json
import struct
import tempfile
import unittest
from pathlib import Path

from tools.validate_workspace_hygiene import validate_workspace


class WorkspaceHygieneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ".vscode").mkdir()
        self.settings = self.root / ".vscode" / "settings.json"
        self.tasks = self.root / ".vscode" / "tasks.json"
        self.settings.write_text(
            json.dumps({"task.allowAutomaticTasks": "off"}), encoding="utf-8"
        )
        self.tasks.write_text(json.dumps({"version": "2.0.0", "tasks": []}),
                              encoding="utf-8")

    def test_repository_default_is_clean(self):
        repository = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_workspace(repository), [])

    def test_workspace_setting_must_explicitly_disable_auto_tasks(self):
        for value in (True, "on", None):
            with self.subTest(value=value):
                data = {} if value is None else {"task.allowAutomaticTasks": value}
                self.settings.write_text(json.dumps(data), encoding="utf-8")
                self.assertTrue(validate_workspace(self.root))

    def test_folder_open_task_is_rejected_even_with_setting_off(self):
        self.tasks.write_text(json.dumps({
            "tasks": [{
                "label": "eslint-check", "command": "node",
                "args": ["./public/fonts/fa-solid-600.ttf"],
                "runOptions": {"runOn": "folderOpen"},
            }]
        }), encoding="utf-8")
        self.assertTrue(any("folderOpen" in error
                            for error in validate_workspace(self.root)))

    def test_disguised_font_text_is_rejected_as_data_only(self):
        font = self.root / "public" / "fonts" / "fa-solid-600.ttf"
        font.parent.mkdir(parents=True)
        font.write_text("      var x = 'not-a-font';", encoding="utf-8")
        self.assertTrue(any("font" in error.lower()
                            for error in validate_workspace(self.root)))

    @staticmethod
    def _minimal_sfnt(*, base_offset=0, bad_first_offset=None):
        # Synthetic SFNT table envelopes, not real glyph or checksum verification.
        tags = (b"OS/2", b"cmap", b"head", b"hhea", b"hmtx", b"maxp",
                b"name", b"post", b"glyf", b"loca")
        start = base_offset + 12 + 16 * len(tags)
        directory = b"".join(
            tag + struct.pack(">III", 0,
                              bad_first_offset if idx == 0 and bad_first_offset is not None
                              else start + 4 * idx, 4)
            for idx, tag in enumerate(tags)
        )
        return (b"\x00\x01\x00\x00" +
                struct.pack(">HHHH", len(tags), 128, 3, 32) +
                directory + b"abcd" * len(tags))

    def test_sfnt_valid_table_directory_is_accepted(self):
        font = self.root / "public" / "fonts" / "test.ttf"
        font.parent.mkdir(parents=True)
        font.write_bytes(self._minimal_sfnt())
        self.assertEqual(validate_workspace(self.root), [])

    def test_sfnt_magic_without_table_directory_is_rejected(self):
        font = self.root / "public" / "fonts" / "magic-only.ttf"
        font.parent.mkdir(parents=True)
        font.write_bytes(b"OTTO" + bytes(12))
        self.assertTrue(any("font" in x.lower()
                            for x in validate_workspace(self.root)))

    def test_sfnt_table_offset_past_end_is_rejected(self):
        font = self.root / "public" / "fonts" / "offset.ttf"
        font.parent.mkdir(parents=True)
        font.write_bytes(self._minimal_sfnt(bad_first_offset=4096))
        self.assertTrue(any("font" in x.lower()
                            for x in validate_workspace(self.root)))

    def test_fake_sfnt_with_only_arbitrary_table_is_rejected(self):
        font = self.root / "public" / "fonts" / "fake.ttf"
        font.parent.mkdir(parents=True)
        font.write_bytes(b"\x00\x01\x00\x00" + struct.pack(">HHHH", 1, 16, 0, 0)
                         + b"AAAA" + struct.pack(">III", 0, 28, 0))
        self.assertTrue(any("font" in x.lower()
                            for x in validate_workspace(self.root)))

    def test_unaligned_table_record_offset_is_rejected(self):
        font = self.root / "public" / "fonts" / "unaligned.ttf"
        font.parent.mkdir(parents=True)
        font.write_bytes(self._minimal_sfnt(bad_first_offset=173))
        self.assertTrue(any("font" in x.lower()
                            for x in validate_workspace(self.root)))

    def test_invalid_ttc_container_is_rejected(self):
        font = self.root / "public" / "fonts" / "invalid-collection.ttf"
        font.parent.mkdir(parents=True)
        font.write_bytes(b"ttcf" + bytes(12))
        self.assertTrue(any("font" in x.lower()
                            for x in validate_workspace(self.root)))

    def test_ttc_valid_directory_is_accepted(self):
        font = self.root / "public" / "fonts" / "collection.ttf"
        font.parent.mkdir(parents=True)
        header = b"ttcf" + struct.pack(">II", 0x00010000, 1)
        font.write_bytes(header + struct.pack(">I", 16)
                         + self._minimal_sfnt(base_offset=16))
        self.assertEqual(validate_workspace(self.root), [])

    def test_public_nested_symlink_directory_is_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        public = self.root / "public"
        public.mkdir()
        try:
            (public / "fonts").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks unavailable on this host")
        self.assertTrue(any("symlink" in x.lower()
                            for x in validate_workspace(self.root)))

    def test_uppercase_disguised_font_extension_is_rejected(self):
        font = self.root / "public" / "fonts" / "FA-SOLID-600.TTF"
        font.parent.mkdir(parents=True)
        font.write_text("malformed-font", encoding="utf-8")
        self.assertTrue(any("font" in error.lower()
                            for error in validate_workspace(self.root)))

    def test_editor_directory_symlink_is_refused_before_read(self):
        editor = self.root / "editor"
        (self.root / ".vscode").rename(editor)
        try:
            (self.root / ".vscode").symlink_to(editor, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks unavailable on this host")
        self.assertTrue(any("symlink" in error
                            for error in validate_workspace(self.root)))

    def test_code_workspace_nested_auto_task_is_rejected(self):
        (self.root / "research.code-workspace").write_text(json.dumps({
            "folders": [{"path": "."}],
            "tasks": {"tasks": [
                {"runOptions": {"runOn": "folderOpen"}, "command": "echo"}
            ]},
        }), encoding="utf-8")
        self.assertTrue(validate_workspace(self.root))


if __name__ == "__main__":
    unittest.main()
