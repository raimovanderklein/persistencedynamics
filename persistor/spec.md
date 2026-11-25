# The persistor: specification

**Version 1.0 · 2026-11-24.** This is the canonical specification of the persistor, the unit of change in Persistence Dynamics. It states what the persistor is, the rules it obeys and how sure each rule is. Dated corrections and test results are in [HISTORY.md](HISTORY.md). The original working reference is kept in [archive/](archive/).

The persistor is also called the **Change Unit** and the **Quadragen**. All three names refer to the same concept in different shapes.

Each statement carries one of these labels:

- **[structural]** follows from the axioms and the definitions
- **[derived]** follows from structural statements plus one stated assumption
- **[open]** is stated and has not been decided by a test
- **[falsified]** failed a test. It is kept so that nobody relies on it

Every quantitative claim also appears in [claims.md](../claims.md) with its evidence.

---

## Part A: The core

### 1. Definition

**A persistor is a cycle that creates the structure for the next cycle to build on.** [structural]

A persistor is one moment in two dimensions, with four faces, and the moment iterates as a cycle. Two dimensions cross at a single point. At the crossing four things are true at once. They are four faces of one event, not four events. The cycle is how that moment repeats, and each completed turn produces the substrate the next turn runs on.

A persistor runs its four regimes in order: Potentiality, Construction, Encounter, Conservation, then Potentiality again. **Without closure there is no persistor.** The Conservation of one round becomes the Potentiality of the next, so the closure is the seed.

### 2. Axioms

Five axioms make up the seed. φ is not an axiom. It is the attractor that appears when the seed closes (§6).

| # | Axiom | Statement |
| --- | --- | --- |
| A1 | Hold and cross | A persistor has two operations at its boundary: hold (keep self) and cross (engage other). |
| A2 | Each on or off | Each operation is active or latent. A persistor has two bits. |
| A3 | Recursive | Every persistor contains persistors and sits inside one. The same two bits appear at every scale. |
| A4 | Mass conserved | Total mass across a closed system of persistors is constant. |
| A5 | Motion exists | Cycles run, gradients drive flows, and crossing engages. |

### 3. Two dimensions and four regimes

The **transactional dimension** is the axis of giving and taking, and it spans space. It runs from Potentiality, which receives, to Encounter, which gives. The **generational dimension** is the axis of loss and birth, and it spans time. It runs from Construction, which spends, to Conservation, which carries forward. [structural]

Two bits give four states, and each state is a regime with its own dynamics:

| Regime | Hold | Cross | Type | What it does |
| --- | --- | --- | --- | --- |
| Potentiality | active | active | Capacitor | Loads against a threshold, then releases at once |
| Construction | latent | active | Factory | Selects among candidates and builds one form |
| Encounter | latent | latent | Reactor | The form meets what it was built for, at many sites in parallel |
| Conservation | active | latent | Homeostat | Keeps what survived, releases the rest, and opens the next gap |

**Hold reads as past and cross reads as future.** Hold is what the persistor has accumulated: identity, lineage, memory and form already built. Cross is what it reaches toward. Potentiality holds the most past while reaching for the most future. Encounter releases both and is pure present. Conservation rebuilds the past while cross stays latent. [structural]

**Fixed layout.** Every drawing places Potentiality top-left, Construction top-right, Encounter bottom-right and Conservation bottom-left. Traversal is clockwise. The transactional diagonal joins Potentiality and Encounter, and the generational diagonal joins Construction and Conservation.

### 4. The regime types

Each regime is a distinct dynamical system, with its own observables, equation of motion and failure modes. [structural]

