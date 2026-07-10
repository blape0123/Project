from PIL import Image, ImageDraw
import math

width, height = 200, 120
img = Image.new('RGB', (width, height), (0, 0, 0))
d = ImageDraw.Draw(img)

for x in range(20, 180):
    d.point((x, 40), fill=(220, 20, 20))
for y in range(40, 90):
    d.point((180, y), fill=(220, 20, 20))
for x in range(50, 180):
    d.point((x, 90), fill=(220, 20, 20))
for y in range(35, 46):
    for x in range(20, 180):
        d.point((x, y), fill=(220, 20, 20))
for y in range(86, 96):
    for x in range(50, 180):
        d.point((x, y), fill=(220, 20, 20))
for x in range(176, 181):
    for y in range(40, 90):
        d.point((x, y), fill=(220, 20, 20))

img.save('sample-maze.png')

canvas_width, canvas_height = width, height
image_data = img.load()

start = (20, 40)
end = (179, 89)
start_color = image_data[start]

def create_grid_from_color(color):
    grid = [0] * (canvas_width * canvas_height)
    tolerance = 100
    for y in range(canvas_height):
        for x in range(canvas_width):
            r, g, b = image_data[x, y]
            dr = r - color[0]
            dg = g - color[1]
            db = b - color[2]
            dist = math.sqrt(dr*dr + dg*dg + db*db)
            grid[y * canvas_width + x] = 1 if dist <= tolerance else 0
    return grid

def find_path(grid, start, end):
    sw, sh = start
    ew, eh = end
    start_idx = sh * canvas_width + sw
    end_idx = eh * canvas_width + ew
    if not grid[start_idx] or not grid[end_idx]:
        return None
    q = [start_idx]
    visited = [False] * (canvas_width * canvas_height)
    prev = [-1] * (canvas_width * canvas_height)
    visited[start_idx] = True
    dirs = [1, -1, canvas_width, -canvas_width]
    while q:
        current = q.pop(0)
        if current == end_idx:
            break
        cy = current // canvas_width
        cx = current % canvas_width
        for delta in dirs:
            nx = cx + (1 if delta == 1 else -1 if delta == -1 else 0)
            ny = cy + (1 if delta == canvas_width else -1 if delta == -canvas_width else 0)
            if nx < 0 or nx >= canvas_width or ny < 0 or ny >= canvas_height:
                continue
            next_idx = current + delta
            if visited[next_idx] or not grid[next_idx]:
                continue
            visited[next_idx] = True
            prev[next_idx] = current
            q.append(next_idx)
    if not visited[end_idx]:
        return None
    path = []
    idx = end_idx
    while idx != -1:
        path.append((idx % canvas_width, idx // canvas_width))
        idx = prev[idx]
    path.reverse()
    return path

grid = create_grid_from_color(start_color)
path = find_path(grid, start, end)
print('start_color', start_color)
print('path length', len(path) if path else 'not found')
if path:
    print('start', path[0], 'end', path[-1])
    print('segment sample', path[:5], path[-5:])
