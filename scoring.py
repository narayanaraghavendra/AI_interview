import matplotlib.pyplot as plt

NEGATIVE = ["maybe", "not sure", "i think", "probably"]

def confidence_score(answer):
    score = 1.0
    for w in NEGATIVE:
        if w in answer.lower():
            score -= 0.15
    return max(0, min(score, 1))

def depth_score(llm, answer, context):
    prompt = f"Score technical depth 0-1. Context: {context}. Answer: {answer}"
    return float(llm.invoke(prompt).content.strip())

def plot_metrics(state):
    plt.figure(figsize=(5,3))
    plt.plot(state["confidence"], label="Confidence")
    plt.plot(state["depth"], label="Depth")
    plt.ylim(0,1)
    plt.legend()
    return plt