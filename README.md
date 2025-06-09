# YouTube Transcript MCP Selection Guide

This guide documents how different prompt patterns influence Claude's selection between two YouTube transcript MCPs:
- @sinco-lab/mcp-youtube-transcript
- @jkawamoto/mcp-youtube-transcript

## MCP Comparison

### @sinco-lab/mcp-youtube-transcript
- **Focus**: Advanced features and comprehensive functionality
- **Key Features**:
  - Multi-language support
  - Language detection
  - Metadata extraction
  - Timestamp preservation
  - Speaker detection
  - Error handling
  - Format conversion
- **Best For**: Complex transcript needs, multilingual content, detailed analysis

### @jkawamoto/mcp-youtube-transcript
- **Focus**: Basic functionality and simplicity
- **Key Features**:
  - Basic transcript extraction
  - Simple text output
  - Quick processing
  - Minimal overhead
- **Best For**: Basic transcript needs, simple text extraction, quick results

## Selection Patterns

### Prompts that favor @sinco-lab
1. **Language-related requests**:
   - "Get the transcript with language detection"
   - "Extract transcript in Spanish"
   - "Show me the French transcript"

2. **Advanced feature requests**:
   - "Get transcript with timestamps"
   - "Extract transcript with speaker detection"
   - "Get transcript with metadata"

3. **Quality-focused requests**:
   - "Get comprehensive transcript"
   - "Extract detailed transcript"
   - "Get accurate transcript with formatting"

### Prompts that favor @jkawamoto
1. **Basic functionality requests**:
   - "Get the subtitles"
   - "Show me the captions"
   - "Extract the text"

2. **Simple requests**:
   - "Get basic transcript"
   - "Quick transcript extraction"
   - "Simple text from video"

3. **Speed-focused requests**:
   - "Fast transcript"
   - "Quick captions"
   - "Rapid text extraction"

## Selection Analysis

### Key Factors
1. **Feature Keywords**
   - Advanced features → @sinco-lab
   - Basic features → @jkawamoto

2. **Language Complexity**
   - Technical terms → @sinco-lab
   - Simple terms → @jkawamoto

3. **Quality Indicators**
   - Quality/accuracy focus → @sinco-lab
   - Speed/simplicity focus → @jkawamoto

### Selection Guarantees
- Claude will always attempt to use an MCP when available
- Selection is based on contextual signals rather than random choice
- Consistent patterns emerge with similar prompts

## Best Practices

### For Advanced Features
1. Use technical terminology
2. Reference specific features
3. Emphasize quality and accuracy
4. Mention language requirements

### For Basic Features
1. Use simple, direct language
2. Emphasize speed and simplicity
3. Avoid technical terms
4. Focus on basic functionality

## Example Prompts

### @sinco-lab Examples
```json
{
  "advanced_features": [
    "Get the transcript with language detection for video_id",
    "Extract transcript with speaker detection and timestamps",
    "Show me the Spanish transcript with metadata",
    "Get comprehensive transcript with formatting",
    "Extract transcript with error handling"
  ],
  "language_focused": [
    "Get the French transcript with translation",
    "Show me the transcript in multiple languages",
    "Extract transcript with language detection"
  ],
  "quality_focused": [
    "Get accurate transcript with formatting",
    "Extract detailed transcript with timestamps",
    "Show me the comprehensive transcript"
  ]
}
```

### @jkawamoto Examples
```json
{
  "basic_functionality": [
    "Get the subtitles from video_id",
    "Show me the captions",
    "Extract the text",
    "Get basic transcript",
    "Show me what's said in the video"
  ],
  "simple_requests": [
    "Quick transcript",
    "Simple text extraction",
    "Basic captions",
    "Raw transcript"
  ],
  "speed_focused": [
    "Fast transcript",
    "Quick captions",
    "Rapid text extraction",
    "Instant subtitles"
  ]
}
```

## Selection Patterns Analysis

### Random Prompts
- @sinco-lab: ~50% selection rate
- @jkawamoto: ~50% selection rate
- Selection based on prompt content and context

### Feature-Specific Prompts
- @sinco-lab: 100% selection for advanced features
- @jkawamoto: 100% selection for basic features
- Clear distinction based on feature requirements

### Language-Focused Prompts
- @sinco-lab: 100% selection for language-specific requests
- @jkawamoto: 0% selection for language-specific requests
- Strong preference for @sinco-lab with language features 