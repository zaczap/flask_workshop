import VSG_Module
import StringIO

image_str = StringIO.StringIO()




im = Image.open(image_str)

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=128)
draw.line((0, im.size[1], im.size[0], 0), fill=128)
del draw

# write to stdout
im.save(sys.stdout, "PNG")