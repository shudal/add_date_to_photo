import exifread
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os,shutil
import piexif

font_size=160
font_path = "/home/heing/font/arial.ttf"

font = ImageFont.truetype(font_path, font_size)
save_dir="./ImageAppWithDate"

fname_list=[]
for parent, dirnames, filenames in os.walk(save_dir,  followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            fname = filename
            fname_list.append(fname)
def f_exist(fname):
    for s in fname_list:
        if s==fname:
            return True
    return False

work_dir="./ImageApp"
for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            print('文件完整路径：%s\n' % file_path)
            fpath=file_path
            fname = filename
            
            b = f_exist(fname)
            if b:
                print("    " + str(fname) + " exist")
                continue
            if "mp4" in fname:
                print("not image")
                continue
            f = open(fpath,"rb")
            tags = exifread.process_file(f)
            #print(tags)
            dt=tags['EXIF DateTimeOriginal']
            dt=str(dt)
            dt2 = ""
            c=0
            f=True
            for ch in dt:
                if f and ch==':':
                    c=c+1
                    dt2 = dt2 + '/'
                    if c==2:
                        f=False
                else:
                    dt2 = dt2 + ch
            dt=dt2
            print("    " + str(dt))
            image = Image.open(fpath)
            draw = ImageDraw.Draw(image)
            size=image.size
            print("    " + str(size))
            txt = str(dt)
            pos=(size[0]-len(txt)*font_size*4/7,size[1]-2*font_size)
            print("    " + str(pos))
            draw.text(pos, txt, fill=(236,236,236), font=font)
            
            exif_bytes=piexif.dump(piexif.load(image.info['exif']))
            image.save(save_dir + "/"+fname, quality=95,exif=exif_bytes)

