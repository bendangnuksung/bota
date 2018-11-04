import imgkit
import random
import pandas
import os
import cv2


css = """
<style type=\"text/css\">
table {
color: #FAFAFA;
font-family: Helvetica, Arial, sans-serif;
width: 1300px;
border-collapse:
collapse; 
border-spacing: 0;
}

td, th {
border: 1px solid transparent; /* No more visible border */
height: 30px;
}

th {
background: #363636; /* Darken header a bit */
font-weight: bold;
font-size: 25;
}

td {
background: #5a6372;
text-align: center;
font-size: 20;
}

table tr:nth-child(odd) td{
background-color: #5a6372;
}
</style>
"""


def DataFrame_to_image(data, css=css, outputfile="out.png", format="png"):
	'''
	For rendering a Pandas DataFrame as an image.
	data: a pandas DataFrame
	css: a string containing rules for styling the output table. This must 
	     contain both the opening an closing <style> tags.
	*outputimage: filename for saving of generated image
	*format: output format, as supported by IMGKit. Default is "png"
	'''
	fn = str(random.random()*100000000).split(".")[0] + ".html"
	print(fn)
	try:
		os.remove(fn)
	except:
		None
	text_file = open(fn, "a")

	# write the CSS
	text_file.write(css)
	# write the HTML-ized Pandas DataFrame
	text_file.write(data.to_html())
	text_file.close()

	# See IMGKit options for full configuration,
	# e.g. cropping of final image
	imgkitoptions = {"format": format}

	imgkit.from_file(fn, outputfile, options=imgkitoptions)
	os.remove(fn)
	img = cv2.imread(outputfile)
	img = cv2.resize(img, (int(img.shape[1]/1.2), int(img.shape[0]/1.2)))
	cv2.imwrite(outputfile, img)
	return outputfile


if __name__ == "__main__":
	import numpy as np
	a = np.ones([10,9])
	a = pandas.DataFrame(a[1:], columns=['Radiant', 'Dire', 'Avg MMR', 'Game Mode', 'Spectators', 'Time', 'R Kills', 'D Kills', 'Gold Lead'])
	r = DataFrame_to_image(a, outputfile='test.png')
	print(r)