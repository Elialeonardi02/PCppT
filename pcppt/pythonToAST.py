import ast

class comment:  #comment on the python code source
    
    def __init__(self, text, start, end):
        self.comment_text=text      #text of the comment
        self.start_position=start   #[line,position] where the comment starts (position of #)
        self.end_position=end       #[line,position] where the comment ends (position of #)
    comment_text =''
    start_position=[int, int]
    end_position=[int, int] 
    
def extractComments(source_code):
    comments = []
    for i, line in enumerate(source_code.splitlines()): #read python source file line by line
        if '#' in line:
            #find the position where the comment starts
            comment_start = line.index('#')
            start_position = [i, comment_start]

            #find the position where the comment ends
            end_position = [i , len(line)]

            comment_text = line[comment_start:].strip()+'\n'
            comments.append(comment(comment_text, start_position, end_position))
    return comments #['comment'(line_start,column_start),(line_end,column_end)]


def generateAstComments(source):
    try:
        with open(source, "r") as file:
            source_code = file.read()
    except FileNotFoundError:   #source is python code
        source_code = source
    finally:
        comments = extractComments(source_code)
        tree = ast.parse(source_code)
        return tree, comments
