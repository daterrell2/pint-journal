from models import Beer, BeerScore

def get_sorted_avg(sort_reverse = False, limit = None):
	'''
	Returns a list of beers objects sorted by their average score.
	By default, sorts in ascending order (set sort_reverse to True to reverse)	
	Limit param determines number of beers returned.
	'''
	q = '''
	SELECT b.id AS id, b.beer_id AS beer_id, avg(s.score) AS score
	FROM pints_main_beer b
	INNER JOIN pints_main_beerscore s
	ON b.id = s.beer_id
	GROUP BY b.id, b.beer_id;
	'''

	q = q.replace('\n', ' ')

	beers = Beer.objects.raw(q)
	if beers:
		b = sorted(beers, key=lambda x: x.score, reverse=sort_reverse)
		if limit:
			return b[:limit+1]
		else:
			return b

	return None


	