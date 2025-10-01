import json
import argparse
from graph_model import FlavorGraph
from greedy import greedy_rank
from backtracking import can_satisfy_recipe
from substitutions import best_substitute

def load_recipes(path='data/recipes.json'):
    with open(path, 'r') as f:
        return json.load(f)

def pretty_print_suggestions(suggestions, fg, available):
    for s in suggestions:
        rid = s['id']
        recipe = fg.recipes[rid]
        print(f"\n=== {recipe.get('title','')} ({rid}) ===")
        print("Matched:", s['matched'])
        print("Missing:", s['missing'])

        ok, sol = can_satisfy_recipe(recipe, set(available))
        if ok:
            print("Can be satisfied with substitutions (ingredient -> used):")
            for ing, used in sol.items():
                print(f"  {ing} -> {used}")
        else:
            if s['missing']:
                miss = s['missing'][0]
                sub, score = best_substitute(miss, set(available))
                if sub is None:
                    print(f"Suggested substitution for {miss}: None (no known substitute)")
                else:
                    available_flag = sub in set(available)
                    print(f"Suggested substitution for {miss}: {sub} (score {score}){' (available)' if available_flag else ' (not available)'}")
            else:
                print("No missing ingredients but could not satisfy by substitution.")
        print(f"Match ratio: {s['ratio']:.2f}")

def main(args):
    recipes = load_recipes()
    fg = FlavorGraph(recipes)
    # normalize input
    available = set([x.strip().lower() for x in args.available.split(',') if x.strip()])
    rec_stats = fg.recipe_match_stats(available)
    suggestions = greedy_rank(rec_stats, k=args.k)
    pretty_print_suggestions(suggestions, fg, available)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--available', type=str, required=True,
                        help='comma-separated ingredient names, e.g. "egg,milk,flour"')
    parser.add_argument('--k', type=int, default=5, help='how many suggestions to show')
    args = parser.parse_args()
    main(args)
