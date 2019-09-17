#SCRABBLE
from graphics import *
import scrabble_library

def main():
    w = GraphWin("Scrabble",800,600) # creating a window
    w.setBackground("light blue")
    left_board = Rectangle(Point(40,40),Point(200,540)) # creating left side board
    left_board.setFill("white")
    left_board.draw(w)
    l = []
    b = []
    b_color = []
    c,flag,index = 0,0,-1
    x,y = 60,90
    count = 0
    ifile = open("list.txt","r")
    for line in ifile:
        l.append(line[:-1])
        button = Rectangle(Point(x,y),Point(x+120,y+30))
        button.draw(w)
        button_text = Text(Point((x+60),(y+15)),l[c]) # x+60 = (x+x+120)/2, y+15 = (y+y+30)/2
        button_text.draw(w)
        b.append(button)
        b_color.append("white")
        y = y+20+30
        c = c + 1
    ifile.close()
    start_button = Rectangle(Point(60,450),Point(180,480)) # 'start over' button
    start_button.draw(w)
    start_button_text = Text(Point(120,465),"Start Over")
    start_button_text.draw(w)
    quit_button = Rectangle(Point(60,500),Point(180,530)) # 'quit' button
    quit_button.draw(w)
    quit_button_text = Text(Point(120,515),"Quit")
    quit_button_text.draw(w)
    main_board = Rectangle(Point(250,40),Point(750,540)) # right side main board
    main_board.setFill("white")
    main_board.draw(w)
    if scrabble_library.drawMainBoard(w,l):
        message = Text(Point(115,y+90),"CLICK ON A\nWORD BUTTON")
    else:
        message = Text(Point(115,y+90),"ENGINE FAILED\nPRESS QUIT")
    message.draw(w)
    while True:
        click = w.getMouse()
        if click.getX() > 60 and click.getX() < 180 and click.getY() > 450 and click.getY() < 480: # if 'start over' is clicked
            message.setText("CLICK ON A\nWORD BUTTON")
            count = 0
            scrabble_library.resetMainBoard()          
            for i in range(c):
                b_color[i] = "white"
                b[i].setFill("white")
        elif click.getX() > 60 and click.getX() < 180 and click.getY() > 500 and click.getY() < 530: # if 'quit' is clicked
            break;                                                                                                                                        
        elif click.getX() > 250 and click.getX() < 750 and click.getY() > 40 and click.getY() < 540:
            if flag == 1:  # checking if the cell is clicked after clicking a word button. 
               scrabble_library.checkMainBoard("",click)
               value = scrabble_library.checkMainBoard(l[index],click)
               if value == 1:
                   b[index].setFill("gray")
                   b_color[index] = "gray"
                   count = count + 1
                   if count == len(b):
                       message.setText("CONGRATS,\nYOU WON!")
                   else:
                       message.setText("CLICK ON A\nWORD TO\n CONTINUE")
               elif value == -1 or value == -2:
                   b[index].setFill("white")
                   b_color[index] = "white"
               else:
                   message.setText("CLICK ON A\nHEAD CELL\nOR TAIL CELL")                  
        else:
             for i in range(c):
                 if click.getX() > 60 and click.getX() < 180 and click.getY() > b[i].getP1().getY() and click.getY() < b[i].getP2().getY() and b_color[i] != "grey":
                       message.setText("NOW CLICK ON\nA CELL")
                       flag = 0
                       for j in range(c):
                           if b_color[j] == "red":
                                 b[j].setFill("white")  
                                 b_color[j] = "white"                                              
                       b[i].setFill("red")
                       b_color[i] = "red"
                       flag = 1
                       index = i
        continue                    
    w.close()
    exit()
main()
