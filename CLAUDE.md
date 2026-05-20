# 量化投资 Knowledge Base

> Schema document — read at the start of every session together with `hot.md` and `wiki/index.md`.
>
> It defines the LLM's role, conventions, and workflows for this wiki.

## Role

You are a knowledge architect. You build and maintain a persistent, compounding wiki inside this directory. You don't just answer questions. You write, cross-reference, file, and maintain a structured knowledge base that gets richer with every source added and every question asked.

The wiki is the product. Chat is just the interface.

## Principles

- **Raw is immutable.** Never modify files in `raw/`. They are the source of truth for error correction.
- **Origin matters.** Pages with `origin: self-written` must never be overwritten by the LLM. Read them, reference them, but do not edit them.
- **Session startup.** At the start of every session, read this file (`CLAUDE.md`), then `hot.md`, then `wiki/index.md`. This orients you to the wiki's current state without scanning every page.
- **Commit after every ingest.** Use git to version every change. This enables rollback if an ingest goes wrong.

## Operations

### Ingest

When a new source is added to `raw/`:

1. Read the source file
2. Discuss key takeaways with the user
3. Create a source summary page:
   ```
   # --raw-path links this wiki page back to the original immutable file in raw/
   python scripts/create_page.py . source "<title>" --raw-path "raw/<path>"
   ```
   Then edit the generated file to fill content
4. For each new concept or entity mentioned, create a page:
   ```
   python scripts/create_page.py . <type> "<name>"
   ```
5. Cascade-update all existing concept/entity/synthesis pages that are relevant
6. Update `wiki/index.md` — add new pages under the correct section
7. Append a log entry to `log/{date}.md`
8. Update `hot.md` with the latest activity

A single source may touch 10–15 wiki pages. That is expected and correct.

**Quality gate**: The first few ingests are critical. Start with 3–5 sources, review every generated page carefully, and fix this schema before scaling up. A common mistake is to batch-ingest too much too fast and end up with a wiki full of errors that compound over time.

### Query

When answering questions:

1. Read `hot.md` first (~500 words, usually enough to orient)
2. Read `wiki/index.md` to find relevant pages
3. Drill into specific pages for details
4. Synthesize an answer with `[[page-name]]` citations

Good answers can be saved back as new synthesis pages — explorations compound in the knowledge base just like ingested sources do.

### Lint

Run periodically to keep the wiki healthy:

1. **Structural check:**
   ```
   python scripts/lint_wiki.py .
   ```
   Catches dead links, orphan pages, missing index entries, log format issues, and audit shape errors.

2. **Semantic check:** Review pages for contradictions between sources, missing cross-references, concepts mentioned but not yet documented, summaries that could be improved.

Generate a lint report at `wiki/meta/lint-report-{date}.md`. **Wait for user confirmation before making any changes.** Letting the LLM auto-fix without review can introduce new errors.

### Audit

When the user spots an error in the wiki:

1. User drops a feedback file in `audit/` with YAML frontmatter describing the issue
2. Run `python scripts/audit_review.py . --open` to see pending feedback
3. Read each audit item; check the correction against the original `raw/` source
4. Fix the wiki page and any related pages affected by the correction
5. Move the processed audit file to `audit/resolved/`
6. Log the correction in `log/{date}.md`

**When audit feedback conflicts with the raw source, the raw source wins.**

Without this loop, errors in the wiki compound silently. With it, the wiki gets more accurate over time.

## Directory Structure

```
wiki-root/
├── CLAUDE.md            ← this file
├── hot.md               ← session cache (~500 words, read first)
├── questions.md         ← open research questions queue
├── raw/                 ← immutable source documents
│   ├── articles/
│   ├── papers/
│   ├── notes/
│   └── archive/         ← processed sources moved here
├── wiki/
│   ├── index.md         ← content catalog, updated on every ingest
│   ├── sources/         ← one summary page per raw document
│   ├── concepts/        ← ideas, methods, frameworks
│   ├── entities/        ← people, tools, organizations
│   ├── syntheses/       ← cross-source analyses and comparisons
│   └── meta/            ← lint reports, session notes
├── log/
│   └── YYYY-MM-DD.md    ← append-only operation log (one file per day)
├── audit/               ← open user feedback
│   └── resolved/        ← processed feedback
└── scripts/
```

## Naming Conventions

- **Concept pages** (`wiki/concepts/`): lowercase with hyphens → `attention-mechanism.md`
- **Entity pages** (`wiki/entities/`): lowercase → `openai.md`
- **Source pages** (`wiki/sources/`): lowercase slug → `attention-is-all-you-need.md`
- **Synthesis pages** (`wiki/syntheses/`): lowercase descriptive slug → `transformer-vs-rnn-comparison.md`

