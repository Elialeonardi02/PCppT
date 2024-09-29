import ast

class comment:
    def __init__(self, text, start, end):
        self.comment_text=text
        self.start_position=start
        self.end_position=end
    comment_text =''
    start_position=[int, int] #line and position start
    end_position=[int, int] #line and position end
def extract_comments_with_positions(source_code):
    comments = []
    for i, line in enumerate(source_code.splitlines()):
        if '#' in line:
            # Trova la posizione del commento
            comment_start = line.index('#')
            comment_text = line[comment_start:].strip()
            # Posizione iniziale e finale del commento
            start_position = [i, comment_start]  # (linea, colonna)
            end_position = [i , len(line)]  # Fine della riga
            comments.append(comment(comment_text, start_position, end_position))
    return comments #['comment'(line_start,position_start),(line_end,position_end)]


def generate_commented_ast(file_path):
    with open(file_path, "r") as file:
        source_code = file.read()
    comments = extract_comments_with_positions(source_code)

    # Parsing del codice sorgente in un AST
    tree = ast.parse(source_code)

    return tree, comments