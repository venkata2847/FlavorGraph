# Simple substitution map (ingredient -> list of (substitute, score))
SUBSTITUTES = {
    "egg": [("flax_egg", 0.9), ("chia_egg", 0.85), ("applesauce", 0.6), ("banana", 0.5)],
    "milk": [("soy_milk", 0.9), ("almond_milk", 0.85), ("water", 0.3)],
    "baking_powder": [("baking_soda+cream_of_tartar", 0.8)]
}

def best_substitute(ingredient, available_set):
    """Return the best substitute (sub, score). Prefer ones that ARE in available_set."""
    if ingredient not in SUBSTITUTES:
        return (None, 0)
    # prefer substitutes present in available_set
    for s, score in SUBSTITUTES[ingredient]:
        if s in available_set:
            return (s, score)
    # otherwise return the top suggestion (even if not present)
    return SUBSTITUTES[ingredient][0]
