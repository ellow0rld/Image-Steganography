from PIL import Image
from google.colab.patches import cv2_imshow
import cv2
import ciphertext

#convert mssg to binary
def convert_to_binary(mssg):
		#print("Cipher text: ",mssg)
		bin = []
		for i in mssg:
			bin.append(format(ord(i), '08b'))
		#print("Binary data: ",bin)
		return bin

#Picture is encoded with mssg
def modPix(pix, mssg):

	binary_mssg = convert_to_binary(mssg)
	immssg = iter(pix)
	for i in range(len(binary_mssg)):

		# Extracting 3 pixels at a time for each character
		pix = [value for value in next(immssg)[:3] + next(immssg)[:3] + next(immssg)[:3]]
		#print("Original Pixels: ",pix)
		for j in range(0, 8):
			if (binary_mssg[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1
			elif (binary_mssg[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1

		if (i == len(binary_mssg) - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		#print("Modified Pixels: ",pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

#Encoding modified pixels in new image
def encode_enc(newimg, mssg):
	w = newimg.size[0]
	(x, y) = (0, 0)
 
	for pixel in modPix(newimg.getdata(), mssg):
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1
  
# Encode mssg into image
def encode():
	img = input("Enter cover image name(with .png) : ")
	print("Cover Image")
	image = cv2.imread(img)
	image = cv2.resize(image, (108, 60))
	cv2_imshow(image)
	image = Image.open(img, mode ='r')

	sec_mssg = input("\nEnter message to be encoded : ")
	mssg = ciphertext.sec_steg(sec_mssg)
	global password
	password = input("Create stego-key: ")
	if (len(mssg) == 0):
		raise ValueError('Message is empty')

	newimg = image.copy()
	encode_enc(newimg, mssg)

	newimg_name = input("Enter the name of Stego-image(with .png) : ")
	newimg.save(newimg_name, str(newimg_name.split(".")[1].upper()))
	print("Stego-Image:")
	newimg = cv2.imread(newimg_name)
	newimg = cv2.resize(newimg, (108, 60))
	cv2_imshow(newimg)

# Decode the mssg in the image
def decode():
	img = input("Enter Stego-image name(with .png) : ")
	image = Image.open(img, 'r')
	mssg = ''
	imgmssg = iter(image.getdata())

	while (True):
		pixels = [value for value in next(imgmssg)[:3] + next(imgmssg)[:3] + next(imgmssg)[:3]]
		binary_mssg = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binary_mssg += '0'
			else:
				binary_mssg += '1'

		mssg += chr(int(binary_mssg, 2))
	#mssg is encoded only for 8 pixs, the last 9th pix indicates if the message is over or not.
		if (pixels[-1] % 2 != 0):
			return mssg

#main
print(":: Welcome to Steganography ::\n")
encode()
x = input("\nDo you want to decode?(y/n) ")
if (x=='y'):
	msg = decode()
	print("Decoded message : " + msg)
	pas = input("Enter stego-key: ")
	if pas == password:
		print("Secret Message: ",ciphertext.sec_steg(msg))
	else:
		print("Incorrect Stego-key")

