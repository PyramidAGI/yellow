import csv
from pathlib import Path

LOG_FILE = Path(__file__).parent / "log.csv"
EXAMPLE_FILE = Path(__file__).parent / "examplecluster.txt"

FIELDS = ["natural language input", "e0", "e1", "e2", "e3", "e4", "v", "threshold", "message output"]


def load_example_cluster() -> tuple[str, list[str]]:
    lines = [l for l in EXAMPLE_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    sentence = lines[0].split(";")[0]
    matches = [";".join(l.split(";")[1:]) for l in lines]
    return sentence, matches


def parse_match(match: str) -> dict:
    parts = match.split(";")
    keys = ["e0", "e1", "e2", "e3", "e4", "v", "threshold", "message output"]
    return {k: (parts[i] if i < len(parts) else "") for i, k in enumerate(keys)}


def log(sentence: str, matches: list[str]) -> None:
    append_matches_cluster(LOG_FILE, sentence, matches)


def append_matches_cluster(path: Path, sentence: str, matches: list[str]) -> None:
    rows_to_write = []
    for index, match in enumerate(matches):
        parsed = parse_match(match)
        row = {
            "natural language input": sentence if index == 0 else "",
            "e0": parsed.get("e0", ""),
            "e1": parsed.get("e1", ""),
            "e2": parsed.get("e2", ""),
            "e3": parsed.get("e3", ""),
            "e4": parsed.get("e4", ""),
            "v": parsed.get("v", ""),
            "threshold": parsed.get("threshold", ""),
            "message output": "",
        }
        if any(value for key, value in row.items() if key != "natural language input") or row["natural language input"]:
            rows_to_write.append(row)

    if not rows_to_write:
        return

    with path.open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(["", "", "", "", "", "", "", "", ""])
        for row in rows_to_write:
            writer.writerow(
                [
                    row["natural language input"],
                    row["e0"],
                    row["e1"],
                    row["e2"],
                    row["e3"],
                    row["e4"],
                    row["v"],
                    row["threshold"],
                    row["message output"],
                ]
            )
        writer.writerow(["", "", "", "", "", "", "", "", ""])


def check_log() -> None:
    if not LOG_FILE.exists():
        print("log.csv not found.")
        return
    errors = []
    with LOG_FILE.open(encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.reader(f, delimiter=";"), start=1):
            if len(row) != 9:
                errors.append(f"  line {i}: expected 9 fields, got {len(row)} — {row}")
    if errors:
        print(f"Found {len(errors)} error(s) in log.csv:")
        for e in errors:
            print(e)
    else:
        print("log.csv OK — no formatting errors.")


def main():
    print("Press 'l' to log the example sentence, 'c' to check log.csv, 'q' to quit.")
    while True:
        key = input("> ").strip().lower()
        if key == "l":
            sentence, matches = load_example_cluster()
            log(sentence, matches)
            print(f"Logged: {sentence}")
        elif key == "c":
            check_log()
        elif key == "q":
            break


if __name__ == "__main__":
    main()
