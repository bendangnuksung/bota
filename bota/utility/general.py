import imgkit
import random
import pandas
import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import six
from matplotlib.cbook import get_sample_data
from bota.web_scrap import scrap_constant
from bota.constant import css, TLG_IMAGE_PATH, CT_IMAGE_PATH
from bota import constant
import os
from datetime import datetime
import re
from bota.constant import REPO_PATH

repo_abs_path = REPO_PATH


def DataFrame_to_image(data, css=css, outputfile=TLG_IMAGE_PATH, format="png"):
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


def get_icon_path(heroes_list, icon_size='small'):
	if icon_size == 'small':
		icon_directory = scrap_constant.icons_path_small
	else:
		icon_directory = scrap_constant.icons_path_big
	icon_paths = []
	for hero in heroes_list:
		hero = hero.lower().strip()
		hero = re.sub('[^a-z- ]', '', hero)
		hero = hero.replace(' ', '-')
		hero_icon_path = os.path.join(*[repo_abs_path, icon_directory, hero + '.png'])
		icon_paths.append(hero_icon_path)
	return icon_paths


def get_icon_axis(icon_index):
	x, y, width, height = scrap_constant.icon_x, scrap_constant.icon_y, scrap_constant.icon_width, scrap_constant.icon_height
	y = y - (scrap_constant.icon_height_diff * icon_index)
	return [x, y, width, height]


def render_mpl_table(data, icon_list=[], title=None, image_path=CT_IMAGE_PATH, col_width=3.0, row_height=1.2,
					 font_size=16, header_color='#40466e', row_colors=['#f1f1f2', 'w'],
					 edge_color='w', bbox=[0, 0, 1, 1], header_columns=0,ax=None, **kwargs):
	"""
	Given a panda datframe, converting to an table image.
	If icon_list is provided, the corresponding hero icon will be appended to each row
	"""
	if ax is None:
		size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
		fig, ax = plt.subplots(figsize=size)
		if title is not None:
			fig.suptitle(title, fontsize=font_size+6)
		# plt.close(fig)
		ax.axis('off')

	if len(icon_list):
		for i, icon_path in enumerate(icon_list):
			image = plt.imread(get_sample_data(icon_path))
			icon_axis = get_icon_axis(i)
			newax = fig.add_axes(icon_axis, anchor='NE', zorder=-1)
			newax.imshow(image)
			newax.axis('off')

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
	dir_path = os.path.dirname(image_path)
	if not os.path.isdir(dir_path):
		os.makedirs(dir_path)
	plt.savefig(image_path)
	plt.clf()
	return image_path


def is_file_old(file_path, sec_threshold):
	'''
	Check if file is older than given threshold
	:param file_path:
	:param sec_threshold:
	:return:
	'''
	if not os.path.isfile(file_path):
		# No file at all, so creating new
		return True
	current_ctime = datetime.now().timestamp()
	file_ctime = os.path.getmtime(file_path)
	time_diff = (current_ctime - file_ctime)
	if time_diff < sec_threshold:
		return False
	return True


def crop_image(image, coords):
	'''
	:param image: numpy image
	:param coords: <list> [xmin, ymin, xmax, ymax]
	:return:
	'''
	cropped_image = image[coords[1]: coords[3], coords[0]: coords[2]]
	return cropped_image


def get_medal_image_path(medal_name, rank=None):
	medal_list = medal_name.split()
	if len(medal_list) > 1:
		medal_name = medal_list[0].strip()
		medal_no = constant.MEDAL_NUMBERING[medal_list[1].strip()]
		medal_image_path = os.path.join(constant.MEDAL_IMAGE_PATH, medal_name + '-' + str(medal_no) + '.png')
		return medal_image_path
	else:
		medal_name = medal_name.strip()
		if rank is None or not len(rank):
			medal_image_path = os.path.join(constant.MEDAL_IMAGE_PATH, medal_name + '.png')
		else:
			rank = int(rank)
			if rank <= 10:
				medal_name = constant.MEDAL_IMMORTAL_UNDER[10]
			elif rank <= 100:
				medal_name = constant.MEDAL_IMMORTAL_UNDER[100]
			else:
				medal_name = constant.MEDAL_IMMORTAL_UNDER[5000]
			medal_image_path = os.path.join(constant.MEDAL_IMAGE_PATH, medal_name)
		return medal_image_path


def get_html_text(url):
	r = requests.get(url, headers=scrap_constant.browser_headers)
	html_text = r.text
	return html_text


def round_df_digits(df):
	df = (df.astype(float).applymap('{:,.2f}'.format))
	return df


if __name__ == "__main__":
	import cv2
	image = cv2.imread('/home/ben/personal/discord-dota-bot/data/temp_images/ursa_skill.png')
	new_image = crop_image(image, constant.SKILL_CROP_COORDS)
	cv2.imwrite('/home/ben/personal/discord-dota-bot/web_scrap/skill.jpg', new_image)
	exit()

	a = np.ones([10,9])
	a = pandas.DataFrame(a[1:], columns=['Radiant', 'Dire', 'Avg MMR', 'Game Mode', 'Spectators', 'Time', 'R Kills', 'D Kills', 'Gold Lead'])
	r = DataFrame_to_image(a, outputfile='test.png')
	print(r)


