# -*- coding: utf-8 -*-
import json
import web
import glob
import imagehash
import uuid
from io import BytesIO
import base64
from PIL import Image

imadbfolder = "./img"
tmp_upload_folder = './tmp'
urls = ('/upload', 'Upload')
hashfunc = imagehash.phash

class Upload:

#     def GET(self):
#         web.header("Content-Type", "text/html; charset=utf-8")
#         return """<html><head></head><body>
# <form method="POST" enctype="multipart/form-data" action="">
# <input type="file" name="myfile" />
# <br/>
# <input type="submit" />
# </form>
# </body></html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = tmp_upload_folder
        if 'file' in x:  # to check if the file-object is created
            # filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            # filename = filepath.split('.')[-1]  # splits the and chooses the last part (the filename with extension)
            # fout = open(filedir + '/' + str(uuid.uuid4())+"."+filename, 'wb')  # creates the file where the uploaded file should be stored
            # fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
            #
            # fout.close()  # closes the file, upload complete.

            filepath = ("filename" in x and x.filename.replace('\\', '/')) or "xxx.jpg"  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('.')[-1]  # splits the and chooses the last part (the filename with extension)
            fout = open(filedir + '/' + str(uuid.uuid4())+"."+filename, 'wb')  # creates the file where the uploaded file should be stored
            fout.write(BytesIO(x.file).read())  # writes the uploaded file to the newly created file.

            fout.close()  # closes the file, upload complete.

            hash_code = hashfunc(Image.open(BytesIO(x.file)))
            images = {}
            mindif = 25
            for key, value in web._imagedb.iteritems():
                dif = abs(hash_code - value)
                images[dif] = images.get(dif, []) + [key]
                if dif < mindif:
                    mindif = dif
            des = {}
            text = u" "
            # find information of the image
            # if mindif in images and images[mindif]:
                # for path in images[mindif]:
                #     for data in web._ypdatas:
                #         if data["images"][0]["path"].split("/")[-1] == path.split("\\")[-1]:
                #             des[path] = data
                #             text += data["atr2"] + u" "+ data["atr8"] + u"\n"
            rettext = text + u"最小相似度值："+ str(mindif)+ u"\n 最相似图片："+ str(images[mindif])
            return rettext

        return u"未找到匹配图片"
        # raise web.seeother('/upload')


if __name__ == "__main__":
    app = web.application(urls, globals())
    web._imagedb = {}
    for imagePath in glob.glob(imadbfolder + "/*.jpg"):
        imageID = imagePath[imagePath.rfind("/") + 1:]
        hash_code = hashfunc(Image.open(imagePath))
        web._imagedb[imageID] = hash_code

    # load image descritption
    # with open('ybk001.json') as f:
    #     web._ypdatas = json.loads(f.read())
    app.run()
