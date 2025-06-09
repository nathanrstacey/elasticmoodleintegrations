def parse_csv_response(response):
    lines = response.strip().splitlines()
    term_score_pairs = []
    for line in lines:
        try:
            term, score = line.split(",", 1)
            term_score_pairs.append((term.strip(), float(score.strip())))
        except:
            continue
    return term_score_pairs
