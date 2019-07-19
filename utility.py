import imgkit
import random
import pandas
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import six


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
	try:
		os.remove(fn)
	except Exception:
		pass
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

	img = Image.open(outputfile)
	width, height = img.size
	img = img.resize((int(width/1.2), int(height/1.2)), Image.ANTIALIAS)
	img.save(outputfile)

	return outputfile


def render_mpl_table(data, title=None, col_width=3.0, row_height=0.8, font_size=16, header_color='#40466e',
					 row_colors=['#f1f1f2', 'w'], edge_color='w', bbox=[0, 0, 1, 1],
					 header_columns=0,ax=None, **kwargs):
	if ax is None:
		size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
		fig, ax = plt.subplots(figsize=size)
		if title is not None:
			fig.suptitle(title, fontsize=22)
		# plt.close(fig)
		ax.axis('off')

	mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
	mpl_table.auto_set_font_size(False)
	mpl_table.set_fontsize(font_size)

	for k, cell in six.iteritems(mpl_table._cells):
		cell.set_edgecolor(edge_color)
		if k[0] == 0 or k[1] < header_columns:
			cell.set_text_props(weight='bold', color='w')
			cell.set_facecolor(header_color)
		else:
			cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
	plt.savefig('foo.png')
	return ax


if __name__ == "__main__":
	a = np.ones([10,9])
	a = pandas.DataFrame(a[1:], columns=['Radiant', 'Dire', 'Avg MMR', 'Game Mode', 'Spectators', 'Time', 'R Kills', 'D Kills', 'Gold Lead'])
	r = DataFrame_to_image(a, outputfile='test.png')
	print(r)