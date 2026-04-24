# Impression Memory

Advanced agents need more than facts and skills.

Facts answer: "What is true?"

Skills answer: "How do I do this procedure?"

Impressions answer: "What does this remind me of, and what route should I try first?"

## Core Claim

An impression chunk is a lightweight associative memory. It is not an authoritative fact and not a full procedure. It is a concept-level cue that helps the agent recall a useful direction without loading an entire map.

Example:

> I live near Hangzhou Normal University in Yuhang. If I want to visit Longxiangqiao near West Lake, I do not need to memorize the whole Hangzhou metro map. I only need the impression that Line 5 can get me there. That cue is enough to start the trip and recover the details on demand.

This is the missing middle layer in many agent systems.

## Three Memory Types

| Memory Type | Purpose | Example | Failure When Overused |
|-------------|---------|---------|-----------------------|
| Fact memory | Store assertions and preferences | "User lives near Hangzhou Normal University in Yuhang" | Becomes a database of disconnected claims |
| Skill memory | Store reusable procedures | "How to create an upstream PR" | Becomes rigid SOP execution |
| Impression memory | Store associative concept cues | "Yuhang to West Lake: Line 5 is the route hint" | Can become vague if treated as truth |

Impressions should be used as retrieval hints, not final evidence.

## Design Shape

An impression chunk can be small:

```json
{
  "cue": "Yuhang Hangzhou Normal University to West Lake Longxiangqiao",
  "impression": "Line 5 is the route hint; retrieve exact transfer details only when needed.",
  "linked_concepts": ["Hangzhou", "metro", "Line 5", "West Lake", "Longxiangqiao"],
  "confidence": 0.72,
  "not_a_fact": true,
  "not_a_skill": true
}
```

Good impression chunks are:

- short
- associative
- easy to invalidate
- connected to concepts
- useful for first-hop retrieval

They should not pretend to be:

- exact historical logs
- verified facts
- complete task procedures
- immutable user preferences

## Agent OS Mapping

In OS terms, impressions are closer to an associative cache index than a file or executable.

They help the agent decide which page to fault in, which skill to inspect, or which fact cluster to verify. They reduce blind search and full-context loading.

## Scanner Implication

`agchk` should warn when a project has fact memory and skill memory but no sign of impression chunks.

The warning does not mean every project needs a complex memory OS. It means the project may be missing the human-like layer that turns isolated records into fast conceptual recall.
