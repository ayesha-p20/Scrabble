#SCRABBLE LIBRARY
from graphics import *
import random
import time
import copy

boxes = []
boxes_text = []
char_box_choose = None
char_box_coord = None



def drawMainBoard(window, words_list):
   order_words, intersec_list, count = generate_intersections(words_list)
   if count == -1:
      return False

   # print(order_words)
   # print(intersec_list)
   coord_lists = draw_chart(order_words, intersec_list)
   # print(coord_lists)
   drawn_dict = {}
   for coord_list in coord_lists:
      box_list = []
      box_text_list = []
      for coord in coord_list:
         if coord not in drawn_dict:
            box = Rectangle(Point(coord[0]-10,coord[1]-10), Point(coord[0]+10,coord[1]+10))
            box.draw(window)
            box_list.append(box)
            text = Text(Point(coord[0], coord[1]), "")
            text.draw(window)
            box_text_list.append(text)
            drawn_dict[coord] = (box, text)
         else:
            box_list.append(drawn_dict[coord][0])
            box_text_list.append(drawn_dict[coord][1])
      boxes.append(box_list)
      boxes_text.append(box_text_list)

   return True

def checkMainBoard(word, click):
   global char_box_choose, char_box_coord

   if click is None or type(click) != type(Point(0,0)):
      return 0

   for i in range(len(boxes)):
      box = boxes[i][0]
      if box.getP1().getX() < click.getX() < box.getP2().getX() and box.getP1().getY() < click.getY() < box.getP2().getY():
         if char_box_choose is not None:
            char_box_choose.setFill("white")
         char_box_choose = box
         char_box_choose.setFill("red")
         char_box_coord = (i, 1)
         break

      box = boxes[i][-1]
      if box.getP1().getX() < click.getX() < box.getP2().getX() and box.getP1().getY() < click.getY() < box.getP2().getY():
         if char_box_choose is not None:
            char_box_choose.setFill("white")
         char_box_choose = box
         char_box_choose.setFill("red")
         char_box_coord = (i, -1)
         break

   time.sleep(0.06)

   if char_box_choose is None or char_box_coord is None:
      return 0

   if word is None or type(word) != type("") or word == "":
      return 0

   i, direction = char_box_coord
   is_possible = True

   if len(boxes[i]) != len(word):
      # print("Error, length not match", len(boxes[i]), len(word))
      char_box_choose.setFill("white")
      char_box_coord = char_box_choose = None
      return -1

   for word_i, alphabet in enumerate(word):
      if direction < 0:
         word_i = -1 - word_i
      fill_alphabet = boxes_text[i][word_i].getText()
      # print("box not empty" if fill_alphabet != "" else "box empty", fill_alphabet, "equal" if fill_alphabet == alphabet else "not equal", alphabet)
      if fill_alphabet != "" and fill_alphabet != alphabet:
         char_box_choose.setFill("white")
         char_box_coord = char_box_choose = None
         return -2

   for word_i, alphabet in enumerate(word):
      if direction < 0:
         word_i = -1 - word_i
      boxes_text[i][word_i].setText(alphabet)

   char_box_choose.setFill("white")
   char_box_coord = char_box_choose = None
   return 1

def resetMainBoard():
   global char_box_choose, char_box_coord
   for i in range(len(boxes)):
      for j in range(len(boxes[i])):
         boxes_text[i][j].setText("")
         boxes[i][j].setFill("white")

   char_box_coord = char_box_choose = None



# this function generate a list of intersections and another list of index count used for the intersection so that this would help positioning the boxes in the chart.
# e.g. the first index of the intersection list is the index count of the second word in the words list
def generate_intersections(words_list):
   counter = 0
   alpha_str = "abcdefghijklmnopqrstuvwxyz"
   order_words = []
   intersection_list = []
   words = sorted(words_list, key=len, reverse=True)

   init_word_i = 0
   for i in range(len(words)-1):
      found = False
      while not found:
         counter += 1
         if( counter > len(words) * 10 ):
            return order_words, intersection_list, -1
         # print("now have", words)
         rand_word_i = random.randrange(0,len(words))
         while rand_word_i == init_word_i:
            rand_word_i = random.randrange(0,len(words))
         intersection = random.randrange(1,len(words[init_word_i])-1)
         intersect_char = words[init_word_i][intersection]
         while alpha_str.find(intersect_char) == -1:
            intersection = random.randrange(1,len(words[init_word_i])-1)
            intersect_char = words[init_word_i][intersection]
         count = 0
         for rand_word_char in words[rand_word_i]:
            count += 1
            if intersect_char == rand_word_char and (count != 1 or count != len(words[rand_word_i])):
               # print("The random index of the word is", intersect_char, "from word", words[init_word_i],"and", words[rand_word_i])
               found = True
               alpha_str = alpha_str.replace(intersect_char,'')
               break
         # print("searching", rand_word_i, words[rand_word_i])
      intersection_list.append((intersection, count-1))
      order_words.append(words[init_word_i])
      words.remove(words[init_word_i])
      if (init_word_i < rand_word_i):
         init_word_i = rand_word_i - 1
      else:
         init_word_i = rand_word_i
   order_words.append(words[0])

   return order_words, intersection_list, counter

# This funciton is used for drawing a small box in the chart and append this box into a list for future use
def draw_small_box(x_pos,y_pos, boxes):
   box = (x_pos,y_pos)
   if box in boxes:
      print("overlap")
   else:
      boxes.append(box)

# TODO, this is the todo part to draw the boxes using order_words and intersections_list
def draw_chart(order_words, intersections_list):
   boxes = []
   curr_x = 500
   curr_y = 295

   box_list = draw_word_horizontal(order_words[0],curr_x,curr_y,intersections_list[0][0])
   boxes.append(box_list)
   for i in range(1,len(order_words)):
      if (i%2==0):
         box_list = draw_word_horizontal(order_words[i],curr_x,curr_y,intersections_list[i-1][1])
         boxes.append(box_list)
         if( i != len(order_words) -1 ):
            curr_x = curr_x + (intersections_list[i][0]-intersections_list[i-1][1])*20
            dist = intersections_list[i][0]-intersections_list[i-1][1]
            #print ("moving", dist, "at round", i)
      else:
         box_list = draw_word_vertical(order_words[i],curr_x,curr_y,intersections_list[i-1][1])
         boxes.append(box_list)
         if( i != len(order_words) - 1 ):
            curr_y = curr_y + (intersections_list[i][0]-intersections_list[i-1][1])*20
            dist = intersections_list[i][0]-intersections_list[i-1][1]
            #print ("moving", dist, "at round", i)
   return boxes

# need a function to draw a word based on x_pixel and y_pixel
def draw_word_horizontal(word, x_pos, y_pos,start_index):
   boxes = []
   horizontal_increment = 20
   first_half = start_index
   second_half = len(word) - start_index
   for i in reversed(range(first_half+1)):
      draw_small_box(x_pos-horizontal_increment*i,y_pos,boxes)
   for i in range(1,second_half):
      draw_small_box(x_pos+horizontal_increment*i,y_pos,boxes)
   return boxes

def draw_word_vertical(word, x_pos, y_pos,start_index):
   vertical_increment = 20
   boxes = []
   #word_length = len(word) // 2
   first_half = start_index
   second_half = len(word) - start_index
   for i in reversed(range(first_half+1)):
      draw_small_box(x_pos, y_pos-vertical_increment*i,boxes)
   for i in range(1,second_half):
      draw_small_box(x_pos, y_pos+vertical_increment*i,boxes)
   return boxes
