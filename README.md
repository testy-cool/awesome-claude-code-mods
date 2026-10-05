# Awesome Claude Code mods [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

Claude Code mods worth keeping. A mod is a Claude Code plugin made of function hooks. It can draw panes, bands above the prompt, status lines and pictures, change how replies look, and react to every tool call.

This repo is also a plugin marketplace, so every mod listed here installs with two commands:

```bash
claude plugin marketplace add testy-cool/awesome-claude-code-mods
claude plugin install glowup@awesome-claude-code-mods
```

Each entry points at the author's own repository, so you always get their latest version.

## Contents

- [Appearance](#appearance)
- [Add one](#add-one)

## Appearance

- [prismantis](https://github.com/NahumLitvin/prismantis) by Nahum Litvin. Draws replies in color: tables, code, headings, Mermaid diagrams and charts, in 15 themes. Install with `claude plugin install prismantis@awesome-claude-code-mods`.
- [glowup](https://github.com/NovusEdge/glowup) by Aliasgar Khimani. A live cockpit pane for changes, subagents and context, an activity band above the prompt, a status line, themes and a pixel pet that acts out what Claude is doing. Install with `claude plugin install glowup@awesome-claude-code-mods`.
- [agent-portrait](https://github.com/testy-cool/claude-agent-portraits) by testy-cool. An animated pixel-art portrait above the prompt that thinks, talks, reads, types, winces at failures and sleeps when idle. Draws a custom character from a description or a photo. Install with `claude plugin install agent-portrait@awesome-claude-code-mods`.

## Add one

Open a pull request that adds the mod to this README and to `.claude-plugin/marketplace.json`. The mod should live in its own public repository with a license, and `claude plugin validate .` should pass in this repo.

## License

The list is [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Each mod keeps its own license.
