def rerank(results):
    results.sort(key=lambda x: x[1])  # smaller distance = closer
    return results[:3]
