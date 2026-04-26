from agchk.scanners.bug_inference import scan_bug_inference


def test_flags_tracked_root_repair_script(tmp_path):
    (tmp_path / "fix2.py").write_text(
        """
from pathlib import Path

target = Path("src/infra/heartbeat-runner.ts")
content = target.read_text()
content = content.replace("runHeartbeat()", "await runHeartbeat()")
target.write_text(content)
""",
        encoding="utf-8",
    )

    findings = scan_bug_inference(tmp_path)

    assert any(finding["title"] == "Tracked one-off repair script can hide stale bugfix state" for finding in findings)


def test_flags_path_like_dynamic_import_without_file_url_normalization(tmp_path):
    (tmp_path / "plugin-loader.ts").write_text(
        """
import path from "node:path";

export async function loadPlugin(root: string) {
  const entryPath = path.resolve(root, "plugin.ts");
  return import(entryPath);
}
""",
        encoding="utf-8",
    )

    findings = scan_bug_inference(tmp_path)

    assert any(
        finding["title"] == "Dynamic import may receive filesystem path without file URL normalization"
        for finding in findings
    )


def test_ignores_dynamic_import_with_file_url_normalization(tmp_path):
    (tmp_path / "plugin-loader.ts").write_text(
        """
import path from "node:path";
import { pathToFileURL } from "node:url";

export async function loadPlugin(root: string) {
  const entryPath = path.resolve(root, "plugin.ts");
  return import(pathToFileURL(entryPath).href);
}
""",
        encoding="utf-8",
    )

    titles = {finding["title"] for finding in scan_bug_inference(tmp_path)}

    assert "Dynamic import may receive filesystem path without file URL normalization" not in titles


def test_flags_unbounded_timer_delay(tmp_path):
    (tmp_path / "scheduler.ts").write_text(
        """
export function schedule(nextRunDelayMs: number) {
  return setTimeout(() => runOnce(), nextRunDelayMs);
}
""",
        encoding="utf-8",
    )

    findings = scan_bug_inference(tmp_path)

    assert any(finding["title"] == "Timer delay may exceed runtime setTimeout limits" for finding in findings)


def test_ignores_clamped_timer_delay(tmp_path):
    (tmp_path / "scheduler.ts").write_text(
        """
const MAX_TIMEOUT = 2_147_483_647;

export function schedule(nextRunDelayMs: number) {
  const timerDelay = Math.min(nextRunDelayMs, MAX_TIMEOUT);
  return setTimeout(() => runOnce(), timerDelay);
}
""",
        encoding="utf-8",
    )

    titles = {finding["title"] for finding in scan_bug_inference(tmp_path)}

    assert "Timer delay may exceed runtime setTimeout limits" not in titles
