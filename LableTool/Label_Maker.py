#! /usr/bin/env python
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser
from tkinter.filedialog import askdirectory
from PIL import Image,ImageTk
from functools import partial
import json
import shutil as sh
#/Users/kevinkuo/anaconda3/envs/bbox/BBox-Label-Tool/Examples/001
#=== Global function definition ===#
Src = {'initimage':'src/white.png','listformat':'src/list.png','picformat':'src/show.png'}
InitAttribute = {'Size':'640 x 480','Scale':'640 x 480','Name':'white.png','Path':'./src/'}
ImgFormat = ['png','PNG','jpg','JPG','JPEG','tif','TIF','pgm','PGM'] #YOU CAN ALSO ADD YOU NEED FORMAT WITH IMAGE
ImgList = []
jImgList = []
OutputPathname = '.attribute'
Theme = {'bg':'white','fg':'black'}
#boxcount = 0
#filter the data is not image format
def ImgFormatFilter(PicList,path):
	ImgList.clear()
	jImgList.clear()
	templist = PicList[:]
	# filtering the directory
	#print(PicList,type(PicList))
	for check in PicList:
		if os.path.isdir(path+check):
			templist.remove(check)
	# filtering the file doesn't image
	for filter in templist:
		for check in ImgFormat:
			if filter.split('.',1)[1] == check:
				ImgList.append(path+filter)
				jImgList.append(filter)
	jImgList.sort()
	ImgList.sort()
	#print(jImgList)
	#print(ImgList)
	return ImgList,jImgList

def ScaleRation(imsize):
	im_w = imsize[0]
	im_h = imsize[1]
	ration = min(640/im_w,480/im_h)
	n_size = int(ration*im_w),int(ration*im_h)
	return n_size,ration

def IAI(imsize,scalesize,filename,path): # image attribute integration
	DataAttribute = ['Size:',imsize[0],'x',imsize[1]],['Scale:',scalesize[0],'x',scalesize[1]],['Name:',filename],['Path:',path]
	#print(DataAttribute)
	return DataAttribute
def BBox_yolo(bbox,imsize):
	imw = imsize[0]
	imh = imsize[1]
	lux = float(bbox[0])
	luy = float(bbox[1])
	rdx = float(bbox[2])
	rdy = float(bbox[3])
	bbw = rdx - lux #lux -rdx
	bbh = rdy - luy #luy -rdy
	centerx = (lux+rdx)/2
	centery = (luy+rdy)/2
	x = centerx/imw
	y = centery/imh
	w = bbw/imw
	h = bbh/imh
	#print("lux:{} luy:{} rdx:{} rdy{}:".format(lux,luy,rdx,rdy))
	return[str(x),str(y),str(w),str(h)]
#==================================#

