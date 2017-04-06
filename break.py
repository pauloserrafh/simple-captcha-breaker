from PIL import Image
import hashlib
import pytesseract
from operator import itemgetter
from scipy.misc import imsave
import numpy
import os
import math

class VectorCompare:
  def magnitude(self,concordance):
    total = 0
    for word,count in concordance.iteritems():
      total += count ** 2
    return math.sqrt(total)

  def relation(self,concordance1, concordance2):
    relevance = 0
    topvalue = 0
    for word, count in concordance1.iteritems():
      if concordance2.has_key(word):
        topvalue += count * concordance2[word]
    return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

def buildvector(im):
  d1 = {}

  count = 0
  for i in im.getdata():
    d1[count] = i
    count += 1

  return d1

def clear_image(image, color):
  for y in range(image.size[1]):
    for x in range(image.size[0]):
      current = image.getpixel((x, y))
      if (current == color):
        image.putpixel((x, y), 255)
  return image

def remove_background(img_path):
  image = Image.open(img_path)

  #force all images to be the same type and size
  # image = image.convert("P")
  # image = image.resize((146,58))

  # print image.getpixel((0,0))
  # print image.size
  # crop = image.crop((20,15, 125, 50))
  # crop.save('images/croped.gif')
  # i = 0
  for y in range(0,image.size[1]):
    for x in range(0, image.size[0]):
      #Avoid getting points in the center that could be the letters
      if (20 < x and x < 125):
        if (15 < y and y < 50):
          continue
      if (15 < y and y < 50):
        if (20 < x and x < 110):
          continue
      pixel_color = image.getpixel((x,y))
      if (pixel_color == 255):
        continue
      image = clear_image(image, pixel_color)
      #For debug
      # image.save('images/clear'+str(i)+'.gif')
      # i = i + 1
  return image

def black_chars(image):
  # his = image.histogram()
  # values = {}

  # for i in range(256):
  #   values[i] = his[i]

  # for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
  #   print j,k
  for y in range(image.size[1]):
    for x in range(image.size[0]):
      if (image.getpixel((x,y)) != 255):
        image.putpixel((x, y), 0)

  # For some reason, when saving using image.save() it saves an all black
  # image. Creating a numpy array and saving does the trick.

  # image.save('images/final.gif')
  # img = numpy.array(image)
  # imsave('images/array.gif', img)

  return image
  # text = pytesseract.image_to_string(Image.open('images/array.gif'))
  # print text

def crop_letters(image):
  #Crop first letter
  first = image.crop((25,15, 48, 50))
  fst = numpy.array(first)
  imsave('images/first.gif', fst)
  # text = pytesseract.image_to_string(Image.open('images/first.gif'))
  # print text

  #Crop second letter
  second = image.crop((46,15, 66, 50))
  scd = numpy.array(second)
  imsave('images/second.gif', scd)
  # text = pytesseract.image_to_string(Image.open('images/second.gif'))
  # print text

  #Crop third letter
  third = image.crop((64,15, 84, 50))
  thd = numpy.array(third)
  imsave('images/third.gif', thd)
  # text = pytesseract.image_to_string(Image.open('images/third.gif'))
  # print text

  #Crop fourth letter
  fourth = image.crop((82,15, 102, 50))
  fth = numpy.array(fourth)
  imsave('images/fourth.gif', fth)
  # text = pytesseract.image_to_string(Image.open('images/fourth.gif'))
  # print text


  #Crop fifth letter
  fifth = image.crop((100,15, 120, 50))
  fth = numpy.array(fifth)
  imsave('images/fifth.gif', fth)
  # text = pytesseract.image_to_string(Image.open('images/fifth.gif'))
  # print text

def find_edges(x, y, left, right):
  pix = image.getpixel((x,y))
  #White pixel or was already visited
  if pix != 0:
    return (left, right)

  #Mark it as visited
  image.putpixel((x, y), 1)

  my_left = left
  my_right = right
  if (x < left):
    my_left = x
  if (x > right):
    my_right = x

  l_left, l_right = find_edges((x-1), y, my_left, my_right)
  r_left, r_right = find_edges((x+1), y, my_left, my_right)
  u_left, u_right = find_edges(x, (y+1), my_left, my_right)
  b_left, b_right = find_edges(x, (y-1), my_left, my_right)

  l = min(l_left, r_left, u_left, b_left, my_left)
  r = max(l_right, r_right, u_right, b_right, my_right)

  return (l, r)

def find_letters(image):
  letters = []

  for x in range(image.size[0]): # slice across
    for y in range(image.size[1]): # slice down
      pix = image.getpixel((x,y))
      if pix == 0:
        start, end = find_edges(x, y, x, x)
        letters.append((start,end))
        x = end
        break
  i = 0

  #In case letters are connected for some reason
  #Split the biggest elements in half
  while (len(letters) < 5):
    diff = 0
    for letter in letters:
      d = letter[1]-letter[0]
      if (d > diff):
        diff = d
        grt = letters.index(letter)
    s, e = letters.pop(grt)
    mid = (s+e)/2
    letters.insert(grt, (s, mid))
    letters.insert(grt+1, (mid+1, e))

  #Create the images
  for letter in letters:
    im3 = image.crop(( letter[0] , 0, letter[1],image.size[1] ))
    arr = numpy.array(im3)
    imsave('images/test'+str(i)+'.gif', im3)
    i += 1

def deCaptcha(imageset, vector):
  letters = ["first", "second", "third", "fourth", "fifth"]

  for l in letters:
    im3 = Image.open('images/'+ l +'.gif')
    guess = []

    for image in imageset:
      for x,y in image.iteritems():
        if len(y) != 0:
          guess.append( ( v.relation(y[0],buildvector(im3)),x))
    guess.sort(reverse=True)
    print "",guess[0]

if __name__ == "__main__":
  image_name = 'captcha5'
  image_ext = '.gif'
  image_in = 'images/' + image_name + image_ext
  image_out= 'images/' + image_name + 'out.jpg'

  v = VectorCompare()
  iconset = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  imageset = []

  # Create the set of images to compare
  for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
      temp = []
      if img != "Thumbs.db": # windows check...
        temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
      imageset.append({letter:temp})

  image = remove_background(image_in)
  image = black_chars(image)
  find_letters(image)
  # crop_letters(image)
  # deCaptcha(imageset, v)
