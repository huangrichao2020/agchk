# Code-Level Anti-Patterns

Concrete grep-searchable patterns to find agent wrapper failures in source code.

These patterns are auto-generated from the [agchk](https://github.com/huangrichao2020/agchk) Python scanners.
Each section lists the regex patterns used by that scanner.

## Usage

```bash
pip install agchk
agchk /path/to/your/agent/project
```

Or run individual grep scans manually:

## Code Execution

**Scanner file**: `agchk/scanners/code_execution.py`

**Default severity**: `medium`

**Regex patterns**:

- `\bexec\s*\(`
- `\beval\s*\(`
- `\bcompile\s*\(`
- `\bos\.system\s*\(`
- `\bnew\s+Function\s*\(`
- `subprocess\..*shell\s*=\s*True`
- `(?:sandbox|docker|container|seccomp|chroot|\bvm\b|`
- `subprocess.*timeout|resource\.setrlimit|jail|`
- `nsjail|firejail|gvisor|kata)`
- `: `

## Hidden Llm

**Scanner file**: `agchk/scanners/hidden_llm.py`

**Default severity**: `high`

**Regex patterns**:

- `(?:chat\.create|messages\.create|completions\.create|llm\.invoke|`
- `fallback.*llm|repair.*prompt|second.*pass|re-prompt|`
- `openai\.chat|anthropic\.messages|vertexai\.predict|`
- `bedrock.*invoke|model\.generate|completion\.create)`
- `(?:agent.*loop|main.*loop|orchestrat|chain.*run|agent.*run|`
- `agent_executor|react.*loop|tool.*loop|cycle.*run)`
- `: `
- `: `

## Memory Patterns

**Scanner file**: `agchk/scanners/memory_patterns.py`

**Default severity**: `low`

**Regex patterns**:

- `(?:memory.*admit|long.?term.*update|persist.*memory|save.*to.*memory|`
- `memory.*store|write.*memory|commit.*memory|memory.*insert)`
- `(?:add.*memory|upsert.*vector|append.*context|history.*append|`
- `messages.*append|memory.*push|context.*grow|buffer.*append|`
- `memory.*add|vector.*insert|embeddings.*store)`
- `(?:max_|limit|ttl|expire|k=|top_|threshold|trim|truncate|`
- `max_|_max|capacity|bounded|evict|prune|retention|window_size)`
- `: `
- `: `

## Observability

**Scanner file**: `agchk/scanners/observability.py`

**Default severity**: `medium`

**Regex patterns**:

- `(?:langsmith|langfuse|opentelemetry|arize|phoenix|`
- `callback.*handler|tracer|telemetry|observ|`
- `cost.*track|token.*count|latency.*track|`
- `span.*create|trace.*start|metric.*record|`
- `promptlayer|helicone|braintrust|smith\.ai|`
- `langsmith\.run|langfuse\.track|otel\.|open telemetry)`
- `: `

## Output Pipeline

**Scanner file**: `agchk/scanners/output_pipeline.py`

**Default severity**: `medium`

**Regex patterns**:

- `(?:mutate.*response|rewrite.*output|transform.*answer|shape.*response|`
- `post.?process.*llm|stream.*chunk|yield.*token|format.*response|`
- `response.*filter|output.*sanitize|strip.*tag|clean.*response|`
- `response.*hook|after.*llm|post.*llm)`
- `(?:buffer|assemble|reconstruct|join|concat|merge.*stream|`
- `chunk.*buffer|response.*build|output.*assemble|token.*stream)`
- `: `

## Secrets

**Scanner file**: `agchk/scanners/secrets.py`

**Default severity**: `critical`

**Regex patterns**:

- `sk-[a-zA-Z0-9]{20,}`
- `ghp_[a-zA-Z0-9]{36}`
- `glpat-[a-zA-Z0-9]{20,}`
- `AKIA[0-9A-Z]{16}`
- `(?i)(?:api[_-]?key|apikey|secret[_-]?key|token)\s*[=:]\s*['\`
- `(?:example|your_|placeholder|xxx|test)`
- `: `

## Tool Enforcement

**Scanner file**: `agchk/scanners/tool_enforcement.py`

**Default severity**: `high`

**Regex patterns**:

- `(?:must use tool|required call|always use|tool is required|`
- `required to call|you must call|mandatory tool use)`
- `(?:tool_call|toolCall|tool_use|function_call|tool_choice|use_tool)`
- `(?:assert |if not |raise |\.validate|\.check|verify|guard|enforce|sanity_check)`
- `: `
- `: `
