import sys
import math
import pygame,copy
from pygame.locals import *
from sys import exit 
import queue as Q
import time

cost1=10
cost2=14
black=(17, 17, 18)
red=(235,64,52)
gray=(245, 243, 237)
blue=(79,126,227)
white=(247, 241, 237)
green=(31, 102, 46)
display_width=700
display_leight=1000
global II1_flag
global II2_flag
pcb=[[1 for i in range(10)] for j in range(10)]


class dot1 (pygame.sprite.Sprite ):

	def __init__(self,color=green,width=64,height=64):

		super(dot1,self).__init__()

		self.image=pygame.Surface((width,height))

		self.image.fill(color)

		self.rect=self.image.get_rect()

	def set_position(self,x,y):
		self.rect.x=x
		self.rect.y=y
	def draw_line(self):

		pygame.draw.line(gamedisplay,red,(100,80),(130,100))

	def set_image(self,filename=None):
		if filename!=None:
			self.image=pygame.image.load(filename)
			self.image=pygame.transform.smoothscale(self.image,(30,30))

class pairOfdot():

	def __init__(self,x, y, name):
		self.x = x
		self.y = y
		self.name=name
	def compareN(self,name):
		if self.name == name:
			return True
	def show(self):
		print(self.x,self.y,self.name)


def dot(x,y):
	pygame.draw.circle(gamedisplay,green,(x,y),8)

def setpic(x,y):
	gamedisplay.blit(space,x,y)

def setgrid(grid):
	for x in range(len(grid)):                       # select each line in the grid
		for y in range(len(grid[x])):                # identify each character in the line
			
			character = grid[x][y]                   # assign the grid reference to the variable character
			screen_x =30+(x*50)               # assign screen_x to screen starting position for x ie -588
			screen_y =30+(y*50)                # assign screen_y to screen starting position for y ie  288
			if character == 1:                     # if grid character contains an +
				dot(screen_x,screen_y)     

def drawtheline(Path):
	n=0
	length=len(Path)
	while (n<length-1):
		pygame.draw.line(gamedisplay,blue,((Path[n+1][1]*50+30),(Path[n+1][0]*50+30)),((Path[n][1]*50+30),(Path[n][0]*50+30)),5)
		n=n+1


def permutation(Set):
	lst=[]
	for n in Set:
		lst.append(n)
	k=len(lst)
	result = []
	length = len(lst)
	tmp = [0]*k
	def next_num(a,ni=0):
		if ni == k:
			result.append(copy.copy(tmp))
			return
		for lj in a:
			tmp[ni] = lj
			b = a[:]
			b.pop(a.index(lj))
			next_num(b,ni+1)
	c = lst[:]
	next_num(c,0)
	return result

