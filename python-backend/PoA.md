# PoA – Phase-wise (Clean & Logical)

👉 **This phase = product readiness**

## PHASE 5 – Frontend Integration (React)

**Goal: Real user flow**

- Paste YouTube URL
- Show "Processing…"
- Enable chat when ready
- Streaming answers
- History per video

👉 **This phase = user experience**


## Feature (On UI)
When LLM answers a question, show a clickable link that opens YouTube at that exact moment.

## What to Build

### 1. Update Prompt
Tell LLM to mention timestamps in answer

### 2. Parse Response
Extract timestamp from LLM answer

### 3. Generate YouTube Link
Format: `https://youtube.com/watch?v=VIDEO_ID&t=26s`

### 4. Show in UI
Display clickable "Watch at 26s" button

## Example

**User asks:** "What is backpropagation?"

**LLM answers:** "Backpropagation is explained at 25.8 seconds..."

**UI shows:**
```
Answer: Backpropagation is when...
[📺 Watch at 25s] ← Clickable, opens YouTube video at 25 seconds
```


# Session ID Design (When Frontend Is Ready)

## Goal
Each chat conversation must have a **stable identifier** so the backend knows **which conversation to continue**.

---

## 1. Frontend Responsibility

### When a user starts a **new chat**
- Frontend generates a new `session_id`
- Use a UUID (random, unique string)

Example:
session_id = "c8a1f3c2-92bd-4e2a-9f31-7a9e..."


Frontend stores this:
- React state
- or `localStorage`
- or URL parameter (optional)

---

## 2. Frontend → Backend Contract

Every API request must include:

```json
{
  "videoId": "youtube_video_id",
  "session_id": "chat_session_id",
  "question": "User question"
}

```
## Frontend PoA

# Frontend Plan of Action

1. Build one screen with:
   - YouTube URL input
   - Question input
   - Ask button

2. On submit:
   - Call `/api/v1/youtube/query`
   - Store `videoId` from backend flow

3. If response = PROCESSING:
   - Show loader
   - Poll `/video-status/{videoId}` every 3–5 seconds

4. When status becomes READY:
   - Show answer text
   - Show timestamps as clickable YouTube links

5. Allow follow-up questions:
   - Reuse same videoId
   - Send only new question
   - Display responses like chat

6. Handle errors:
   - FAILED → show message + reset option
   - Empty input → block submit

Frontend does UI only.
Backend does all logic.
