# MCP Selection Optimization

This repository focuses on understanding and influencing Claude's MCP (Model Context Protocol) selection behavior. The primary goal is to develop and test methods for:

1. Ensuring Claude consistently selects specific MCPs when multiple similar options are available
2. Validating that Claude properly utilizes MCPs rather than falling back to base functionality
3. Measuring and optimizing selection rates through prompt engineering

## Current Focus: YouTube Transcript MCPs

We're currently testing selection patterns using two similar YouTube transcript MCPs from Smithery:
- [@sinco-lab/mcp-youtube-transcript](https://smithery.ai/server/@sinco-lab/mcp-youtube-transcript)
- [@jkawamoto/mcp-youtube-transcript](https://smithery.ai/server/@jkawamoto/mcp-youtube-transcript)

These MCPs provide an ideal test case as they:
- Share identical core functionality (YouTube transcript extraction)
- Have different implementation characteristics
- Allow us to measure and influence Claude's selection preferences

## Key Findings

Our research has revealed several important patterns in Claude's MCP selection behavior:

### Selection Triggers
- @sinco-lab/mcp-youtube-transcript is favored by:
  - Language-related terms (e.g., "transcript", "language detection")
  - Advanced feature requests (e.g., "metadata", "formatting")
  - Quality indicators (e.g., "accurate", "detailed")
  
- @jkawamoto/mcp-youtube-transcript is favored by:
  - Basic functionality terms (e.g., "simple", "basic", "plain")
  - Speed indicators (e.g., "quick", "fast", "rapid")
  - Simplicity emphasis (e.g., "nothing fancy", "keep it simple")

### Selection Rates
- Initial testing showed @sinco-lab at 73% vs @jkawamoto at 27%
- After optimizing for basic functionality, @jkawamoto achieved 100% selection rate
- Most effective prompts combine "simple", "basic", "quick", and "nothing fancy"

## Repository Structure

```
mcp-selection/
├── research/           # Analysis of Claude's selection patterns
├── optimization/       # MCP implementations and selection enhancement
├── testing/           # Selection testing framework and results
└── docs/             # Documentation and findings
```

## Testing Framework

Our testing framework includes:

1. Automated test generation with varied prompts
2. Detailed selection pattern analysis
3. Comprehensive results tracking in JSON format
4. Selection rate optimization through prompt engineering

### Results Format
Each test result JSON file includes:
- Summary of results (selection rates, patterns)
- Test methodology description
- Experiment parameters
- Detailed prompt analysis
- Selection triggers and their effectiveness

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run selection tests:
```bash
python mcp-selection/testing/transcript_selection_test.py
```

3. View results in `mcp-selection/testing/results/`

## Contributing

Contributions are welcome! Areas of interest include:
- Additional MCP comparison cases
- New selection optimization techniques
- Enhanced testing methodologies
- Results visualization improvements

## License

MIT 