def validate_citation(results):
    top = results[0]
    return {
        "answer": top["payload"]["text"],
        "page": top["payload"]["page_number"],
        "confidence": top["score"]
    }
