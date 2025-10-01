from flask import Flask, request, render_template_string
import json
from graph_model import FlavorGraph
from greedy import greedy_rank
from backtracking import can_satisfy_recipe
from substitutions import best_substitute
import os

app = Flask(__name__)

# Load recipes from JSON file
def load_recipes():
    path = os.path.join(os.path.dirname(__file__), '../data/recipes.json')
    with open(path, 'r') as f:
        return json.load(f)

# Core function to get recipe suggestions
def get_suggestions(available_list, k=5):
    recipes = load_recipes()
    fg = FlavorGraph(recipes)
    available = set([x.strip().lower() for x in available_list if x.strip()])
    rec_stats = fg.recipe_match_stats(available)
    suggestions = greedy_rank(rec_stats, k=k)

    result = []
    for s in suggestions:
        rid = s['id']
        recipe = fg.recipes[rid]

        subs = {}
        ok, sol = can_satisfy_recipe(recipe, available)
        if ok:
            for ing, used in sol.items():
                subs[ing] = used
        else:
            for miss in s['missing']:
                sub, score = best_substitute(miss, available)
                subs[miss] = sub if sub else None

        result.append({
            'id': rid,
            'title': recipe.get('title', ''),
            'matched': s['matched'],
            'missing': s['missing'],
            'match_ratio': round(s['ratio'], 2),
            'substitutions': subs
        })
    return result

# Interactive home page
@app.route('/', methods=['GET', 'POST'])
def home():
    suggestions = []
    ingredients_input = ""
    if request.method == 'POST':
        ingredients_input = request.form.get('ingredients', '')
        ingredients_list = [i.strip() for i in ingredients_input.split(',') if i.strip()]
        suggestions = get_suggestions(ingredients_list, k=5)

    html = """
    <h1>FlavorGraph Recipe Suggestions</h1>
    <form method="POST">
        <label>Enter available ingredients (comma separated):</label><br>
        <input type="text" name="ingredients" size="50" value="{{ingredients_input}}">
        <input type="submit" value="Get Suggestions">
    </form>
    <hr>
    {% for s in suggestions %}
        <h2>{{s.title}} (ID: {{s.id}})</h2>
        <p><b>Matched:</b> {{s.matched|join(', ')}}</p>
        <p><b>Missing:</b> {{s.missing|join(', ')}}</p>
        <p><b>Match ratio:</b> {{s.match_ratio}}</p>
        <p><b>Substitutions:</b></p>
        <ul>
            {% for ing, sub in s.substitutions.items() %}
                <li>{{ing}} → {{sub if sub else 'None'}}</li>
            {% endfor %}
        </ul>
        <hr>
    {% endfor %}
    """
    return render_template_string(html, suggestions=suggestions, ingredients_input=ingredients_input)

if __name__ == "__main__":
    app.run(debug=True)
