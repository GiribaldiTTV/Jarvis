# Jarvis Desktop Assistant

Jarvis is a custom Windows desktop assistant project built around a Jarvis-inspired desktop presence, controlled launch flow, diagnostics tooling, and long-term boot-to-desktop orchestration goals.

This repository is an active development project and is not yet a packaged end-user release.

## Project Summary

Jarvis currently focuses on:

- A controlled Windows desktop launch path
- Startup reliability and recovery behavior
- Observability through logs, markers, and validation tooling
- Dev-only boot and transition testing
- A modular architecture that separates desktop runtime, diagnostics, audio, and developer tooling

The project is being developed incrementally, with emphasis on evidence-first changes and controlled iteration.

## Current Status

Jarvis is a work in progress.

Current active repository behavior includes:

- A normal/manual desktop launch path through:
  - `launch_jarvis_desktop.vbs`
  - `desktop/jarvis_desktop_launcher.pyw`
  - `desktop/jarvis_desktop_main.py`
- A separate dev-only boot harness through `main.py`
- Boot/desktop transition testing and validation tooling
- Internal diagnostics, observability, and regression support

Important note:
- `main.py` is currently treated as a development harness, not the normal end-user entrypoint.

## Core Goals

- Build a stable Jarvis-style desktop assistant experience on Windows
- Keep launcher behavior deterministic and recoverable
- Improve visibility into startup, shutdown, and failure behavior
- Preserve a modular architecture across desktop, boot, diagnostics, and tooling
- Reduce visible friction between major Jarvis phases over time

## High-Level Architecture

Jarvis currently operates in two primary modes:

### 1. Desktop Runtime Path
Normal/manual desktop launch path:

- `launch_jarvis_desktop.vbs`
- `desktop/jarvis_desktop_launcher.pyw`
- `desktop/jarvis_desktop_main.py`

### 2. Dev Boot / Transition Harness
Development-focused boot and transition path:

- `main.py`
- supporting wrappers and launchers under `dev/launchers/`

This dev path is used for controlled testing, transition checks, and internal validation work.

### Main Component Areas

- `desktop/` — desktop launcher and runtime behavior
- `Audio/` — voice/audio-related modules
- `dev/` — developer tooling, launchers, harnesses, and validation utilities
- `Docs/` — architecture, planning, backlog, and source-of-truth documentation
- `logs/` — runtime and validation artifacts

## Repository Layout

Top-level areas currently include:

- `Audio/`
- `desktop/`
- `dev/`
- `Docs/`
- `jarvis_visual/`
- `logs/`

Primary manual launch entry:

- `launch_jarvis_desktop.vbs`

Primary dev harness entry:

- `main.py`

## How To Run

### Normal / Manual Desktop Launch
Run:

```text
launch_jarvis_desktop.vbs
