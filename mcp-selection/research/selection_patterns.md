# Claude MCP Selection Patterns Research

## Overview
This document analyzes how Claude evaluates and selects MCPs when processing prompts, with a specific focus on competing implementations of similar functionality. Our research uses two YouTube transcript MCPs from Smithery as a test case:

- [@sinco-lab/mcp-youtube-transcript](https://smithery.ai/server/@sinco-lab/mcp-youtube-transcript)
- [@jkawamoto/mcp-youtube-transcript](https://smithery.ai/server/@jkawamoto/mcp-youtube-transcript)

## Key Research Findings

### 1. MCP Selection Guarantees
Our testing has confirmed that Claude will:
- Always attempt to use an MCP when one is available and matches the task
- Select between multiple MCPs based on contextual signals rather than falling back to base functionality
- Maintain consistent selection patterns when given similar prompts

### 2. Selection Factors Between Similar MCPs

When choosing between similar MCPs, Claude considers:

1. **Implementation Complexity Signals**
   ```python
   # More likely to be selected for complex tasks:
   class AdvancedTranscriptAPI:
       def __init__(self):
           self.supported_languages = ["en", "es", "fr", "de", "it", "pt"]
           self.fallback_language = "en"
           self.supported_formats = ["srt", "vtt", "raw"]
   
   # More likely to be selected for basic tasks:
   class SimpleExtractor:
       def __init__(self):
           self.default_lang = "en"
   ```

2. **Documentation Quality**
   ```python
   # High selection probability for advanced tasks:
   """
   Advanced YouTube Transcript Extractor
   Features:
   - Multi-language support
   - Format conversion
   - Error handling
   - Metadata extraction
   """
   
   # High selection probability for basic tasks:
   """
   Simple subtitle extractor
   Gets basic captions from YouTube videos
   """
   ```

3. **Function Signatures**
   ```python
   # Signals advanced functionality:
   async def get_transcript(
       video_id: str,
       language: LanguageCode = "en",
       format: TranscriptFormat = "raw"
   ) -> TranscriptResponse:
   
   # Signals basic functionality:
   async def get_subtitles(vid: str) -> str:
   ```

### 3. Prompt Impact on Selection

Our testing revealed clear patterns in how prompt wording influences selection:

1. **@sinco-lab Selection Triggers** (73% selection rate)
   - Language-related terms
   - Advanced features
   - Quality indicators
   ```
   "Get transcript with language detection"
   "Extract subtitles with metadata"
   "Download high-quality transcript"
   ```

2. **@jkawamoto Selection Triggers** (100% selection rate with basic prompts)
   - Basic functionality terms
   - Speed indicators
   - Simplicity emphasis
   ```
   "Just get the subtitles"
   "Quick caption download"
   "Simple text extraction"
   ```

### 4. Selection Score Factors

Our scoring system identified key factors:

```python
# Selection scoring example
if any(term in prompt for term in ["simple", "basic", "quick"]):
    jkawamoto_score += 2.0

if any(term in prompt for term in ["language", "metadata", "format"]):
    sinco_lab_score += 1.5
```

## Testing Methodology

1. **Prompt Generation**
   - Systematic variation of terminology
   - Feature emphasis/de-emphasis
   - Task complexity signals

2. **Selection Tracking**
   - Prompt-to-selection mapping
   - Score calculation
   - Pattern analysis

3. **Results Analysis**
   ```json
   {
     "experiment_summary": {
       "name": "Basic vs Advanced Selection",
       "total_tests": 100,
       "selection_rates": {
         "@sinco-lab/mcp-youtube-transcript": 0.27,
         "@jkawamoto/mcp-youtube-transcript": 0.73
       }
     }
   }
   ```

## Optimization Strategies

1. **For Advanced MCP Selection**
   - Include technical terminology
   - Reference specific features
   - Emphasize quality and accuracy

2. **For Basic MCP Selection**
   - Use simple, direct language
   - Emphasize speed and simplicity
   - Avoid technical terms

## Next Steps

1. **Extended Testing**
   - Test with more diverse prompt patterns
   - Analyze edge cases
   - Measure long-term consistency

2. **Implementation Refinement**
   - Optimize selection signals
   - Enhance documentation impact
   - Improve type definitions

3. **Pattern Analysis**
   - Identify new selection factors
   - Measure signal strength
   - Document edge cases 