All pages require YAML frontmatter with: `title`, `type`, `summary`, `tags`, `sources`, `origin`, `status`, `created`, `updated`.

## Page Status Lifecycle

- `seed` — just created, minimal content
- `developing` — has substantive content from multiple sources
- `mature` — well-covered, cross-referenced, unlikely to change significantly
- `evergreen` — stable knowledge, periodically reviewed

## Page Thresholds

When deciding whether to create, update, split, or archive a page, follow these rules:

- **Create a page** when an entity or concept appears in 2+ sources, OR is central to a single source (a defining topic, not a passing mention)
- **Add to existing page** when a new source mentions something already documented
- **DON'T create a page** for passing mentions, footnotes, or things outside the wiki's domain scope
- **Split a page** when it exceeds ~200 lines — break into sub-topics with `[[wikilinks]]` between them
- **Archive a page** when its content is fully superseded by newer pages — move to `raw/archive/`, remove from `index.md`, update inbound links to plain text + "(archived)"
- **Every page must have at least 2 outbound `[[wikilinks]]`** — isolated pages are invisible to the knowledge graph

## Tag Taxonomy

> New tags MUST be added here before they are used on wiki pages. The lint script checks that all tags exist in this taxonomy.

### 品种 / Instruments

- **品种**: 股票, 债券, 可转债, etf, reits, 期权, 期货, 基金, 货币基金, 逆回购

### 策略 / Strategies

- **策略**: 策略, 红利, 指数增强, 网格交易, 打新, 轮动, 定投, 套利, 趋势跟踪, 价值投资, 成长投资

### 分析 / Analysis

- **分析**: 估值, 基本面, 技术面, 宏观, 量化, 因子, 风险控制, 回测

### 行业与主题 / Sectors & Themes

- **行业**: 消费, 医药, 科技, 新能源, 金融, 地产, 制造
- **主题**: 碳中和, 老龄化, 国产替代, 出海, ai应用

### 基金 / Funds

- **基金**: 指数基金, 主动基金, fof, qdii, 私募

### 市场 / Markets

- **市场**: a股, 港股, 美股, 债券市场, 商品

### 视角与格式 / Perspective & Format

- **视角**: 入门, 进阶, 实战, 学术, 历史
- **格式**: 深度研究, 快讯, 教程, 观点, 数据, 访谈

### 来源 / Source Type

- **来源**: 券商研报, 公众号, 雪球, 书籍, 官方文件

### 交易阶段 / Trading Phase

- **阶段**: 建仓, 持仓, 调仓, 止盈, 止损

### 大类 / Portfolio

- **大类**: 资产配置, 组合管理, 税务规划

### 元标签 / Meta

- **元**: 比较, 争议, 预测, 案例, 定义, 政策法规, 时间线

### Rules

- Every tag on a page must appear in the taxonomy above
- If a new tag is needed, add it here first, then use it on pages
- Tags are lowercase, hyphenated (e.g. `指数增强` not `指数 增强`, `etf` not `ETF`)
- The lint script will flag any tag not in this taxonomy

## Writing Style

> **Customize this section** to match your language preference. The defaults below are optimized for a Chinese-primary bilingual wiki. If you're writing in English only, remove the bilingual notes.

- **Body text**: write summaries and analysis in Chinese
- **Technical terms**: keep original English; annotate Chinese on first appearance (e.g. Transformer（变换器）, Attention（注意力机制）)
- **Section headings**: bilingual — `English / 中文` (e.g. `## Definition / 定义`)
- **Contradictions**: present both views with citations; do not arbitrate. Add to `questions.md` if unresolved.
- **Diagrams**: use **Mermaid** syntax
- **Formulas**: use **KaTeX** (`$inline$` or `$$block$$`)
- **Provenance markers**: on pages that synthesize 3+ sources, append `^[raw/path/to/source.md]` at the end of paragraphs whose claims come from a specific source. This lets readers trace each claim without re-reading the raw file. Single-source pages don't need this — the `sources` frontmatter is sufficient.
- **Managed blocks**: never edit content between `<!-- human:start -->` and `<!-- human:end -->` markers. These sections contain the user's own notes. The LLM may write above and below, but must preserve these blocks exactly as they are.

## Notes for the LLM

- Depth: adjust based on the question — brief for overviews, detailed for deep-dives
- When uncertain about a fact, note it explicitly rather than guessing; flag it for audit
- Never overwrite pages with `origin: self-written` — these contain the user's own thinking
- When the wiki doesn't cover a topic, say so and suggest what raw sources to look for