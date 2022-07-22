import pygame as p
from queue import PriorityQueue
import math

#Defining the constants we will use:

red_fox = (195, 88, 23)
light_green = (154, 205, 50)
indigo = (75, 0, 130)
cyan_blue = (0, 139, 139)
silver = (192, 192, 192)
white = (255, 255, 255)
black = (30, 30, 30)
yellow = (235, 225, 0)
orange = (255, 69, 0)
light_turquoise = (64, 224, 208)

width_of_window = 600
pygame_window = p.display.set_mode((width_of_window, width_of_window))

'''
  _ _   _ _   _ _   _ _   _ _   _ _
| _*_ | _*_ | _*_ | _*_ | _*_ | _*_ | 
| _*_ | _*_ | _*_ | _*_ | _*_ | _*_ |
| _*_ | _*_ | _*_ | _*_ | _*_ | _*_ |
| _*_ | _*_ | _*_ | _*_ | _*_ | _*_ |
| _*_ | _*_ | _*_ | _*_ | _*_ | _*_ |
| _*_ | _*_ | _*_ | _*_ | _*_ | _*_ |
| _*_ | _*_ | _*_ | _*_ | _*_ | _*_ |

This is a simple grid, where each ' * ' represents a node, to represent properties of node like color,coordinates,end,start,wall etc,
we will make a class to represent each seperate node.
'''

#class node of grid:
class node:
	
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = black
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
		self.visited = 0
		'''
		Now we will initialise member functions of this class node:
			1. Make function: will make any changes in condition of node.
			2. Check function: will check condition of node.
			3. position function.
			4. rectangle(node) color filling
			5. neighbour update of node.
		'''

	def make(self, string):
		if string == 'make it closed': #checking if the given node is closed or not for searching the path while run of recursive call
			self.color = red_fox

		if string == 'make it open': #checking if the given node is open or not for searching the path while run of recursive call
			self.color = light_green

		if string == 'make it barrier':
			self.color = silver

		if string == 'make it start':  # making our node start point
			self.color = yellow

		if string == 'make it end':
			self.color = cyan_blue #  making the node our destination 

		if string == 'make it final path':
			self.color = light_turquoise 

		if string == 'make path reset':
			self.color = black 

	def check(self, string):

		if string == 'check closed': #checking if the given node is closed or not for searching the path while run of recursive call
			return self.color == red_fox

		if string == 'check open': #checking if the given node is open or not for searching the path while run of recursive call
			return self.color == light_green

		if string == 'check barrier':
			return self.color == silver

		if string == 'check start':  # checking if it is our start point
			return self.color == yellow

		if string == 'check end':
			return self.color == cyan_blue # checking if it is our destination

	def fill_color(self,pygame_window):
		p.draw.rect(pygame_window, self.color, (self.x, self.y, self.width, self.width))

	def position_row_col(self):
		return self.col , self.row

	def update_neighbors(self, grid):

		#adding down neighbour
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].check('check barrier'): 
			self.neighbors.append(grid[self.row + 1][self.col])

		#adding upper neighbour
		if self.row > 0 and not grid[self.row - 1][self.col].check('check barrier'): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		#adding right neighbour
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].check('check barrier'): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		#adding left neighbour
		if self.col > 0 and not grid[self.row][self.col - 1].check('check barrier'): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])
			
		#diagonal down right
		if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][self.col +1].check('check barrier'): #down right
			self.neighbors.append(grid[self.row + 1][self.col+1])
			
		#diagonal up right
		if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].check('check barrier'):
			self.neighbors.append(grid[self.row - 1][self.col+1])

		#diagonal up left	
		if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].check('check barrier'): 
			self.neighbors.append(grid[self.row - 1][self.col - 1])

		#diagonal down left	
		if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].check('check barrier'): 
			self.neighbors.append(grid[self.row + 1][self.col - 1])


class grid_construction_manipulation():

	def make_grid(self, rows, width):
		grid = []
		gap = width // rows
		for i in range(rows):
			grid.append([])
			for j in range(rows):
				Node = node(i, j, gap, rows)
				grid[i].append(Node)

		return grid


	def draw_grid(self, pygame_window ,rows, width):
		gap = width // rows
		for i in range(rows):
			p.draw.line(pygame_window, white, (0, i * gap), (width, i * gap))
			for j in range(rows):
				p.draw.line(pygame_window, white, (j * gap, 0), (j * gap, width))


	def draw(self,pygame_window, grid, rows, width):
		pygame_window.fill(black)

		for row in grid:
			for Node in row:
				Node.fill_color(pygame_window)

		self.draw_grid(pygame_window, rows, width)
		p.display.update()

	def reconstruct_path(came_from, current, draw):
		while current in came_from:
			current = came_from[current]
			current.make('make it final path')
			draw()


class A_star_algorithm(grid_construction_manipulation):

	

	def h_function(self,p1, p2):
		x1, y1 = p1
		x2, y2 = p2
		return math.sqrt((x2 - x1)**2 + abs(y2 - y1)**2)  # I have defined H function simply as direct shortest distance of two nodes

	def evaluate(self,draw, grid, start, end):
		count = 0
		open_set = PriorityQueue()
		open_set.put((0, count, start))
		came_from = {}
		g_score = {spot: float("inf") for row in grid for spot in row}
		g_score[start] = 0
		f_score = {spot: float("inf") for row in grid for spot in row}
		f_score[start] = self.h_function(start.position_row_col(), end.position_row_col())

		open_set_hash = {start}

		while not open_set.empty():
			for event in p.event.get():
				if event.type == p.QUIT:
					p.quit()

			current = open_set.get()[2]
			open_set_hash.remove(current)

			if current == end:
				grid_construction_manipulation.reconstruct_path(came_from, end, draw)
				end.make('make it end')
				return True

			for neighbor in current.neighbors:
				temp_g_score = g_score[current] + 1

				if temp_g_score < g_score[neighbor]:
					came_from[neighbor] = current
					g_score[neighbor] = temp_g_score
					f_score[neighbor] = temp_g_score + self.h_function(neighbor.position_row_col(), end.position_row_col())
					if neighbor not in open_set_hash:
						count += 1
						open_set.put((f_score[neighbor], count, neighbor))
						open_set_hash.add(neighbor)
						neighbor.make('make it open')

			draw()

			if current != start:
				current.make('make it close')

		return False

