# Awesome Claude Code mods [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

Claude Code mods worth keeping. A mod is a Claude Code plugin made of function hooks. It can draw panes, bands above the prompt, status lines and pictures, change how replies look, and react to every tool call.

This repo is also a plugin marketplace, so every mod listed here installs with two commands:

```bash
claude plugin marketplace add testy-cool/awesome-claude-code-mods
claude plugin install glowup@awesome-claude-code-mods
```

Each entry points at the author's own repository, so you always get their latest version.

## Contents

- [Mods](#mods)
- [Finding new mods](#finding-new-mods)
- [Add one](#add-one)

## Mods

<!-- mods:start -->
### Appearance

| Mod | What it does | Stars | Last update |
|-----|--------------|------:|-------------|
| [skins](https://github.com/hellosverre/claude-skins) | Skins for Claude Code's transcript: themed tool rows, reply gutters and spinner words. /skin swaps them live. | ★ 75 | 2026-10-09 |
| [prismantis](https://github.com/NahumLitvin/prismantis) | Colorful, themeable replies: tables, code, diagrams, charts and tool rows in 15 themes. | ★ 71 | 2026-10-09 |
| [flightdeck](https://github.com/scasella/claude-flightdeck) | Flightdeck: a live agent dashboard for Claude Code. Main model vitals, an on-call architect, every permission check, subagent cards and swimlanes, a turn receipt and a session log, all from real session events | ★ 56 | 2026-10-02 |
| [pokemon](https://github.com/dgokcin/claude-pokemon-mod) | A pixel Pokémon that lives at the right edge of the band above the prompt | ★ 25 | 2026-10-09 |
| [glowup](https://github.com/NovusEdge/glowup) | A live cockpit pane for changes, subagents and context, an activity band, shareable themes and a pixel pet. | ★ 22 | 2026-10-08 |
| [human-in-the-loop](https://github.com/tzafrir/human-in-the-loop) | Claude assigns you the tasks only you can do. They wait in a My tasks pane, counted under the prompt, until you answer or reject them, so nothing Claude needs from you gets lost in the chat. | ★ 19 | 2026-10-05 |
| [paste-view](https://github.com/Amorfx/claude-paste-view) | See what you paste into Claude Code: image thumbnails and long-text previews above the prompt instead of bare [Image #1] and [Pasted text #2] tags | ★ 18 | 2026-10-09 |
| [desktop-statusline](https://github.com/centminmod/claude-plugins/tree/master/plugins/desktop-statusline) | Status band above the prompt in the Claude Desktop app's Code tab: folder, git branch and state, session age, prompt count and cost, a context meter, 5-hour and weekly plan usage limit meters with reset countdowns, last-turn model, duration and cache hit rate, idle time against the prompt-cache TTL, compactions, and running agents. Toasts at 80% and 95% of a usage limit. Draws only on the desktop surface, so a CLI statusLine is left alone. | ★ 15 | 2026-10-08 |
| [glass](https://github.com/rashedInt32/glass) | A desktop-app look for Claude Code's terminal: colored shell commands in prose, a Bottom line card, content-fit code cards, borderless tables, gutter marks beside paragraphs that need you, painted tool rows and a turn footer. | ★ 11 | 2026-10-09 |
| [agentpane](https://github.com/xuanji86/claude-agentpane) | A side pane for Claude Code that lists the subagents a session runs, what each is doing and what it costs in tokens, with each one's conversation a click away. | ★ 9 | 2026-10-04 |
| [deck](https://github.com/nvr0x5/claude-deck) | A cockpit for Claude Code: plan bars and subagent strips, context, usage limits with reset countdowns and burn rates, spend, the model route and a pet. Six bar styles, three collapsed looks. CLI and Desktop. | ★ 9 | 2026-10-10 |
| [pinboard](https://github.com/sirkitree/pinboard) | Keeps open decisions, the task list and links Claude creates in a sidebar pane, updated through its own tool | ★ 9 | 2026-10-07 |
| [claude-mods](https://github.com/ersinkoc/claude-mods) | KOZMOS — live, visual mods for Claude Code (CLI + desktop): bands above the prompt, sidebars, status ticker, companions, guards and sound. | ★ 9 | 2026-10-10 |
| [statuspane](https://github.com/xuanji86/claude-statuspane) | A floating status card above the Claude Code prompt — model, effort, context, 5h/week limits, cost, directory and branch, GitHub CI and deploys — with clickable settings and a progress-row API any script or mod can feed. | ★ 7 | 2026-10-08 |
| [figures](https://github.com/natsukium/claude-code-figures-plugin) | Draw diagrams, LaTeX math, and tool-result images inline in kitty-graphics terminals | ★ 6 | 2026-10-10 |
| [paneline](https://github.com/markneonin/paneline) | Claude Code mod (plugin) that adds a side pane with Activity, Files, Agents, Context and MCP tabs, a status line above the prompt, a restyled chat, Mermaid diagrams in the terminal, tables, and code and diff panels. Colours follow both /color and the /theme (dark, light and others). | ★ 6 | 2026-10-06 |
| [mdview](https://github.com/xuanji86/claude-mdview) | Click a .md path in the Claude Code conversation to read it rendered as markdown beside the session, pictures included, and point at any block to have Claude edit it. | ★ 6 | 2026-10-03 |
| [whats-agent-doing](https://github.com/tzafrir/whats-agent-doing) | A small box above the prompt that always says what the agent is doing right now (reading, thinking, writing, running a tool, waiting for you) and expands to show what it has done. | ★ 6 | 2026-10-04 |
| [remcycle](https://github.com/lianmatsuo/remcycle) | Garbage collection for Claude Code's memory. A mod that rereads your sessions every day, keeps what you decided, and questions the notes that have gone stale. | ★ 5 | 2026-10-07 |
| [fynn-mods](https://github.com/FynnXland/fynn-mods) | Six mods for Claude Code: animated Clawd mascot, usage-limit and prompt-cache bars, a pre-send message checker, quick replies, a to-do queue and a cost ledger. Terminal and desktop app, English/German. | ★ 3 | 2026-10-09 |
| [archpane](https://github.com/facumarcet/archpane/tree/main/plugins/archpane) | Live architecture diagram in a side pane that Claude draws and edits while you talk | ★ 3 | 2026-10-04 |
| [ricky-pixel-mod](https://github.com/muxia23/ricky-pixel-mod) | Ricky, a pixel-art cat companion for Claude Code: an animated night-sky pane with a task / subagent / activity / files board, a cat in the band above the prompt, and a purple-gold spinner | ★ 3 | 2026-10-05 |
| [dopa-mode](https://github.com/charimsma/dopa-mode/tree/main/plugin) | DOPA MODE (DOPA is short for dopamine) for Claude Code: fireworks for everything you do and every milestone Claude reaches (finished turns, commits, pushes, pull requests, passing tests), context and plan-limit meters with warnings, trophies, a daily command card and a focus timer. | ★ 3 | 2026-10-03 |
| [mod-store](https://github.com/hellosverre/mod-store) | An app store for Claude Code mods, inside Claude Code: /mods to browse, search and install 2,700 mods, or ask Claude to find one | ★ 2 | 2026-10-07 |
| [glanceflow](https://github.com/Antreas-Strb/glanceflow) | GlanceFlow for Claude Code: a calm checklist above the prompt showing the plan, progress and when Claude needs you. Simple view for everyone, Details for engineers. | ★ 2 | 2026-10-10 |
| [sessiondeck](https://github.com/NetipunJi/sessiondeck) | Live session dashboard mod for Claude Code: context, cache, permissions, tool latency, and a chart band for up to a hundred agents. | ★ 2 | 2026-10-05 |
| [claude-code-agent-monitor](https://github.com/NeriakTo/claude-code-agent-monitor) | A Claude Code mod: a band above the prompt and a /monitor pane tracking inbox, running tools, dispatches and custom cards. | ★ 2 | 2026-10-07 |
| [installguard](https://github.com/griches/installguard) | Claude Code mod: looks up every new package before Claude installs it, and holds made-up names, typosquats and days-old releases for your answer | ★ 2 | 2026-10-09 |
| [a2a-mod](https://github.com/NovusEdge/a2a-mod) | A2A protocol client for Claude Code: Claude hands tasks to non-Claude worker agents over Agent2Agent and picks up their results. | ★ 1 | 2026-10-04 |
| [claude-code-tint-mod](https://github.com/JimmySadek/claude-code-tint-mod) | Claude Code mod (CC tint mod): color each window by its repository, ring the window you are in, number your threads, and tint the whole Claude desktop app. Light and dark mode. | ★ 1 | 2026-10-09 |
| [agent-portrait](https://github.com/testy-cool/claude-agent-portraits) | Animated pixel-art portrait above the prompt that reacts to thinking, talking, tools, failures and idle time. | ★ 0 | 2026-10-05 |
| [repo-radar](https://github.com/lakmadev/repo-radar) | A live map of your codebase for Claude Code that lights up where Claude is working, with a colour per subagent. | ★ 0 | 2026-10-09 |
| [claude-devtools-mod](https://github.com/NMenzel/claude-devtools-mod) | Claude DevTools: a debugger for Claude Code tool calls. Breakpoints, pause/step/reject, timeline, inspector and Error Lens failure diagnosis, as a Claude Code mod. | ★ 0 | 2026-10-09 |
| [code-wrapped](https://github.com/lakmadev/code-wrapped) | Your Claude Code Wrapped: activity heatmap, coding personality and unlockable achievements, right in your terminal. | ★ 0 | 2026-10-09 |
| [glimt](https://github.com/mmedum/glimt) | A quiet side pane for Claude Code: what this session is doing, its plan, its agents, and every other session | ★ 0 | 2026-10-10 |
| [codyssey](https://github.com/delexw/codyssey) | Turn every Claude Code session into a little adventure: generative music that follows the agent's mood, a pixel knight who battles a monster for every edit and command, and a transcript retold in game style. | ★ 0 | 2026-10-10 |
<!-- mods:end -->

Install any of them with `claude plugin install <mod>@awesome-claude-code-mods`.

## Finding new mods

Every Monday a GitHub Action opens an issue listing new mods and the ones gaining the most stars. It reads the catalogue that [karanb192/awesome-claude-code-mods](https://github.com/karanb192/awesome-claude-code-mods) builds by scanning GitHub every few hours, and skips mods that fail validation or are already listed here. The good ones get added.

## Add one

Open a pull request that adds the mod to `.claude-plugin/marketplace.json`. The tables in this README are built from that file, with stars and dates refreshed every day. The mod should live in its own public repository with a license, and `claude plugin validate .` should pass in this repo.

## License

The list is [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Each mod keeps its own license.
