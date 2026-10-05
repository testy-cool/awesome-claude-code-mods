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

| Mod | What it does | Stars | Updated |
|-----|--------------|-------|---------|
| [prismantis](https://github.com/NahumLitvin/prismantis)<br>by Nahum Litvin | Draws replies in color: tables, code, headings, Mermaid diagrams and charts, in 15 themes. | ![stars](https://img.shields.io/github/stars/NahumLitvin/prismantis?style=flat&label=) | ![last commit](https://img.shields.io/github/last-commit/NahumLitvin/prismantis?style=flat&label=) |
| [glowup](https://github.com/NovusEdge/glowup)<br>by Aliasgar Khimani | A live cockpit pane for changes, subagents and context, an activity band, a status line, themes and a pixel pet that acts out what Claude is doing. | ![stars](https://img.shields.io/github/stars/NovusEdge/glowup?style=flat&label=) | ![last commit](https://img.shields.io/github/last-commit/NovusEdge/glowup?style=flat&label=) |
| [agent-portrait](https://github.com/testy-cool/claude-agent-portraits)<br>by testy-cool | An animated pixel-art portrait above the prompt that thinks, talks, reads, types, winces at failures and sleeps when idle. Draws a custom character from a description or a photo. | ![stars](https://img.shields.io/github/stars/testy-cool/claude-agent-portraits?style=flat&label=) | ![last commit](https://img.shields.io/github/last-commit/testy-cool/claude-agent-portraits?style=flat&label=) |

Install any of them with `claude plugin install <mod>@awesome-claude-code-mods`.

## Add one

Open a pull request that adds the mod to the right table in this README and to `.claude-plugin/marketplace.json`. The mod should live in its own public repository with a license, and `claude plugin validate .` should pass in this repo.

## License

The list is [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Each mod keeps its own license.