#====== Class For Main Panel ======#
class MainPanelCreate():
	def __init__(self,main):
		self.JsonFormat = {}
		self.bndboxlist = []
		self.bndboxattribute = []
		self.OutputFormatSelect = []
		self.boxcount = 0
		self.classIDandclassname = {}
		self.allclassIDandclassname = {}
		#self.allclassID = {}
		self.Objphoto = None
		self.allclassID = {}
		self.classID = {}
		self.OutputPath = {'yolo':'YLabel','normal':'NLabel'}
		self.classcount = 0 #class count
		self.ObjPath = None
		self.root = main
		self.picturelist = None
		self.ObjList = None
		self.boxcolor = None
		self.ImageBox = []
		self.ImageBoxupLabel = []
		#==================Main Panel===================#
		self.MainPanel=tk.Frame(main,bd=10,relief=tk.GROOVE)
		self.MainPanel.grid(row=0,column =0,sticky = tk.W+tk.E+tk.N+tk.S)
		#self.menubar = tk.Menu(main)
		#self.loadmenu = tk.Menu(self.menubar,tearoff=1)
		#self.loadmenu.add_command(label="Select Folder")
		#======ImageListDisplay======#
		# self.ImageListDisplay = tk.LabelFrame(self.MainPanel,bg=Theme['fg'],fg='black',text='ImageListDisplay',height=585,width=200)
		# self.ListFormat = Image.open(Src['listformat'])
		# resizelist = self.ListFormat.resize((20, 20),Image.ANTIALIAS)
		# self.Listphoto = ImageTk.PhotoImage(resizelist)
		# self.ShowFormat = Image.open(Src['picformat'])
		# resizepic = self.ShowFormat.resize((20, 20),Image.ANTIALIAS)
		# self.Showphoto = ImageTk.PhotoImage(resizepic)
		# self.ShowWayFrame = tk.Frame(self.ImageListDisplay,width=150,height=565,bg ='red')
		# self.ListButton = tk.Button(self.ShowWayFrame,image = self.Listphoto,height=25,width=25)
		# self.PicButton = tk.Button(self.ShowWayFrame,image = self.Showphoto,height=25,width=25)
		# self.ListButton.grid(row=1,column=0,sticky = tk.W+tk.N)
		# self.PicButton.grid(row=1,column=1,sticky = tk.W+tk.N)
		# self.ShowWayFrame.grid(row=0,column=0,sticky = tk.W+tk.N)
		# self.ImageListDisplay.grid(row=0,column=0,sticky = tk.N+tk.W+tk.S)
		#=============================#
		#    mouse initialize     #
		self.STATE = {}
		self.STATE['click'] = 0
		self.STATE['x'],self.STATE['y'] = 0,0
		self.h = None
		self.v = None
		self.bboxret = None
		#======Display Monitor======#
		self.DisplayFrame = tk.LabelFrame(self.MainPanel,bg=Theme['bg'],fg=Theme['fg'],text='ImageDisplay',height=600,width=640)
		self.DisplayFrame.grid(row=0,column=1)
		self.DirectoryPathL = tk.Label(self.DisplayFrame,text='Directory Path :',bg=Theme['bg'],fg=Theme['fg'])
		self.DirectoryPathE = tk.Entry(self.DisplayFrame,bg=Theme['bg'],fg=Theme['fg'])
		#self.OutCanFrame = tk.Label(self.DisplayFrame,bg='blue',height=480,width=640)
		self.canvas = tk.Canvas(self.DisplayFrame, bg=Theme['bg'],cursor='tcross',height=477,width=637,relief=tk.SUNKEN,border=5)
		main.bind("<Escape>",self.cancelBBox)
		main.bind("s",self.cancelBBox)
		self.cp = tk.StringVar()
		self.CursorPosition = tk.Label(self.DisplayFrame,textvariable=self.cp,fg=Theme['fg'],bg=Theme['bg'])
		self.cp.set('x:  ,y:  ')
		self.CursorPosition.grid(row=3,column=2,sticky=tk.E+tk.W)
		self.img = Image.open(Src['initimage'])
		self.photo = ImageTk.PhotoImage(self.img)
		self.image_on_canvas = self.canvas.create_image(0, 0, anchor = tk.N+tk.W, image =self.photo)
		self.DirectoryPathB = tk.Button(self.DisplayFrame,text='SelectPath',width=14,command=self.SelectPath,fg=Theme['fg'])
		self.DirectoryPathB1 = tk.Button(self.DisplayFrame,text='Load',width=14,command=self.LoadImage,fg=Theme['fg'])
		self.DirectoryPathL.grid(row=0,column=0,sticky=tk.W)
		self.DirectoryPathE.grid(row=0,column=1,sticky=tk.E+tk.W)
		self.DirectoryPathB.grid(row=0,column=2)
		self.DirectoryPathB1.grid(row=1,column=2,sticky=tk.N)
		#if want to destroy widgets must declare first and geometry dosen't do both together that will let the widgets not destroy
		self.PreButton = tk.Button(self.DisplayFrame,width=10,text='<< Prev',fg=Theme['fg'])
		self.NextButton = tk.Button(self.DisplayFrame,width=10,text='Next >>',fg=Theme['fg'])
		self.PreButton.grid(row=2,column=0)
		self.NextButton.grid(row=2,column=2)
		self.canvas.grid(row=1,column=1,sticky=tk.W+tk.E)
		#self.OutCanFrame.grid(row=1,column=1,sticky=tk.W+tk.E)
		self.imginfo = tk.StringVar()
		self.ImgnameLabel = tk.Label(self.DisplayFrame,textvariable=self.imginfo,bg=Theme['bg'],fg=Theme['fg'])
		self.imginfo.set('Image Name:________________')
		self.ImgnameLabel.grid(row=2,column=1)
		self.ImageJumpLabel = tk.Label(self.DisplayFrame,text='Image No. : ',bg=Theme['bg'],fg=Theme['fg']).grid(row=3,column=0,sticky=tk.E)
		self.ImageJumpEntry = tk.Entry(self.DisplayFrame,width = 1,bg=Theme['bg'],fg=Theme['fg'])
		self.ImageJumpButton = tk.Button(self.DisplayFrame,text='Jump',width=10,fg=Theme['fg'])
		self.ImageJumpButton.grid(row=3,column=1,sticky=tk.E)
		self.ImageJumpEntry.grid(row=3,column=1,sticky=tk.W)
		self.DisplayFrame.columnconfigure(0,weight=1)
		self.DisplayFrame.rowconfigure(0,weight=1)
		self.DisplayFrame.columnconfigure(1,weight=1)
		self.DisplayFrame.rowconfigure(1,weight=1)
		self.DisplayFrame.columnconfigure(2,weight=1)
		self.DisplayFrame.rowconfigure(2,weight=1)
		self.DisplayFrame.columnconfigure(3,weight=1)
		self.DisplayFrame.rowconfigure(3,weight=1)
		#============================#

		#======Attribute Options======#
		self.AttributeOptions = tk.LabelFrame(self.MainPanel,bg=Theme['bg'],fg=Theme['fg'],text='Attribute Options',height=585,width=200)
		self.AttributeOptions.grid(row=0,column=2,sticky=tk.N+tk.S)
		self.BasicImageData = tk.LabelFrame(self.AttributeOptions,text='Basic Image Data',bg=Theme['bg'],fg=Theme['fg'])
		self.BIDListbox= tk.Listbox(self.BasicImageData,height=4,width=27,bg=Theme['bg'],fg=Theme['fg'])
		self.BIDListbox.insert(1,'Size : {}'.format(InitAttribute['Size']))  # listbox insert the image attribute
		self.BIDListbox.insert(2,'Scale : {}'.format(InitAttribute['Scale']))
		self.BIDListbox.insert(3,'Name : {}'.format(InitAttribute['Name']))
		self.BIDListbox.insert(4,'Path : {}'.format(InitAttribute['Path']))
		self.BIDListbox.pack()
		self.BasicImageData.grid(row=0,column=0)
		self.BBOXFrame = tk.LabelFrame(self.AttributeOptions,text='Bounding Box',bg=Theme['bg'],fg=Theme['fg'])
		self.BBOXListbox = tk.Listbox(self.BBOXFrame,width=27,height=6,bg=Theme['bg'],fg=Theme['fg'])
		#self.BBOXListbox.bind("<<ListboxSelect>>",self.bboxshow)
		self.BoxRemoveButton = tk.Button(self.BBOXFrame,text='<Del One>',width=10,fg=Theme['fg'])
		self.BoxDelallButton = tk.Button(self.BBOXFrame,text='<Del All>',width=10,fg=Theme['fg'])
		self.BBOXListbox.pack()
		self.BBOXFrame.grid(row=1,column=0)
		self.BoxDelallButton.pack(side=tk.LEFT)
		self.BoxRemoveButton.pack(side=tk.RIGHT)
		self.AttributeAddFrame = tk.LabelFrame(self.AttributeOptions,text='Class Attribute Add',bg=Theme['bg'],fg=Theme['fg'])
		self.AttributeAddListbox = tk.Listbox(self.AttributeAddFrame,width=27,height=5,bg=Theme['bg'],fg=Theme['fg'])
		self.AttributeAddListbox.bind("<<ListboxSelect>>",self.getbboxcolor)
		self.AttributeAddButton = tk.Button(self.AttributeAddFrame,text='<Add>',width=5,fg=Theme['fg'])
		self.AttributeRemoveButton = tk.Button(self.AttributeAddFrame,text='<Remove>',width=9,fg=Theme['fg'])
		#self.AttributeAddListbox.insert(1,'Name : {}'.format(InitAttribute['Name']))
		self.AttributeAddListbox.pack()
		self.AttributeRemoveButton.pack(side = tk.LEFT)
		self.AttributeAddButton.pack(side = tk.RIGHT)
		self.AttributeAddFrame.grid(row=2,column=0)
		self.FormatOutFrame = tk.LabelFrame(self.AttributeOptions,text='Label Output Format',bg=Theme['bg'],fg=Theme['fg'])
		self.yolovar = tk.IntVar()
		self.norvar = tk.IntVar()
		self.YoloFormat = tk.Checkbutton(self.FormatOutFrame,text='Yolo label',variable=self.yolovar ,onvalue=1 ,offvalue=0,bg=Theme['bg'],fg=Theme['fg'])
		self.NormalFormat = tk.Checkbutton(self.FormatOutFrame,text='Normal label',variable=self.norvar ,onvalue=1 ,offvalue=0,bg=Theme['bg'],fg=Theme['fg'])
		self.YoloPathE = tk.Entry(self.FormatOutFrame,width=14,bg=Theme['bg'],fg=Theme['fg'])
		self.NorPathE = tk.Entry(self.FormatOutFrame,width=14,bg=Theme['bg'],fg=Theme['fg'])
		self.FileGen = tk.Button(self.FormatOutFrame,text='Gerenate',fg=Theme['fg'])
		self.YoloFormat.grid(row=0,column=0,sticky=tk.W)
		self.YoloPathE.grid(row=0,column=1)
		self.NormalFormat.grid(row=1,column=0)
		self.NorPathE.grid(row=1,column=1)
		self.FileGen.grid(row=2,column=0,columnspan=2,sticky=tk.W+tk.E)
		self.FormatOutFrame.grid(row=3,column=0)
		self.FormatOutFrame.columnconfigure(0,weight=1)
		self.FormatOutFrame.columnconfigure(1,weight=1)
		self.FormatOutFrame.rowconfigure(0,weight=1)
		self.FormatOutFrame.rowconfigure(1,weight=1)
		self.FormatOutFrame.rowconfigure(2,weight=1)
		# self.MainPanel.columnconfigure(0,weight=1)
		# self.MainPanel.columnconfigure(2,weight=1)
		# self.MainPanel.rowconfigure(0,weight=1)
		#self.
		#self.StatusShow = tk.Label(self.AttributeOptions,text='Prosess image')
		#self.TxtFormat = tk.LabelFrame(self.AttributeOptions,text='TXT Format').pack(fill=tk.BOTH)
		#=============================#
		#=================================================#
	def Maintain(self):
		# self.canvas.bind("<Button-1>",self.mouseClick)
		# self.canvas.bind("<Motion>",self.mouseMove)
		out = self.picturelist[self.flag].split('.')[0]
		out = '/'+out+'.json'
		if not os.path.isfile(OutputPathname+out):
			self.Objimg = Image.open(self.ObjList[self.flag])
			self.nsize,self.ration = ScaleRation(self.Objimg.size)
			#print(self.nsize)
			self.show = self.Objimg.resize(self.nsize,Image.ANTIALIAS)
			self.Objphoto = ImageTk.PhotoImage(self.show)
			self.canvas.config(width = self.nsize[0],height=self.nsize[1])
			self.canvas.itemconfig(self.image_on_canvas, image = self.Objphoto)
			self.DataA = IAI(self.Objimg.size,self.nsize,self.picturelist[self.flag],self.ObjPath)
			for listinsert in range(len(self.DataA)):
				self.BIDListbox.insert(listinsert,self.DataA[listinsert])
			temptext = self.picturelist[self.flag]
			infotext = 'Image Name : '+temptext + '( '+ str(self.flag+1) +' / '+str(len(self.picturelist))+' )'
			self.imginfo.set(infotext)
			self.filecheckbox.destroy()
		else:
			self.readjson()
			self.filecheckbox.destroy()
	def DeleteDir(self):
		sh.rmtree(OutputPathname)
		os.mkdir(OutputPathname)
		#print(OutputPathname,'Remove and Creating ...')
		self.flag=0
		self.Objimg = Image.open(self.ObjList[self.flag])
		self.nsize,self.ration = ScaleRation(self.Objimg.size)
		#print(self.nsize)
		self.show = self.Objimg.resize(self.nsize,Image.ANTIALIAS)
		self.Objphoto = ImageTk.PhotoImage(self.show)
		self.canvas.config(width = self.nsize[0],height=self.nsize[1])
		self.canvas.itemconfig(self.image_on_canvas, image = self.Objphoto)
		self.DataA = IAI(self.Objimg.size,self.nsize,self.picturelist[self.flag],self.ObjPath)
		for listinsert in range(len(self.DataA)):
			self.BIDListbox.insert(listinsert,self.DataA[listinsert])
		temptext = self.picturelist[self.flag]
		infotext = 'Image Name : '+temptext + '( '+ str(self.flag+1) +' / '+str(len(self.picturelist))+' )'
		self.imginfo.set(infotext)
		#self.BIDListbox.delete(1)
		#self.BIDListbox.delete(2)
		#self.BIDListbox.delete(3)
		#add new function with display directory images on the right side
		'''ObjLbel = tk.Label(DisplayFrame,image=Objphoto)
			ObjLbel.grid(row=1,column=1,sticky=tk.W+tk.E)'''
		self.filecheckbox.destroy()
	#=== LoadImage definition ===#
	def SelectPath(self):
		if self.Objphoto != None:
			self.saveImagedata()
		self.picturelist = []
		self.ObjList = []
		self.tp = tk.StringVar()
		path = askdirectory()
		if path == "":
			messagebox.showwarning("Warning","Directory entry no path input or select. \n \t\t\tTry again!!")
		else:
			self.tp.set(path)
			self.DirectoryPathE.config(textvariable=self.tp)
			self.DirectoryPathB.config(text='Load',command=self.LoadImage)
			self.DirectoryPathB1.destroy()
	def att_widgets_function_open(self):
		self.PreButton.config(command = self.PreLoad)
		self.NextButton.config(command = self.NextLoad)
		self.ImageJumpButton.config(command = self.ImageJump)
		self.BoxRemoveButton.config(command= self.removebox)
		self.BoxDelallButton.config(command=self.deleteallbox)
		self.AttributeAddButton.config(command = self.addattribute)
		self.AttributeRemoveButton.config(command= self.removeattribute)
		self.YoloFormat.config(command=self.pathinsert)
		self.NormalFormat.config(command=self.pathinsert)
		self.FileGen.config(command=self.gerenatefile)
	def LoadImage(self):
		#self.AttributeAddListbox.delete(0)
		#if not self.DirectoryPathE.get()
		self.ObjPath=self.DirectoryPathE.get()
		#print('line 198 here -------------->',self.ObjPath)
		if not self.ObjPath: # [path](not input)
			messagebox.showwarning("Warning","Directory entry no path input or select!!")
		else:# [path](have input)
			self.ObjPath = self.ObjPath+'/'
			if not os.path.isdir(self.ObjPath):# directory not exist
				messagebox.showwarning("Warning","No Such directory :\"{}\"!!".format(self.ObjPath))
			else: # directory exist
				self.picturelist = os.listdir(self.ObjPath)
				#print(self.picturelist)
				for check in self.picturelist:
					if check != '.DS_Store':
						continue
					elif check == '.DS_Store':
						self.picturelist.remove('.DS_Store')
				self.picturelist.sort()
				#print(self.picturelist)
				self.ObjList,self.picturelist = ImgFormatFilter(self.picturelist,self.ObjPath)
				if len(self.picturelist) == 0: # represent that this Directory is have not anymore images
					messagebox.showwarning("Load Image Warning","This directory: '{}' No images file!!".format(self.ObjPath))
					# clean DirectoryPathE method 1
					# self.tp.("")
					# self.DirectoryPathE.config(textvariable=self.tp)
					# clean DirectoryPathE method 2
					self.DirectoryPathE.delete(0,tk.END)
				else: # Directory is have images
					#print('objlist:{}\npicturelist:{}'.format(self.ObjList,self.picturelist))
					if self.bboxret:
						self.canvas.delete(self.bboxret)
					self.BIDListbox.delete(0,tk.END)
					self.removeallattribute()
					self.deleteallbox()
					self.canvas.bind("<Button-1>",self.mouseClick)
					self.canvas.bind("<Motion>",self.mouseMove)
					self.att_widgets_function_open()
					if not os.path.isdir(OutputPathname): #[.attribute](not exist)
						os.mkdir(OutputPathname)
						print(OutputPathname,'creating ...')
						self.flag=0
						self.Objimg = Image.open(self.ObjList[self.flag])
						self.nsize,self.ration = ScaleRation(self.Objimg.size)
						#print(self.nsize)
						self.show = self.Objimg.resize(self.nsize,Image.ANTIALIAS)
						self.Objphoto = ImageTk.PhotoImage(self.show)
						# self.canvas.bind("<Button-1>",self.mouseClick)
						# self.canvas.bind("<Motion>",self.mouseMove)
						self.canvas.config(width = self.nsize[0],height=self.nsize[1])
						self.canvas.itemconfig(self.image_on_canvas, image = self.Objphoto)
						self.DataA = IAI(self.Objimg.size,self.nsize,self.picturelist[self.flag],self.ObjPath)
						for listinsert in range(len(self.DataA)):
							self.BIDListbox.insert(listinsert,self.DataA[listinsert])
						temptext = self.picturelist[self.flag]
						infotext = 'Image Name : '+temptext + '( '+ str(self.flag+1) +' / '+str(len(self.picturelist))+' )'
						self.imginfo.set(infotext)
						#self.BIDListbox.delete(1)
						#self.BIDListbox.delete(2)
						#self.BIDListbox.delete(3)
						#add new function with display directory images on the right side
						'''ObjLbel = tk.Label(DisplayFrame,image=Objphoto)
							ObjLbel.grid(row=1,column=1,sticky=tk.W+tk.E)'''
					else : # [.attribute](exist)
						filecheck = os.listdir(OutputPathname)
						#print('filecheck:',len(filecheck))
						#messagebox.showinfo("showinfo demo", "Info")
						for check in filecheck:
							if check != '.DS_Store':
								continue
							elif check == '.DS_Store':
								filecheck.remove('.DS_Store')
						if len(filecheck) != 0: # [.attribute](exist) [json file](exist)
							self.filecheckbox = tk.Toplevel()
							self.filecheckbox.title('Attribute directory status')
							self.filechecktext = tk.Label(self.filecheckbox,text='Attribute dictery have file\nDo you want to remove all file or maintain the all file',relief=tk.RIDGE)
							self.MaintainB = tk.Button(self.filecheckbox,text='Maintain',command=self.Maintain)
							self.DeleteDirB = tk.Button(self.filecheckbox,text='Delete',command=self.DeleteDir)
							self.filechecktext.pack()
							self.MaintainB.pack(side=tk.LEFT)
							self.DeleteDirB.pack(side=tk.RIGHT)
							self.flag=0
							self.filecheckbox.grab_set()
							self.filecheckbox.attributes('-topmost',True)
						else: # [.attribute](exist) [json file](not exist)
							self.flag=0
							self.Objimg = Image.open(self.ObjList[self.flag])
							self.nsize,self.ration = ScaleRation(self.Objimg.size)
							#print(self.nsize)
							self.show = self.Objimg.resize(self.nsize,Image.ANTIALIAS)
							self.Objphoto = ImageTk.PhotoImage(self.show)
							# self.canvas.bind("<Button-1>",self.mouseClick)
							# self.canvas.bind("<Motion>",self.mouseMove)
							self.canvas.config(width = self.nsize[0],height=self.nsize[1])
							self.canvas.itemconfig(self.image_on_canvas, image = self.Objphoto)
							self.DataA = IAI(self.Objimg.size,self.nsize,self.picturelist[self.flag],self.ObjPath)
							for listinsert in range(len(self.DataA)):
								self.BIDListbox.insert(listinsert,self.DataA[listinsert])
							temptext = self.picturelist[self.flag]
							infotext = 'Image Name : '+temptext + '( '+ str(self.flag+1) +' / '+str(len(self.picturelist))+' )'
							self.imginfo.set(infotext)
							#self.BIDListbox.delete(1)
							#self.BIDListbox.delete(2)
							#self.BIDListbox.delete(3)
							#add new function with display directory images on the right side
							'''ObjLbel = tk.Label(DisplayFrame,image=Objphoto)
								ObjLbel.grid(row=1,column=1,sticky=tk.W+tk.E)'''
		self.DirectoryPathE.delete(0,tk.END)
		self.DirectoryPathB.config(text='SelectPath',command=self.SelectPath)
		self.DirectoryPathB1 = tk.Button(self.DisplayFrame,text='Load',width=14,command=self.LoadImage,fg=Theme['fg'])
		self.DirectoryPathB1.grid(row=1,column=2,sticky=tk.N)
		#============================#

		#=== PreLoadImage definition ===#
	def PreLoad(self):
		self.saveImagedata()
		if self.bboxret:
			self.canvas.delete(self.bboxret)
		self.deleteallbox()
		self.ImageBox.clear()
		self.ImageBoxupLabel.clear()
		self.bndboxattribute = []
		self.classIDandclassname = {}
		self.classID = {}
		self.BIDListbox.delete(0,tk.END) #clean listbox
		self.boxcolor = None
		if self.flag == -len(self.ObjList):
			self.flag = 0
		else:
			self.flag -=1
			#if self.flag > len(self.ObjList:
		out = self.picturelist[self.flag].split('.')[0]
		out = '/'+out+'.json'
		if not os.path.isfile(OutputPathname+out): # check attribute json status (didn't exist)
			self.Objimg = Image.open(self.ObjList[self.flag])
			#print("ImageList Index:{}".format(self.flag))
			self.nsize,self.ration = ScaleRation(self.Objimg.size)
			#print(self.nsize)
			self.show = self.Objimg.resize(self.nsize,Image.ANTIALIAS)
			self.Objphoto = ImageTk.PhotoImage(self.show)
			self.canvas.config(width = self.nsize[0],height=self.nsize[1])
			self.canvas.itemconfig(self.image_on_canvas, image = self.Objphoto)
			self.DataA = IAI(self.Objimg.size,self.nsize,self.picturelist[self.flag],self.ObjPath)
			for listinsert in range(len(self.DataA)):
				self.BIDListbox.insert(listinsert,self.DataA[listinsert])
			temptext = self.picturelist[self.flag]
			if self.flag >= 0:
				infotext = 'Image Name : '+temptext + '( '+ str(self.flag+1) +' / '+str(len(self.picturelist))+' )'
				self.imginfo.set(infotext)
			elif self.flag < 0:
				infotext = 'Image Name : '+temptext + '( '+ str(self.flag+len(self.ObjList)+1) +' / '+str(len(self.picturelist))+' )'
				self.imginfo.set(infotext)
			#ObjLbel = tk.Label(DisplayFrame,image=Objphoto)
			#ObjLbel.grid(row=1,column=1,sticky=tk.W+tk.E)
		else:
			self.readjson()
	#============================#

	#=== NextLoadImage definition ===#
	def NextLoad(self):
		self.saveImagedata()
		if self.bboxret:
			self.canvas.delete(self.bboxret)
		self.deleteallbox()
		#print(self.ImageBox)
		self.ImageBox.clear()
		self.ImageBoxupLabel.clear()
		self.bndboxattribute = []
		self.classIDandclassname = {}
		self.classID = {}
		self.BIDListbox.delete(0,tk.END) # clean listbox
		self.boxcolor = None
		if self.flag == len(self.ObjList)-1:
			self.flag =0
		else:
			self.flag +=1
		if self.flag <0:
			self.flag += len(self.ObjList)
		out = self.picturelist[self.flag].split('.')[0]
		out = '/'+out+'.json'
		if not os.path.isfile(OutputPathname+out): # check attribute json status (didn't exist)
			self.Objimg = Image.open(self.ObjList[self.flag])
			#print("ImageList Index:{}".format(self.flag))
			self.nsize,self.ration = ScaleRation(self.Objimg.size)
			#print(self.nsize)
			self.show = self.Objimg.resize(self.nsize,Image.ANTIALIAS)
			self.Objphoto = ImageTk.PhotoImage(self.show)
			self.canvas.config(width = self.nsize[0],height=self.nsize[1])
			self.canvas.itemconfig(self.image_on_canvas, image = self.Objphoto)
			self.DataA = IAI(self.Objimg.size,self.nsize,self.picturelist[self.flag],self.ObjPath)
			for listinsert in range(len(self.DataA)):
				self.BIDListbox.insert(listinsert,self.DataA[listinsert])
			temptext = self.picturelist[self.flag]
			infotext = 'Image Name : '+temptext + '( '+ str(self.flag+1) +' / '+str(len(self.picturelist))+' )'
			self.imginfo.set(infotext)
			#ObjLbel = tk.Label(DisplayFrame,image=Objphoto)
			#ObjLbel.grid(row=1,column=1,sticky=tk.W+tk.E)
		else :
			self.readjson()#(exist)
		#============================#

		#=== JumpLoadImage definition ===#
	def ImageJump(self):
		picnumber = self.ImageJumpEntry.get()
		if picnumber == "":
			messagebox.showwarning("Load Jump Warning","Jump image number entry no input!!")
			self.ImageJumpEntry.delete(0,tk.END)
		elif not picnumber.isdigit():
			messagebox.showwarning("Load Jump Warning","Input must be number!!")
			self.ImageJumpEntry.delete(0,tk.END)
		else:
			if int(picnumber) > len(self.picturelist): #check the picnumber is or not out of index
				messagebox.showwarning("Load Jump Warning","Input number is out of index!!")
			else:
				self.saveImagedata()
				if self.bboxret:
					self.canvas.delete(self.bboxret)
				self.deleteallbox()
				self.removeallattribute()
				self.ImageBox.clear()
				self.ImageBoxupLabel.clear()
				self.bndboxattribute = []
				self.classIDandclassname = {}
				self.classID = {}
				self.BIDListbox.delete(0,tk.END) # clean listbox
				self.boxcolor = None
				self.flag = int(picnumber)-1
				print('self.flag:',self.flag)
				if self.flag <0:
					self.flag += len(self.ObjList)
				print('self.flag:',self.flag)
				out = self.picturelist[self.flag].split('.')[0]
				out = '/'+out+'.json'
				if not os.path.isfile(OutputPathname+out): # check attribute json status (didn't exist)
					self.Objimg = Image.open(self.ObjList[self.flag])
					#print("ImageList Index:{}".format(self.flag))
					self.nsize,self.ration = ScaleRation(self.Objimg.size)
					#print(self.nsize)
					self.show = self.Objimg.resize(self.nsize,Image.ANTIALIAS)
					self.Objphoto = ImageTk.PhotoImage(self.show)
					self.canvas.config(width = self.nsize[0],height=self.nsize[1])
					self.canvas.itemconfig(self.image_on_canvas, image = self.Objphoto)
					self.DataA = IAI(self.Objimg.size,self.nsize,self.picturelist[self.flag],self.ObjPath)
					for listinsert in range(len(self.DataA)):
						self.BIDListbox.insert(listinsert,self.DataA[listinsert])
					temptext = self.picturelist[self.flag]
					infotext = 'Image Name : '+temptext + '( '+ str(self.flag+1) +' / '+str(len(self.picturelist))+' )'
					self.imginfo.set(infotext)
					#ObjLbel = tk.Label(DisplayFrame,image=Objphoto)
					#ObjLbel.grid(row=1,column=1,sticky=tk.W+tk.E)
				else:
					self.readjson()
			self.ImageJumpEntry.delete(0,tk.END)
		#============================#
	def mouseClick(self,event):
		if (len(self.classIDandclassname) == 0) and (self.Objphoto != None) :
			messagebox.showwarning("Warning","You must to create classes and click the attribute")
			self.STATE['click'] = 2
		if self.boxcolor == None:
			messagebox.showwarning("Warning","You must to create classes and click the attribute")
			self.STATE['click'] = 2
		if self.STATE['click'] == 0: # recode position original
			self.STATE['x'],self.STATE['y'] = event.x,event.y
			#print('x:{},y:{}'.format(event.x,event.y))
		elif self.STATE['click'] == 1: #record end position
			x1,x2 = min(self.STATE['x'],event.x),max(self.STATE['x'],event.x) # no matter where you plot can get the correct postion from left up side to right down side
			y1,y2 = min(self.STATE['y'],event.y),max(self.STATE['y'],event.y)
			retangleo = x1,y1,x2,y2
			#print('x:{},y:{}'.format(event.x,event.y))
			if self.ration > 1 : #ratio is scale up --> canvas coordinate must be scale down
				print('line 559 down',self.ration)
				retangle= int(retangleo[0]/self.ration),int(retangleo[1]/self.ration),int(retangleo[2]/self.ration),int(retangleo[3]/self.ration)
			elif self.ration < 1: #ratio is scale down --> canvas coordinate must be scale up
				print('line 562 up',self.ration)
				retangle= int(retangleo[0]/self.ration),int(retangleo[1]/self.ration),int(retangleo[2]/self.ration),int(retangleo[3]/self.ration)
			else: # no resize
				retangle = retangleo
			self.bndboxlist.append(retangle)
			#print(self.bndboxlist)
			self.BBOXListbox.insert(tk.END,'BOX{} :[LP:{},{} --> RD:{},{}]'.format(self.boxcount,retangle[0],retangle[1],retangle[2],retangle[3]))
			self.ImageBoxupLabel.append(self.canvas.create_text(retangleo[0],retangleo[1],fill=self.boxcolor[2],font=('Time',12),text=self.name,anchor=tk.N+tk.W))
			self.ImageBox.append(self.canvas.create_rectangle(retangleo[0],retangleo[1],retangleo[2],retangleo[3],outline=self.boxcolor[2],width=2))
			self.bndboxattribute.append([self.name,self.boxcolor[2],[retangle[0],retangle[1],retangle[2],retangle[3]]])
			#print(self.bndboxattribute)
			self.boxcount +=1
			#boxcount +=1
		else: #propect user touch canvas but not click attribute have some error
			print('self.STATE:',self.STATE['click'])
			self.STATE['click'] = 1
		self.STATE['click'] = 1 - self.STATE['click'] # toggle state
	def mouseMove(self,event):
		# show cursor position x & y
		postionx = str(event.x)
		postiony = str(event.y)
		textp = '( x:'+postionx+', y:'+postiony+' )'
		self.cp.set(textp)
		if self.Objphoto :
			if self.h: # horzi
				self.canvas.delete(self.h)
			self.h = self.canvas.create_line(0,event.y,self.Objphoto.width(),event.y,width = 2)
			if self.v:
				self.canvas.delete(self.v)
			self.v = self.canvas.create_line(event.x,0, event.x,self.Objphoto.height(),width = 2)
		if self.STATE['click'] == 1:
			if self.bboxret:
				#print('################3###############')
				self.canvas.delete(self.bboxret)
			self.bboxret = self.canvas.create_rectangle(self.STATE['x'],self.STATE['y'],event.x,event.y,width =2,outline='red')
	def cancelBBox(self,event):
		if 1 == self.STATE['click']:
			if self.bboxret:
				self.canvas.delete(self.bboxret)
				self.bboxret = None
				self.STATE['click'] = 0
	def addattribute(self): # child window create add new attribute
		#self.root.withdraw()
		self.subwindow = tk.Toplevel()
		self.subwindow.title('Class Attribute')
		self.subclasslebel = tk.Label(self.subwindow,text='Class Number:')
		self.subspinbox = tk.Spinbox(self.subwindow,from_=0,to=10,width=5)
		self.subbutton = tk.Button(self.subwindow,text='create',command=self.createclass)
		self.subbuttond = tk.Button(self.subwindow,text='delete',command=self.deleteclass)
		self.subbuttonc = tk.Button(self.subwindow,text='insert',command=self.inserlist)
		self.subclasslebel.grid(row=0,column=0)
		self.subspinbox.grid(row=0,column=1)
		self.subbutton.grid(row=0,column=2)
		self.subbuttond.grid(row=0,column=3)
		self.subbuttonc.grid(row=0,column=4)
		self.subwindow.grab_set()
		self.subwindow.attributes('-topmost',True)
		self.classnumber = None
	def createclass(self):
		#print('class:{}'.format(self.subspinbox.get()))
		self.classlabel = []
		self.classentry = []
		self.classcolorlabel = []
		self.classcolorentry = []
		self.classcolorbutton = []
		self.classIDlabel = []
		self.classIDentry = []
		#self.btnclick = []
		#print(self.classlabel)
		self.classnumber = int(self.subspinbox.get())
		if self.classnumber == 0:
			messagebox.showwarning("Attribute Add Warning","You input 0 class (At least select or input 1 class)!!")
		for name in range(self.classnumber): #dynamic create Labeel and Entry
			tempL = tk.Label(self.subwindow,text='Class {} Name:'.format(name))
			tempE = tk.Entry(self.subwindow,width=5)
			tempL2 = tk.Label(self.subwindow,text='Class {} ID:'.format(name))
			tempE2 = tk.Entry(self.subwindow,width=5)
			tempL1 = tk.Label(self.subwindow,text='Class {} color:'.format(name))
			tempE1 = tk.Label(self.subwindow,width=5,relief=tk.SUNKEN,border=1)
			tempB = tk.Button(self.subwindow,text='select'+str(name),command=partial(self.choosecolor,i=name))
			self.classlabel.append(tempL)
			self.classentry.append(tempE)
			self.classIDlabel.append(tempL2)
			self.classIDentry.append(tempE2)
			self.classcolorlabel.append(tempL1)
			self.classcolorentry.append(tempE1)
			self.classcolorbutton.append(tempB)
			#self.btnclick.append('select'+str(name))
			tempL=None # clean temp
			tempE=None
			tempL2=None
			tempE2=None
			tempL1=None
			tempE1=None
			tempB=None
		#print(self.btnclick)
		for name in range(self.classnumber):
			self.classlabel[name].grid(row=1+name,column=0,sticky=tk.W)
			self.classentry[name].grid(row=1+name,column=1,sticky=tk.W)
			self.classIDlabel[name].grid(row=1+name,column=2,sticky=tk.W)
			self.classIDentry[name].grid(row=1+name,column=3,sticky=tk.W)
			self.classcolorlabel[name].grid(row=1+name,column=4,sticky=tk.W)
			self.classcolorentry[name].grid(row=1+name,column=5,sticky=tk.W)
			self.classcolorbutton[name].grid(row=1+name,column=6,sticky=tk.W)
		#print(self.classcolorentry)
		#print(self.classlabel)
	def choosecolor(self,i):
		#print('hey I\'here',i)
		(rgb,hx) = colorchooser.askcolor()
		#self.class
		#print(self.classcolorbutton[i])
		print('line 690',hx)
		if hx != None:
			self.classcolorbutton[i].destroy()
			self.classcolorentry[i].config(bg=hx,text=hx)
		#self.colorchIndex.append(hx)
	def deleteclass(self):
		# use compare to remove unnecessary label and entry
		if self.classnumber == None:
			messagebox.showwarning("Attribute Add Warning","You must click \"create\" first !!")
		elif self.classnumber == 0:
			messagebox.showwarning("Attribute Add Warning","NO class can be delete !!")
		else:
			for name in range(self.classnumber):
				#print('==================')
				self.classlabel[name].destroy()
				self.classentry[name].destroy()
				self.classIDlabel[name].destroy()
				self.classIDentry[name].destroy()
				self.classcolorlabel[name].destroy()
				self.classcolorentry[name].destroy()
				self.classcolorbutton[name].destroy()
	def inserlist(self):
		self.spinboxclassname = []
		self.spinboxclasscolor = []
		self.spinboxclassidtemp = []
		self.insertflag = 0
		#print(' line 632 again')
		#self.classcount = len(self.allclassID)
		if self.classnumber == None:
			messagebox.showwarning("Attribute Add Warning","You must click \"create\" first !!")
		elif self.classnumber == 0:
			messagebox.showwarning("Attribute Add Warning","You didn't create anyone class !!")
		else:
			for getin in range(self.classnumber):
				# check classname is a digit or nothing in the variable
				if self.classentry[getin].get() == " " :
					self.insertflag += 1
					messagebox.showwarning("classname Warning","Number{} ClassName No input any char !!".format(getin))
				elif self.classentry[getin].get().isdigit() :
					self.insertflag += 1
					self.classentry[getin].delete(0,tk.END)
					messagebox.showwarning("classname Warning","Number{} ClassName input must be char not number !!".format(getin))
				else:
					self.spinboxclassname.append(self.classentry[getin].get())
				# check classid is a digit or nothing in the variable
				if self.classIDentry[getin].get() == " " :
					self.insertflag += 1
					messagebox.showwarning("classID Warning","Number{} ClassID No input any char !!".format(getin))
				elif self.classIDentry[getin].get().isdigit() :
					self.spinboxclassidtemp.append(self.classIDentry[getin].get())
				elif not self.classIDentry[getin].get().isdigit():
					self.insertflag += 1
					self.classIDentry[getin].delete(0,tk.END)
					messagebox.showwarning("classID Warning","Number{} ClassID input must be number not char !!".format(getin))
				# check classcolor has selected in the variable
				if self.classcolorentry[getin].cget("text") == "" :
					self.insertflag += 1
					messagebox.showwarning("classcolor Warning","Number{} Classcolor No select any color !!".format(getin))
				elif self.classcolorentry[getin].cget("text").isdigit():
					self.insertflag += 1
					self.classcolorentry[getin].config(text = "")
					messagebox.showwarning("classID Warning","Number{} ClassID input must be color string not number !!".format(getin))
				else:
					self.spinboxclasscolor.append(self.classcolorentry[getin].cget("text"))
				print('classname:{} , classcolor:{}, classID:{}'.format(self.classentry[getin].get(),self.classcolorentry[getin].cget("text"),self.classIDentry[getin].get()))
				print(type(self.classentry[getin].get()),type(self.classcolorentry[getin].cget("text")),type(self.classIDentry[getin].get()))
				# insert real can work label attribute
				#print(self.spinboxclassname.append(self.classentry[getin].get()),self.spinboxclasscolor.append(self.classcolorentry[getin].get()))
			if self.insertflag == 0:
				for attinsert in range(self.classnumber):
					self.AttributeAddListbox.insert(tk.END,'Name:{},Color:{}'.format(self.spinboxclassname[attinsert],self.spinboxclasscolor[attinsert]))
					self.allclassIDandclassname[self.spinboxclassname[attinsert]]=self.spinboxclasscolor[attinsert]
					#self.allclassID[self.spinboxclassname[attinsert]] = self.classcount + attinsert
					self.allclassID[self.spinboxclassname[attinsert]] = self.spinboxclassidtemp[attinsert]
				print('self.allclassID:',self.allclassID)
				#print('self.allclassID:',self.allclassID)
				#print('hello here is classIDandclassname',self.allclassIDandclassname)
				self.subwindow.destroy()
			else:
				self.insertflag = 0
	def removeattribute(self):
		traget = self.AttributeAddListbox.curselection()
		if not traget:
			messagebox.showwarning("Attribute Remove Warning","You didn't select any Attribute !!")
		else:
			self.AttributeAddListbox.delete(traget)
			self.allclassIDandclassname.pop(self.name)
			#self.allclassID.pop(self.name)
			self.allclassID.pop(self.name)
			#index = 0
			# for reset in self.allclassID:
			# 	self.allclassID[reset] = index
			# 	index += 1
			# print('self.allclassID:',self.allclassID)
			#print(self.allclassIDandclassname)
			self.classnumber -=1
			self.boxcolor = None
			self.name = None
	def removeallattribute(self):
		size = self.AttributeAddListbox.size()
		for plugout in range(size):
			self.AttributeAddListbox.delete(0)
	def removebox(self):
		traget = self.BBOXListbox.curselection()
		print(traget)
		#print(self.BBOXListbox.get(traget))
		if not traget:
			messagebox.showwarning("Bounding Box Delete Warning","You didn't select any bounding box coordinate !!")
		else:
			if self.bboxret:
				#print('################3###############')
				self.canvas.delete(self.bboxret)
			self.BBOXListbox.delete(traget,tk.END)# delete all listbox box position
			self.canvas.delete(self.ImageBox[traget[0]])# delete traget canvas bbox rectangle
			self.canvas.delete(self.ImageBoxupLabel[traget[0]]) # delete traget canvas label on rectangle
			#print('original:{}\nscale:{}'.format(self.bndboxlist,self.ImageBox))
			self.ImageBox.pop(traget[0]) # pop traget from ImageBox
			self.ImageBoxupLabel.pop(traget[0]) # pop traget from ImageBoxupLabel
			self.bndboxlist.pop(traget[0]) # pop traget from bndboxlist
			self.bndboxattribute.pop(traget[0])
			#print('original:{}\nscale:{}'.format(self.bndboxlist,self.ImageBox))
			#print(self.bndboxattribute)
			self.boxcount -=1
			#insert the new list to listbox
			for reassign in range(traget[0],self.boxcount):
				self.BBOXListbox.insert(tk.END,'BOX{} :[LP:{},{} --> RD:{},{}]'.format(reassign,self.bndboxlist[reassign][0],self.bndboxlist[reassign][1],self.bndboxlist[reassign][2],self.bndboxlist[reassign][3]))
			#print(self.ImageBox)
	def deleteallbox(self):
		size = self.BBOXListbox.size()
		#print('listbox size:',size)
		for plugout in range(size):
			self.BBOXListbox.delete(0)
			self.canvas.delete(self.ImageBox[0])
			self.canvas.delete(self.ImageBoxupLabel[0])
			self.bndboxattribute.pop(0)
			self.bndboxlist.pop(0)
			self.ImageBox.pop(0)
			self.ImageBoxupLabel.pop(0)
			#print(self.ImageBox)
		self.boxcount = 0
		#print('bndboxlist:{}\nboxcount:{}'.format(self.bndboxlist,self.boxcount))
	def getbboxcolor(self,event):
		target = event.widget.curselection()
		#print('bingo line 785',target)
		#print(target[0],type(target)) tuple can slice
		if not target :
			messagebox.showwarning("Bounding Box Select Warning","You didn't add attribute or not selected any attribute !!")
		else:
			objstr = self.AttributeAddListbox.get(target)
			self.boxcolor = objstr.split(':')
			self.name=self.boxcolor[1].split(',')[0]
			#print('line 594',self.boxcolor)
			self.classIDandclassname[self.name]=self.boxcolor[2]
			#print('line 596',self.allclassID)
			self.classID[self.name]=self.allclassID[self.name]
			self.canvas.itemconfig(self.bboxret,outline=self.boxcolor[2])
			#self.canvas.itemconfig(self.ImageBox[self.boxcount],outline=att[2])
			#change canvas bunbox color attribute
			#target = self.AttributeAddListbox.curselection()
	def pathinsert(self):
		self.OutputPath = {'yolo':'YLabel','normal':'NLabel'}
		self.outdir = tk.StringVar()
		self.outselect = tk.StringVar()
		if (self.yolovar.get() == 1 ) & (self.norvar.get() == 0):
			self.OutputFormatSelect=[]
			self.OutputFormatSelect.append('yolo')
			if not self.YoloPathE.get():
				print(self.YoloPathE.get())
				print('yolo default:{}'.format(self.OutputPath['yolo']))
			else:
				self.OutputPath['yolo'] = self.YoloPathE.get()
				print('yolo path:{}'.format(self.OutputPath['yolo']))
			#print(self.OutputFormatSelect)
			self.outselect.set('Label select format: {}'.format(self.OutputFormatSelect[0]))
			self.outdir.set('Output directory: {}'.format(self.OutputPath[self.OutputFormatSelect[0]]))
		elif (self.yolovar.get() == 0 ) & (self.norvar.get() == 1):
			self.OutputFormatSelect=[]
			self.OutputFormatSelect.append('normal')
			if not self.NorPathE.get():
				print('normal default:{}'.format(self.OutputPath['normal']))
			else:
				self.OutputPath['normal'] = self.NorPathE.get()
				#print('normal path:{}'.format(self.OutputPath['normal']))
			#print(self.OutputFormatSelect)
			self.outselect.set('Label select format: {}'.format(self.OutputFormatSelect[0]))
			self.outdir.set('Output directory: {}'.format(self.OutputPath[self.OutputFormatSelect[0]]))
		elif (self.yolovar.get() == 1 ) & (self.norvar.get() == 1):
			self.OutputFormatSelect=[]
			self.OutputFormatSelect.append('yolo')
			self.OutputFormatSelect.append('normal')
			if (not self.YoloPathE.get()) & (not self.NorPathE.get()):
				print('yolo:{} & normal:{}'.format(self.OutputPath['yolo'],self.OutputPath['normal']))
			elif (self.YoloPathE.get()!=None) & (not self.NorPathE.get()):
				self.OutputPath['yolo'] = self.YoloPathE.get()
				#print('yolo path:{}\nnormal:{}'.format(self.OutputPath['yolo'],self.OutputPath['normal']))
			elif (not self.YoloPathE.get()) & (self.NorPathE.get()!=None):
				self.OutputPath['normal'] = self.NorPathE.get()
				#print('default yolo\nnormal path:{}'.format(self.OutputPath['yolo'],self.OutputPath['normal']))
			else:
				self.OutputPath['yolo'] = self.YoloPathE.get()
				self.OutputPath['normal'] = self.NorPathE.get()
				#print('yolo path:{}\nnormal path:{}'.format(self.OutputPath['yolo'],self.OutputPath['normal']))
			#print(self.OutputFormatSelect)
			self.outselect.set('Label select format: {},{}'.format(self.OutputFormatSelect[0],self.OutputFormatSelect[1]))
			self.outdir.set('Output directory: {},{}'.format(self.OutputPath[self.OutputFormatSelect[0]],self.OutputPath[self.OutputFormatSelect[1]]))
		else :
			self.OutputFormatSelect=[]
			#print('nothing to select')
	'''def classification(self):
		# create class name
		for key,value in self.classIDandclassname.items():
			locals()[key+" attribute"] = [0,key,value]
		for clsficat in self.bndboxattribute:
			for key,value in self.classIDandclassname.items():
				if (clsficat[0] == key) & (clsficat[1] == value):
					locals()[key+" attribute"][0] += 1
					locals()[key+" attribute"].append(clsficat[2])
					print(locals()[key+" attribute"])
		print(locals())'''
	def saveImagedata(self):
		self.Imgdata = []
		#self.ObjPath #present working directory
		#self.ObjList[self.flag] #this image name & directory
		#self.picturelist[self.flag] #this image name
		#self.Objimg.size #image original size
		#self.nsize #image scale size
		#self.boxcolor #boxmember element
		#self.name #boxmember element
		#self.OutputPath #output path'''
		#self.OutputFormatSelect # Label Format
		self.Imgdata.append({'Path':self.ObjPath})
		self.Imgdata.append({'IMGName':self.picturelist[self.flag]})
		self.Imgdata.append({'Size':[self.Objimg.size[0],self.Objimg.size[1]]})
		self.Imgdata.append({'Scale':[self.nsize[0],self.nsize[1],self.ration]})
		self.Imgdata.append(self.classIDandclassname)
		self.Imgdata.append(self.classID)
		#self.Imgdata.append(self.allclassID)
		# classfication per class
		for key,value in self.classIDandclassname.items():
			locals()[key+" attribute"] = [0,key,value]
		#print('line 912',self.bndboxattribute)
		for clsficat in self.bndboxattribute:
			for key,value in self.classIDandclassname.items():
				if (clsficat[0] == key) & (clsficat[1] == value):
					locals()[key+" attribute"][0] += 1
					locals()[key+" attribute"].append(clsficat[2])
					#print(locals()[key+" attribute"])
		#print('ha ha local is here',locals())
		for key,value in self.classIDandclassname.items():
			if locals()[key+" attribute"][0] == 0 :
				continue
			else :
				self.Imgdata.append(locals()[key+" attribute"])
		self.Imgdata.append({'OutputPath':self.OutputPath,'Format':self.OutputFormatSelect})
		#print('line 926',self.Imgdata)
		if (self.Imgdata[4] != {}) and (self.Imgdata[5] != {}) and (len(self.Imgdata[6]) > 3) :
			out = self.picturelist[self.flag].split('.')[0]
			out = '/'+out+'.json'
			with open(OutputPathname+out,'w') as file:
				self.text=json.dumps(self.Imgdata,indent = 2)
				file.write(self.text)
		else: #erase the json file
			try:
				out = self.picturelist[self.flag].split('.')[0]
				out = '/'+out+'.json'
				os.remove(OutputPathname+out)
			except FileNotFoundError :
				pass
				#messagebox.showwarning("Save json file Warning","File:'{}' will not be save !!".format(out))
	def gerenatefile(self):
		if len(self.OutputFormatSelect) == 0:
			messagebox.showwarning("Outpu Path Warning","You do not select output format")
		else :
			if os.path.isdir(OutputPathname):
				attributefile = os.listdir(OutputPathname)
				attributefile.sort()
				#print(attributefile)
				self.Gwindow = tk.Toplevel()
				self.Gwindow.title('Gerenate Output')
				self.Glabel = tk.Label(self.Gwindow,text='Gerenate:')
				self.Gshow = tk.Label(self.Gwindow,text='Totall alreadly labeled file number : {}'.format(len(attributefile)))
				self.Gselect = tk.Label(self.Gwindow,textvariable=self.outselect)
				self.Goutput = tk.Label(self.Gwindow,textvariable=self.outdir)
				self.GYButton = tk.Button(self.Gwindow,text='Yes',command=self.GYes,width=8)
				self.GNButton = tk.Button(self.Gwindow,text='No',command=self.GNo,width=8)
				self.Glabel.grid(row=0,column=0,sticky=tk.W)
				self.Gshow.grid(row=1,column=1)
				self.Gselect.grid(row=2,column=1,sticky=tk.W)
				self.Goutput.grid(row=3,column=1,sticky=tk.W)
				self.GYButton.grid(row=4,column=0)
				self.GNButton.grid(row=4,column=2)
				self.Gwindow.grab_set()
				self.Gwindow.attributes('-topmost',True)
			else:
				messagebox.showwarning("attribute folder status","Attributefile doesn't exist !!")
	def GYes(self):
		Lpath = []
		# get all outputpath string
		for name in range(2):
			try :
				Lpath.append(self.OutputPath[self.OutputFormatSelect[name]])
				outname = self.OutputPath[self.OutputFormatSelect[name]]
				if self.OutputFormatSelect[name] =='normal':
					# check attribute status
					if os.path.isdir('.attribute'):#path notice
						tempfile = os.listdir('.attribute')#path notice
						if '.DS_Store' in tempfile:
							tempfile.remove('.DS_Store')
						tempfile.sort()
						if os.path.isfile('outlog.txt'):
							os.remove('outlog.txt')
						for item in tempfile :
							with open(OutputPathname+'/'+item,'r') as check :#path notice
								jsondata = json.load(check)
								#check box status
								if len(jsondata[6]) == 0:
									with open('outlog.txt','a') as log:
										log.write(item+' object bbox is 0\n')
								else :
									if not os.path.isdir(outname):
										os.mkdir(outname)
									filename = jsondata[1]['IMGName'].split('.')[0]+'.txt'
									with open(outname+'/'+filename,'a') as label:
										i = 0 # class number count from 0 start
										for k in range(len(jsondata)-7):
											i += 1 #jsondata index to fetch object list
											iteration = jsondata[5+i][0] #get bbox number on key object
											for bboxcount in range(iteration):
												coordinate = jsondata[5+i][3+bboxcount]
												x1,y1,x2,y2 = coordinate[0],coordinate[1],coordinate[2],coordinate[3]
												label.write(jsondata[5][jsondata[5+i][1]]+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+'\n')
					else :
						messagebox.showwarning("Warning","Attribute file didn't exist")
				elif self.OutputFormatSelect[name] == 'yolo':
					# check attribute status
					if os.path.isdir('.attribute'):#path notice
						tempfile = os.listdir('.attribute')#path notice
						if '.DS_Store' in tempfile:
							tempfile.remove('.DS_Store')
						tempfile.sort()
						if os.path.isfile('outlog.txt'):
							os.remove('outlog.txt')
						for item in tempfile :
							with open(OutputPathname+'/'+item,'r') as check :#path notice
								jsondata = json.load(check)
								# check box status
								if len(jsondata[6]) == 0:
									with open('outlog.txt','a') as log:
										log.write(item+' object bbox is 0\n')
								else :
									if not os.path.isdir(outname):
										os.mkdir(outname)
									filename = jsondata[1]['IMGName'].split('.')[0]+'.txt'
									with open(outname+'/'+filename,'a') as label:
										i = 0 # class number count from 0 start
										for k in range(len(jsondata)-7):
											i += 1 #jsondata index to fetch object list
											iteration = jsondata[5+i][0] #get bbox number on key object
											for bboxcount in range(iteration):
												coordinate = jsondata[5+i][3+bboxcount]
												imsize = jsondata[2]['Size']
												yolotxt = BBox_yolo(coordinate,imsize)
												label.write(jsondata[5][jsondata[5+i][1]]+' '+yolotxt[0]+' '+yolotxt[1]+' '+yolotxt[2]+' '+yolotxt[3]+'\n')
					else:
						messagebox.showwarning("Warning","Attribute file didn't exist")
		 #print(Lpath)
			except:
				print('keyError from GYes')
			self.Gwindow.destroy()
						#check object
		self.YoloPathE.delete(0,tk.END)
		self.NorPathE.delete(0,tk.END)
	def GNo(self):
		self.Gwindow.destroy()
	def readjson(self):
		jspath = self.picturelist[self.flag].split('.')[0]
		jspath = '/'+jspath+'.json'
		with open(OutputPathname+jspath,'r') as file:
			jsdata = json.load(file)
		photo = jsdata[0]['Path']+jsdata[1]['IMGName']
		ratio = jsdata[3]['Scale'][2]
		self.Objimg = Image.open(photo)
		#print("ImageList Index:{}".format(self.flag))
		self.nsize,self.ration = ScaleRation(self.Objimg.size)
		#print(self.nsize)
		self.show = self.Objimg.resize(self.nsize,Image.ANTIALIAS)
		self.Objphoto = ImageTk.PhotoImage(self.show)
		self.canvas.config(width = self.nsize[0],height=self.nsize[1])
		self.canvas.itemconfig(self.image_on_canvas, image = self.Objphoto)
		self.DataA = IAI(self.Objimg.size,self.nsize,jsdata[1]['IMGName'],self.ObjPath)
		for listinsert in range(len(self.DataA)):
			self.BIDListbox.insert(listinsert,self.DataA[listinsert])
		temptext = self.picturelist[self.flag]
		infotext = 'Image Name : '+temptext + '( '+ str(self.flag+1) +' / '+str(len(self.picturelist))+' )'
		self.imginfo.set(infotext)
		# show box attribute on Listbox
		self.boxcount = jsdata[6][0]
		self.removeallattribute()
		for key,value in jsdata[4].items():
			self.AttributeAddListbox.insert(tk.END,'Name:{},Color:{}'.format(key,value))
			self.classIDandclassname[key]=value
		for key,value in jsdata[5].items():
			self.allclassID[key]=value
			self.classID[key]=value
		# show box on Canvas
		# len(jsdata)-7 => class number and start from jsdata[6]
		for object in range(len(jsdata)-7):
			color = jsdata[object+6][2]
			self.name = jsdata[object+6][1]
			for box in range(len(jsdata[object+6])-3):
				if ratio > 1: # scale up --> original box size scale up
					retangle = int(jsdata[object+6][3+box][0]*ratio),int(jsdata[object+6][3+box][1]*ratio),int(jsdata[object+6][3+box][2]*ratio),int(jsdata[object+6][3+box][3]*ratio)
				elif ratio < 1: # scale down --> original box size scale down
					retangle = int(jsdata[object+6][3+box][0]*ratio),int(jsdata[object+6][3+box][1]*ratio),int(jsdata[object+6][3+box][2]*ratio),int(jsdata[object+6][3+box][3]*ratio)
				else:
					retangle = jsdata[object+6][3+box][0],jsdata[object+6][3+box][1],jsdata[object+6][3+box][2],jsdata[object+6][3+box][3]
				print('jsretangle:{}'.format(jsdata[object+6][3+box]))
				print('retangle:',retangle)
				self.bndboxlist.append(retangle)
				self.ImageBoxupLabel.append(self.canvas.create_text(retangle[0],retangle[1],fill=color,font=('Time',12),text=self.name,anchor=tk.N+tk.W))
				self.ImageBox.append(self.canvas.create_rectangle(retangle[0],retangle[1],retangle[2],retangle[3],outline=color,width=2))
				self.bndboxattribute.append([self.name,color,[jsdata[object+6][3+box][0],jsdata[object+6][3+box][1],jsdata[object+6][3+box][2],jsdata[object+6][3+box][3]]])
				# print(self.bndboxlist)
				self.BBOXListbox.insert(tk.END,'BOX{} :[LP:{},{} --> RD:{},{}]'.format(box,jsdata[object+6][3+box][0],jsdata[object+6][3+box][1],jsdata[object+6][3+box][2],jsdata[object+6][3+box][3]))
'''	def bboxshow(self,event):
		target = event.widget.curselection() # get id in listbox
		objstr = self.BBOXListbox.get(target)
		self.canvas.itemconfig(self.ImageBox[target[0]],outline=self.boxcolor[2])'''
	#def reassign(self):
#==================================#

#========GUI RUN=========#
root=tk.Tk()
root.title('Label Maker')
root.geometry('1170x620')
def on_close():
	close = messagebox.askokcancel("Close", "Would you like to close the program?")
	if close:
		if not control.ObjPath:
			root.destroy()
		else:
			if len(control.picturelist) == 0:
				root.destroy()
			else:
				control.saveImagedata()
				root.destroy()
root.protocol("WM_DELETE_WINDOW",  on_close)
control = MainPanelCreate(root)
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
root.mainloop()
#=========================#
