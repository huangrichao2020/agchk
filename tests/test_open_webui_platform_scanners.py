from __future__ import annotations

from pathlib import Path

from agchk.audit import run_audit
from agchk.config import AuditConfig
from agchk.maturity import score_maturity
from agchk.scanners.pipeline_middleware_integrity import scan_pipeline_middleware_integrity
from agchk.scanners.plugin_execution_policy import scan_plugin_execution_policy
from agchk.scanners.rag_pipeline_governance import scan_rag_pipeline_governance
from agchk.scanners.tool_server_boundary import scan_tool_server_boundary


def _titles(findings: list[dict]) -> list[str]:
    return [finding["title"] for finding in findings]


def test_rag_pipeline_governance_flags_retrieval_without_controls(tmp_path: Path) -> None:
    (tmp_path / "rag.py").write_text(
        "\n".join(
            [
                "RAG_FULL_CONTEXT = True",
                "def rag_query(query):",
                "    embedding = embed(query)",
                "    vector_store.add(document_upload)",
                "    docs = vector_db.search(query)",
                "    return knowledge_base.answer(docs)",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_rag_pipeline_governance(tmp_path)

    assert "RAG pipeline lacks retrieval governance" in _titles(findings)
    assert "RAG full-context mode lacks context budget" in _titles(findings)


def test_rag_pipeline_governance_accepts_chunked_budgeted_ingestion(tmp_path: Path) -> None:
    (tmp_path / "rag.py").write_text(
        "\n".join(
            [
                "def rag_query(query):",
                "    chunks = split_documents(document_upload, chunk_size=500, chunk_overlap=50)",
                "    content_hash = calculate_hash(chunks)",
                "    ingest_status = reindex_if_changed(content_hash)",
                "    docs = vector_db.search(query, top_k=5)",
                "    ranked = rerank(docs, max_context_tokens=4000, retrieval_budget=5)",
                "    return knowledge_base.answer(ranked)",
            ]
        ),
        encoding="utf-8",
    )

    assert scan_rag_pipeline_governance(tmp_path) == []


def test_plugin_execution_policy_flags_dynamic_plugins_without_policy(tmp_path: Path) -> None:
    (tmp_path / "functions.py").write_text(
        "\n".join(
            [
                "class Pipe:",
                "    def __init__(self):",
                "        self.valves = Valves()",
                "",
                "    async def pipe(self, body, __user__):",
                "        code = body['plugin_code']",
                "        module = importlib.import_module(body['function_name'])",
                "        exec(code)",
                "        requirements = body.get('requirements', [])",
                "        subprocess.run(['pip', 'install', *requirements])",
                "        return module.run(body)",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_plugin_execution_policy(tmp_path)

    assert "Executable plugin system lacks sandbox policy" in _titles(findings)
    assert "Plugin dependency installation lacks supply-chain policy" in _titles(findings)


def test_plugin_execution_policy_accepts_sandboxed_plugins(tmp_path: Path) -> None:
    (tmp_path / "functions.py").write_text(
        "\n".join(
            [
                "ALLOWED_PACKAGES = {'pandas==2.2.0'}",
                "PINNED_REQUIREMENTS = {'pandas': 'sha256:abc'}",
                "PLUGIN_SCOPE = {'read_scope': ['/workspace'], 'write_scope': ['/workspace/out']}",
                "",
                "class Pipe:",
                "    def __init__(self):",
                "        self.valves = Valves()",
                "",
                "    async def pipe(self, body, __user__):",
                "        require_permission(__user__, PLUGIN_SCOPE)",
                "        sandbox = create_sandbox(timeout=30, capability=PLUGIN_SCOPE)",
                "        validate_package_allowlist(body['requirements'], ALLOWED_PACKAGES, PINNED_REQUIREMENTS)",
                "        return sandbox.run(body['plugin_code'])",
            ]
        ),
        encoding="utf-8",
    )

    assert scan_plugin_execution_policy(tmp_path) == []


def test_tool_server_boundary_flags_untrusted_remote_tool_loading(tmp_path: Path) -> None:
    (tmp_path / "tools.py").write_text(
        "\n".join(
            [
                "TOOL_SERVER_CONNECTIONS = [",
                "    {'type': 'openapi', 'url': 'http://localhost:8080/openapi.json'},",
                "    {'type': 'mcp', 'url': 'http://localhost:3000/mcp'},",
                "]",
                "def load_tools(server_url):",
                "    spec = requests.get(server_url + '/openapi.json').json()",
                "    tools = load_spec(spec)",
                "    terminal = tools['shell']",
                "    return terminal.execute('git push')",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_tool_server_boundary(tmp_path)

    assert "Remote tool server lacks trust-boundary policy" in _titles(findings)
    assert "Remote tool schema is not pinned or versioned" in _titles(findings)
    assert "High-agency remote tools lack approval boundary" in _titles(findings)


def test_tool_server_boundary_accepts_pinned_authenticated_tools(tmp_path: Path) -> None:
    (tmp_path / "tools.py").write_text(
        "\n".join(
            [
                "ALLOWED_SERVERS = {'https://tools.example.com'}",
                "SCHEMA_VERSION = '2026-04-01'",
                "SPEC_SHA256 = 'abc123'",
                "def load_tools(server_url):",
                "    assert server_url in ALLOWED_SERVERS",
                "    spec = requests.get(server_url + '/openapi.json', timeout=10, headers=auth_headers()).json()",
                "    validate_jsonschema(spec, schema_version=SCHEMA_VERSION, sha256=SPEC_SHA256)",
                "    tools = load_openapi_spec(spec)",
                "    require_approval(tools['shell'], policy='needs_approval')",
                "    return tools",
            ]
        ),
        encoding="utf-8",
    )

    assert scan_tool_server_boundary(tmp_path) == []


def test_pipeline_middleware_integrity_flags_mutation_without_observability(tmp_path: Path) -> None:
    (tmp_path / "pipeline.py").write_text(
        "\n".join(
            [
                "class Filter:",
                "    def inbound(self, messages):",
                "        messages = sanitize(messages)",
                "        messages = redact(messages)",
                "        return inject_prompt(messages)",
                "",
                "    def outbound(self, response):",
                "        return translate(response)",
                "",
                "pipeline_filters = [Filter()]",
            ]
        ),
        encoding="utf-8",
    )

    findings = scan_pipeline_middleware_integrity(tmp_path)

    assert "LLM pipeline mutates messages without audit trail" in _titles(findings)
    assert "LLM pipeline order is implicit" in _titles(findings)
    assert "LLM pipeline lacks filter failure policy" in _titles(findings)


def test_pipeline_middleware_integrity_accepts_ordered_audited_filters(tmp_path: Path) -> None:
    (tmp_path / "pipeline.py").write_text(
        "\n".join(
            [
                "class Filter:",
                "    stage = 'inbound'",
                "    priority = 10",
                "",
                "    def inbound(self, messages):",
                "        raw_message = list(messages)",
                "        try:",
                "            transformed_message = sanitize(messages)",
                "        except Exception:",
                "            fail_closed('sanitize failed')",
                "        audit_log.record(raw_message=raw_message, transformed_message=transformed_message)",
                "        return transformed_message",
                "",
                "FILTER_ORDER = sorted([Filter()], key=lambda item: item.priority)",
            ]
        ),
        encoding="utf-8",
    )

    assert scan_pipeline_middleware_integrity(tmp_path) == []


def test_open_webui_inspired_scanners_are_enabled_in_personal_audits(tmp_path: Path) -> None:
    test_rag_pipeline_governance_flags_retrieval_without_controls(tmp_path)
    test_plugin_execution_policy_flags_dynamic_plugins_without_policy(tmp_path)
    test_tool_server_boundary_flags_untrusted_remote_tool_loading(tmp_path)
    test_pipeline_middleware_integrity_flags_mutation_without_observability(tmp_path)

    results = run_audit(str(tmp_path), config=AuditConfig.from_profile("personal"), verbose=False)
    titles = _titles(results["findings"])

    assert "RAG pipeline lacks retrieval governance" in titles
    assert "Executable plugin system lacks sandbox policy" in titles
    assert "Remote tool server lacks trust-boundary policy" in titles
    assert "LLM pipeline mutates messages without audit trail" in titles


def test_maturity_score_rewards_open_webui_platform_primitives(tmp_path: Path) -> None:
    (tmp_path / "platform_agent.md").write_text(
        "\n".join(
            [
                "methodology: platform agent governance rubric",
                "RAG knowledge_base uses chunk_size, chunk_overlap, top_k, retrieval_budget, rerank, and hybrid_search",
                "plugin sandbox policy uses allowed_packages, pinned requirements, plugin_scope, and capability limits",
                "MCP and OpenAPI tool servers use trusted_servers, schema_validation, schema_version, timeout, and auth",
                "pipeline middleware keeps raw_message and transformed_message in audit_log with filter_order and fail_closed",
            ]
        ),
        encoding="utf-8",
    )

    score = score_maturity(tmp_path, findings=[])

    assert "RAG governance" in score["strengths"]
    assert "plugin sandbox policy" in score["strengths"]
    assert "remote tool boundary" in score["strengths"]
    assert "middleware observability" in score["strengths"]
