import csv

def load_dialogue(path="dialogue.csv"):
    pairs = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            pairs[row["input"].strip().lower()] = row["response"].strip()
    return pairs

def match(query, pairs):
    query = query.strip().lower()
    results = []
    for key, response in pairs.items():
        if query == key or query in key or key in query:
            results.append((key, response))
    return results

def main():
    pairs = load_dialogue()
    print("Type a question (or 'quit' to exit).")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "quit":
            break
        results = match(user_input, pairs)
        if not results:
            print("no match found")
        for key, response in results:
            print(f"match: {key}")
            print(response)

if __name__ == "__main__":
    main()
