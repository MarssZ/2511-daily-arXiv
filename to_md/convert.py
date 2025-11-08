import json
import argparse
import os
from itertools import count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="Path to the jsonline file")
    args = parser.parse_args()
    data = []
    preference = os.environ.get('CATEGORIES', 'cs.CV, cs.CL').split(',')
    preference = list(map(lambda x: x.strip(), preference))
    def rank(cate):
        if cate in preference:
            return preference.index(cate)
        else:
            return len(preference)

    with open(args.data, "r") as f:
        for line in f:
            data.append(json.loads(line))

    categories = set([item["categories"][0] for item in data])
    template = open("paper_template.md", "r").read()
    categories = sorted(categories, key=rank)
    cnt = {cate: 0 for cate in categories}
    for item in data:
        if item["categories"][0] not in cnt.keys():
            continue
        cnt[item["categories"][0]] += 1

    markdown = f"<div id=toc></div>\n\n# Table of Contents\n\n"
    for idx, cate in enumerate(categories):
        markdown += f"- [{cate}](#{cate}) [Total: {cnt[cate]}]\n"

    idx = count(1)
    for cate in categories:
        markdown += f"\n\n<div id='{cate}'></div>\n\n"
        markdown += f"# {cate} [[Back]](#toc)\n\n"
        papers = []
        for item in data:
            if item["categories"][0] == cate:
                # Safely access AI fields with default values
                ai_data = item.get('AI', {})
                if not ai_data or not isinstance(ai_data, dict):
                    print(f"Skipping item '{item.get('title', 'Unknown')}' due to missing or invalid AI data")
                    continue

                # Check if all required AI fields are present (new field structure)
                required_fields = ['core_problem', 'key_insight', 'method', 'method_formula', 'core_finding',
                                 'mechanism_insight', 'action_value', 'transferability', 'value_score',
                                 'summary_core', 'summary_layman']
                if not all(field in ai_data for field in required_fields):
                    print(f"Skipping item '{item.get('title', 'Unknown')}' due to incomplete AI fields")
                    continue

                papers.append(
                    template.format(
                        title=item["title"],
                        authors=", ".join(item["authors"]),
                        summary=item["summary"],
                        url=item['abs'],
                        core_problem=ai_data.get('core_problem', ''),
                        key_insight=ai_data.get('key_insight', ''),
                        method=ai_data.get('method', ''),
                        method_formula=ai_data.get('method_formula', ''),
                        core_finding=ai_data.get('core_finding', ''),
                        mechanism_insight=ai_data.get('mechanism_insight', ''),
                        action_value=ai_data.get('action_value', ''),
                        transferability=ai_data.get('transferability', ''),
                        value_score=ai_data.get('value_score', ''),
                        summary_core=ai_data.get('summary_core', ''),
                        summary_layman=ai_data.get('summary_layman', ''),
                        cate=item['categories'][0],
                        idx=next(idx)
                    )
                )
        markdown += "\n\n".join(papers)
    with open(args.data.split('_')[0] + '.md', "w") as f:
        f.write(markdown)