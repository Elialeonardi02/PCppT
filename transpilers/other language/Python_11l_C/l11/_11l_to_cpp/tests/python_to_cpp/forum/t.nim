
proc y(): int =
    1

proc f(x: int): int =
    x+y()

echo f(1)
