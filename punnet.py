#!/usr/bin/env python3

"""Punnet square generator

Sample Input:

AaBb

Sample output:

   +----+----+----+----+
   |AB  |Ab  |ab  |aB  |
+--+----+----+----+----+
|AB|AABB|AABb|ABab|ABBa|
|Ab|AABb|AAbb|Aabb|ABab|
|ab|ABab|Aabb|aabb|Baab|
|aB|ABBa|ABab|Baab|BBaa|
+--+----+----+----+----+

AABB: 1 (1/16)
AABb: 2 (1/8)
AAbb: 1 (1/16)
ABBa: 2 (1/8)
ABab: 4 (1/4)
Aabb: 2 (1/8)
BBaa: 1 (1/16)
Baab: 2 (1/8)
aabb: 1 (1/16)

"""

import os.path
import json
from sys import stdout, stderr
from collections import OrderedDict
from argparse import ArgumentParser
from pprint import pprint
from fractions import Fraction

class PunnetGenerator:
	def __init__(self, debug):
		self.debug = debug

	def d(self, msg):
		if self.debug:
			pprint(msg)

	def generate(self, mommy, daddy):
		mommy = mommy.strip() # Make it rain
		daddy = daddy.strip()
		len_mommy = len(mommy)
		len_daddy = len(daddy)
		if len_mommy != len_daddy:
			raise ValueError("The length of the mother's genotype must be equal to the father's")
		# Check for genotypes of odd lengths
		if len_mommy % 2 != 0:
			raise ValueError("The mommy genotype must be even in length")
		if len_daddy % 2 != 0:
			raise ValueError("The daddy genotype must be even in length")
		
		column_headers = None
		row_headers = None
		geno_count = len_mommy / 2
		if geno_count < 1:
			raise ValueError("Genotype count cannot be less than one")

		column_headers = None
		row_headers = None

		if geno_count == 1:
			# Monohybrid
			column_headers = [mommy[0], mommy[1]]
			row_headers = [daddy[0], daddy[1]]
		else:
			# Dihybrid and up
			column_headers = self._generate_headers(mommy)
			row_headers = self._generate_headers(daddy)

		if len(column_headers) != len(row_headers):
			raise ValueError("Column and row headers were not of equal sizes")

		if len(column_headers) != len(row_headers):
			raise ValueError("Column and row headers were not of equal sizes")
		
		grid_size = len(column_headers)
		
		# http://stackoverflow.com/a/1805540/1275092
		data = [([None] * grid_size) for x in range(grid_size)]
		# data[y][x] where (0, 0) is at the top left corner and (1, 0) is right below it
		
		for y in range(grid_size):
			for x in range(grid_size):
				# Create the grid
				cell = sorted(list(column_headers[x] + row_headers[y]))
				# cell is now an array of chars, turn it back into a string
				cell = ''.join(cell)

				data[y][x] = cell
				x += 1
				if x == grid_size:
					x = 0
					y += 1
		
		self.print_table(data, column_headers, row_headers)
		stdout.write("\n")
		self.print_stats(data)
	
	def _generate_headers(self, geno):
		terms = []
		if not self._is_even(len(geno)):
			raise ValueError("Genotype length must be even")

		# Split the string into an array of strings 2 chars long
		# http://stackoverflow.com/a/9475354/1275092
		gametes = [list(geno[i:i + 2]) for i in range(0, len(geno), 2)]
		# An array of array of integers (1 or 0) corresponding to 'gametes'
		counters = [[1, 0] for i in range(len(gametes))]
		back_counter = len(gametes) - 1
		
		for unused in range(2 ** len(gametes)):
			self.d(gametes)
			self.d(counters)
			# Extract the gametes where its index in 'counters' is 1
			term = ""
			for i, array in enumerate(counters):
				for j in array:
					if array[j] == 1:
						term += gametes[i][j]
			self.d(term)
			terms.append(term)
			
			counters[-back_counter][0] = self._flip(counters[-back_counter][0])
			counters[-back_counter][1] = self._flip(counters[-back_counter][1])
			back_counter -= 1
			if back_counter == -1:
				back_counter = len(gametes) - 1
		return terms
	
	def _flip(self, num):
		# Flips 1 and 0
		if num != 1 and num != 0:
			raise ValueError("num must be either 1 or 0")
	
		return 0 if num == 1 else 1

	
	def _is_even(self, num):
		return num % 2 == 0


	def print_table(self, data, column_headers, row_headers):
		cell_size = len(data[0][0])
		if not self._is_even(cell_size):
			raise ValueError("Cell size must be even")
		header_length = int(cell_size / 2)
		column_header_offset = header_length + 1
		column_grid_indicies = [0]

		# Top grid line
		self._write_spaces(column_header_offset)
		column_grid_indicies.append(column_grid_indicies[-1] + header_length + 1)
		for col in column_headers:
			stdout.write("+")
			self._write_char(cell_size, "-")
			column_grid_indicies.append(column_grid_indicies[-1] + cell_size + 1)
			
		stdout.write("+\n")
		total_grid_size = column_header_offset + 1 + cell_size
	
		# Create the empty space at the top left of the grid
		self._write_spaces(column_header_offset)
		
		# Draw the column headers
		for col in column_headers:
			stdout.write("|")
			stdout.write(col)
			self._write_spaces(header_length)
			total_grid_size += len(col) + header_length
		# End the column headers
		stdout.write("|\n")
		total_grid_size += 1
		
		# Draw the line separating the column headers from the data
		self._hor_grid_line(column_grid_indicies, total_grid_size)

		# Draw each row out
		for i, row in enumerate(data):
			# Row header
			stdout.write("|" + row_headers[i] + "|")
		
			# Write the data
			for cell in row:
				stdout.write(cell + "|")

			stdout.write("\n")

		# Final encapsulating grid line
		self._hor_grid_line(column_grid_indicies, total_grid_size)
	
	def _hor_grid_line(self, indicies, total_length):
		for i in range(total_length - 1):
			if i in indicies:
				stdout.write("+")
			else:
				stdout.write("-")
		stdout.write("\n")
	
	def print_stats(self, data):
		# Dictionary of cells and their amount of appearances in the table
		# Example: {"BB": 1, "Bb": 2, "bb": 1}
		stats = {}

		for i, row in enumerate(data):
			for genotype in row:
				if genotype in stats:
					# The cell is already logged in the stats
					stats[genotype] += 1
				else:
					# The cell is not in the stats
					stats[genotype] = 1
		
		# Sort the stats by genotype
		stats = OrderedDict(sorted(stats.items()))
		total_items = sum(stats.values())
		for genotype, count in stats.items():
			frac = Fraction(count, total_items)
			stdout.write("{}: {} ({})\n".format(genotype, count, str(frac.numerator) + "/" + str(frac.denominator)))

	def _write_spaces(self, count):
		self._write_char(count, " ")
	
	def _write_char(self, count, char):
		for i in range(count):	
			stdout.write(char)

def main():
	parser = ArgumentParser()
	parser.add_argument("mommy", help="the first genotype to cross")
	parser.add_argument("daddy", help="the second genotype to cross")
	args = parser.parse_args()

	debug = False
	# Load extra properties
	if os.path.isfile('cfg.json'):
		with open('cfg.json', 'r') as config_file:
			config = json.load(config_file)
			if "debug" in config:
				debug = config["debug"]

	gen = PunnetGenerator(debug)
	gen.generate(args.mommy, args.daddy)

if __name__ == "__main__":
	main()
