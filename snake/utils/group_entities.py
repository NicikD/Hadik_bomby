# Groups static entities that   to create static groups using depth first search
#  used in the static engine


def dfs(grid, visited, x, y, current_group):
    """Perform DFS to find all overlapping shapes."""
    # Directions for left, right, up, down movements
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if visited[cx][cy]:
            continue

        visited[cx][cy] = True
        current_group.append((cx, cy))

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            # Check boundaries and ensure we are visiting only same shapes
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not visited[nx][ny]:
                stack.append((nx, ny))


def find_overlapping_groups(grid):
    """Find all groups of overlapping shapes."""
    if not grid or not grid[0]:
        return []

    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    groups = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not visited[i][j]:
                current_group = []
                dfs(grid, visited, i, j, current_group)
                if current_group:
                    groups.append(current_group)

    return groups

