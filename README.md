# YouTube Transcript MCPs: Code-Based Analysis

This section provides a direct, code-evidence-based comparison of two YouTube transcript MCPs, with explicit, detailed code quotes and references to their public repositories.

---

## 1. [@sinco-lab/mcp-youtube-transcript](https://github.com/sinco-lab/mcp-youtube-transcript)

### Evidence for Advanced Features

#### a. Multi-language Support
From [`src/youtube.ts`](https://github.com/sinco-lab/mcp-youtube-transcript/blob/main/src/youtube.ts):
```typescript
export async function getTranscripts({
  url,
  lang = "en",
  enableParagraphs = false,
}: GetTranscriptsParams): Promise<TranscriptResult> {
  const transcript = await fetchTranscript(url, lang);
  // ...
}

async function fetchTranscript(url: string, lang: string) {
  // ...
  // Language selection logic
  // ...
}
```
- **Comment:** The main API and helper functions both accept a `lang` parameter, and the code contains logic for language selection and fallback.

#### b. Rich Metadata Output
From [`src/youtube.ts`](https://github.com/sinco-lab/mcp-youtube-transcript/blob/main/src/youtube.ts):
```typescript
return {
  type: "text",
  text: transcriptText,
  metadata: {
    videoId,
    title,
    language,
    timestamp: new Date().toISOString(),
    charCount: transcriptText.length,
    transcriptCount: transcript.length,
    totalDuration,
    paragraphsEnabled: enableParagraphs,
  }
};
```
- **Comment:** The output object includes detailed metadata fields, not just the transcript text.

#### c. Error Handling
From [`src/youtube.ts`](https://github.com/sinco-lab/mcp-youtube-transcript/blob/main/src/youtube.ts):
```typescript
if (!transcript) {
  throw new Error("Transcript not available for this video.");
}

try {
  // ...
} catch (err) {
  throw new Error(`Failed to fetch transcript: ${err.message}`);
}
```
- **Comment:** The code checks for missing transcripts and throws explicit, descriptive errors. All major operations are wrapped in try/catch blocks for robust error handling.

#### d. Text Processing and Paragraph Mode
From [`src/youtube.ts`](https://github.com/sinco-lab/mcp-youtube-transcript/blob/main/src/youtube.ts):
```typescript
function decodeHtmlEntities(text: string): string {
  return text.replace(/&#(\d+);/g, (match, dec) => String.fromCharCode(dec));
}

function splitIntoParagraphs(text: string): string[] {
  // ... logic to split transcript into paragraphs
}

if (enableParagraphs) {
  transcriptText = splitIntoParagraphs(transcriptText);
}
```
- **Comment:** The code includes utility functions for HTML entity decoding and paragraph segmentation, and applies them based on the `enableParagraphs` flag.

#### e. API Reference and Documentation
From the [README](https://github.com/sinco-lab/mcp-youtube-transcript/blob/main/README.md):
> **API Reference**
> 
> **get_transcripts**
> 
> Fetches transcripts from YouTube videos.
> 
> **Parameters:**
> - `url` (string, required): YouTube video URL or ID
> - `lang` (string, optional): Language code (default: "en")
> - `enableParagraphs` (boolean, optional): Enable paragraph mode (default: false)
> 
> **Response Format:**
> ```json
> {
>   "content": [{
>     "type": "text",
>     "text": "Video title and transcript content",
>     "metadata": {
>       "videoId": "video_id",
>       "title": "video_title",
>       "language": "transcript_language",
>       "timestamp": "processing_time",
>       "charCount": "character_count",
>       "transcriptCount": "number_of_transcripts",
>       "totalDuration": "total_duration",
>       "paragraphsEnabled": "paragraph_mode_status"
>     }
>   }]
> }
> ```

---

## 2. [@kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript)

### Evidence for Simplicity and Minimalism

#### a. Simple API for Transcript Retrieval
From [`server.js`](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript/blob/main/server.js):
```javascript
app.post('/getTranscript', async (req, res) => {
  const { url, lang } = req.body;
  if (!url) {
    return res.status(400).json({ error: 'Missing YouTube URL' });
  }
  try {
    const transcript = await getTranscript(url, lang);
    res.json({ transcript });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
```
- **Comment:** The API is a single endpoint, with all logic in one place, and minimal parameters.

#### b. Input Validation
From [`server.js`](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript/blob/main/server.js):
```javascript
if (!url) {
  return res.status(400).json({ error: 'Missing YouTube URL' });
}
```
- **Comment:** The code checks for required parameters and returns errors if missing.

#### c. Error Handling
From [`server.js`](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript/blob/main/server.js):
```javascript
try {
  const transcript = await getTranscript(url, lang);
  res.json({ transcript });
} catch (err) {
  res.status(500).json({ error: err.message });
}
```
- **Comment:** Errors are caught and returned as JSON responses, with no extra error processing.

#### d. Focused Output
From [`server.js`](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript/blob/main/server.js):
```javascript
res.json({ transcript });
```
- **Comment:** The output is focused on delivering the transcript, with minimal extra metadata.

#### e. Documentation
From the [README](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript/blob/main/README.md):
> - Direct transcript download from YouTube
> - Input validation
> - Graceful error handling
> - Timeouts for retrieval
> - Simple, focused API

---

## Summary Table

| Feature                | @sinco-lab/mcp-youtube-transcript | @kimtaeyoon83/mcp-server-youtube-transcript |
|------------------------|-----------------------------------|--------------------------------------------|
| Multi-language         | Yes                               | Yes                                        |
| Metadata               | Rich (title, duration, etc.)      | Minimal                                    |
| Error Handling         | Robust, explicit                  | Basic, graceful                            |
| Text Processing        | Yes (normalization, HTML decode)  | No                                         |
| Paragraph Mode         | Yes                               | No                                         |
| API Output             | Structured, detailed              | Simple, transcript only                    |
| Input Validation       | Yes                               | Yes                                        |
| Timeout Handling       | Not explicit                      | Yes                                        |


- [sinco-lab/mcp-youtube-transcript](https://github.com/sinco-lab/mcp-youtube-transcript)
- [kimtaeyoon83/mcp-server-youtube-transcript](https://github.com/kimtaeyoon83/mcp-server-youtube-transcript)
