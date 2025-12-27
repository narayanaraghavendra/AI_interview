from langchain_groq import ChatGroq
from scoring import confidence_score, depth_score

llm_fast = ChatGroq(model="llama3-8b-8192", temperature=0.2)
llm_deep = ChatGroq(model="llama3-70b-8192", temperature=0.3)

def run_graph(screen_text, speech_text, answer, state):
    if answer is None:
        prompt = f"Generate interview question based on:\n{screen_text}\n{speech_text}"
        question = llm_deep.invoke(prompt).content
        return question, None

    conf = confidence_score(answer)
    depth = depth_score(llm_fast, answer, screen_text + speech_text)

    state["confidence"].append(conf)
    state["depth"].append(depth)

    prompt = f"Ask next interview question. Previous answer: {answer}"
    question = llm_deep.invoke(prompt).content

    return question, plot_metrics(state)