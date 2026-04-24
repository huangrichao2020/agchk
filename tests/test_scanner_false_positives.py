from __future__ import annotations

from pathlib import Path

from agchk.scanners.code_execution import scan_code_execution
from agchk.scanners.hidden_llm import scan_hidden_llm_calls
from agchk.scanners.memory_patterns import scan_memory_patterns


def _titles(findings: list[dict]) -> list[str]:
    return [finding["title"] for finding in findings]


def test_re_compile_is_not_flagged_as_unsafe_code_execution(tmp_path: Path) -> None:
    (tmp_path / "regexes.py").write_text(
        "\n".join(
            [
                "import re",
                "EMAIL_RE = re.compile(r'[^@]+@[^@]+')",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_code_execution(tmp_path)

    assert "Unsafe code execution: compile(" not in _titles(findings)


def test_builtin_compile_remains_flagged(tmp_path: Path) -> None:
    (tmp_path / "danger.py").write_text(
        "compiled = compile(user_input, '<string>', 'exec')\n",
        encoding="utf-8",
    )

    findings = scan_code_execution(tmp_path)

    assert "Unsafe code execution: compile(" in _titles(findings)


def test_generated_chunk_asset_is_skipped_for_code_execution(tmp_path: Path) -> None:
    asset_dir = tmp_path / "console" / "assets"
    asset_dir.mkdir(parents=True)
    (asset_dir / "chunk-B4BG7PRW-Czrfivbn.js").write_text(
        "function x(){ exec(userInput) }\n",
        encoding="utf-8",
    )

    findings = scan_code_execution(tmp_path)

    assert findings == []


def test_duplicated_hashed_asset_copy_is_skipped_for_code_execution(tmp_path: Path) -> None:
    asset_dir = tmp_path / "console" / "assets"
    asset_dir.mkdir(parents=True)
    (asset_dir / "cytoscape.esm-BQaXIfA_ 2.js").write_text(
        "function x(){ exec(userInput) }\n",
        encoding="utf-8",
    )

    findings = scan_code_execution(tmp_path)

    assert findings == []


def test_provider_implementation_is_not_treated_as_hidden_llm(tmp_path: Path) -> None:
    providers_dir = tmp_path / "providers"
    providers_dir.mkdir()
    (providers_dir / "openai_provider.py").write_text(
        "\n".join(
            [
                "class OpenAIProvider:",
                "    def generate(self, prompt):",
                "        return self.client.chat.completions.create(messages=[{'role': 'user', 'content': prompt}])",
            ]
        ),
        encoding="utf-8",
    )
    (tmp_path / "main.py").write_text(
        "\n".join(
            [
                "from providers.openai_provider import OpenAIProvider",
                "def agent_loop(prompt):",
                "    provider = OpenAIProvider()",
                "    return provider.generate(prompt)",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_hidden_llm_calls(tmp_path)

    assert findings == []


def test_generated_chunk_asset_is_skipped_for_hidden_llm(tmp_path: Path) -> None:
    asset_dir = tmp_path / "console" / "assets"
    asset_dir.mkdir(parents=True)
    (asset_dir / "blockDiagram-VD42YOAC-Cb2bh-C5.js").write_text(
        "client.chat.completions.create(messages=[{'role':'user','content':'x'}])\n",
        encoding="utf-8",
    )

    findings = scan_hidden_llm_calls(tmp_path)

    assert findings == []


def test_repair_fallback_llm_call_is_still_flagged(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        "def agent_loop(prompt):\n    return prompt\n",
        encoding="utf-8",
    )
    (tmp_path / "repair_pass.py").write_text(
        "\n".join(
            [
                "def repair_output(client, prompt):",
                "    repair_prompt = f'Repair this: {prompt}'",
                "    return client.chat.completions.create(messages=[{'role': 'user', 'content': repair_prompt}])",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_hidden_llm_calls(tmp_path)

    assert "Hidden or secondary LLM call detected" in _titles(findings)


def test_memory_admission_alone_is_not_flagged(tmp_path: Path) -> None:
    (tmp_path / "memory_manager.py").write_text(
        "\n".join(
            [
                "def save_to_memory(record):",
                "    memory_store(record)",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_memory_patterns(tmp_path)

    assert findings == []


def test_unbounded_memory_growth_is_still_flagged(tmp_path: Path) -> None:
    (tmp_path / "history.py").write_text(
        "\n".join(
            [
                "def append_message(history, message):",
                "    history.append(message)",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_memory_patterns(tmp_path)

    assert "Memory growth without apparent limit" in _titles(findings)
