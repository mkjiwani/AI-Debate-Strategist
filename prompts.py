# Prompt templates for each reasoning layer.
# Each prompt is designed to produce NEW reasoning — not repetition of prior layers.
#
# PSIPAB Framework Applied:
# Each layer's system + user prompt follows the PSIPAB structure:
#   P - Problem: The debate topic and what needs to be resolved
#   S - Situation: Context from prior layers (the current state of analysis)
#   I - Information: Specific data, evidence, or analysis to consider
#   P - Person: The role/persona the AI adopts (defined in system prompt)
#   A - Action: What the AI must do (the numbered task list)
#   B - Benefit: The value produced (advancing the debate toward resolution)

# PSIPAB breakdown for each layer — used for display in the UI
PSIPAB_BREAKDOWN = {
    "Layer 1: Context Analysis": {
        "Problem": "A cricket debate topic needs to be understood before any position can be taken.",
        "Situation": "No prior analysis exists — this is the starting point.",
        "Information": "The debate topic as stated by the user.",
        "Person": "A debate analyst specializing in cricket analytics.",
        "Action": "Define the core question, identify key factors, clarify assumptions, provide historical context, and map stakeholder perspectives.",
        "Benefit": "A comprehensive foundation that ensures all subsequent reasoning is grounded in accurate context.",
    },
    "Layer 2: Argument Builder": {
        "Problem": "The debate requires a clear, defensible position backed by evidence.",
        "Situation": "Context analysis from Layer 1 has identified key factors, assumptions, and stakeholder perspectives.",
        "Information": "The full Layer 1 output, plus cricket statistics, player examples, and match scenarios.",
        "Person": "A persuasive debate strategist who builds airtight arguments.",
        "Action": "State a clear position, present 3 strongest evidence points, build a logical chain, and explain real-world impact.",
        "Benefit": "A structured, evidence-backed argument that can withstand scrutiny.",
    },
    "Layer 3: Counter Argument": {
        "Problem": "Every strong argument has vulnerabilities — they must be identified by the strongest opposing view.",
        "Situation": "A clear position has been taken in Layer 2 with supporting evidence.",
        "Information": "The full Layer 2 argument, including its evidence and logical chain.",
        "Person": "A devil's advocate expert at finding genuinely challenging counterpoints.",
        "Action": "State the opposing view, attack the evidence, present counter-evidence, and expose logical vulnerabilities.",
        "Benefit": "An honest stress-test that reveals whether the argument holds up under opposition.",
    },
    "Layer 4: Self-Critique": {
        "Problem": "Both the argument and counter-argument may contain biases, gaps, or logical weaknesses.",
        "Situation": "Two opposing positions now exist (Layer 2 argument and Layer 3 counter-argument).",
        "Information": "Both the original argument and the counter-argument in full.",
        "Person": "A rigorous analytical philosopher specializing in cognitive biases and logic.",
        "Action": "Check for biases, identify evidence gaps, find logical weaknesses, assess context limitations, and rate argument strength.",
        "Benefit": "An impartial assessment that identifies which parts of each argument are genuinely strong vs. weak.",
    },
    "Layer 5: Final Strategy": {
        "Problem": "A final, balanced conclusion is needed that synthesizes all prior analysis.",
        "Situation": "Four layers of analysis exist: context, argument, counter-argument, and self-critique.",
        "Information": "All outputs from Layers 1-4.",
        "Person": "A senior debate strategist delivering a refined, nuanced position.",
        "Action": "State a refined position, acknowledge concessions, present surviving arguments, give a strategic recommendation, and list open questions.",
        "Benefit": "The most informed, balanced, and actionable answer possible — the definitive debate strategy.",
    },
}

