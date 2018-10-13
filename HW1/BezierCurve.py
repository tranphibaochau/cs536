#!/usr/bin/env python3
import sys
import math
from decimal import Decimal as D
#helper function to calculate combination
def nCr(n,r):
    return (math.factorial(n) / math.factorial(r) / math.factorial(n-r))
#helper function to list all number between a and b given step c
def frange(a, b, c):
	while a < b:
		yield round(D(a), 4)
		a+=c
#create a class to calculate Bezier curve
class BezierCurve:
	def __init__(self, d=0.05, l= [], r= 0.1):
		#input that specifies the increment u
		self.d = d
		#list of input control points
		self.point_list = l
		#radius of the curve, only serves purpose in FreeCAD
		self.radius = r
		#number of input points
		self.num_of_points= 0
		#number of output points
		self.num_of_output = 0
	#function to calculate the Bezier curve, given the input control points and the increment
	def calculate_curve(self):
		point_list =[]
		for t in frange(0, 1+ self.d, self.d):
			self.num_of_output +=1
			#separately calculate p for each dimension
			p_x = 0
			p_y = 0
			p_z = 0
			for i in range(self.num_of_points+1):
				#calculate Bezier Curve using the formula
				p_x += nCr(self.num_of_points, i) * math.pow(round((1-t), 6), (self.num_of_points-i))* math.pow(t, i) * self.point_list[i][0]
				p_y += nCr(self.num_of_points, i) * math.pow(round((1-t), 6), (self.num_of_points-i))* math.pow(t, i) * self.point_list[i][1]
				p_z += nCr(self.num_of_points, i) * math.pow(round((1-t), 6), (self.num_of_points-i))* math.pow(t, i) * self.point_list[i][2]
			print(round(p_x, 6), round(p_y, 6), round(p_z, 6), end= ",\n")

def main():
	filename ="HW1_test4.txt"
	u = 0.01
	r= 0.1
	#check for specified arguments, otherwise the program will run with default values
	for i in range(len(sys.argv)):
		if sys.argv[i] == "-f":
			filename = sys.argv[i+1]
		elif sys.argv[i] == "-u":
			u = round(float(sys.argv[i+1]), 4)
		elif sys.argv[i] == "-r":
			r = round(float(sys.argv[i+1]), 4)
	#initiate the object
	bz = BezierCurve(u, [], r)
	with open(filename) as file:
		#record output to fit Open Inventor format
		output = ""
		#read input file, record the control points
		for line in file:
			s ="Separator {LightModel {model PHONG}Material {	diffuseColor 1.0 1.0 1.0}\nTransform {translation\n"
			point=[]
			line = line.split("\n")[0]
			points = line.split(" ")
			for p in points:
				s+= p + " "
				p = float(p)
				point.append(p)
			s+="\n}Sphere {	radius " + str(r) + " }}\n"
			output+=s
			#store all input control points to later calculate the curve
			bz.point_list.append(point)
			bz.num_of_points=len(bz.point_list)-1
	print("#Inventor V2.0 ascii\nSeparator {LightModel {model BASE_COLOR} Material {diffuseColor 1.0 1.0 1.0}\nCoordinate3 { 	point [")

	#calculate the curve then output to stdout
	bz.calculate_curve()
	print("] }")
	#record output to fit Open Inventor format
	indexes = "IndexedLineSet {coordIndex [\n"
	for i in range(bz.num_of_output):
		indexes+= str(i) + ", "
	indexes+="-1, \n] } }"
	print(indexes)
	print(output)
	#close the file
	file.close()
main()