| Regime | Observables | Equation of motion | Characteristic failures |
| --- | --- | --- | --- |
| Potentiality (capacitor) | loading rate, charge, threshold | dCharge/dt = inflow − leak; fires when Charge ≥ threshold | loading stays below threshold; the threshold drifts; substrate is present but does not fit the gap |
| Construction (factory) | throughput, differentiation, yield | dOutput/dt = throughput × yield × differentiation fraction | throughput drops; differentiation is skewed; yield is low; output backs up |
| Encounter (reactor) | reaction rate, yield, balance | dProduct/dt = Σ over sites (rate × yield); balance = substrate in − substrate out | the rate is low; the yield is low; the balance is negative |
| Conservation (homeostat) | setpoint integrity, drift sensitivity, gap coherence | dState/dt = −k(state − setpoint) + drift; perturbation out = f(correction) | the setpoint is lost; nothing is released; over-correction; **gap erasure** (it closes without opening a next gap) |

#### 4.1 Potentiality makes the clock

- **The threshold turns a flow into a clock.** Without a threshold, outflow would track inflow and there would be no rhythm. The period is (threshold − resting state) ÷ loading current. [structural]
- **The capacitor shows a sign flip.** Below threshold the loading signal acts as a brake. Above threshold the same signal is the trigger. Finding this flip is how a capacitor is recognised. Examples are the cardiac pacemaker, the oestrogen-driven LH surge and T cell licensing. [structural]
- **Potentiality is a structured gap, not a full tank.** It is the gap-shape left by the previous Conservation, and it pulls on substrate. Construction's candidates compete on their fit to that gap. [structural]
- **Residence per unit is undefined at Potentiality.** What is measured is the pool's load-to-threshold dynamics, not how long any single unit stays. [structural]
- **Two clocks run in one decision.** Loading runs on *substrate time*: it takes as long as the substrate needs. After the discharge, the other three regimes run on *clock time*. A measurement made on clock time cannot see loading-phase work. [structural]
- **Every failure, traced down, ends at a capacitor that did not load.** This is the depth diagnostic. [open: argued from convergent phenomenology, with no cohort validation yet]

#### 4.2 Construction makes order

Of the four regimes, only Construction turns a symmetric field of candidates into a ranking. Potentiality outputs a scalar, Encounter outputs symmetric relations, and Conservation outputs a retained set. **Every before-and-after traces back to a Construction event.** Sequence is made in Construction. [structural; see R11]

#### 4.3 Conservation has two outputs

Conservation is bipartite. One closure event produces two outputs: the **lineage**, which carries forward, and the **gap**, which becomes the next Potentiality. Their edges match, because they were one piece before the cut. A Conservation that produces no gap closes into a loop that no longer adapts. [structural]

### 5. The four thresholds

Exactly one bit flips between each pair of regimes. Hold-axis and cross-axis flips alternate. [structural]

| Threshold | Transition | Bit that flips | Class |
| --- | --- | --- | --- |
| Activation | Potentiality → Construction | hold | within a generation |
| Egress | Construction → Encounter | cross | within a generation |
| Drain | Encounter → Conservation | hold | within a generation |
| Suppression | Conservation → Potentiality | cross | **passes a generation** |

At Suppression the receiver is a new cycle. From the ending cycle it reads as depth 4, and from the new one as depth 0.

### 6. The formal core

**Within one cycle the dynamics are lossless trigonometry.** At one level, a persistor is two coupled oscillators 90° apart, z(t) = e^(iωt). Its trajectory is a circle, the regimes are its four quadrants, and the thresholds are its four cardinal points. The radius does not shrink within one revolution, so dissipation happens only across levels. [structural]

```latex
\text{hold} = \frac{1-\cos\theta}{2}, \qquad \text{cross} = \frac{1+\sin\theta}{2}
```

The regime centres sit at θ = 135° (Potentiality), 45° (Construction), −45° (Encounter) and −135° (Conservation). Each regime spans 90° and holds four sub-positions of 22.5°, which makes **16 positions**. [structural]

**Across levels, closure fixes the contraction ratio.** For the recursion to be self-similar, the ratio d between levels must satisfy [derived: assumes self-similarity]

```latex
d^2 + d = 1 \quad\Rightarrow\quad d = \frac{1}{\varphi} \approx 0.618
```

