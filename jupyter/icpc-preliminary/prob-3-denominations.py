def denominate(num_str):
	denominations = [5000,
					 1000,
					  500,
					  200,
					  100,
					  50,
					  20,
					  10]

	for idx, denom in enumerate(denominations):
		if len(str(denom)) == len(num_str):
			denominations = denominations[idx:]
			break

	num_str2 = num_str
	num = int(num_str2)
	results = []
	
	for denom in denominations:		
		rem = int(num / denom)
		# print(num, '/' ,denom, '=>', rem)

		if rem != 0:
			num = abs(num-(rem*denom))

		results.append("{}x{}".format(rem, denom))

	for idx, result in enumerate(results):
		if result[0] != '0':
			results = results[idx:]
			break

	return results

# print(denomination('4270'))
# print(denomination('320'))

with open('P5_input.txt') as f:
	for line_number, line in enumerate(f):
		if line_number == 0:
			continue

		results = denominate(line)
		print("Case #{}: {}".format(line_number, ', '.join(results)))