def game_loop():
	print("Running...")
	path_list_show_index=0
	path_list_show=[] 
	text_Pos_list=[]
	path_result_cost_screen=""
	path_result_order_screen=""
	bumped=False
	A_star=0
	II_switch=L1_switch=L2_switch=n_switch=v_switch=0
	v_flag=II_flag=n_flag=L1_flag=L2_flag=0
	path_list=list()
	dot_group=pygame.sprite.Group()
	a_dot=dot1()
	queue = Q.PriorityQueue()
	picture1=dot1()
	picture1=pygame.image.load("agent1.png")
	picture1=pygame.transform.scale(picture1,(150,150))
	dot_group.add(a_dot)
	path=[]
	dots=[]
	nameSet=set()
	pcb_copy=copy.deepcopy(pcb)  
	text=pygame.font.Font(None,30)
	fail_text=text.render(None,True,white)
	while not bumped:
		gamedisplay.fill(black)
		setgrid(pcb)
		gamedisplay.blit(picture1,(650,30))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				bumped=True
			if event.type==pygame.MOUSEMOTION:
				mouse_pos=pygame.mouse.get_pos()
				a_dot.set_position(mouse_pos[0],mouse_pos[1])
			if event.type==pygame.KEYDOWN:
				II_key=L1_key=n_key=L2_key=v_key=0 # which II the users choose
				

				if(event.key==pygame.K_q):
					if II_switch==0:
						a_dot.set_image("II.png")
						II_switch=1
						II_key=1
					elif II_switch==1:
						a_dot.set_image("II2.png")
						II_switch=0
						II_key=2
				if(event.key==pygame.K_w):
					if L1_switch==0:
						a_dot.set_image("l1_1.png")
						L1_switch=1
						L1_key=2
					elif L1_switch==1:
						a_dot.set_image("l1.png")
						L1_switch=0
						L1_key=1
				if(event.key==pygame.K_e):
					if L2_switch==0:
						a_dot.set_image("l2.png")
						L2_switch=1
						L2_key=1
					elif L2_switch==1:
						a_dot.set_image("l2_1.png")
						L2_switch=0
						L2_key=2
				if(event.key==pygame.K_a):
					if n_switch==0:
						a_dot.set_image("n.png")
						n_switch=1
						n_key=1
					elif n_switch==1:
						a_dot.set_image("n1.png")
						n_switch=0
						n_key=2
				if(event.key==pygame.K_s):
					if v_switch==0:
						a_dot.set_image("v1.png")
						v_switch=1
						v_key=1
					elif v_switch==1:
						a_dot.set_image("v.png")
						v_switch=0
						v_key=2

				if(event.key==pygame.K_p):
					for i in range(len(pcb_copy)):
						print(pcb_copy[i])
					print('-------------------------------------------')
				if(event.key==pygame.K_m):
					time_start=time.time()
					if len(nameSet) !=0 and A_star!=1:
						A_star=1
						cost_set=set()
						fail_path=0
						permuta=permutation(nameSet)
						optimal_cost=0
						for lst in permuta:
							path_con=[]
							Total_cost=0
							pcb_per=copy.deepcopy(pcb_copy)
							path_flag=0
							for n in lst:
								con=[]
								for d in dots:
									if d.compareN(n):
										con.append(d)
								if len(con)==2:
									pcb_per[con[0].x][con[0].y]=1
									pcb_per[con[1].x][con[1].y]=1
									tmp,cost=Astar((con[0].x,con[0].y),(con[1].x,con[1].y),pcb_per)
									if(tmp ==None):
										path_flag=1
										print(lst,"failed!")
										break
									else:
										Remove_n(pcb_per,tmp)
										path_con.append(tmp)
										Total_cost=Total_cost+cost
								if len(con)==1:
									fail_path=1
							if path_flag==0:
								if Total_cost not in cost_set:
									queue.put((Total_cost,path_con,lst))
									cost_set.add(Total_cost)
						if queue.empty():
							print("No avaiable path!!")
							fail_path=1
						else:
							while not queue.empty():
								path_list_show.append(queue.get())#final_cost,final_path,lst
							for n in path_list_show[path_list_show_index][1]:
								path_list.append(n)
							print(path_list_show[path_list_show_index][2])
							print("Toal cost is " ,path_list_show[path_list_show_index][0])
							path_result_cost_screen=path_list_show[path_list_show_index][0]
							path_result_order_screen=path_list_show[path_list_show_index][2]
							path_list_show_index+=1
							picture1=pygame.image.load("agent2.png")
							picture1=pygame.transform.scale(picture1,(200,150))
						if fail_path==1:
							fail_text=text.render(("Sorry!Agent can not find paths for every pair of nodes"),True,red)
							picture1=pygame.image.load("agent3.png")
							picture1=pygame.transform.scale(picture1,(200,150))
					time_end=time.time()
					print('totally time cost',time_end-time_start)
				if(event.key==pygame.K_n):
					time_start=time.time()
					if len(nameSet) !=0 and A_star!=1:
						A_star=1
						cost_set=set()
						fail_path=0
						permuta=permutation(nameSet)
						optimal_cost=0
						optimal_path=[]
						optimal_list=[]
						for lst in permuta:
							path_con=[]
							Total_cost=0
							pcb_per=copy.deepcopy(pcb_copy)
							path_flag=0
							for n in lst:
								con=[]
								for d in dots:
									if d.compareN(n):
										con.append(d)
								if len(con)==2:
									pcb_per[con[0].x][con[0].y]=1
									pcb_per[con[1].x][con[1].y]=1
									tmp,cost=Astar((con[0].x,con[0].y),(con[1].x,con[1].y),pcb_per)
									if(tmp ==None):
										path_flag=1
										break
									else:
										Remove_n(pcb_per,tmp)
										path_con.append(tmp)
										Total_cost=Total_cost+cost
								if Total_cost>optimal_cost and optimal_cost!=0:
									break
								if len(con)==1:
									fail_path=1
							if path_flag==0:
								if Total_cost < optimal_cost or optimal_cost==0 :
									optimal_cost=Total_cost
									optimal_path=path_con
									optimal_list=lst
									path_result_cost_screen=optimal_cost
						if optimal_cost==0:
							print("No avaiable path!!")
							fail_path=1
						else:
							for n in optimal_path:
								path_list.append(n)
							print("Toal cost is " ,optimal_cost)
							path_result_order_screen=optimal_list
							path_list_show_index+=1
							picture1=pygame.image.load("agent2.png")
							picture1=pygame.transform.scale(picture1,(200,150))
						if fail_path==1:
							fail_text=text.render(("Sorry!Agent can not find paths for every pair of nodes"),True,red)
							picture1=pygame.image.load("agent3.png")
							picture1=pygame.transform.scale(picture1,(200,150))
					time_end=time.time()
					print('totally cost',time_end-time_start)


			if event.type==pygame.MOUSEBUTTONUP :
				a1_dot=dot1()
				type_n=0
				if II_flag !=1 and II_key==2:
					a1_dot.set_image("II2.png")
					type_n=1
					II_flag=1
				if  II_flag !=1 and II_key==1:
					a1_dot.set_image("II.png")
					type_n=2
					II_flag=1
				if  L1_flag !=1 and L1_key==1:
					a1_dot.set_image("l1.png")
					type_n=1
					L1_flag=1
				if  L1_flag !=1 and L1_key==2:
					a1_dot.set_image("l1_1.png")
					type_n=2
					L1_flag=1
				if  L2_flag !=1 and L2_key==1:
					a1_dot.set_image("l2.png")
					type_n=1
					L2_flag=1
				if  L2_flag !=1 and L2_key==2:
					a1_dot.set_image("l2_1.png")
					type_n=2
					L2_flag=1
				if n_flag !=1 and n_key==2:
					a1_dot.set_image("n1.png")
					type_n=1
					n_flag=1
				if  n_flag !=1 and n_key==1:
					a1_dot.set_image("n.png")
					type_n=2
					n_flag=1
				if  v_flag !=1 and v_key==1:
					a1_dot.set_image("v1.png")
					type_n=1
					v_flag=1
				if  v_flag !=1 and v_key==2:
					a1_dot.set_image("v.png")
					type_n=2
					v_flag=1
				if type_n==1:
					mouse_pos=pygame.mouse.get_pos()
					a1_dot.set_position(mouse_pos[0],mouse_pos[1])
					dot_group.add(a1_dot)
					y_pos=round((mouse_pos[0]-30)/50)
					x_pos=round((mouse_pos[1]-30)/50)
					pcb_copy[x_pos][y_pos]=0
					pcb_copy[x_pos][y_pos+1]=0
					name1=input("Please input a name for one dot: ")
					name2=input("Please input a name for one dot: ")
					nameSet.add(name1)
					nameSet.add(name2)
					text_Pos_list.append([name1,(y_pos*50+30,x_pos*50+30)])
					text_Pos_list.append([name2,((y_pos+1)*50+30,x_pos*50+30)])
					pairD1=pairOfdot(x_pos,y_pos,name1)
					pairD2=pairOfdot(x_pos,y_pos+1,name2)
					dots.append(pairD1)
					dots.append(pairD2)
					print(x_pos,y_pos)
					print(x_pos,y_pos+1)
				if type_n==2:
					mouse_pos=pygame.mouse.get_pos()
					a1_dot.set_position(mouse_pos[0],mouse_pos[1])
					dot_group.add(a1_dot)
					y_pos=round((mouse_pos[0]-30)/50)
					x_pos=round((mouse_pos[1]-30)/50)
					pcb_copy[x_pos][y_pos]=0
					pcb_copy[x_pos+1][y_pos]=0
					name1=input("Please input a name for one dot: ")
					name2=input("Please input a name for one dot: ")
					nameSet.add(name1)
					nameSet.add(name2)
					text_Pos_list.append([name1,(y_pos*50+20,x_pos*50+20)])
					text_Pos_list.append([name2,(y_pos*50+20,(x_pos+1)*50+20)])
					pairD1=pairOfdot(x_pos,y_pos,name1)
					pairD2=pairOfdot(x_pos+1,y_pos,name2)
					dots.append(pairD1)
					dots.append(pairD2)
					print(x_pos,y_pos)
					print(x_pos+1,y_pos)

			if event.type==pygame.KEYDOWN:
				if(event.key==pygame.K_n):
					for p in path_list:
						print(p)


			if event.type==pygame.KEYDOWN:
				if len(path_list_show)>1:
					if len(nameSet) !=0:
						if(event.key==pygame.K_t):
							if path_list_show_index ==len(path_list_show):
								path_list_show_index=0
							path_list.clear()
							for n in path_list_show[path_list_show_index][1]:
								path_list.append(n)
							print(path_list_show[path_list_show_index][2])
							print("Toal cost is " ,path_list_show[path_list_show_index][0])
							path_result_cost_screen=path_list_show[path_list_show_index][0]
							path_result_order_screen=path_list_show[path_list_show_index][2]
							path_list_show_index+=1

		for n in path_list:
			if n!=None:
				drawtheline(n)
		dot_group.draw(gamedisplay)
		for n in text_Pos_list:
			text_node=text.render(n[0],True,red)
			gamedisplay.blit(text_node,n[1])

		text_cost_text=text.render(("Total Cost: "),True,blue)
		gamedisplay.blit(text_cost_text,(500,220))

		text_cost=text.render(str(path_result_cost_screen),True,blue)
		gamedisplay.blit(text_cost,(630,220))

		text_order_text=text.render(("Order of node's name: "),True,blue)
		gamedisplay.blit(text_order_text,(500,250))

		text_order=text.render(str(path_result_order_screen),True,blue)
		gamedisplay.blit(text_order,(750,250))

		text_order_text=text.render(("----------------------------------------------"),True,blue)
		gamedisplay.blit(text_order_text,(500,270))

		text_order_text=text.render(("Instruction: "),True,blue)
		gamedisplay.blit(text_order_text,(500,290))

		text_order_text=text.render(("Type Q,W,E,A,S to change different component. "),True,blue)
		gamedisplay.blit(text_order_text,(500,320))

		text_order_text=text.render(("Set the name of each node in the terminal. "),True,blue)
		gamedisplay.blit(text_order_text,(500,350))

		text_order_text=text.render(("When all names are set, you can type m or n. "),True,blue)
		gamedisplay.blit(text_order_text,(500,380))

		text_order_text=text.render(("m: To get all the possible solutions. "),True,blue)
		gamedisplay.blit(text_order_text,(500,410))

		text_order_text=text.render(("n: To get the optimal solution. "),True,blue)
		gamedisplay.blit(text_order_text,(500,440))

		text_order_text=text.render(("If used m command, you can type t to switch. "),True,blue)
		gamedisplay.blit(text_order_text,(500,470))

		gamedisplay.blit(fail_text,(300,600))

		pygame.display.update()
		clock.tick(60)


