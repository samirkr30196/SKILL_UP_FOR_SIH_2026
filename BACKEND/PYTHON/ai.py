def classify_complaint(description):
    text = description.lower()

    if any(word in text for word in ["road", "pothole", "street"]):
        return "Road"
    if any(word in text for word in ["garbage", "waste", "dustbin"]):
        return "Sanitation"
    if any(word in text for word in ["water", "pipe", "leak"]):
        return "Water"
    if any(word in text for word in ["light", "electricity", "streetlight"]):
        return "Electricity"

    return "Other"

def calculate_priority(description):
    text = description.lower()

    if any(word in text for word in ["urgent", "danger", "accident", "emergency"]):
        return "High"
    if any(word in text for word in ["broken", "major", "severe"]):
        return "Medium"

    return "Low"