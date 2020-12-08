




def handi_calc(score, course_rating, slope):
	top = (score - course_rating) * 113
	bottom = slope
	handi = top / bottom
	return handi


r = handi_calc(85, 68.4, 113)
print(r)