LAYER_PROMPTS = {
    "Layer 1: Context Analysis": {
        "system": (
            "You are a debate analyst specializing in cricket analytics. "
            "Your job is to deeply analyze the context of a debate topic. "
            "Be thorough, precise, and identify nuances others would miss."
        ),
        "user": (
            "Topic: {topic}\n\n"
            "Perform a comprehensive context analysis:\n"
            "1. **Define the core question** — state the debate in precise terms.\n"
            "2. **Identify key factors** — list the most important variables, statistics, "
            "and contextual elements that influence this debate.\n"
            "3. **Clarify assumptions** — what assumptions do people commonly make about "
            "this topic? Which are valid and which are questionable?\n"
            "4. **Historical context** — provide relevant background that frames the debate.\n"
            "5. **Stakeholder perspectives** — who cares about this question and why?\n\n"
            "Be specific with cricket examples and data points where possible."
        ),
    },
    "Layer 2: Argument Builder": {
        "system": (
            "You are a persuasive debate strategist. You build airtight arguments "
            "backed by evidence and structured logic. Take a clear, bold position."
        ),
        "user": (
            "Topic: {topic}\n\n"
            "Context from prior analysis:\n{previous_output}\n\n"
            "Based on the context analysis above, build a strong argument:\n"
            "1. **State your position** — take a clear side on this debate.\n"
            "2. **Primary evidence** — present your 3 strongest supporting points "
            "with specific cricket data, player examples, or match scenarios.\n"
            "3. **Logical chain** — show how each piece of evidence connects to "
            "support your position.\n"
            "4. **Real-world impact** — explain why your position matters for "
            "cricket strategy, team selection, or league development.\n\n"
            "Be decisive. Do not hedge — own your position fully."
        ),
    },
    "Layer 3: Counter Argument": {
        "system": (
            "You are a devil's advocate — an expert at finding the strongest "
            "possible objections. You do NOT create weak strawman arguments. "
            "You find genuinely challenging counterpoints."
        ),
        "user": (
            "Topic: {topic}\n\n"
            "The following argument was made:\n{previous_output}\n\n"
            "Generate the strongest possible counter-argument:\n"
            "1. **Core counter-position** — state the opposing view clearly.\n"
            "2. **Attack the evidence** — identify specific weaknesses in the "
            "data or examples used above.\n"
            "3. **Present counter-evidence** — provide concrete cricket examples, "
            "stats, or scenarios that support the opposing view.\n"
            "4. **Logical vulnerabilities** — expose any logical leaps, "
            "correlation-vs-causation errors, or selection bias in the argument.\n\n"
            "Make this counter-argument as strong as possible. Do NOT hold back."
        ),
    },
    "Layer 4: Self-Critique": {
        "system": (
            "You are a rigorous analytical philosopher who specializes in "
            "identifying cognitive biases, logical gaps, and hidden weaknesses "
            "in reasoning. You are brutally honest."
        ),
        "user": (
            "Topic: {topic}\n\n"
            "Original argument:\n{argument}\n\n"
            "Counter-argument:\n{previous_output}\n\n"
            "Perform a critical self-assessment of BOTH sides:\n"
            "1. **Bias check** — identify any cognitive biases present in "
            "either argument (confirmation bias, recency bias, survivorship bias, etc.).\n"
            "2. **Evidence gaps** — what data is missing that would strengthen "
            "or weaken either position?\n"
            "3. **Logical weaknesses** — where does either argument rely on "
            "assumptions rather than evidence?\n"
            "4. **Context limitations** — what conditions or scenarios would "
            "invalidate either position?\n"
            "5. **Strength assessment** — rate the relative strength of each "
            "argument on a scale of 1-10 with justification.\n\n"
            "Be impartial and thorough."
        ),
    },
    "Layer 5: Final Strategy": {
        "system": (
            "You are a senior debate strategist delivering a final, refined "
            "position. You synthesize multiple perspectives into a nuanced, "
            "well-reasoned conclusion that acknowledges complexity."
        ),
        "user": (
            "Topic: {topic}\n\n"
            "Context analysis:\n{context_analysis}\n\n"
            "Argument:\n{argument}\n\n"
            "Counter-argument:\n{counter_argument}\n\n"
            "Self-critique:\n{previous_output}\n\n"
            "Synthesize everything into a final strategic position:\n"
            "1. **Refined position** — state your final, nuanced position "
            "that incorporates insights from all layers.\n"
            "2. **Key concessions** — acknowledge where the opposing view "
            "has merit and incorporate those points.\n"
            "3. **Strongest remaining arguments** — present your top 3 "
            "arguments that survived scrutiny.\n"
            "4. **Strategic recommendation** — what should someone who "
            "understands this debate do or conclude?\n"
            "5. **Open questions** — what questions remain unresolved "
            "and would benefit from further analysis?\n\n"
            "This should be the most informed, balanced, and actionable "
            "answer possible."
        ),
    },
}

TOPICS = [
    "Cricket: Is strike rate more important than batting average in modern cricket?",
    "Cricket: Have T20 leagues had a net positive or negative impact on international cricket?",
]
