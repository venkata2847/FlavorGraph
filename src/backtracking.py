from substitutions import SUBSTITUTES

def can_satisfy_recipe(recipe, available_set):
    """
    Try to satisfy recipe using available_set and known substitutes.
    Returns (True, solution_map) if there is a feasible assignment where
    each required role ingredient is either available or replaced by a substitute present in available_set.
    Otherwise returns (False, {}).
    """
    required = list(recipe.get('ingredients', []))
    missing = [ing for ing in required if ing not in available_set]
    sol = {}

    def try_fill(idx):
        if idx >= len(missing):
            return True
        ing = missing[idx]
        # if ingredient is actually available (shouldn't be in missing, but check nonetheless)
        if ing in available_set:
            sol[ing] = ing
            return try_fill(idx + 1)
        # try substitutes that are present in available_set
        for s, _ in SUBSTITUTES.get(ing, []):
            if s in available_set:
                sol[ing] = s
                if try_fill(idx + 1):
                    return True
        # if ingredient has no required role, allow skipping (treat as optional)
        role = recipe.get('roles', {}).get(ing)
        if role is None:
            sol[ing] = None
            return try_fill(idx + 1)
        # failed to satisfy this required ingredient
        return False

    ok = try_fill(0)
    if ok:
        # fill matched ingredients mapping to themselves
        for ing in required:
            if ing in available_set:
                sol[ing] = ing
            elif ing not in sol:
                sol[ing] = None
        return True, sol
    else:
        return False, {}
