### Prototype

**You own the design decision, not the production code. The prototype is a throwaway instrument. The real build follows Feature.**

Speed over polish; code quality does not matter; no formal planning required. The rigor is in picking the right design cheaply. Propose variations the user did not ask for, throw an approach away, and try another.

1. **Scope the Decision:** State the specific decision the prototype exists to make: layout, interaction, state density, data structure, or timing. No decision means no prototype; route to Feature.
2. **Gather References:** When the design space is open, search for prior art, summarize architectural options, and compare tradeoffs before building.
3. **Build in Isolated Scratch Directory:** Build throwaway code in `.scratch/` or a temporary isolated directory, strictly separate from production source. Use vanilla HTML/CSS/JS or the lightest script that answers the question. No production framework indirection, no tests, no abstractions.
4. **Compare Alternatives Side-by-Side:** When comparing alternatives, build 2–3 competing prototypes side-by-side behind a single switcher or comparative runner (**principle-exhaust-the-design-space**).
5. **Verify Empirically:** For visual decisions, render and observe interaction. For behavioral or timing decisions, log timings, print outputs, and observe runtime behavior directly. The observation is the test here, not unit assertions (**principle-prove-it-works**).
6. **Synthesize & Recommend:** Present alternatives, tradeoffs, and a clear recommendation. The output is an architectural decision, not shippable code. Hand the chosen direction to **Feature** (or **architect**) for production implementation.

**Reply:** variants explored, empirical observation, tradeoffs, recommendation, and scratch directory path. State plainly that the prototype is throwaway.
