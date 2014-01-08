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

class PunnetGenerator:
	def generate(self, first, second):
		first = first.strip()
		second = second.strip()
		lenfirst = len(first)
		lensecond = len(second)
		if lenfirst != lensecond:
			raise ValueError("The length of the first string must be equal to the length of the second")
		if lenfirst % 2 != 0:
			# Odd number
			raise ValueError("The first string must be even in length")
		if lensecond % 2 != 0:
			raise ValueError("The second string must be even in length")

		column_headers = [first[0], first[1]]
		row_headers = [second[0], second[1]]
		
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


	def print_table(self, data, column_headers, row_headers):
		cell_size = len(data[0][0])
		if cell_size % 2 != 0:
			raise ValueError("Cell size must be even")
		header_length = int(cell_size / 2)
		total_grid_size = 0
	
		# Create the empty space at the top left of the grid
		self._write_spaces(header_length)
		total_grid_size += header_length
		
		# Draw the column headers
		for col in column_headers:
			stdout.write("|" + col)
			self._write_spaces(header_length)
			total_grid_size += len("|" + col) + header_length
		# End the column headers
		stdout.write("|\n")
		total_grid_size += 1
		
		# Draw the line separating the column headers from the data
		for i in range(total_grid_size):
			stdout.write("-")
		stdout.write("\n")

		# Draw each row out
		for i, row in enumerate(data):
			# Column header
			stdout.write(row_headers[i] + "|")
		
			# Write the data
			for cell in row:
				stdout.write(cell + "|")

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
			stdout.write("{}: {} ({})\n".format(genotype, count, (str(count)) + "/" + str(total_items)))

	def _write_spaces(self, count):
		for i in range(count):
			stdout.write(" ")


def main():
	parser = ArgumentParser()
	parser.add_argument("first", help="the first genotype to cross")
	parser.add_argument("second", help="the second genotype to cross")
	args = parser.parse_args()

	gen = PunnetGenerator()
	gen.generate(args.first, args.second)

if __name__ == "__main__":
	main()
