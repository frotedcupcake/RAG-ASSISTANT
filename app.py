from pipeline.rag_pipeline import rag_answer

while True:
    q = input("\nAsk a question: ")
    print(rag_answer(q))
