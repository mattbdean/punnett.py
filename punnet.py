#!/usr/bin/env python3

"""Punnet square generator

Sample Input:

BbRr BbRr

Sample output:

  |BR  |Br  |bR  |br  |
=======================
BR|BBRR|BBRr|BbRR|BbRr|
Br|BBRr|BBRR|BbRr|Bbrr|
bR|BbRr|BbRr|bbRR|bbRr|
br|BbRr|Bbrr|bbRr|bbrr|

BBRR: 1 (1/16)
BBRr: 2 (1/8)
BbRR: 2 (1/8)
BbRr: 4 (1/4)
BBrr: 1 (1/16)
Bbrr: 2 (1/8)
bbRR: 1 (1/16)
bbRr: 2 (1/8)
bbrr: 1 (1/8)

"""

from sys import stdout, stderr
from collections import OrderedDict
from argparse import ArgumentParser
from pprint import pprint
from fractions import Fraction

class PunnetGenerator:
	def generate(self, mommy, daddy):
		mommy = mommy.strip()
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

		if geno_count == 1:
			# Monohybrid
			column_headers = [mommy[0], mommy[1]]
			row_headers = [daddy[0], daddy[1]]
		elif geno_count == 2:
			# Dihybrid
			# FOIL the parents to get row and column headers
			column_headers = self._foil(mommy)
			row_headers = self._foil(daddy)
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
	
	def _foil(self, geno):
		terms = []
		mommy = geno[:2]
		daddy = geno[2:]

		for i in mommy:
			for j in daddy:
				terms.append(i + j)
		return terms


	def print_table(self, data, column_headers, row_headers):
		cell_size = len(data[0][0])
		if cell_size % 2 != 0:
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

	gen = PunnetGenerator()
	gen.generate(args.mommy, args.daddy)

if __name__ == "__main__":
	main()