**This is the only place φ enters.** Everything in the framework that contains φ descends from this equation. Across many levels, the circle becomes a φ-spiral. φ is a *sustained-imbalance* number. Perfect symmetry (½ + ½) has no gradient and does no work. φ splits a conserved whole unequally, which is just enough asymmetry to drive motion while the whole stays conserved.

**Damping.** One damped oscillator with γT = L · ln φ traces the same orbit as a lossless stack of L levels. L = 4 gives γT = 4 ln φ ≈ 1.924. [derived]

**Gate losses.** The drain at the two hold-axis gates is D = (1 − A)/φ + (1 − S)/φ², where A is the address match at Activation and S is the scale match at Drain. The exponents are set by gate depth. [derived; empirical fit open]

### 7. Recursion rules

These rules generate the whole structure. R4 is not used.

| Rule | Statement | Status |
| --- | --- | --- |
| R1 | **A closed cycle at level N is a single axis at level N+1.** Closure drops a dimension and hands one up. Unpacked, any axis is a four-regime cycle. | structural |
| R2 | **One diameter goes up, the other stays contained.** A closed cycle hands up one of its two diameters as the axis. The other becomes the contained radius at its own level. | structural |
| R3 | **The axis keeps its arrow.** The cycle runs one way, so the axis it becomes is directed. | structural |
| R5 | **The crossing chooses the diameter.** The diameter that goes up is the one aligned with what the cycle crosses into. Crossing, observation and closure-read-from-above are one event. | structural |
| R6 | **Closure failure is monotone with reading accuracy.** | derived; consistent on one cohort |
| R7 | **carried² + contained² = R²** at every position. This is plain Pythagoras, with no φ in it. | structural; internally consistent on one cohort |
| R8 | **φ enters at the level-crossing.** A cycle hands up an axis at scale d, and d + d² = 1 forces d = 1/φ. | derived; no cross-level measurement yet (open) |
| R9 | **Closure deficit ρ = 1 − R**, where R is the length of the resultant of regime mass placed at the four cardinals. R is the health coordinate and 1 − R the pathology coordinate. | derived; correlates on one cohort |
| R10 | **Crossings are ordered.** A running cycle is not yet an axis, so one cycle closes first (the standing axis) and the other closes into it (the arriving axis). | structural |
| R11 | **Construction is the origin of sequence.** | structural |
| R12 | **Every persistor is built from a holding cycle and a crossing cycle.** The holding cycle is one level up: slow, standing, spatial, and it gives identity and field. The crossing cycle is one level down: fast, arriving, temporal, and it drives traversal. | structural |
| R13 | **Position-to-parent table** (§9.2): at each of the 16 positions, both parent cycles must be at set cardinals for the position to close. | derived; first test inconclusive (open) |

**R7 and R9 measure different things.** *Contained* = R · sin ψ is arc position: how far the persistor is around its orbit. That is motion, not sickness. *ρ* = 1 − R is how far the circle has collapsed inward, and that is pathology. Only the four cardinals are clean hand-off points. Elsewhere a persistor is in transit.

### 8. Nesting

- **Every axis is a cycle one level down.** The sine and cosine seen at one level are the projections of the cycles running below. [structural]
- **Every cycle is built from two cycles.** One closed cycle supplies one axis, and a persistor needs two. The two are ordered (R10): a standing axis and an arriving axis. [structural] Whether standing = space and arriving = time, or the reverse, is [open].
- **There is no top and no bottom.** Every persistor is one quadrant of a larger persistor and contains smaller ones. In a drawing, the area outside a persistor's circle belongs to its parent, not to empty space. [structural]

#### 8.1 Levels and the five dimensions

L counts the structural dimensions a system has in operation. Each dimension is forced by an axiom, and each depends on the one below it. [derived: the derivation reads the axioms with structural intent]

