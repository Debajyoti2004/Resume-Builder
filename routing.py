def route_query(query):
    passions = {
        "Data Science": ["data science", "machine learning", "AI", "artificial intelligence", "deep learning"],
        "Software Engineering": ["software engineer", "backend", "frontend", "full stack", "developer"],
        "Product Management": ["product manager", "product management", "PM", "product strategy"],
        "Design": ["UI/UX", "user experience", "graphic design", "design"],
    }

    query_lower = query.lower()
    for passion, keywords in passions.items():
        if any(keyword in query_lower for keyword in keywords):
            return passion
    return "Unknown"

