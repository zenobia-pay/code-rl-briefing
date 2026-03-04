# Briefing Process Contract

When Ryan says "do a briefing", run this exact pipeline in order for the requested topic/date window:

1. **step-01-papers-alphaxiv**
   - Go to `https://www.alphaxiv.org/` first.
   - Find relevant papers for the topic/time window.
   - Save exact query prompt + raw results + normalized papers.

2. **step-02-supergrok-topic**
   - Use browser-use.com (saved profile) to open X + SuperGrok.
   - Ask the topic query prompt exactly.
   - Save exact prompt + raw output + normalized tweet list.

3. **step-03-supergrok-paper-discussion**
   - For each paper title from step-01, ask SuperGrok exactly:
     "what are people saying about this exact paper title?"
   - Save prompt and output per paper.

4. **step-04-signals-pass**
   - Ask SuperGrok what tracked signal accounts discussed today for this topic.

5. **step-05-history-updates**
   - Ask SuperGrok for updates tied to 1/3/7/14-day prior briefing bullets.

6. **step-06-exa-people**
   - Call Exa API with deep search category=people.
   - Save exact API request payloads + responses.

7. **step-07-synthesis**
   - Build one-pager from persisted files only.

## Required Artifacts Per Step

Each step writes under `data/runs/YYYY-MM-DD/steps/step-XX-name/`:
- `prompt.txt` (exact prompt/query sent)
- `story.md` (plain-English what was done)
- `raw.*` (raw API/browser output)
- `normalized.json` (structured output)

This contract is the durable definition of "run briefing".