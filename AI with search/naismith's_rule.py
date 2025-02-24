# Task 5. Naismith's Rule 
The rule states that it takes 1 hour to walk 5 km, with an extra hour added for each 600m of climbing. So, if you were to walk up a hill that was precisely 5km long, but with a gradient of 12%, it should take you 2 hours to complete.

Amend your search to work out the path cost according to Naismith's rule. Assume that walking downhill takes as long as walking horizontally. Use Naismith's rule as the new heuristic too. Re-run your search and compare performance to previous attempts.

def heur_sld(from_node, to_node):
  """Return the sld between two nodes."""
  return sld_dists[from_node,to_node]


def heur_naismith(from_node, to_node):
  """Return the Naismith-adjusted time between two nodes."""

  dist = sld_dists[from_node,to_node]

  # 1 hr per 5km + 1hr for every 600m
  delta_elev = elevations[to_node] - elevations[from_node]
  time_flat = dist / 5.0
  # if we're going uphill, add 1 hr per 600 m
  extra_time_uphill = 0 if (delta_elev <= 0) else delta_elev / 600.0
  return time_flat + extra_time_uphill


def path_cost_naismith(from_node, to_node):
  """Return the Naismith-adjusted time between two nodes."""

  
  path_cost = g.edges[from_node, to_node]['distance']

  # 1 hr per 5km + 1hr for every 600m
  delta_elev = elevations[to_node] - elevations[from_node]
  time_flat = path_cost / 5.0
  # if we're going uphill, add 1 hr per 600 m
  extra_time_uphill = 0 if (delta_elev <= 0) else delta_elev / 600.0
  return time_flat + extra_time_uphill


def successors(node):
  """Find the neighbouring nodes

  Returns:
    list of (node,edge cost) pairs for all neighbours
  """
  # find edges starting or ending at our node
  matches = [(a,b,cost) for (a,b,cost) in paths if (node in (a,b))]
  return [ (a if node==b else b,c) for (a,b,c) in matches ]
