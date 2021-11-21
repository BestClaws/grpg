import genshinstats as gs
gs.set_cookie(ltuid=76762900,
              ltoken="gZc3s6wNGYQjnmxQe7n1GEZm60dmAFe1JosWUQ3q")
data = gs.get_all_user_data('812786494')

with open('character.json', 'w') as f:
    import json
    json.dump(data['characters'][0], f)