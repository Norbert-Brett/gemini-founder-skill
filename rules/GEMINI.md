# Gemini Founder Skill Operating Rules

When the Gemini Founder Skill plugin is active, Antigravity agents have access to eleven specialized business-validation skills that share state in the workspace's `founder/` directory:

```text
founder-board -> founder-competitors -> founder-consumer -> founder-pricing -> founder-offer -> founder-cfo -> founder-marketing -> founder-brand -> founder-ops -> founder-launch -> founder-plan
```

## 1. Shared Workspace State (`founder/`)
- All skills read and write files inside `founder/` in the active workspace (beginning with `founder/idea.md`).
- Each skill can run standalone or as part of the full sequence, building on whatever artifacts already exist in `founder/`.

## 2. Subagent Orchestration in Antigravity
- **`founder-board`**: Convene three independent board members in parallel using `invoke_subagent` (`TypeName: "self"`, `Model: "inherit"`), one for each framework in `lenses.md` (Offers, Monopoly, Product). Wait for reactive wakeup notifications when the three memos in `founder/board/` are written.
- **`founder-consumer`**: Deal buyer cards and briefs using `panel.py`, then dispatch buyer subagents in waves of up to 10 using `invoke_subagent` (`TypeName: "self"`, `Model: "flash"` or `"inherit"`). Using `Model: "flash"` allows 20-buyer (`--quick`) or 100-buyer panels to run fast and economically. Never fabricate or write a buyer answer yourself; every answer must come from a buyer subagent.

## 3. Evidence & Analytical Integrity
- **Published Frameworks Only**: The three board lenses apply published frameworks (*$100M Offers*, *Zero to One*, and Walter Isaacson's *Steve Jobs*). Never roleplay as those individuals, quote them, or claim their endorsement.
- **Public Sources with Links**: Competitor research, supplier pricing, and regulatory checks must cite verifiable public links. Never invent competitors, prices, ratings, or customer reviews.
- **Traceable Numbers**: Unit economics (`unit_economics.py`), price sensitivity (`van_westendorp.py`), and the final business plan verdict (`compile.py`) must be computed by the deterministic Python tools in each skill's directory. Never write a `Profitable` verdict by hand or guess missing inputs.
- **Honest Limits**: Simulated buyer panels surface objections and positioning gaps; always remind the user to validate major spend decisions with a real-world test (`founder-launch`) and professional legal/accounting review.
