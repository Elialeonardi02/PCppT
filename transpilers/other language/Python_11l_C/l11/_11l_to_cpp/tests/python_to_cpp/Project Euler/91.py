def is_right_triangle(x1, y1, x2, y2):
    a = x1*x1 + y1*y1
    b = x2*x2 + y2*y2
    c = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
    return (a + b == c) or (b + c == a) or (c + a == b)

LIMIT = 51
ans = 0
for x1 in range(LIMIT):
    for y1 in range(LIMIT):
        for x2 in range(LIMIT):
            for y2 in range(LIMIT):
                # For uniqueness, ensure that (x1,y1) has a larger angle than (x2,y2)
                if y2 * x1 < y1 * x2 and is_right_triangle(x1, y1, x2, y2):
                    ans += 1
print(ans)