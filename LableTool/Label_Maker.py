import os
import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
from PIL import Image,ImageTk
from functools import partial
import json
import shutil as sh
#/Users/kevinkuo/anaconda3/envs/bbox/BBox-Label-Tool/Examples/001
#=== Global function definition ===#
Src = {'initimage':'src/white.png','listformat':'src/list.png','picformat':'src/show.png'}
InitAttribute = {'Size':'640 x 480','Scale':'640 x 480','Name':'white.png','Path':'./src/'}
ImgFormat = ['png','PNG','jpg','JPEG','tif','TIF','pgm','PGM'] #YOU CAN ALSO ADD YOU NEED FORMAT WITH IMAGE
ImgList = []
OutputPathname = '.attribute'
#boxcount = 0
#filter the data is not image format
def ImgFormatFilter(PicList,path):
	ImgList.clear()
	for filter in PicList:
		for check in ImgFormat:
			if filter.split('.',1)[1] == check:
				ImgList.append(path+filter)
	ImgList.sort()
	return ImgList

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
    print("lux:{} luy:{} rdx:{} rdy{}:".format(lux,luy,rdx,rdy))
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
		self.allclassID = {}
		self.classID = {}
		self.OutputPath = {'yolo':'YLabel','normal':'NLabel'}
		self.classcount = 0 #class count
		self.ObjPath = None
		#==================Main Panel===================#
		self.MainPanel=tk.Frame(main,bg='blue')
		self.MainPanel.grid(row=0,column =0,sticky = tk.W+tk.E+tk.N+tk.S)
		#self.menubar = tk.Menu(main)
		#self.loadmenu = tk.Menu(self.menubar,tearoff=1)
		#self.loadmenu.add_command(label="Select Folder")
		#======ImageListDisplay======#
		# self.ImageListDisplay = tk.LabelFrame(self.MainPanel,bg='white',fg='black',text='ImageListDisplay',height=585,width=200)
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
		self.DisplayFrame = tk.LabelFrame(self.MainPanel,bg='white',fg='black',text='ImageDisplay',height=600,width=640)
		self.DisplayFrame.grid(row=0,column=1)
		self.DirectoryPathL = tk.Label(self.DisplayFrame,text='Directory Path :')
		self.DirectoryPathE = tk.Entry(self.DisplayFrame)
		self.OutCanFrame = tk.Label(self.DisplayFrame,bg='blue',height=480,width=640)
		self.canvas = tk.Canvas(self.OutCanFrame, bg='black',cursor='tcross',height=480,width=640)
		self.canvas.bind("<Button-1>",self.mouseClick)
		self.canvas.bind("<Motion>",self.mouseMove)
		main.bind("<Escape>",self.cancelBBox)
		self.cp = tk.StringVar()
		self.CursorPosition = tk.Label(self.DisplayFrame,textvariable=self.cp)
		self.cp.set('x:  ,y:  ')
		self.CursorPosition.grid(row=3,column=2,sticky=tk.E+tk.W)
		self.img = Image.open(Src['initimage'])
		self.photo = ImageTk.PhotoImage(self.img)
		self.image_on_canvas = self.canvas.create_image(0, 0, anchor = tk.N+tk.W, image =self.photo)
		self.canvas.pack()
		self.DirectoryPathB = tk.Button(self.DisplayFrame,text='LOAD',width=14,command=self.LoadImage)
		self.DirectoryPathL.grid(row=0,column=0,sticky=tk.W)
		self.DirectoryPathE.grid(row=0,column=1,sticky=tk.E+tk.W)
		self.DirectoryPathB.grid(row=0,column=2)
		self.PreButton = tk.Button(self.DisplayFrame,width=10,text='<< Prev',command = self.PreLoad)
		self.NextButton = tk.Button(self.DisplayFrame,width=10,text='Next >>',command = self.NextLoad)
		self.PreButton.grid(row=2,column=0)
		self.NextButton.grid(row=2,column=2)
		self.OutCanFrame.grid(row=1,column=1,sticky=tk.W+tk.E)
		self.imginfo = tk.StringVar()
		self.ImgnameLabel = tk.Label(self.DisplayFrame,textvariable=self.imginfo)
		self.imginfo.set('Image Name:________________')
		self.ImgnameLabel.grid(row=2,column=1)
		self.ImageJumpLabel = tk.Label(self.DisplayFrame,text='Image No. : ').grid(row=3,column=0,sticky=tk.E)
		self.ImageJumpEntry = tk.Entry(self.DisplayFrame,width = 1)
		self.ImageJumpButton = tk.Button(self.DisplayFrame,text='Jump',width=10,command = self.ImageJump).grid(row=3,column=1,sticky=tk.E)
		self.ImageJumpEntry.grid(row=3,column=1,sticky=tk.W)
		#============================#

		#======Attribute Options======#
		self.AttributeOptions = tk.LabelFrame(self.MainPanel,bg='white',fg='black',text='Attribute Options',height=585,width=200)
		self.AttributeOptions.grid(row=0,column=2,sticky=tk.N+tk.S)
		self.BasicImageData = tk.LabelFrame(self.AttributeOptions,text='Basic Image Data')
		self.BIDListbox= tk.Listbox(self.BasicImageData,height=4,width=27)
		self.BIDListbox.insert(1,'Size : {}'.format(InitAttribute['Size']))  # listbox insert the image attribute
		self.BIDListbox.insert(2,'Scale : {}'.format(InitAttribute['Scale']))
		self.BIDListbox.insert(3,'Name : {}'.format(InitAttribute['Name']))
		self.BIDListbox.insert(4,'Path : {}'.format(InitAttribute['Path']))
		self.BIDListbox.pack()
		self.BasicImageData.pack()
		self.BBOXFrame = tk.LabelFrame(self.AttributeOptions,text='Bnding Box')
		self.BBOXListbox = tk.Listbox(self.BBOXFrame,width=27,height=6)
		#self.BBOXListbox.bind("<<ListboxSelect>>",self.bboxshow)
		self.BoxRemoveButton = tk.Button(self.BBOXFrame,text='<->',width=5,command= self.removebox)
		self.BoxDelallButton = tk.Button(self.BBOXFrame,text='<delete all>',width=10,command=self.deleteallbox)
		self.BBOXListbox.pack()
		self.BBOXFrame.pack(side=tk.TOP)
		self.BoxDelallButton.pack(side=tk.LEFT)
		self.BoxRemoveButton.pack(side=tk.LEFT)
		self.AttributeAddFrame = tk.LabelFrame(self.AttributeOptions,text='Class Attribute Add')
		self.AttributeAddListbox = tk.Listbox(self.AttributeAddFrame,width=27,height=5)
		self.AttributeAddListbox.bind("<<ListboxSelect>>",self.getbboxcolor)
		self.AttributeAddButton = tk.Button(self.AttributeAddFrame,text='<+>',width=5,command = self.addattribute)
		self.AttributeRemoveButton = tk.Button(self.AttributeAddFrame,text='<->',width=5,command= self.removeattribute)
		#self.AttributeAddListbox.insert(1,'Name : {}'.format(InitAttribute['Name']))
		self.AttributeAddListbox.pack()
		self.AttributeRemoveButton.pack(side = tk.LEFT)
		self.AttributeAddButton.pack(side = tk.RIGHT)
		self.AttributeAddFrame.pack()
		self.FormatOutFrame = tk.LabelFrame(self.AttributeOptions,text='Label Output Format')
		self.yolovar = tk.IntVar()
		self.norvar = tk.IntVar()
		self.YoloFormat = tk.Checkbutton(self.FormatOutFrame,text='Yolo label',variable=self.yolovar ,onvalue=1 ,offvalue=0,command=self.pathinsert)
		self.NormalFormat = tk.Checkbutton(self.FormatOutFrame,text='Normal label',variable=self.norvar ,onvalue=1 ,offvalue=0,command=self.pathinsert)
		self.YoloPathE = tk.Entry(self.FormatOutFrame,width=14)
		self.NorPathE = tk.Entry(self.FormatOutFrame,width=14)
		self.FileGen = tk.Button(self.FormatOutFrame,text='Gerenate',command=self.gerenatefile)
		self.YoloFormat.grid(row=0,column=0,sticky=tk.W)
		self.YoloPathE.grid(row=0,column=1)
		self.NormalFormat.grid(row=1,column=0)
		self.NorPathE.grid(row=1,column=1)
		self.FileGen.grid(row=2,column=0,columnspan=2,sticky=tk.W+tk.E)
		self.FormatOutFrame.pack(fill=tk.X)
		#self.StatusShow = tk.Label(self.AttributeOptions,text='Prosess image')
		#self.TxtFormat = tk.LabelFrame(self.AttributeOptions,text='TXT Format').pack(fill=tk.BOTH)
		#=============================#
		#=================================================#
	def Maintain(self):
		self.readjson()
		self.filecheckbox.destroy()
	def DeleteDir(self):
		sh.rmtree(OutputPathname)
		os.mkdir(OutputPathname)
		print(OutputPathname,'Remove and Creating ...')
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
	def LoadImage(self):
		self.ImageBox = []
		self.ImageBoxupLabel = []
		self.BIDListbox.delete(0,tk.END)
		#self.AttributeAddListbox.delete(0)
		#if not self.DirectoryPathE.get()
		self.ObjPath=self.DirectoryPathE.get()
		#print('line 198 here -------------->',self.ObjPath)
		if not self.ObjPath:
			messagebox.showwarning("Warning","Directory entry no path input!!")
		else:
			self.ObjPath = self.ObjPath+'/'
		if not os.path.isdir(self.ObjPath):
			messagebox.showwarning("Warning","Cannot find the directory!!")
		self.picturelist = os.listdir(self.ObjPath)
		for check in self.picturelist:
			if check != '.DS_Store':
				continue
			elif check == '.DS_Store':
				self.picturelist.remove('.DS_Store')
		self.picturelist.sort()
		#print(self.picturelist)
		self.ObjList = ImgFormatFilter(self.picturelist,self.ObjPath)
		#print(self.ObjList)
		if not os.path.isdir(OutputPathname): #[.attribute](not exist)
			os.mkdir(OutputPathname)
			print(OutputPathname,'creating ...')
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
		else : # [.attribute](exist)
			filecheck = os.listdir(OutputPathname)
			print('filecheck:',len(filecheck))
			#messagebox.showinfo("showinfo demo", "Info")
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
			else: # [.attribute](exist) [json file](not exist)
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
		#============================#

		#=== PreLoadImage definition ===#
	def PreLoad(self):
		self.saveImagedata()
		self.canvas.delete(self.bboxret)
		self.deleteallbox()
		self.ImageBox = []
		self.ImageBoxupLabel = []
		self.bndboxattribute = []
		self.classIDandclassname = {}
		self.classID = {}
		self.BIDListbox.delete(0,tk.END) #clean listbox
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
				infotext = 'Image Name : '+temptext + '( '+ str(self.flag++1) +' / '+str(len(self.picturelist))+' )'
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
		self.canvas.delete(self.bboxret)
		self.deleteallbox()
		print(self.ImageBox)
		self.ImageBox = []
		self.ImageBoxupLabel = []
		self.bndboxattribute = []
		self.classIDandclassname = {}
		self.classID = {}
		self.BIDListbox.delete(0,tk.END) # clean listbox
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
		self.saveImagedata()
		self.canvas.delete(self.bboxret)
		self.deleteallbox()
		self.removeallattribute()
		self.ImageBox = []
		self.ImageBoxupLabel = []
		self.bndboxattribute = []
		self.classIDandclassname = {}
		self.classID = {}
		self.BIDListbox.delete(0,tk.END) # clean listbox
		picnumber = self.ImageJumpEntry.get()
		self.flag = int(picnumber)-1
		if self.flag <0:
			self.flag += len(self.ObjList)+1
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
		#============================#
	def mouseClick(self,event):
		if len(self.classIDandclassname) == 0:
			messagebox.showwarning("Warning","You must to create classes and click the attribute")
		if self.STATE['click'] == 0: # recode position original
			self.STATE['x'],self.STATE['y'] = event.x,event.y
			#print('x:{},y:{}'.format(event.x,event.y))
		else: #record end position
			x1,x2 = min(self.STATE['x'],event.x),max(self.STATE['x'],event.x) # no matter where you plot can get the correct postion from left up side to right down side
			y1,y2 = min(self.STATE['y'],event.y),max(self.STATE['y'],event.y)
			retangleo = x1,y1,x2,y2
			#print('x:{},y:{}'.format(event.x,event.y))
			if self.ration > 1 : #scale up
				retangle= int(retangleo[0]/self.ration),int(retangleo[1]/self.ration),int(retangleo[2]/self.ration),int(retangleo[3]/self.ration)
			elif self.ration < 1: #scale down
				retangle= int(retangleo[0]*self.ration),int(retangleo[1]*self.ration),int(retangleo[2]*self.ration),int(retangleo[3]*self.ration)
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
		else :
			messagebox.showwarning("Warning","You must to paste the Path to entry and click\"LOAD\"")
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
		self.classcolorbutton[i].destroy()
		self.classcolorentry[i].config(bg=hx,text=hx)
		#self.colorchIndex.append(hx)
	def deleteclass(self):
		# use compare to remove unnecessary label and entry
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
		#self.classcount = len(self.allclassID)
		for getin in range(self.classnumber):
			self.spinboxclassname.append(self.classentry[getin].get())
			self.spinboxclasscolor.append(self.classcolorentry[getin].cget("text"))
			self.spinboxclassidtemp.append(self.classIDentry[getin].get())
			#print(self.spinboxclassname.append(self.classentry[getin].get()),self.spinboxclasscolor.append(self.classcolorentry[getin].get()))
		for attinsert in range(self.classnumber):
			self.AttributeAddListbox.insert(tk.END,'Name:{},Color:{}'.format(self.spinboxclassname[attinsert],self.spinboxclasscolor[attinsert]))
			self.allclassIDandclassname[self.spinboxclassname[attinsert]]=self.spinboxclasscolor[attinsert]
			#self.allclassID[self.spinboxclassname[attinsert]] = self.classcount + attinsert
			self.allclassID[self.spinboxclassname[attinsert]] = self.spinboxclassidtemp[attinsert]
		print('self.allclassID:',self.allclassID)
		#print('self.allclassID:',self.allclassID)
		#print('hello here is classIDandclassname',self.allclassIDandclassname)
		self.subwindow.destroy()
	def removeattribute(self):
		traget = self.AttributeAddListbox.curselection()
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
		#print(traget)
		#print(self.BBOXListbox.get(traget))
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
		print(self.ImageBox)
	def deleteallbox(self):
		self.bndboxlist=[]#reset to none
		self.bndboxattribute = [] #reset to none
		#print('====5====',self.boxcount)
		size = self.BBOXListbox.size()
		#print('listbox size:',size)
		for plugout in range(size):
			self.BBOXListbox.delete(0)
			self.canvas.delete(self.ImageBox[0])
			self.canvas.delete(self.ImageBoxupLabel[0])
			self.ImageBox.pop(0)
			self.ImageBoxupLabel.pop(0)
			#print(self.ImageBox)
		self.boxcount = 0
		#print('bndboxlist:{}\nboxcount:{}'.format(self.bndboxlist,self.boxcount))
	def getbboxcolor(self,event):
		target = event.widget.curselection()
		#print(target[0],type(target)) tuple can slice
		objstr = self.AttributeAddListbox.get(target)
		self.boxcolor = objstr.split(':')
		self.name=self.boxcolor[1].split(',')[0]
		print('line 594',self.boxcolor)
		self.classIDandclassname[self.name]=self.boxcolor[2]
		print('line 596',self.allclassID)
		self.classID[self.name]=self.allclassID[self.name]
		self.canvas.itemconfig(self.bboxret,outline=self.boxcolor[2])
		#self.canvas.itemconfig(self.ImageBox[self.boxcount],outline=att[2])
		#change canvas bunbox color attribute
		#target = self.AttributeAddListbox.curselection()
	def pathinsert(self):
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
		elif (self.yolovar.get() == 0 ) & (self.norvar.get() == 1):
			self.OutputFormatSelect=[]
			self.OutputFormatSelect.append('normal')
			if not self.NorPathE.get():
				print('normal default:{}'.format(self.OutputPath['normal']))
			else:
				self.OutputPath['normal'] = self.NorPathE.get()
				#print('normal path:{}'.format(self.OutputPath['normal']))
			#print(self.OutputFormatSelect)
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
		self.Imgdata.append({'Scale':[self.nsize[0],self.nsize[1]]})
		self.Imgdata.append(self.classIDandclassname)
		self.Imgdata.append(self.classID)
		#self.Imgdata.append(self.allclassID)
		# classfication per class
		for key,value in self.classIDandclassname.items():
			locals()[key+" attribute"] = [0,key,value]
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
		if (self.Imgdata[4] != {}) and (self.Imgdata[5] != {}):
			out = self.picturelist[self.flag].split('.')[0]
			out = '/'+out+'.json'
			with open(OutputPathname+out,'w') as file:
				self.text=json.dumps(self.Imgdata,indent = 2)
				file.write(self.text)
	def gerenatefile(self):
		if len(self.OutputFormatSelect) == 0:
			messagebox.showwarning("Outpu Path Warning","You do not select output format")
		else :
			if os.path.isdir(OutputPathname):
				attributefile = os.listdir(OutputPathname)
				attributefile.sort()
				#print(attributefile)
			else:
				messagebox.showwarning("attribute folder status","Attributefile doesn't exist !!")
			self.Gwindow = tk.Toplevel()
			self.Gwindow.title('Gerenate Output')
			self.Glabel = tk.Label(self.Gwindow,text='Gerenate:')
			self.Gshow = tk.Label(self.Gwindow,text='From [{}] to [{}] \nTotall file number {}'.format(attributefile[0],attributefile[-1],len(attributefile)))
			self.Gselect = tk.Label(self.Gwindow,text='label select{}'.format(self.OutputFormatSelect))
			self.GYButton = tk.Button(self.Gwindow,text='Yes',command=self.GYes,width=5)
			self.GNButton = tk.Button(self.Gwindow,text='No',command=self.GNo,width=5)
			self.Glabel.grid(row=0,column=1,sticky=tk.W)
			self.Gshow.grid(row=1,column=1)
			self.Gselect.grid(row=2,column=1,sticky=tk.W)
			self.GYButton.grid(row=3,column=0)
			self.GNButton.grid(row=3,column=2)
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
										for key,value in jsondata[5].items():
											i += 1 #jsondata index to fetch object list
											iteration = jsondata[5+i][0] #get bbox number on key object
											for bboxcount in range(iteration):
												coordinate = jsondata[5+i][3+bboxcount]
												x1,y1,x2,y2 = coordinate[0],coordinate[1],coordinate[2],coordinate[3]
												label.write(str(value)+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+'\n')
					else :
						messagebox.showwarning("Warning","Attribute file didn't exist")
				elif self.OutputFormatSelect[name] == 'yolo':
					# check attribute status
					if os.path.isdir('.attribute'):#path notice
						tempfile = os.listdir('.attribute')#path notice
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
										for key,value in jsondata[5].items():
											i += 1 #jsondata index to fetch object list
											iteration = jsondata[5+i][0] #get bbox number on key object
											for bboxcount in range(iteration):
												coordinate = jsondata[5+i][3+bboxcount]
												imsize = jsondata[2]['Size']
												yolotxt = BBox_yolo(coordinate,imsize)
												label.write(str(value)+' '+yolotxt[0]+' '+yolotxt[0]+' '+yolotxt[0]+' '+yolotxt[0]+'\n')
					else:
						messagebox.showwarning("Warning","Attribute file didn't exist")
		 #print(Lpath)
			except:
				print('keyError from GYes')
			self.Gwindow.destroy()
						#check object
	def GNo(self):
		self.Gwindow.destroy()
	def readjson(self):
		self.deleteallbox()
		jspath = self.picturelist[self.flag].split('.')[0]
		jspath = '/'+jspath+'.json'
		with open(OutputPathname+jspath,'r') as file:
			jsdata = json.load(file)
		photo = jsdata[0]['Path']+jsdata[1]['IMGName']
		ratio = jsdata[2]['Size'][0]/jsdata[3]['Scale'][0]
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
				if ratio > 1:
					retangle = int(jsdata[object+6][3+box][0]*ratio),int(jsdata[object+6][3+box][1]*ratio),int(jsdata[object+6][3+box][2]*ratio),int(jsdata[object+6][3+box][3]*ratio)
				elif ratio < 1:
					retangle = int(jsdata[object+6][3+box][0]/ratio),int(jsdata[object+6][3+box][1]/ratio),int(jsdata[object+6][3+box][2]/ratio),int(jsdata[object+6][3+box][3]/ratio)
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
root.geometry('1150x600')
def on_close():
	close = messagebox.askokcancel("Close", "Would you like to close the program?")
	if close:
		if not control.ObjPath:
			root.destroy()
		else:
			control.saveImagedata()
			root.destroy()
root.protocol("WM_DELETE_WINDOW",  on_close)
control = MainPanelCreate(root)
root.mainloop()
#=========================#