| L | Dimension | Forced by | What it adds |
| --- | --- | --- | --- |
| 0 | none | | Matter following physics, not self-organising |
| 1 | Identity | A1 (hold needs something to hold) | A self that can be held or dropped |
| 2 | Other | A1 (cross needs a target) | A boundary, beyond which is something else |
| 3 | Occurrence | A5 (motion exists) | Engagement actually happens: the active/latent distinction |
| 4 | Closure | A4 (mass conserved) | The cycle gives back what it received and feeds the next round. d² + d = 1 is this dimension in formal terms. |
| 5 | Recursion | A3 (recursive) | The closed cycle becomes one element of a larger cycle. R1 is this dimension in formal terms. |

- **Five is the limit within one meta-cycle.** No sixth dimension can be derived. Going further starts a new meta-cycle, in which an L5 system becomes the L1 substrate one scale up. [derived]
- **Closure runs in order.** Dimension N closes only after N − 1 has closed. [structural]
- **A failure un-closes everything above it.** Losing dimension N removes the closure of every dimension above N, because each higher dimension stands on the lower ones. The right intervention therefore addresses the lowest unclosed dimension first. [structural]
- **Each dimension's closure is itself a four-regime cycle.** [structural]

### 9. Three speeds

#### 9.1 The sandwich

One persistor involves three cycles moving at three speeds: [structural]

| Cycle | Level | Speed | Role |
| --- | --- | --- | --- |
| Holding cycle | parent, above | slow (1 : 4 to the unit) | Sustains the field and gives substrate downward |
| The unit | level N | medium | Addresses the signal from below with substrate from above |
| Crossing cycle | below | fast (4 : 1 to the unit) | Steps the unit through its positions, and turns substrate into signal |

The crossing cycle's four regimes compress to an active/latent square wave on the unit's cross-axis: Potentiality and Construction read as active, Encounter and Conservation as latent. The holding cycle does the same on the hold-axis, 90° out of phase.

**Means becomes self at every level-crossing.** A closed unit becomes substrate for its parent. What was a means at one level becomes self at the level above.

#### 9.2 Position-to-parent table (R13)

| Positions | Regime | Holding cycle at | Crossing cycle at |
| --- | --- | --- | --- |
| P1 to P4 | Potentiality | Encounter | Pot, C, E, Co in turn |
| P5 to P8 | Construction | Potentiality | Pot, C, E, Co in turn |
| P9 to P12 | Encounter | Potentiality | Pot, C, E, Co in turn |
| P13 to P16 | Conservation | Encounter | Pot, C, E, Co in turn |

The holding cycle changes cardinal only at the hold-axis thresholds, Activation and Drain. This reproduces the threshold classes of §5 without assuming them. A position that will not close has one of two causes. Either the holding cycle has not reached its cardinal, so the whole regime is blocked and the fix is upstream. Or the crossing cycle is at the wrong sub-regime, so the sub-step is blocked and the fix is below.

### 10. The substrate economy

- **Hold is the self being sustained, and cross is the problem being addressed.** A persistor is a problem-and-self pair in motion. [structural]
- **The crossing cycle is a role.** A role is a primed unit, drawn from inventory, that matches one class of problem. [structural]
- **Lineage and novelty work together.** Lineage is substrate flowing down from closures that succeeded. Novelty is signal flowing up, and it comes from the correction-residue of cycles that failed but tried to recover. A cycle that never fails, or that fails without correcting, produces no novelty. [structural]
- **Atonement.** A young persistor is fed from above. To close as a self, the feeding has to stop, and from then on substrate comes from its own encounters. If atonement comes too early, the persistor starves. If it never comes, the persistor stays dependent. [structural]
- **A new cycle is born in regime order.** Its capacitor forms first by pooling correction-residue, then Construction, then Encounter, then Conservation. Where a rescue cycle stops in that order says which intervention it needs. [structural]

### 11. Failure is required

