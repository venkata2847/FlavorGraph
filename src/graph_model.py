import networkx as nx

class FlavorGraph:
    def __init__(self, recipes):
        self.G = nx.Graph()
        self.recipes = {r['id']: r for r in recipes}
        self._build_graph()

    def _build_graph(self):
        for rid, r in self.recipes.items():
            self.G.add_node(rid, type='recipe', title=r.get('title', rid))
            for ing in r.get('ingredients', []):
                self.G.add_node(ing, type='ingredient')
                self.G.add_edge(rid, ing)

    def recipe_match_stats(self, available_set):
        """Return list of (recipe_id, matched_list, missing_list, match_ratio) sorted by best match."""
        out = []
        for rid, r in self.recipes.items():
            ingredients = set(r.get('ingredients', []))
            matched = ingredients & available_set
            missing = ingredients - available_set
            ratio = len(matched) / len(ingredients) if ingredients else 0
            out.append((rid, sorted(list(matched)), sorted(list(missing)), ratio))
        out.sort(key=lambda x: (-x[3], len(x[2])))
        return out
