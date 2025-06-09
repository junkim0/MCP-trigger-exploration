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

## Repository Structure

```
mcp-selection/
├── research/           # Analysis of Claude's selection patterns
├── optimization/       # MCP implementations and selection enhancement
├── testing/           # Selection testing framework and results
└── docs/             # Documentation and findings
```

## Key Features

### Selection Testing Framework
- Automated testing of MCP selection patterns
- Detailed prompt analysis and scoring
- Comprehensive results tracking
- Selection rate optimization

### Implementation Comparison
- Feature-rich vs. basic implementations
- Selection trigger analysis
- Effectiveness measurement

### Results Analysis
- Detailed test results in JSON format
- Selection pattern visualization
- Trigger word effectiveness tracking
- Historical test comparison

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

## Key Findings

Our research has shown that Claude's MCP selection can be influenced through:
1. Specific prompt wording and terminology
2. Feature emphasis or de-emphasis
3. Implementation complexity signals
4. Context clarity and specificity

## Contributing

Contributions are welcome! Areas of interest include:
- Additional MCP comparison cases
- New selection optimization techniques
- Enhanced testing methodologies
- Results visualization improvements

## License

MIT 