If each of the 16 position-closures survives with probability 1/φ, a working L4 cycle needs about φ¹⁶ ≈ 7,000 attempts, and an L5 cycle about φ²⁰ ≈ 50,000. This assumes the positions close independently, so it is an upper bound. Correlation between positions lowers it. Known selection ratios range from about 2 : 1 (neuronal pruning) to about 10⁸ : 1 (sperm). Drug candidates per approved drug, at roughly 5,000 to 10,000 : 1, sit at the predicted order. [derived; order of magnitude only]

What follows is structural. **Failure is required, not wasteful.** A parent has to feed the whole population of attempts, not only the successes. That is why young, parent-fed systems can experiment widely, while mature, self-fed systems must succeed more often per attempt.

---

## Part B: Reading a persistor

### 12. The sixteen verbs

Each of the 16 positions is an operation. Each verb has a *thing-form*, used when the other is substrate, and a *being-form*, used when the other runs its own cycle. The structure is canonical. The words are a first pass. [structural for the positions; open for the word choice]

| Position | Regime / sub-position | Thing-form | Being-form |
| --- | --- | --- | --- |
| P1 | Potentiality / Pot | absorb | receive |
| P2 | Potentiality / C | sort | recognise |
| P3 | Potentiality / E | release | reach |
| P4 | Potentiality / Co | discharge | commit |
| P5 | Construction / Pot | gather | recruit |
| P6 | Construction / C | shape | train |
| P7 | Construction / E | test | challenge |
| P8 | Construction / Co | finalise | choose |
| P9 | Encounter / Pot | approach | meet |
| P10 | Encounter / C | engage | negotiate |
| P11 | Encounter / E | consume | exchange |
| P12 | Encounter / Co | deposit | part |
| P13 | Conservation / Pot | store | remember |
| P14 | Conservation / C | consolidate | integrate |
| P15 | Conservation / E | maintain | tend |
| P16 | Conservation / Co | hand off | release forward |

P1 to P12 are the doings of the open arc. P13 to P16 turn that engagement into persisting structure, and P16 is the Suppression threshold expressed as a verb. Which others a system treats as things and which as beings is itself diagnostic.

### 13. Diagnosis in brief

1. **Find the regime.** Use the observables in §4.
2. **Find the position.** If the persistor is stuck, check both parent cycles against the table in §9.2.
3. **Find the lowest unclosed dimension** (§8.1) and address it first.
4. **Check the capacitor.** At depth, every failure ends at a gap that did not fill. Either no substrate fitted, or the gap itself was malformed.

### 14. What kind of theory this is

Every view of the persistor is consistent on its own: the bit table, the gap-and-filling reading, the two diameters, the 16 positions and the five dimensions. They do not combine into one picture in three dimensions. The persistor behaves like an object that can be charted locally but not covered by one global map. Every drawing on this site is a local chart. [open: an interpretation]

The five dimensions also read as a grammar: identity is the subject, other is the object, occurrence is the aspect, closure is completion and recursion is nesting. On this reading, the framework names what any process needs in order to be described as a process at all, and it is also a testable dynamical theory. Its tests check whether systems that are taken to be coherent processes have this structure. [open: an interpretation]

---

## Part C: Open seams

These are the open questions, most load-bearing first.

1. **The depth diagnostic has no cohort-level validation.** Testing it needs single-cell longitudinal data, paired multi-scale observation and a way to tell failure classes apart.
2. **The φ step between levels (R8) has not been measured.**
3. **R13 has not had a sharp test.** That would need three nested, truly adjacent bands on a non-resting signal.
4. **Standing = space, arriving = time (R10)** is one inference deep and could be the other way round.
5. **The 9.47 envelope** rests on two data points.
6. **Encounter and Conservation lack full formulas.** Potentiality and Construction are specified, the other two only scaffolded.
7. **Three things sit outside the axioms:** why there are exactly two operations, time as a fractal ratio, and the origin of the role asymmetry between Construction and Encounter.
8. **The particle/wave reading** (a cycle collapsed onto one diameter or the other) is consistent with every test so far and not demonstrated.

---

*Cite as: van der Klein, R. (2026). The persistor: specification. Persistence Dynamics. https://persistencedynamics.com*
