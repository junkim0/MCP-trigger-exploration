# MCP Selection Analysis

A personal project exploring how to influence Claude's MCP (Model Context Protocol) selection behavior, specifically testing with YouTube transcript MCPs.

## Overview

This project analyzes and tests different approaches to influence which MCP Claude selects when multiple options are available. Currently focused on two YouTube transcript MCPs:
- @sinco-lab/mcp-youtube-transcript
- @jkawamoto/mcp-youtube-transcript

## Key Findings

### Selection Patterns
- @sinco-lab is favored by:
  - Language-related terms
  - Advanced feature requests
  - Quality indicators
  - Translation and multilingual contexts
- @jkawamoto is favored by:
  - Basic functionality terms
  - Speed indicators
  - Simplicity emphasis
  - Documentation and analysis contexts

### Selection Rates
- Initial test: @sinco-lab (73%) vs @jkawamoto (27%)
- After optimization: @sinco-lab (0%) vs @jkawamoto (100%)
- Blender-inspired test: @sinco-lab (53%) vs @jkawamoto (47%)

## Project Structure

```
mcp-selection/
├── research/          # Selection pattern analysis
├── optimization/      # MCP implementations
├── testing/          # Selection testing framework
└── docs/             # Documentation
```

## Testing Framework

The project includes two testing approaches:

1. **Basic Selection Testing**
   - Measures raw selection patterns
   - Tracks feature usage
   - Records selection rates

2. **Blender-Inspired Testing**
   - Context-aware selection analysis
   - Project-type based testing
   - Detailed feature usage tracking
   - Comprehensive results analysis

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   python mcp-selection/testing/transcript_selection_test.py
   python mcp-selection/testing/blender_inspired_test.py
   ```

## Results Format

Test results are saved in JSON format with:
- Timestamp
- Selection rates
- Context patterns
- Feature usage
- Detailed test history

## License

MIT License 