def Remove_n(PCB_nodes, Path_to_remove):
	a=Path_to_remove[0][0]
	b=Path_to_remove[0][1]
	for rm in Path_to_remove:
		if rm[0]-a!=0 and rm[1]-b!=0:
			PCB_nodes[a][b]=2
			PCB_nodes[rm[0]][rm[1]]=2
		else:
			PCB_nodes[rm[0]][rm[1]]=0
		a=rm[0]
		b=rm[1]

def Cal_heuristic (Start_node, Target_node):
	distance=math.sqrt(((Target_node[0]-Start_node[0])*5)**2+((Target_node[1]-Start_node[1])*5)**2)
	return distance

def get_next(cur_node,PCB_nodes):
	next_list=[]
	a=0
	b=0
	c=0
	d=0
	if cur_node[1]-1>=0 :
		if PCB_nodes[cur_node[0]][cur_node[1]-1]!=0 and PCB_nodes[cur_node[0]][cur_node[1]-1]!=2: #left
			next_list.append((cur_node[0],cur_node[1]-1,cost1))
			a=1

	if cur_node[1]+1<10 :
		if PCB_nodes[cur_node[0]][cur_node[1]+1]!=0 and PCB_nodes[cur_node[0]][cur_node[1]+1]!=2: #right
			next_list.append((cur_node[0],cur_node[1]+1,cost1))
			b=1

	if cur_node[0]-1>=0 :
		if PCB_nodes[cur_node[0]-1][cur_node[1]]!=0 and PCB_nodes[cur_node[0]-1][cur_node[1]]!=2: #up
			next_list.append((cur_node[0]-1,cur_node[1],cost1))
			c=1

	if cur_node[0]+1<10 :
		if PCB_nodes[cur_node[0]+1][cur_node[1]]!=0 and PCB_nodes[cur_node[0]+1][cur_node[1]]!=2: #down
			next_list.append((cur_node[0]+1,cur_node[1],cost1))
			d=1

	if cur_node[0]-1>=0 and cur_node[1]-1>=0 :
		if PCB_nodes[cur_node[0]-1][cur_node[1]-1]!=0 and PCB_nodes[cur_node[0]-1][cur_node[1]-1]!=2: #left up:
			if PCB_nodes[cur_node[0]][cur_node[1]-1]!=2 or PCB_nodes[cur_node[0]-1][cur_node[1]]!=2:
				next_list.append((cur_node[0]-1,cur_node[1]-1,cost2))

	if cur_node[0]+1<10 and cur_node[1]-1>=0 :
		if PCB_nodes[cur_node[0]+1][cur_node[1]-1]!=0 and PCB_nodes[cur_node[0]+1][cur_node[1]-1]!=2: #left down
				if PCB_nodes[cur_node[0]][cur_node[1]-1]!=2 or PCB_nodes[cur_node[0]+1][cur_node[1]]!=2:
					next_list.append((cur_node[0]+1,cur_node[1]-1,cost2))

	if cur_node[0]-1>=0 and cur_node[1]+1<10 :
		if PCB_nodes[cur_node[0]-1][cur_node[1]+1]!=0 and PCB_nodes[cur_node[0]-1][cur_node[1]+1]!=2: #right up
				if PCB_nodes[cur_node[0]][cur_node[1]+1]!=2 or PCB_nodes[cur_node[0]-1][cur_node[1]]!=2:
					next_list.append((cur_node[0]-1,cur_node[1]+1,cost2))

	if cur_node[0]+1<10 and cur_node[1]+1<10:
		if PCB_nodes[cur_node[0]+1][cur_node[1]+1]!=0 and PCB_nodes[cur_node[0]+1][cur_node[1]+1]!=2: #right down
				if PCB_nodes[cur_node[0]][cur_node[1]+1]!=2 or PCB_nodes[cur_node[0]+1][cur_node[1]]!=2:
					next_list.append((cur_node[0]+1,cur_node[1]+1,cost2))
	return next_list

def Astar(Start_node,Target_node, PCB_nodes):
	visited=[]
	queue = Q.PriorityQueue()
	path=list()
	pre={}
	queue.put((0,0,Start_node,None))
	while not queue.empty():
		h,c,cur,pren=queue.get()
		if cur not in visited:
			visited.append(cur)
			pre[cur]=pren
			if cur == Target_node :
				while pre[cur]!=None:
					path.append(cur)
					cur=pre[cur]
				path.append(Start_node)
				return path[::-1],c
			for w in get_next(cur,PCB_nodes):
				if w[0] != cur:
					queue.put((Cal_heuristic((w[0],w[1]),Target_node)+c+w[2],c+w[2],(w[0],w[1]),cur))
	return None,None

pygame.init()
gamedisplay=pygame.display.set_mode((display_leight,display_width),pygame.RESIZABLE)
pygame.display.set_caption("PCB")
clock=pygame.time.Clock()
game_loop()
pygame.quit()
quit()




