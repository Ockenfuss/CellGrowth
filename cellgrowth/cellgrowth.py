#%%
import numpy as np
import matplotlib.pyplot as plt
# np.random.seed(123)
gamesize=100
total_cells=1000
gen_code=np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,4,2,2,0])
gen_code=np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,50,1,1,1,1,1,1,1,1,0])
# gen_code=np.array([1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,0])
generations=np.sum(gen_code)
print(f"number of cells: {np.sum([np.prod(gen_code[:i+1]) for i in range(len(gen_code))])}")

#Initialize arrays
idmap=-np.ones((gamesize, gamesize)).astype(int)
cell_x=-np.ones(total_cells).astype(int)
cell_y=-np.ones(total_cells).astype(int)
cell_gen=-np.ones(total_cells).astype(int)
cell_childs=-np.ones(total_cells).astype(int)
cell_max_childs=-np.ones(total_cells).astype(int)
#Test setup
# cell_x[:5]=[2,3,3,3,4]
# cell_y[:5]=[3,2,3,4,3]
# cell_gen[:5]=0
# cell_childs[:5]=0
# idmax=4

#set starting cell
cell_x[0]=int(gamesize/2)
cell_y[0]=int(gamesize/2)
cell_gen[0]=0
cell_childs[0]=0
cell_max_childs[0]=gen_code[0]
idmax=0
#Initialize map
ids=np.where(cell_x>0)[0]
idmap[cell_x[ids], cell_y[ids]]=ids

def make_map(idmap, cell_arr):
    cell_map=cell_arr[idmap]
    cell_map[idmap==-1]=-1
    return cell_map

def get_pos(id):
    return cell_x[id], cell_y[id]

def add_cell(x,y, gen):
    global idmax
    idmax+=1
    assert(idmap[x,y]==-1)
    assert(idmax<total_cells)
    idmap[x,y]=idmax
    cell_x[idmax]=x
    cell_y[idmax]=y
    cell_gen[idmax]=gen
    cell_childs[idmax]=0
    cell_max_childs[idmax]=gen_code[gen]#fix max_childs based on generation for now

def add_child(id, x,y):
    add_cell(x,y,cell_gen[id]+1)
    cell_childs[id]+=1

def shift_down(id, self=True, fill=True):
    x,y=get_pos(id)
    if not self:
        x+=1
    cell_x[idmap[x:-1,y]]+=1
    cell_x[idmap[-1,y]]=-1
    cell_y[idmap[-1,y]]=-1
    idmap[x+1:,y]=idmap[x:-1,y]
    idmap[x,y]=-1
    if fill:
        add_child(id, x,y)


def shift_up(id, self=True, fill=True):
    x,y=get_pos(id)
    if not self:
        x-=1
    cell_x[idmap[1:x+1,y]]-=1
    cell_x[idmap[0,y]]=-1
    cell_y[idmap[0,y]]=-1
    idmap[:x,y]=idmap[1:x+1,y]
    idmap[x,y]=-1
    if fill:
        add_child(id, x,y)

def shift_left(id, self=True, fill=True):
    x,y=get_pos(id)
    if not self:
        y-=1
    cell_y[idmap[x,1:y+1]]-=1
    cell_y[idmap[x,0]]=-1
    cell_x[idmap[x,0]]=-1
    idmap[x,:y]=idmap[x,1:y+1]
    idmap[x,y]=-1
    if fill:
        add_child(id, x,y)

def shift_right(id, self=True, fill=True):
    x,y=get_pos(id)
    if not self:
        y+=1
    cell_y[idmap[x,y:-1]]+=1
    cell_x[idmap[x,-1]]=-1
    cell_y[idmap[x,-1]]=-1
    idmap[x,y+1:]=idmap[x,y:-1]
    idmap[x,y]=-1
    if fill:
        add_child(id, x,y)

def count_up(id):
    x,y=get_pos(id)
    return np.sum(idmap[:x,y]>-1)

def count_down(id):
    x,y=get_pos(id)
    return np.sum(idmap[x+1:,y]>-1)

def count_right(id):
    x,y=get_pos(id)
    return np.sum(idmap[x,y+1:]>-1)

def count_left(id):
    x,y=get_pos(id)
    return np.sum(idmap[x,:y]>-1)

shift={1:"up", 2: "down", 3: "left", 4: "right"}

def split_cell(id):
    dir=shift[np.random.randint(1,5)]
    if dir == "up":
        if count_up(id)>count_down(id):
            shift_down(id)
        else:
            shift_up(id, self=False)
    if dir == "down":
        if count_up(id)<count_down(id):
            shift_up(id)
        else:
            shift_down(id, self=False)
    if dir == "left":
        if count_left(id)>count_right(id):
            shift_right(id)
        else:
            shift_left(id, self=False)
    if dir == "right":
        if count_left(id)<count_right(id):
            shift_left(id)
        else:
            shift_right(id, self=False)
            
def advance():
    for id in range(idmax+1):
        if cell_childs[id]<cell_max_childs[id]:
            split_cell(id)




for i in range(generations):
    advance()
#Plot
print(idmap)
gen_map=make_map(idmap, cell_gen)
masked_id=np.ma.masked_where(idmap==-1, gen_map)
fig, ax=plt.subplots()
ax.imshow(masked_id, extent=[0,gamesize, 0, gamesize], cmap='jet')
ax.grid(True)

# %%
