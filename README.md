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
| [prismantis](https://github.com/NahumLitvin/prismantis)<br>by Nahum Litvin | Colorful, themeable replies: tables, code, diagrams, charts and tool rows in 15 themes. | ★ 39 | 2026-10-06 |
| [glowup](https://github.com/NovusEdge/glowup)<br>by Aliasgar Khimani | A live cockpit pane for changes, subagents and context, an activity band, shareable themes and a pixel pet. | ★ 11 | 2026-10-06 |
| [agent-portrait](https://github.com/testy-cool/claude-agent-portraits)<br>by testy-cool | Animated pixel-art portrait above the prompt that reacts to thinking, talking, tools, failures and idle time. | ★ 0 | 2026-10-05 |

### Games

| Mod | What it does | Stars | Last update |
|-----|--------------|------:|-------------|
| [spinlings](https://github.com/416rehman/spinlings)<br>by 416rehman | Creature collection, trading and saved-team player duels inside Claude Code 2.1.287+, with online and offline worlds. | ★ 1 | 2026-10-06 |
<!-- mods:end -->

Install any of them with `claude plugin install <mod>@awesome-claude-code-mods`.

## Finding new mods

Every Monday a GitHub Action opens an issue listing new mods and the ones gaining the most stars. It reads the catalogue that [karanb192/awesome-claude-code-mods](https://github.com/karanb192/awesome-claude-code-mods) builds by scanning GitHub every few hours, and skips mods that fail validation or are already listed here. The good ones get added.

## Add one

Open a pull request that adds the mod to `.claude-plugin/marketplace.json`. The tables in this README are built from that file, with stars and dates refreshed every day. The mod should live in its own public repository with a license, and `claude plugin validate .` should pass in this repo.

## License

The list is [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Each mod keeps its own license.