class BFS():
	pass

class DFS(grid_construction_manipulation):

	def distance_function(self,p1, p2):
		x1, y1 = p1
		x2, y2 = p2
		return math.sqrt((x2 - x1)**2 + abs(y2 - y1)**2)  # I have defined H function simply as direct shortest distance of two nodes

	def evaluate(self,draw, grid, start, end):

		start.visited = 1

		neigbours = start.neighbors 

		distance_param = []
		
		for x in neigbours:
			if(x.visited == 1):
				continue
			distance_param.append(abs(self.distance_function(x.position_row_col(), end.position_row_col())))
		

		for i in range(len(distance_param)):
			for j in range(len(distance_param)):
				if(distance_param[i]<distance_param[j]):
					temp = distance_param[i]
					distance_param[i] = distance_param[j]
					distance_param[j] = temp

					temp2 = neigbours[i]
					neigbours[i] = neigbours[j]
					neigbours[j] = temp2 

		for x in neigbours:

			if(x.visited == 1):
				continue

			if(x.position_row_col() == end.position_row_col()):
				print("lock")
				x.make('make it end')
				return True

			x.make('make it open')
			draw()
			para = self.evaluate(draw, grid, x, end)

			if(para==False):
				x.make('make it close')
			else:
				x.make('make it final path')
				return True
		
		return False

class Dyjkstra(grid_construction_manipulation):

	def distance_function(self,p1, p2):
		x1, y1 = p1
		x2, y2 = p2
		return math.sqrt((x2 - x1)**2 + abs(y2 - y1)**2)  # I have defined H function simply as direct shortest distance of two nodes

	def evaluate(self,draw, grid, start, end):
		count = 0
		open_set = PriorityQueue()
		open_set.put((0, count, start))
		came_from = {}
		g_score = {spot: float("inf") for row in grid for spot in row}
		g_score[start] = 0
		f_score = {spot: float("inf") for row in grid for spot in row}
		f_score[start] = self.distance_function(start.position_row_col(), end.position_row_col())

		open_set_hash = {start}

		while not open_set.empty():
			for event in p.event.get():
				if event.type == p.QUIT:
					p.quit()

			current = open_set.get()[2]
			open_set_hash.remove(current)

			if current == end:
				grid_construction_manipulation.reconstruct_path(came_from, end, draw)
				end.make('make it end')
				return True

			distance_param = []

			neigbours = current.neighbors

			for x in neigbours:

				distance_param.append(abs(self.distance_function(x.position_row_col(), end.position_row_col())))
			

			for i in range(len(distance_param)):
				for j in range(len(distance_param)):
					if(distance_param[i]<distance_param[j]):
						temp = distance_param[i]
						distance_param[i] = distance_param[j]
						distance_param[j] = temp

						temp2 = neigbours[i]
						neigbours[i] = neigbours[j]
						neigbours[j] = temp2 

			for neighbor in current.neighbors:
				temp_g_score = g_score[current] + 1

				if temp_g_score < g_score[neighbor]:
					came_from[neighbor] = current
					g_score[neighbor] = temp_g_score
					f_score[neighbor] = temp_g_score
					if neighbor not in open_set_hash:
						count += 1
						open_set.put((f_score[neighbor], count, neighbor))
						open_set_hash.add(neighbor)
						neighbor.make('make it open')

			draw()

			if current != start:
				current.make('make it close')

		return False


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

if __name__ == '__main__':
	
	class_grid = grid_construction_manipulation()
	param = input("enter 1 for A star, 2 for Dyjkstra, 3 for DFS")
	param = int(param)
	if(param==1):
		algo= A_star_algorithm()
	if(param==2):
		algo= Dyjkstra()
	if(param==3):
		algo= DFS()
	rows = input("enter the number of rows you want in your grid")
	rows = int(rows)
	grid = class_grid.make_grid(rows, width_of_window)

	start = None
	end = None

	run = True
	while run:
		class_grid.draw(pygame_window, grid, rows, width_of_window)
		for event in p.event.get():
			if event.type == p.QUIT:
				run = False

			if p.mouse.get_pressed()[0]: # LEFT
				pos = p.mouse.get_pos()
				row, col = get_clicked_pos(pos, rows, width_of_window)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make('make it start')

				elif not end and spot != start:
					end = spot
					end.make('make it end')

				elif spot != end and spot != start:
					spot.make('make it barrier')

			elif p.mouse.get_pressed()[2]: # RIGHT
				pos = p.mouse.get_pos()
				row, col = get_clicked_pos(pos, rows, width_of_window)
				spot = grid[row][col]
				spot.make('make path reset')
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == p.KEYDOWN:
				if event.key == p.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algo.evaluate(lambda: class_grid.draw(pygame_window, grid, rows, width_of_window), grid, start, end)

				if event.key == p.K_c:
					start = None
					end = None
					grid = class_grid.make_grid(rows, width_of_window)
	p.quit()

		
			