#!/usr/bin/env python -i

VSGVersion='VSG2CT_07_23_14'
## For Current Version of VSG_Module and Documentation, see:  https://www.dropbox.com/s/8gsn92gejp3wblq/VSG_Module_Current.zip



from math import *
import os
import sys
ver1=sys.version_info[0]+0.1*sys.version_info[1]  ##e.g. ver1=2.7 for python version 2.7
if ver1>=3:
    long=int

try:
    import gc
    gcimported1=True
except:
    gcimported1=False
from copy import copy,deepcopy

try:
    import webbrowser
    webbrowserimported1=True
except:
    webbrowserimported1=False


try:
    import Tkinter as tk
    tkimported1=True
except:
    try:
        import tkinter as tk
        tkimported1=True
    except:
        tkimported1=False
try:
    import tkFont
    tkFontimported1=True
except:
    try:
        import tkinter.font as tkFont
        tkFontimported1=True
    except:
        tkFontimported1=False

try:
    from ScrolledText import *
    ScrolledTextimported1=True
except:
    try:
        from tkinter.scrolledtext import *
        ScrolledTextimported1=True
    except:
        ScrolledTextimported1=False

from subprocess import check_call,check_output
from time import asctime
import datetime

try:
    import Image, ImageDraw, ImageFont
    Imageimported1=True
except:
    try:
        from PIL import Image, ImageDraw, ImageFont
        Imageimported1=True
    except:
        Imageimported1=False

## Some code to detect if VSG has been called from with iPython Notebook (viPython will be true)
try:
    __IPYTHON__
    from IPython.core.display import display as I_display
    from IPython.core.display import Image as I_Image
    from IPython.core.display import SVG as I_SVG
    ##from IPython.core.display import HTML as I_HTML
    viPython=True
except:
    viPython=False

##buglist
## MVG doesn't properly render bold font or rotations
## SVG and MVG textwidths are not precisely calculated
## SVG display has very rudimentary mouse actions
## Rotated text in TK will require tk version 8.6.  Need to update when available
## some external code constructions are specific to python 2.x (specifically 2.7) may needs to be updated to 3 for some modules
## rendering of mouse links in PDF would be nice
## Grid command for text entries would be useful
## setting of coordinants for colorkey is a bit cumbersome and should match coordinant setting for any other object, indeed colorkey should just be another object
## a "label" attribute for items would be useful; also perhaps clickonlabel (clicking on item shows label)
## IF WE TOOK OUT THE BONES IT WOULDN'T BE CRUNCHY!
## VSG2 Copywrite 2009-2013 Andrew Fire and Stanford University.  All rights reserved
## Send bug reports to afire<rat>stanford.edu (changing the nice rodent into an @ sign)

## need to have the whole set of path variables to use graphicsmagick... this may need to be
## be revisited with other installations of GM or with other systems.
## the issue here is that IDLE (and likely other IDEs) doesn't use the same
## PATH options as the terminal as run from the operating systems.  At least for mac
## this makes it difficult to call programs that have been installed for use at the command
## line in terminal.  The list below was pulled out 3/2011 from a MAC snow leopard terminal
## using the command echo $PATH in terminal

os.environ["PATH"]=os.getenv("PATH")+':/Library/Frameworks/Python.framework/Versions/Current/bin:/Library/Frameworks/EPD64.framework/Versions/Current/bin:/opt/local/bin:/opt/local/sbin:/Library/Frameworks/EPD64.framework/Versions/Current/bin:/Library/Frameworks/Python.framework/Versions/Current/bin:/Library/Frameworks/Python.framework/Versions/Current/bin:/Library/Frameworks/Python.framework/Versions/2.7/bin:/Library/Frameworks/Python.framework/Versions/2.7/bin:/Library/Frameworks/Python.framework/Versions/2.7/bin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/Library/Frameworks/Python.framework/Versions/2.6/bin:/Library/Frameworks/Python.framework/Versions/Current/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin'
colordict1={}  ## associates specific strings with (arbitrary but consistent) colors
sitedict1={}   ## associates pairs of (canvas,object) with weblink
msgdict1={}    ## associates pairs of canvas,object with mouseover messages 
popupdict1={}   ## associates pairs of canvas,object with on-click popups
detaildict1={}  ## dictionary of detailed pointsp
fontabbrevdict={} ## previous evaluations of font abbreviations
fontdict={}   ## list of font objects as a function of element descriptions
none=''

## TK alignment options
anchordict={('start','top'):'nw',('middle','top'):'n',('end','top'):'ne',
            ('start','center'):'w',('middle','center'):'center',('end','center'):'e',
            ('start','bottom'):'sw',('middle','bottom'):'s',('end','bottom'):'se'}

## MVG alignment options
gravitydict={('start','top'):'NorthWest',('middle','top'):'North',('end','top'):'NorthEast',
            ('start','center'):'West',('middle','center'):'Center',('end','center'):'East',
            ('start','bottom'):'SouthWest',('middle','bottom'):'South',('end','bottom'):'SouthEast'}

## tk alignment options
tkjustD={'start':'left','middle':'center','end':'right'}

## html alignment options
htmljustD={'start':'start','middle':'center','end':'end'}

## MVG colors defines virtually every word for a color as an RGB value set
## in older versions of VSG, this was a separate file, now incorporated into VSG: from MVGColors import *
## color definitions for MVG, all items have been made lower case
vhue={'yellow': 'rgb(255,255,0)', 'grey61': 'rgb(156,156,156)', 'grey60': 'rgb(153,153,153)', 'darkseagreen': 'rgb(143,188,143)', 'grey62': 'rgb(158,158,158)', 'grey65': 'rgb(166,166,166)', 'grey64': 'rgb(163,163,163)', 'grey67': 'rgb(171,171,171)', 'grey66': 'rgb(168,168,168)', 'grey69': 'rgb(176,176,176)', 'grey68': 'rgb(173,173,173)', 'gray32': 'rgb(82,82,82)', 'deepskyblue2': 'rgb(0,178,238)', 'gray30': 'rgb(77,77,77)', 'gray31': 'rgb(79,79,79)', 'gray36': 'rgb(92,92,92)', 'gray37': 'rgb(94,94,94)', 'gray34': 'rgb(87,87,87)', 'gray35': 'rgb(89,89,89)', 'aquamarine4': 'rgb(69,139,116)', 'gray38': 'rgb(97,97,97)', 'gray39': 'rgb(99,99,99)', 'aquamarine1': 'rgb(127,255,212)', 'aquamarine3': 'rgb(102,205,170)', 'aquamarine2': 'rgb(118,238,198)', 'crimson': 'rgb(220,20,60)', 'deepskyblue1': 'rgb(0,191,255)', 'brown': 'rgb(165,42,42)', 'coral3': 'rgb(205,91,69)', 'gray8': 'rgb(20,20,20)', 'gray9': 'rgb(23,23,23)', 'gray2': 'rgb(5,5,5)', 'cyan': 'rgb(0,255,255)', 'gray0': 'rgb(0,0,0)', 'gray1': 'rgb(3,3,3)', 'fractal': 'rgb(128,128,128)', 'gray7': 'rgb(18,18,18)', 'gray4': 'rgb(10,10,10)', 'gray5': 'rgb(13,13,13)', 'skyblue': 'rgb(135,206,235)', 'deepskyblue4': 'rgb(0,104,139)', 'rosybrown3': 'rgb(205,155,155)', 'grey63': 'rgb(161,161,161)', 'indianred1': 'rgb(255,106,106)', 'lightpink': 'rgb(255,182,193)', 'indianred2': 'rgb(238,99,99)', 'teal': 'rgb(0,128,128)', 'grey11': 'rgb(28,28,28)', 'lemonchiffon3': 'rgb(205,201,165)', 'lemonchiffon2': 'rgb(238,233,191)', 'lemonchiffon1': 'rgb(255,250,205)', 'bisque': 'rgb(255,228,196)', 'grey12': 'rgb(31,31,31)', 'lemonchiffon4': 'rgb(139,137,112)', 'gray99': 'rgb(252,252,252)', 'grey13': 'rgb(33,33,33)', 'grey14': 'rgb(36,36,36)', 'lightgoldenrodyellow': 'rgb(250,250,210)', 'lavender': 'rgb(230,230,250)', 'chartreuse3': 'rgb(102,205,0)', 'chartreuse2': 'rgb(118,238,0)', 'chartreuse1': 'rgb(127,255,0)', 'grey16': 'rgb(41,41,41)', 'chartreuse4': 'rgb(69,139,0)', 'grey17': 'rgb(43,43,43)', 'dimgrey': 'rgb(105,105,105)', 'blue': 'rgb(0,0,255)', 'opaque': 'rgb(0,0,0)', 'maroon4': 'rgb(139,28,98)', 'maroon3': 'rgb(205,41,144)', 'maroon2': 'rgb(238,48,167)', 'maroon1': 'rgb(255,52,179)', 'gold3': 'rgb(205,173,0)', 'gold2': 'rgb(238,201,0)', 'gold1': 'rgb(255,215,0)', 'gold4': 'rgb(139,117,0)', 'gray41': 'rgb(105,105,105)', 'gray33': 'rgb(84,84,84)', 'skyblue4': 'rgb(74,112,139)', 'skyblue1': 'rgb(135,206,255)', 'skyblue3': 'rgb(108,166,205)', 'skyblue2': 'rgb(126,192,238)', 'coral4': 'rgb(139,62,47)', 'lightskyblue4': 'rgb(96,123,139)', 'floralwhite': 'rgb(255,250,240)', 'gray60': 'rgb(153,153,153)', 'firebrick3': 'rgb(205,38,38)', 'firebrick2': 'rgb(238,44,44)', 'steelblue3': 'rgb(79,148,205)', 'steelblue2': 'rgb(92,172,238)', 'steelblue4': 'rgb(54,100,139)', 'firebrick4': 'rgb(139,26,26)', 'grey51': 'rgb(130,130,130)', 'aliceblue': 'rgb(240,248,255)', 'greenyellow': 'rgb(173,255,47)', 'lightseagreen': 'rgb(32,178,170)', 'sienna': 'rgb(160,82,45)', 'blue1': 'rgb(0,0,255)', 'lime': 'rgb(0,255,0)', 'goldenrod2': 'rgb(238,180,34)', 'royalblue': 'rgb(65,105,225)', 'gainsboro': 'rgb(220,220,220)', 'peru': 'rgb(205,133,63)', 'darkslategray': 'rgb(47,79,79)', 'red3': 'rgb(205,0,0)', 'red2': 'rgb(238,0,0)', 'red1': 'rgb(255,0,0)', 'dodgerblue': 'rgb(30,144,255)', 'red4': 'rgb(139,0,0)', 'lemonchiffon': 'rgb(255,250,205)', 'lightgreen': 'rgb(144,238,144)', 'darkgrey': 'rgb(169,169,169)', 'olive': 'rgb(128,128,0)', 'antiquewhite': 'rgb(250,235,215)', 'grey18': 'rgb(46,46,46)', 'grey19': 'rgb(48,48,48)', 'moccasin': 'rgb(255,228,181)', 'grey10': 'rgb(26,26,26)', 'chocolate1': 'rgb(255,127,36)', 'chocolate2': 'rgb(238,118,33)', 'chocolate3': 'rgb(205,102,29)', 'chocolate4': 'rgb(139,69,19)', 'grey15': 'rgb(38,38,38)', 'darkslateblue': 'rgb(72,61,139)', 'lightskyblue': 'rgb(135,206,250)', 'gray69': 'rgb(176,176,176)', 'gray68': 'rgb(173,173,173)', 'deeppink': 'rgb(255,20,147)', 'gray65': 'rgb(166,166,166)', 'gray64': 'rgb(163,163,163)', 'gray67': 'rgb(171,171,171)', 'gray66': 'rgb(168,168,168)', 'gray61': 'rgb(156,156,156)', 'coral': 'rgb(255,127,80)', 'gray63': 'rgb(161,161,161)', 'gray62': 'rgb(158,158,158)', 'springgreen1': 'rgb(0,255,127)', 'springgreen2': 'rgb(0,238,118)', 'springgreen3': 'rgb(0,205,102)', 'springgreen4': 'rgb(0,139,69)', 'lightgray': 'rgb(211,211,211)', 'seashell2': 'rgb(238,229,222)', 'seashell3': 'rgb(205,197,191)', 'magenta': 'rgb(255,0,255)', 'seashell1': 'rgb(255,245,238)', 'tan': 'rgb(210,180,140)', 'seashell4': 'rgb(139,134,130)', 'pink': 'rgb(255,192,203)', 'palevioletred': 'rgb(219,112,147)', 'powderblue': 'rgb(176,224,230)', 'mediumblue': 'rgb(0,0,205)', 'grey89': 'rgb(227,227,227)', 'gray100': 'rgb(255,255,255)', 'grey87': 'rgb(222,222,222)', 'grey86': 'rgb(219,219,219)', 'grey85': 'rgb(217,217,217)', 'grey84': 'rgb(214,214,214)', 'midnightblue': 'rgb(25,25,112)', 'grey82': 'rgb(209,209,209)', 'grey81': 'rgb(207,207,207)', 'grey80': 'rgb(204,204,204)', 'gray40': 'rgb(102,102,102)', 'lightslategray': 'rgb(119,136,153)', 'dodgerblue1': 'rgb(30,144,255)', 'mediumpurple1': 'rgb(171,130,255)', 'mediumpurple2': 'rgb(159,121,238)', 'mediumpurple3': 'rgb(137,104,205)', 'mediumpurple4': 'rgb(93,71,139)', 'violetred2': 'rgb(238,58,140)', 'khaki4': 'rgb(139,134,78)', 'paleturquoise4': 'rgb(102,139,139)', 'paleturquoise3': 'rgb(150,205,205)', 'khaki1': 'rgb(255,246,143)', 'khaki2': 'rgb(238,230,133)', 'khaki3': 'rgb(205,198,115)', 'salmon1': 'rgb(255,140,105)', 'honeydew4': 'rgb(131,139,131)', 'salmon3': 'rgb(205,112,84)', 'salmon2': 'rgb(238,130,98)', 'salmon4': 'rgb(139,76,57)', 'linen': 'rgb(250,240,230)', 'burlywood1': 'rgb(255,211,155)', 'green': 'rgb(0,128,0)', 'blueviolet': 'rgb(138,43,226)', 'brown2': 'rgb(238,59,59)', 'brown3': 'rgb(205,51,51)', 'brown1': 'rgb(255,64,64)', 'brown4': 'rgb(139,35,35)', 'orange4': 'rgb(139,90,0)', 'orange1': 'rgb(255,165,0)', 'orange3': 'rgb(205,133,0)', 'orange2': 'rgb(238,154,0)', 'slategrey': 'rgb(112,128,144)', 'gray3': 'rgb(8,8,8)', 'darkslategrey': 'rgb(47,79,79)', 'gray6': 'rgb(15,15,15)', 'yellow4': 'rgb(139,139,0)', 'yellow3': 'rgb(205,205,0)', 'yellow2': 'rgb(238,238,0)', 'yellow1': 'rgb(255,255,0)', 'orange': 'rgb(255,165,0)', 'grey88': 'rgb(224,224,224)', 'grey58': 'rgb(148,148,148)', 'grey59': 'rgb(150,150,150)', 'grey54': 'rgb(138,138,138)', 'mediumorchid4': 'rgb(122,55,139)', 'grey56': 'rgb(143,143,143)', 'grey57': 'rgb(145,145,145)', 'mediumorchid1': 'rgb(224,102,255)', 'silver': 'rgb(192,192,192)', 'mediumorchid3': 'rgb(180,82,205)', 'mediumorchid2': 'rgb(209,95,238)', 'cyan2': 'rgb(0,238,238)', 'cyan3': 'rgb(0,205,205)', 'gray23': 'rgb(59,59,59)', 'cyan1': 'rgb(0,255,255)', 'gray25': 'rgb(64,64,64)', 'gray24': 'rgb(61,61,61)', 'cyan4': 'rgb(0,139,139)', 'darkviolet': 'rgb(148,0,211)', 'gray29': 'rgb(74,74,74)', 'grey83': 'rgb(212,212,212)', 'darkgray': 'rgb(169,169,169)', 'darkmagenta': 'rgb(139,0,139)', 'navy': 'rgb(0,0,128)', 'ghostwhite': 'rgb(248,248,255)', 'darkkhaki': 'rgb(189,183,107)', 'gray94': 'rgb(240,240,240)', 'gray95': 'rgb(242,242,242)', 'gray96': 'rgb(245,245,245)', 'gray97': 'rgb(247,247,247)', 'gray90': 'rgb(229,229,229)', 'gray91': 'rgb(232,232,232)', 'gray92': 'rgb(235,235,235)', 'gray93': 'rgb(237,237,237)', 'violetred': 'rgb(208,32,144)', 'gray98': 'rgb(250,250,250)', 'cornsilk': 'rgb(255,248,220)', 'red': 'rgb(255,0,0)', 'peachpuff': 'rgb(255,218,185)', 'lightslateblue': 'rgb(132,112,255)', 'steelblue': 'rgb(70,130,180)', 'lightskyblue1': 'rgb(176,226,255)', 'lightskyblue2': 'rgb(164,211,238)', 'lightskyblue3': 'rgb(141,182,205)', 'lightslategrey': 'rgb(119,136,153)', 'blue3': 'rgb(0,0,205)', 'blue2': 'rgb(0,0,238)', 'blue4': 'rgb(0,0,139)', 'lightgrey': 'rgb(211,211,211)', 'burlywood': 'rgb(222,184,135)', 'darksalmon': 'rgb(233,150,122)', 'violetred1': 'rgb(255,62,150)', 'slategray2': 'rgb(185,211,238)', 'slategray3': 'rgb(159,182,205)', 'violetred4': 'rgb(139,34,82)', 'grey27': 'rgb(69,69,69)', 'tomato4': 'rgb(139,54,38)', 'tomato1': 'rgb(255,99,71)', 'tomato3': 'rgb(205,79,57)', 'tomato2': 'rgb(238,92,66)', 'grey21': 'rgb(54,54,54)', 'grey75': 'rgb(191,191,191)', 'mistyrose': 'rgb(255,228,225)', 'grey23': 'rgb(59,59,59)', 'orangered': 'rgb(255,69,0)', 'navajowhite': 'rgb(255,222,173)', 'grey78': 'rgb(199,199,199)', 'slategray': 'rgb(112,128,144)', 'grey79': 'rgb(201,201,201)', 'lightcyan': 'rgb(224,255,255)', 'mistyrose1': 'rgb(255,228,225)', 'white': 'rgb(255,255,255)', 'gray26': 'rgb(66,66,66)', 'tomato': 'rgb(255,99,71)', 'gray46': 'rgb(117,117,117)', 'gray44': 'rgb(112,112,112)', 'gray43': 'rgb(110,110,110)', 'seagreen4': 'rgb(46,139,87)', 'seagreen3': 'rgb(67,205,128)', 'seagreen2': 'rgb(78,238,148)', 'seagreen1': 'rgb(84,255,159)', 'paleturquoise2': 'rgb(174,238,238)', 'mistyrose4': 'rgb(139,125,123)', 'paleturquoise1': 'rgb(187,255,255)', 'limegreen': 'rgb(50,205,50)', 'lightyellow': 'rgb(255,255,224)', 'mistyrose3': 'rgb(205,183,181)', 'palegreen1': 'rgb(154,255,154)', 'palegreen3': 'rgb(124,205,124)', 'palegreen2': 'rgb(144,238,144)', 'palegreen4': 'rgb(84,139,84)', 'mistyrose2': 'rgb(238,213,210)', 'grey43': 'rgb(110,110,110)', 'turquoise3': 'rgb(0,197,205)', 'turquoise2': 'rgb(0,229,238)', 'lightcyan3': 'rgb(180,205,205)', 'lightcyan2': 'rgb(209,238,238)', 'lightcyan4': 'rgb(122,139,139)', 'rosybrown': 'rgb(188,143,143)', 'turquoise4': 'rgb(0,134,139)', 'whitesmoke': 'rgb(245,245,245)', 'lightblue': 'rgb(173,216,230)', 'snow': 'rgb(255,250,250)', 'grey46': 'rgb(117,117,117)', 'gray58': 'rgb(148,148,148)', 'gray59': 'rgb(150,150,150)', 'grey45': 'rgb(115,115,115)', 'olivedrab4': 'rgb(105,139,34)', 'purple4': 'rgb(85,26,139)', 'gray52': 'rgb(133,133,133)', 'gray53': 'rgb(135,135,135)', 'purple1': 'rgb(155,48,255)', 'olivedrab1': 'rgb(192,255,62)', 'olivedrab2': 'rgb(179,238,58)', 'olivedrab3': 'rgb(154,205,50)', 'orangered3': 'rgb(205,55,0)', 'orangered2': 'rgb(238,64,0)', 'orangered1': 'rgb(255,69,0)', 'orangered4': 'rgb(139,37,0)', 'thistle3': 'rgb(205,181,205)', 'thistle2': 'rgb(238,210,238)', 'thistle1': 'rgb(255,225,255)', 'salmon': 'rgb(250,128,114)', 'thistle4': 'rgb(139,123,139)', 'oldlace': 'rgb(253,245,230)', 'gray19': 'rgb(48,48,48)', 'darkseagreen4': 'rgb(105,139,105)', 'darkseagreen3': 'rgb(155,205,155)', 'darkseagreen2': 'rgb(180,238,180)', 'darkseagreen1': 'rgb(193,255,193)', 'gray14': 'rgb(36,36,36)', 'lightpink1': 'rgb(255,174,185)', 'grey100': 'rgb(255,255,255)', 'gray17': 'rgb(43,43,43)', 'gold': 'rgb(255,215,0)', 'slategray1': 'rgb(198,226,255)', 'burlywood3': 'rgb(205,170,125)', 'lightsalmon4': 'rgb(139,87,66)', 'lightsalmon2': 'rgb(238,149,114)', 'lightsalmon3': 'rgb(205,129,98)', 'mediumforestgreen': 'rgb(50,129,75)', 'lightsalmon1': 'rgb(255,160,122)', 'green4': 'rgb(0,139,0)', 'green1': 'rgb(0,255,0)', 'green3': 'rgb(0,205,0)', 'green2': 'rgb(0,238,0)', 'darkslategray1': 'rgb(151,255,255)', 'darkslategray2': 'rgb(141,238,238)', 'darkslategray3': 'rgb(121,205,205)', 'darkslategray4': 'rgb(82,139,139)', 'steelblue1': 'rgb(99,184,255)', 'papayawhip': 'rgb(255,239,213)', 'black': 'rgb(0,0,0)', 'orchid4': 'rgb(139,71,137)', 'orchid1': 'rgb(255,131,250)', 'orchid2': 'rgb(238,122,233)', 'orchid3': 'rgb(205,105,201)', 'antiquewhite3': 'rgb(205,192,176)', 'antiquewhite2': 'rgb(238,223,204)', 'antiquewhite1': 'rgb(255,239,219)', 'hotpink': 'rgb(255,105,180)', 'antiquewhite4': 'rgb(139,131,120)', 'bisque4': 'rgb(139,125,107)', 'bisque1': 'rgb(255,228,196)', 'bisque2': 'rgb(238,213,183)', 'bisque3': 'rgb(205,183,158)', 'gray': 'rgb(126,126,126)', 'darkturquoise': 'rgb(0,206,209)', 'slategray4': 'rgb(108,123,139)', 'cornsilk1': 'rgb(255,248,220)', 'gray22': 'rgb(56,56,56)', 'plum4': 'rgb(139,102,139)', 'plum3': 'rgb(205,150,205)', 'plum2': 'rgb(238,174,238)', 'plum1': 'rgb(255,187,255)', 'lightblue3': 'rgb(154,192,205)', 'grey49': 'rgb(125,125,125)', 'grey48': 'rgb(122,122,122)', 'thistle': 'rgb(216,191,216)', 'violet': 'rgb(238,130,238)', 'darkorchid4': 'rgb(104,34,139)', 'grey42': 'rgb(107,107,107)', 'grey41': 'rgb(105,105,105)', 'grey40': 'rgb(102,102,102)', 'grey47': 'rgb(120,120,120)', 'darkorchid1': 'rgb(191,62,255)', 'darkorchid2': 'rgb(178,58,238)', 'darkorchid3': 'rgb(154,50,205)', 'honeydew': 'rgb(240,255,240)', 'gray18': 'rgb(46,46,46)', 'cornflowerblue': 'rgb(100,149,237)', 'darkblue': 'rgb(0,0,139)', 'gray15': 'rgb(38,38,38)', 'gray16': 'rgb(41,41,41)', 'gray82': 'rgb(209,209,209)', 'gray10': 'rgb(26,26,26)', 'gray11': 'rgb(28,28,28)', 'gray12': 'rgb(31,31,31)', 'gray13': 'rgb(33,33,33)', 'palevioletred4': 'rgb(139,71,93)', 'palevioletred1': 'rgb(255,130,171)', 'palevioletred2': 'rgb(238,121,159)', 'palevioletred3': 'rgb(205,104,137)', 'mediumpurple': 'rgb(147,112,219)', 'lightblue2': 'rgb(178,223,238)', 'darkcyan': 'rgb(0,139,139)', 'lightblue1': 'rgb(191,239,255)', 'lightblue4': 'rgb(104,131,139)', 'darkred': 'rgb(139,0,0)', 'lavenderblush1': 'rgb(255,240,245)', 'lavenderblush3': 'rgb(205,193,197)', 'lavenderblush2': 'rgb(238,224,229)', 'lavenderblush4': 'rgb(139,131,134)', 'grey99': 'rgb(252,252,252)', 'mediumturquoise': 'rgb(72,209,204)', 'grey38': 'rgb(97,97,97)', 'grey39': 'rgb(99,99,99)', 'grey36': 'rgb(92,92,92)', 'grey37': 'rgb(94,94,94)', 'grey34': 'rgb(87,87,87)', 'grey35': 'rgb(89,89,89)', 'aqua': 'rgb(0,255,255)', 'grey33': 'rgb(84,84,84)', 'grey30': 'rgb(77,77,77)', 'grey31': 'rgb(79,79,79)', 'gray83': 'rgb(212,212,212)', 'sienna4': 'rgb(139,71,38)', 'gray81': 'rgb(207,207,207)', 'gray80': 'rgb(204,204,204)', 'sienna1': 'rgb(255,130,71)', 'gray86': 'rgb(219,219,219)', 'sienna3': 'rgb(205,104,57)', 'sienna2': 'rgb(238,121,66)', 'lightyellow1': 'rgb(255,255,224)', 'lightyellow2': 'rgb(238,238,209)', 'lightyellow3': 'rgb(205,205,180)', 'lightyellow4': 'rgb(139,139,122)', 'lightgoldenrod': 'rgb(238,221,130)', 'gray87': 'rgb(222,222,222)', 'navajowhite4': 'rgb(139,121,94)', 'mediumorchid': 'rgb(186,85,211)', 'olivedrab': 'rgb(107,142,35)', 'navajowhite1': 'rgb(255,222,173)', 'navajowhite2': 'rgb(238,207,161)', 'darkgoldenrod1': 'rgb(255,185,15)', 'darkgoldenrod2': 'rgb(238,173,14)', 'palegreen': 'rgb(152,251,152)', 'seashell': 'rgb(255,245,238)', 'aquamarine': 'rgb(127,255,212)', 'tan4': 'rgb(139,90,43)', 'tan3': 'rgb(205,133,63)', 'tan2': 'rgb(238,154,73)', 'tan1': 'rgb(255,165,79)', 'lawngreen': 'rgb(124,252,0)', 'maroon': 'rgb(176,48,96)', 'darkorange4': 'rgb(139,69,0)', 'mintcream': 'rgb(245,255,250)', 'darkorange1': 'rgb(255,127,0)', 'darkorange3': 'rgb(205,102,0)', 'darkorange2': 'rgb(238,118,0)', 'saddlebrown': 'rgb(139,69,19)', 'goldenrod4': 'rgb(139,105,20)', 'goldenrod1': 'rgb(255,193,37)', 'mediumgoldenrod': 'rgb(209,193,102)', 'goldenrod3': 'rgb(205,155,29)', 'grey32': 'rgb(82,82,82)', 'darkgoldenrod': 'rgb(184,134,11)', 'lightcyan1': 'rgb(224,255,255)', 'sandybrown': 'rgb(244,164,96)', 'turquoise1': 'rgb(0,245,255)', 'ivory3': 'rgb(205,205,193)', 'ivory2': 'rgb(238,238,224)', 'ivory1': 'rgb(255,255,240)', 'burlywood2': 'rgb(238,197,145)', 'mediumseagreen': 'rgb(60,179,113)', 'ivory4': 'rgb(139,139,131)', 'darkorange': 'rgb(255,140,0)', 'grey9': 'rgb(23,23,23)', 'firebrick1': 'rgb(255,48,48)', 'burlywood4': 'rgb(139,115,85)', 'gray89': 'rgb(227,227,227)', 'palegoldenrod': 'rgb(238,232,170)', 'gray85': 'rgb(217,217,217)', 'violetred3': 'rgb(205,50,120)', 'gray84': 'rgb(214,214,214)', 'grey72': 'rgb(184,184,184)', 'grey73': 'rgb(186,186,186)', 'grey70': 'rgb(179,179,179)', 'grey71': 'rgb(181,181,181)', 'grey76': 'rgb(194,194,194)', 'grey77': 'rgb(196,196,196)', 'grey74': 'rgb(189,189,189)', 'gray88': 'rgb(224,224,224)', 'pink1': 'rgb(255,181,197)', 'pink3': 'rgb(205,145,158)', 'pink2': 'rgb(238,169,184)', 'pink4': 'rgb(139,99,108)', 'gray47': 'rgb(120,120,120)', 'darkolivegreen4': 'rgb(110,139,61)', 'gray45': 'rgb(115,115,115)', 'lightsteelblue': 'rgb(176,196,222)', 'darkolivegreen1': 'rgb(202,255,112)', 'gray42': 'rgb(107,107,107)', 'darkolivegreen3': 'rgb(162,205,90)', 'darkolivegreen2': 'rgb(188,238,104)', 'lavenderblush': 'rgb(255,240,245)', 'gray49': 'rgb(125,125,125)', 'gray48': 'rgb(122,122,122)', 'azure1': 'rgb(240,255,255)', 'azure3': 'rgb(193,205,205)', 'azure2': 'rgb(224,238,238)', 'indigo': 'rgb(75,0,130)', 'azure4': 'rgb(131,139,139)', 'firebrick': 'rgb(178,34,34)', 'indianred': 'rgb(205,92,92)', 'darkolivegreen': 'rgb(85,107,47)', 'grey55': 'rgb(140,140,140)', 'lightsteelblue1': 'rgb(202,225,255)', 'lightsteelblue2': 'rgb(188,210,238)', 'lightsteelblue3': 'rgb(162,181,205)', 'lightsteelblue4': 'rgb(110,123,139)', 'darkgoldenrod4': 'rgb(139,101,8)', 'grey50': 'rgb(127,127,127)', 'magenta4': 'rgb(139,0,139)', 'magenta3': 'rgb(205,0,205)', 'magenta2': 'rgb(238,0,238)', 'magenta1': 'rgb(255,0,255)', 'darkgoldenrod3': 'rgb(205,149,12)', 'chartreuse': 'rgb(127,255,0)', 'mediumslateblue': 'rgb(123,104,238)', 'grey52': 'rgb(133,133,133)', 'springgreen': 'rgb(0,255,127)', 'grey53': 'rgb(135,135,135)', 'lightsalmon': 'rgb(255,160,122)', 'gray21': 'rgb(54,54,54)', 'turquoise': 'rgb(64,224,208)', 'grey8': 'rgb(20,20,20)', 'gray20': 'rgb(51,51,51)', 'grey6': 'rgb(15,15,15)', 'grey7': 'rgb(18,18,18)', 'grey4': 'rgb(10,10,10)', 'grey5': 'rgb(13,13,13)', 'grey2': 'rgb(5,5,5)', 'grey3': 'rgb(8,8,8)', 'grey0': 'rgb(0,0,0)', 'grey1': 'rgb(3,3,3)', 'gray50': 'rgb(127,127,127)', 'goldenrod': 'rgb(218,165,32)', 'gray51': 'rgb(130,130,130)', 'navajowhite3': 'rgb(205,179,139)', 'darkgreen': 'rgb(0,100,0)', 'gray27': 'rgb(69,69,69)', 'peachpuff4': 'rgb(139,119,101)', 'gray54': 'rgb(138,138,138)', 'slateblue4': 'rgb(71,60,139)', 'slateblue3': 'rgb(105,89,205)', 'slateblue2': 'rgb(122,103,238)', 'slateblue1': 'rgb(131,111,255)', 'peachpuff3': 'rgb(205,175,149)', 'purple3': 'rgb(125,38,205)', 'gray28': 'rgb(71,71,71)', 'purple2': 'rgb(145,44,238)', 'peachpuff1': 'rgb(255,218,185)', 'royalblue4': 'rgb(39,64,139)', 'yellowgreen': 'rgb(154,205,50)', 'royalblue1': 'rgb(72,118,255)', 'peachpuff2': 'rgb(238,203,173)', 'lightgoldenrod3': 'rgb(205,190,112)', 'lightgoldenrod2': 'rgb(238,220,130)', 'orchid': 'rgb(218,112,214)', 'purple': 'rgb(160,32,240)', 'deeppink4': 'rgb(139,10,80)', 'wheat4': 'rgb(139,126,102)', 'wheat1': 'rgb(255,231,186)', 'wheat3': 'rgb(205,186,150)', 'wheat2': 'rgb(238,216,174)', 'indianred4': 'rgb(139,58,58)', 'coral2': 'rgb(238,106,80)', 'coral1': 'rgb(255,114,86)', 'rosybrown4': 'rgb(139,105,105)', 'deepskyblue3': 'rgb(0,154,205)', 'rosybrown2': 'rgb(238,180,180)', 'rosybrown1': 'rgb(255,193,193)', 'indianred3': 'rgb(205,85,85)', 'khaki': 'rgb(240,230,140)', 'wheat': 'rgb(245,222,179)', 'gray55': 'rgb(140,140,140)', 'deepskyblue': 'rgb(0,191,255)', 'grey44': 'rgb(112,112,112)', 'gray56': 'rgb(143,143,143)', 'plum': 'rgb(221,160,221)', 'beige': 'rgb(245,245,220)', 'azure': 'rgb(240,255,255)', 'honeydew1': 'rgb(240,255,240)', 'dodgerblue2': 'rgb(28,134,238)', 'dodgerblue3': 'rgb(24,116,205)', 'dodgerblue4': 'rgb(16,78,139)', 'gray57': 'rgb(145,145,145)', 'mediumvioletred': 'rgb(199,21,133)', 'snow4': 'rgb(139,137,137)', 'snow2': 'rgb(238,233,233)', 'snow3': 'rgb(205,201,201)', 'snow1': 'rgb(255,250,250)', 'lightcoral': 'rgb(240,128,128)', 'grey29': 'rgb(74,74,74)', 'grey28': 'rgb(71,71,71)', 'grey25': 'rgb(64,64,64)', 'grey24': 'rgb(61,61,61)', 'mediumspringgreen': 'rgb(0,250,154)', 'grey26': 'rgb(66,66,66)', 'fuchsia': 'rgb(255,0,255)', 'grey20': 'rgb(51,51,51)', 'blanchedalmond': 'rgb(255,235,205)', 'grey22': 'rgb(56,56,56)', 'gray78': 'rgb(199,199,199)', 'gray79': 'rgb(201,201,201)', 'gray76': 'rgb(194,194,194)', 'gray77': 'rgb(196,196,196)', 'gray74': 'rgb(189,189,189)', 'gray75': 'rgb(191,191,191)', 'gray72': 'rgb(184,184,184)', 'gray73': 'rgb(186,186,186)', 'gray70': 'rgb(179,179,179)', 'gray71': 'rgb(181,181,181)', 'ivory': 'rgb(255,255,240)', 'lightpink2': 'rgb(238,162,173)', 'lightpink3': 'rgb(205,140,149)', 'forestgreen': 'rgb(34,139,34)', 'lightpink4': 'rgb(139,95,101)', 'cornsilk4': 'rgb(139,136,120)', 'cornsilk2': 'rgb(238,232,205)', 'cornsilk3': 'rgb(205,200,177)', 'lightgoldenrod4': 'rgb(139,129,76)', 'grey90': 'rgb(229,229,229)', 'grey91': 'rgb(232,232,232)', 'grey92': 'rgb(235,235,235)', 'grey93': 'rgb(237,237,237)', 'grey94': 'rgb(240,240,240)', 'grey95': 'rgb(242,242,242)', 'grey96': 'rgb(245,245,245)', 'grey97': 'rgb(247,247,247)', 'grey98': 'rgb(250,250,250)', 'lightgoldenrod1': 'rgb(255,236,139)', 'royalblue3': 'rgb(58,95,205)', 'cadetblue': 'rgb(95,158,160)', 'royalblue2': 'rgb(67,110,238)', 'slateblue': 'rgb(106,90,205)', 'honeydew3': 'rgb(193,205,193)', 'dimgray': 'rgb(105,105,105)', 'seagreen': 'rgb(46,139,87)', 'cadetblue4': 'rgb(83,134,139)', 'cadetblue3': 'rgb(122,197,205)', 'cadetblue2': 'rgb(142,229,238)', 'cadetblue1': 'rgb(152,245,255)', 'paleturquoise': 'rgb(175,238,238)', 'deeppink3': 'rgb(205,16,118)', 'deeppink2': 'rgb(238,18,137)', 'deeppink1': 'rgb(255,20,147)', 'darkorchid': 'rgb(153,50,204)', 'hotpink3': 'rgb(205,96,144)', 'hotpink2': 'rgb(238,106,167)', 'hotpink1': 'rgb(255,110,180)', 'chocolate': 'rgb(210,105,30)', 'hotpink4': 'rgb(139,58,98)', 'honeydew2': 'rgb(224,238,224)', 'navyblue': 'rgb(0,0,128)', 'mediumaquamarine': 'rgb(102,205,170)'}
red,green,blue,cyan,magenta,yellow,black,white,gray,grey,brown,orange,maroon,lime,purple='red','green','blue','cyan','magenta','yellow','black','white','gray','grey','brown','orange','maroon','lime','purple'
Auto=auto=AUTO='auto'
def vcolorlegacy():
    '''a legacy routine that defines all colors as explicit variable names so that no quotation marks are used
    This is very cumbersome in debugging anything as a very large number of unused variables are added, mostly 
    of use for rescuing older scripts that used VSG at an early stage where colors were indeed their own variables'''
    for colorname in vhue.keys():
        globals()[colorname]=vhue[colorname]
FL1 = [] ## a list of all fonts available to the system.  This will be platform-specific
for font_path in ["","./vsgFonts","./vsgFonts/freefont","./vsgFonts/dejavu","./vsgFonts/dejavu/ttf","/Library/Fonts",
                  "/System/Library/Fonts","/System/Library/Fonts/Microsoft",os.path.expanduser("~/Library/Fonts"),
                  "/usr/X11R6/lib/X11/fonts/","/usr/share/fonts/","/usr/share/fonts/truetype/freefont/",
                  "~/.fonts","/usr/share/fonts/truetype/ttf-dejavu",
                  "/Library/Fonts","/Library/Fonts/Microsoft"]:
    if os.path.isdir(font_path):
        FL1.extend(
            [os.path.join(font_path, cur_font) 
             for cur_font in list(filter(lambda x:x.endswith('.ttf'),os.listdir(font_path)))
            ]
        )
FL2=sorted(FL1,key=lambda x:len(x.split('/')[-1]))  ## a sorted version of FL1
OpenFontsTTF1={}
OpenFontsTk={}
def commarize(w1):
    dquo=False
    squo=False
    mulspace=0
    w2=''
    for c1 in w1:
        if c1=='"':
            dquo=not(dquo)
        if c1=="'":
            squo=not(squo)
        if not(dquo or squo):
            if c1==' ':
                if mulspace>0:
                    continue
                else:
                    c1=','
                mulspace+=1
            else:
                mulspace=0
        w2+=c1
    return w2
        
def readexternalfile(epath1):
    U1=open(epath1,mode='rU')
    K1=U1.read()
    U1.close()
    K2=K1.split('!')
    for L1 in K2:
        L2=L1.split('<',1)
        if not(L2) or not(L2[0]):
            continue
        L3=L2[1].rfind('>')
        if L3<0:
            continue
        L4=L2[1][:L3].strip()
        canvas2=L2[0].strip()
        if not(canvas2 in globals()):
            exec(canvas2+'=VSGcanvas()')
        elif type(globals()[canvas2])!=VSGcanvas:
            canvas2+='___'
        L5=L4.split(' ',1)
        L5[1]=commarize(L5[1])
        try:
            exec(canvas2+'.'+L5[0]+'('+L5[1]+')')
        except:
            try:
                exec(canvas2+'.v'+L5[0]+'('+L5[1]+')')
            except:
                print('error with '+canvas2+'.v'+L5[0]+'('+L5[1]+')')

def num1(n1):
	# given a value of string or number type, tries to make a number out of the result.  
    if (type(n1)==(float)) or ('ecimal' in str(type(n1))):
        return float(n1)
    if type(n1) in  (int,long):
        return int(n1)
    if type(n1)==str:
        if n1.isdigit():
            return int(n1)
        if '.' in n1:
            try:
                return float(n1)
            except:
                pass
        try:
            return int(n1)
        except:
            pass
        try:
            return float(n1)
        except:
            pass
    return 'NAN'

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def font_ttf(f1):
    ## Returns a font file... f1 is a string with the font name plus the style (bold, oblique, italic, condensed)
    DefaultFont="DejaVuSans"

    ## first look for the really perfect match
    if f1 in FL1:
        return f1        

    ## next look for a match to all terms of the query
    L1=(f1+' .ttf').split(' ')
    for f2 in FL2:
        if all(l1.lower().replace('oblique','italic') in f2.lower().replace('oblique','italic') for l1 in L1):
            return f2

    ## okay, if there is no perfect match, give 'em Deja Vu font with the relevant features
    ## these should be in "./vsgFonts/dejavu/ttf"
    fontsublist=[['DejaVuSans','Arial','Helvetica','Verdana','Tahoma','Geneva','Trebuchet','FreeSans','Lucida','Gadget','sans'],
    ['DejaVuSerif','Georgia','Times','Palatino','FreeSerif','Antiqua','York','serif'],
    ['DejaVuSansMono','DejaVuMono','Courier','Lucida','Monaco','FreeMono','monospace','tty','mono']]
    f3=DefaultFont
    for ltype1 in fontsublist:
        for lta1 in ltype1:
            if lta1.lower() in f1.lower():
                f3=ltype1[0]
                break
        if f3!=DefaultFont:
            break
    f4=''
    if 'bold' in f1.lower():
        f4="Bold"
    if ('italic' in f1.lower()) or ('oblique' in f1.lower()):
        if "sans" in f3.lower():
            f4+='Oblique'
        if "serif" in f3.lower():
            f4+='Italic'
    if ('condensed' in f1.lower()) and ('mono' not in f3):
        f3+='Condensed'
    if f4:
        f3+='-'+f4
    f3+='.ttf'
    for f2 in FL1:
        if f3 in f2:
            return f2
    return DefaultFont

def fontbase(fb1):
	#given a font described as a string (e.g., "courier bold" or a ttf file (e.g. courierbold.ttf) returns the basic name of the font)
    fb2=fb1.split('/')[-1]
    fb2=fb2.replace('bold','').replace('Bold','').replace('Italic','').replace('italic','')
    fb2=fb2.replace('oblique','').replace('Oblique','').replace('Condensed','').replace('condensed','')
    fb2=fb2.replace('.ttf','').strip('-')
    return fb2.strip()
    
## Items that are always text
## textitems={'text','tag','label','popup','details','detail','mouseover','weblink'}
## mvg font options
mvgslant={'bold':'bold','roman':'normal','normal':'normal','italic':'italic','oblique':'oblique'}

##http://docs.huihoo.com/tkinter/tkinter-reference-a-gui-for-python/fonts.html
def rgb(r2,g2,b2):
    r3=str(int(round(float(r2))))
    g3=str(int(round(float(g2))))
    b3=str(int(round(float(b2))))
    return 'rgb('+','.join([r3,g3,b3])+')'
def rgbof(list1):
    """input list, output rgb or rgba string.  takes a variety of color description inputs and yields rgb output"""
    if len(list1)==3:
        return 'rgb('+str(list1[0])+','+str(list1[1])+','+str(list1[2])+')'
    if len(list1)==4:
        return 'rgba('+str(list1[0])+','+str(list1[1])+','+str(list1[2])+','+str(list1[3])+')'
def hexcolor(rgbs0):
    if rgbs0 in vhue:
        rgbs=vhue[rgbs0]
	# input is of the form "(rgb(x,y,z), output is in hexcolor format #rrggbb)"
    else:
        rgbs=rgbs0
    if rgbs==none or rgbs.lower()=='none':
        return ''
    if rgbs[0]=='#':
        return rgbs
    rgbss=str(rgbs).strip()
    if not(rgbss.startswith('rgb')):
        rgbss=vcolor(rgbs)
    hc= "#%02x%02x%02x" % tuple(list(map(int,rgbss.strip('rgb() \r\n\t').split(',')))[:3])
    return hc
def vcolor(sc0,**cod1):
	# input is almost any object, output is an 'rgb(r,g,b)' string.  Does it's best to guess
	# input of integers gives colors on a log scale 0-1088 (black to rainbow to white).  Input of floating numbers 0.0-1.0 gives a similar linear scale
    if sc0 in vhue:
        sc1=vhue[sc0]
    else:
        sc1=sc0
    typesc1=type(sc1)
    cvc=False
    if 'self1' in cod1:
        cvc=True
        cvc1=cod1['self1']
    nokey=False
    if 'nokey' in cod1 and cod1['nokey']==True:
        nokey=True
    if 'index1' in cod1 and cvc:
        cvc1.logcolorimax=max(float(cod1['index1']),cvc1.logcolorimax)
        cvc1.logcolorimin=min(float(cod1['index1']),cvc1.logcolorimin)
        cvc1.linearcolorimax=max(float(cod1['index1']),cvc1.logcolorimax)
        cvc1.linearcolorimin=min(float(cod1['index1']),cvc1.logcolorimin)
        
    ## cod1['self1'] is the canvas name, cod1['index1'] is the scalar value associated with the color being referenced
    if sc1==none or (type(sc1)==str and sc1.lower()=='none'):
        return ''
    primelist1=(3517,3581,3659,3733,3823,3911,4001,4073,4153,4241,4327,4421,4507,4591,4663,4759,4861,4943,5009,5099,5189,5281,5393,5449,5527,5641,5701,5801,5861,5953,6067,6143,6229,6311,6373,6481,6577,6679,6763,6841,6947,7001,7109,7211,7307,7417,7507,7573,7649,7727,7841,7927,8039,8117,8221,8293,8389,8513,8599,8681,8747,8837,8933,9013,9127,9203,9293,9391,9461,9539,9643,9739,9817,9901)
    global primelist
    global colordict1
    sc2=num1(sc1)
    if sc2=='NAN':
        sc1=str(sc1).lower().strip().replace(' ','')
        if sc1 in globals() and type(globals()[sc1])==str and globals()[sc1].strip().startswith('rgb'):
            return globals()[sc1].strip().replace(' ','')
        if sc1.startswith('rgb'):
            return sc1
        if sc1.startswith('#') and len(sc1)==4:
            try:
                return 'rgb('+str(int(sc1[1],16)*17)+','+str(int(sc1[2],16)*17)+','+str(int(sc1[3],16)*17)+')'
            except ValueError:
                pass
        if sc1.startswith('#') and len(sc1)==7:
            try:
                return 'rgb('+str(int(sc1[1:3],16))+','+str(int(sc1[3:5],16))+','+str(int(sc1[5:],16))+')'
            except ValueError:
                pass
        if ',' in sc1:
            try:
                s1=eval(sc1)
                if len(s1)==3:
                    return 'rgb('+str(s1[0])+','+str(s1[1])+','+str(s1[2])+')'
                if len(s1)==4:
                    return 'rgba('+str(s1[0])+','+str(s1[1])+','+str(s1[2])+','+str(s1[3])+')'
            except ValueError:
                pass
        if sc1 in colordict1:
            return colordict1[sc1]
        else:
            ind1=0
            colorindex1=1
            for c11 in sc1:
                colorindex1+=primelist1[ind1]*ord(c11)
                ind1=ind1+1
                if ind1>=len(primelist1): ind1=0
            colorindex1=colorindex1*988007
            heat1=[0,0,0]
            heat1[0]=colorindex1%256
            colorindex1=colorindex1/256
            heat1[1]=colorindex1%256
            colorindex1=colorindex1/256
            heat1[2]=colorindex1%256
            total1=heat1[0]+heat1[1]+heat1[2]
            if total1<64:
                if total1==-1:
                    total1=0
                mult1=256/(total1+1)
                heat1[0]=heat1[0]*mult1
                heat1[1]=heat1[1]*mult1
                heat1[2]=heat1[2]*mult1
            if total1>704:
                if total1==769:
                    total1=768
                mult1=256/(769-total1)
                heat1[0]=255-(255-heat1[0])*mult1
                heat1[1]=255-(255-heat1[1])*mult1
                heat1[2]=255-(255-heat1[2])*mult1
            colordict1[sc1]=rgbof([heat1[0],heat1[1],heat1[2]])
            return colordict1[sc1]
    sc1=sc2
    sc1=max(sc1,0)
    sc1=min(sc1,1088)
    if 'index1' in cod1:
        isc1=float(cod1['index1'])
    else:
        isc1=float(sc1)

    if typesc1==int:
        if cvc and not(nokey):
            cvc1.logcolormax=max(sc1,cvc1.logcolormax)
            cvc1.logcolormin=min(sc1,cvc1.logcolormin)
            cvc1.logcolorimax=max(isc1,cvc1.logcolorimax)
            cvc1.logcolorimin=min(isc1,cvc1.logcolorimin)
            cvc1.logcolor=True
        if sc1>-1.0:
            sc1=int(log(float(sc1+1),2)*100.0)
    else:
        if cvc and not(nokey):
            cvc1.linearcolormax=max(sc1,cvc1.linearcolormax)
            cvc1.linearcolormin=min(sc1,cvc1.linearcolormin)
            cvc1.linearcolorimax=max(isc1,cvc1.linearcolorimax)
            cvc1.linearcolorimin=min(isc1,cvc1.linearcolorimin)
            cvc1.linearcolor=True
        sc1=int(sc1*1088.0)
    sr=sc1 % 64
    if sc1<=0: return rgbof([0,0,0])
    if sc1<128:
        return rgbof([0,0,2*sc1])
    if sc1<192:
        return rgbof([0,2*sr,255])
    if sc1<256:
        return rgbof([0,sr+128,255])
    if sc1<320:
        return rgbof([0,sr+192,255])
    if sc1<384:
        return rgbof([0,255,255-sr])
    if sc1<448:
        return rgbof([0,255,191-sr])
    if sc1<512:
        return rgbof([0,255,127-2*sr])
    if sc1<576:
        return rgbof([2*sr,255,0])
    if sc1<640:
        return rgbof([sr+128,255,0])
    if sc1<704:
        return rgbof([sr+192,255,0])
    if sc1<768:
        return rgbof([255,255-sr,0])
    if sc1<832:
        return rgbof([255,191-sr,0])
    if sc1<896:
        return rgbof([255,127-2*sr,0])
    if sc1<960:
        return rgbof([255,0,2*sr])
    if sc1<1024:
        return rgbof([255,2*sr,128+sr])
    if sc1<1088:
        return rgbof([255,2*sr+128,192+sr])
    return rgbof([255,255,255])
        
def pointstr(v1):
    ## a function that takes any kind of list (intended to be point coordinants)
    ## as a python object and returns a simple comma-delimited string "x1,y1,x2,y2..."
    u1=''.join(filter(lambda x: x in 'eE-1234567890,.',str(v1)))
    return str(u1)

def pointarray(v1):
    ## a function that takes any kind of list (intended to be point coordinants)
    ## as a python object and returns a point array [[x1,y1],[x2,y2],...]

    u1=''.join(filter(lambda x: x in 'eE-1234567890,. ',str(v1)))
    u1=u1.strip(', \t')
    u1=u1.replace('\t',',')
    while ', ' in u1:
        u1=u1.replace(', ',',')        
    while ' ,' in u1:
        u1=u1.replace(' ,',',')
    while '  ' in u1:
        u1=u1.replace('  ',' ')
    u1=u1.replace(' ',',')
    u2=u1.split(',')
    u3=u2[::2]
    u4=u2[1::2]
    u5=[]
    for (u6,u7) in list(zip(u3,u4)):
        if '.' in u6:
            u8=float(u6)
        else:
            u8=int(u6)
        if '.' in u7:
            u9=float(u7)
        else:
            u9=int(u7)
        u5+=[[u8,u9]]
    return u5

def svgpointstr(v1):
    ## a function that takes a comma delimited list (text) or python list of xy values and returns a list 
    ## where different points are separated by space
    ## input "x1,y,x2,y2..." or [x1,y1,x2,y2,...] or ((x1,y1),(x2,y2)...), etc
    ## output "x1,y1 x2,y2..." for use in svg routines
    u1=''.join(filter(lambda x: x in 'eE-1234567890,.',str(v1)))
    u2=u1.split(',')
    u3=u2[::2]
    u4=u2[1::2]
    u5=''
    for (u6,u7) in list(zip(u3,u4)):
        u5+=u6+','+u7+' '
    return u5[:-1]

def find_names(obj):
    ## borrowed code to find the text name of an object (names if there are several) given the object
    ## so for a variable x1=33. find_names(x1)='x1'.  This code is set to find just the first occuring name of
    ## any object with multiple names
    try:
        frame = sys._getframe()
        for frame in iter(lambda: frame.f_back, None):
            frame.f_locals
        result = []
        for referrer in gc.get_referrers(obj):
            if isinstance(referrer, dict):
                if float(sys.version[:3])<3.0:
                    for k, v in referrer.iteritems():
                        if v is obj:
                            result=k
                else:
                    for k, v in list(referrer.items()):
                        if v is obj:
                            result=k                
        return result
    except:
        return ['object']

def griddiv(z1,z2,**dgrid1):
    '''input z1,z2; return a default set of grid settings between z1 and z2'''
    gprecise1=False
    for u in dgrid1:
        dgrid1[u.lower()]=dgrid1[u]
    if "precise" in dgrid1:
        gprecise1=bool(dgrid1['precise'])
    listg1=[]
    listg2=[]
    if z1==z2:
        if z1==0:
            zmin1=-1.0
            zmax1=1.0
        else:
            if gprecise1:
                zmin1=0.999999*z1
                zmax1=z1/0.999999
            else:
                zmin1=0.95*z1
                zmax1=z1/0.95
    else:
        zmina1=min(z1,z2)
        zmaxa1=max(z1,z2)
        if gprecise1:
            zmin1=zmina1-0.000001*(zmaxa1-zmina1)
            zmax1=zmaxa1+0.000001*(zmaxa1-zmina1)
        else:
            zmin1=zmina1-0.05*(zmaxa1-zmina1)
            zmax1=zmaxa1+0.05*(zmaxa1-zmina1)
    zd1=zmax1-zmin1
    if zd1<=0:
        zd1=0.1  ## safe harbor
    zd1L=log10(zd1)
    zd1Li=int(floor(zd1L))
    zd1Lf=pow(10,zd1L-zd1Li)
    zd5=float(zd1)/5.0
    zd5L=log10(zd5)
    zd5Li=int(floor(zd5L))
    zd5Lf=pow(10,zd5L-zd5Li)
    if 1<=zd5Lf<=2:
        base1=pow(10,zd5Li)
        base2=float(base1)/5.0
    elif 2<zd5Lf<=5:
        base1=2*pow(10,zd5Li)
        base2=float(base1)/2.0
    else:
        base1=5*pow(10,zd5Li)
        base2=float(base1)/5.0
    if base1==0.0:
        base1=0.1
    curnum=floor(zmin1/base1)*base1+base1
    while curnum<=zmax1:
        listg1.append(curnum)
        if len(listg1)>1 and abs(listg1[-1])>10000000*abs(listg1[-2]):
            listg1[-2]=0.0
        if len(listg1)>1 and abs(listg1[-2])>10000000*abs(listg1[-1]):
            listg1[-1]=0.0
        curnum+=base1
    if base2==0.0:
        base2=0.1
    curnum2=floor(zmin1/base2)*base2+base2
    while curnum2<=zmax1:  
        listg2.append(curnum2)
        if len(listg2)>1 and abs(listg2[-1])>10000000*abs(listg2[-2]):
            listg2[-2]=0.0
        if len(listg2)>1 and abs(listg2[-2])>10000000*abs(listg2[-1]):
            listg2[-1]=0.0
        curnum2+=base2            
    return [(zmin1,zmax1),base1,listg1,listg2]

def griddivlinear(glist,clist,**dgrid1):
	# input a list of experimental values (measurements) [glist] and a set of corresponding canvas values [clist]
	# output is a series of rational markings for relevant axes.  This is for linear graphs
	# input format ([first_observation,second_observation...],[first canvas value, second canvas value...])
	# output format is a tuple as follows 
	# 0: (zmin1,zmax1)- The range of values recommended for the full graph
	# 1: base1- the interval between major markings on the axis
	# 2: listg1- list of major demarkations (labels in string format)
	# 3: listc1- list of positions for each major demarkation
	# 4: base2- list of minor demarkations
	# 5: listg2[1:-1]: list of minor demarkations (lables in string format),
	# 6: listc2[1:-1]]: list of minor demarkations in string format

    gprecise1=False
    for u in dgrid1:
        dgrid1[u.lower()]=dgrid1[u]
    if "precise" in dgrid1:
        gprecise1=bool(dgrid1['precise'])
	
    if glist==[]:glist=[0]
    if clist==[]:clist=[0]
    z1=min(glist)
    z2=max(glist)
    z1c=min(clist)
    z2c=max(clist)
    
    listg1=[]  ##major gridline indices
    listg2=[]  ##minor gridline indices
    if z1==z2:
        if z1==0:
            zmin1=-1.0
            zmax1=1.0
        else:
            if gprecise1:
                zmin1=0.999999*z1
                zmax1=z1/0.999999
            else:
                zmin1=0.95*z1
                zmax1=z1/0.95
    else:
        zmina1=min(z1,z2)
        zmaxa1=max(z1,z2)
        if gprecise1:
            zmin1=zmina1-0.000001*(zmaxa1-zmina1)
            zmax1=zmaxa1+0.000001*(zmaxa1-zmina1)
        else:
            zmin1=zmina1-0.05*(zmaxa1-zmina1)
            zmax1=zmaxa1+0.05*(zmaxa1-zmina1)
    zd1=zmax1-zmin1
    if zd1<=0:
        zd1=0.1
    zd1L=log10(zd1)
    zd1Li=int(floor(zd1L))
    zd1Lf=pow(10,zd1L-zd1Li)
    zd5=float(zd1)/5.0
    zd5L=log10(zd5)
    zd5Li=int(floor(zd5L))
    zd5Lf=pow(10,zd5L-zd5Li)
    if 1<=zd5Lf<=2:
        base1=pow(10,zd5Li)
        if base1>0:
            base2=base1/5
        else:
            base2=float(base1)/5.0
    elif 2<zd5Lf<=5:
        base1=2*pow(10,zd5Li)
        if base1>0:
            base2=base1/2
        else:
            base2=float(base1)/2.0
    else:
        base1=5*pow(10,zd5Li)
        if base1>0:
            base2=base1/5
        else:
            base2=float(base1)/5.0
    if base1==0.0:
        base1=0.1
    curnum=floor(zmin1/base1)*base1+base1
    while curnum<=zmax1:
        listg1.append(curnum)
        if len(listg1)>1 and abs(listg1[-1])>10000000*abs(listg1[-2]):
            listg1[-2]=0.0
        if len(listg1)>1 and abs(listg1[-2])>10000000*abs(listg1[-1]):
            listg1[-1]=0.0
        curnum+=base1
    listc1=[]  #major gridline coordinants
    if z1==z2:
        for e1 in listg1:
            listc1.append(copy(z1c))
    else:
        for e1 in listg1:
            listc1.append(z1c+(z2c-z1c)*(e1-z1)/(z2-z1))
    if base2==0.0:
        base2=0.1
    curnum=floor(zmin1/base2)*base2+base2
    while curnum<=zmax1:
        listg2.append(curnum)
        if len(listg2)>1 and abs(listg2[-1])>10000000*abs(listg2[-2]):
            listg2[-2]=0.0
        if len(listg2)>1 and abs(listg2[-2])>10000000*abs(listg2[-1]):
            listg2[-1]=0.0
        curnum+=base2
    listc2=[] #minor gridline coordinants
    if z1==z2:
        for e1 in listg2:
            listc2.append(copy(z1c))
    else:
        for e1 in listg2:
            listc2.append(z1c+(z2c-z1c)*(e1-z1)/(z2-z1))
        
    return [(zmin1,zmax1),base1,listg1,listc1,base2,listg2[1:-1],listc2[1:-1]]

def griddivlog(glist,clist,logbase,**dgrid1):

	# input a list of experimental values (measurements) [glist] and a set of corresponding canvas values [clist]
	# output is a series of rational markings for relevant axes.  This is for linear graphs
	# input format ([first_observation,second_observation...],[first canvas value, second canvas value...])
	# output format is a tuple as follows 
	# 0: (zmin1,zmax1)- The range of values recommended for the full graph
	# 1: <1> <not relevant for log axes>
	# 2: listg1- list of major demarkations (labels in string format)
	# 3: listc1- list of positions for each major demarkation
	# 4: <1> <not relevant for log axes>
	# 5: listg2[1:-1]: list of minor demarkations (lables in string format),
	# 6: listc2[1:-1]]: list of minor demarkations in string format
    gprecise1=False
    for u in dgrid1:
        dgrid1[u.lower()]=dgrid1[u]
    if "precise" in dgrid1:
        gprecise1=bool(dgrid1['precise'])
	
    z1=min(glist)
    z2=max(glist)
    z1c=min(clist)
    z2c=max(clist)
    if z1<=0:
        z1=0.1
    if z2<=0:
        z2=0.1
    if gprecise1:
        floorlog=int(ceil(0.99999*log(z1,logbase)))
        ceillog=int(floor(1.00001*log(z2,logbase)))
    else:
        floorlog=int(ceil(0.99*log(z1,logbase)))
        ceillog=int(floor(1.01*log(z2,logbase)))
    listg1=[]
    for fnde in range(floorlog,ceillog+1):
        listg1.append(pow(logbase,fnde))
    listc1=[]
##    listc2=[]  ## 06/07 Remove this line
    for e1 in listg1:
        if e1<=0:
            e1=0.1
        zlog01=log((float(z2)/float(z1)),logbase)
        if zlog01==0.0:
            zlog01=1.0
        listc1.append(z1c+(z2c-z1c)*log(float(e1)/float(z1),logbase)/zlog01)
    return [(z1c-0.01*(z2c-z1c),z2c+0.01*(z2c-z1c)),1,listg1,listc1,1,listg1,listc1]

htmle1 = {"&": "&amp;",'"': "&quot;","'": "&apos;",">": "&gt;","<": "&lt;"}
def htmle(text):
    return "".join(htmle1.get(c,c) for c in text)

class VSGcanvas(list):
    """Each VSG canvas is a list of items denoting objects and metadata that describe a 2D drawing"""
                
    def __init__(self,**d3):
        """initialize a new VSG object,
            optionally with significant state parameters)"""
        ## first clear out any previous info
        for uu1 in dir(self):
            try:
                delattr(self,uu1)
            except:
                pass
        del self[:]
        ## overall appearance variables
        self.drawtop=True ## draw items on top of the current drawing (drawtop=False is to draw below current drawing)
        self.priority=0 ## priority of this object (higher numbers=higher priority and will be drawn last)
        self.negordinal=0  ## ordinal number of item in list of objects, for objects to be drawn "first"
        self.posordinal=0  ## ordinal number of item in list of objects, for objects to be drawn "last" (ie on top)
        self.bg=hexcolor('gray60')   ## background color
        self.screenwidth=1024  ## Maximum width for display of output in browser (svg or html) or iPython Notebook 
        self.bd=2.0     ## tk canvas border
        self.takefocus=True ## allows  tk canvas to pick up tab focus
        self.curx=0.0    ## current focal point-x (upper left x of next object if not specified)
        self.cury=0.0    ## current focal point-y (upper left y of next object if not specified)
        self.curwidth=20.0    ##  (width of next object if not specified)
        self.curheight=20.0    ##  (height of next object if not specified)
        self.xd=25.0    ##  (x offset next object if not specified)
        self.yd=25.0    ##  (y offset of next object if not specified)
        self.xmax=25.0  ## right extreme of drawing (doesn't include margin) 
        self.xmin=0.0  ## left extreme of drawing (doesn't include margin)
        self.ymax=25.0  ## bottom extreme of drawing (doesn't include margin)
        self.ymin=0.0  ## top extreme of drawing (doesn't include margin)

        self.xlabels=[] ## a string listing items along the x axis.  Format "item1-1,item1-2,item1-3,item1-4;item2-1,item2-2,item2-3...", commas separate items of a like type, semicolons of different type 
        self.ylabels=[] ## a string listing items along the x grid.  Format "item1-1,item1-2,item1-3,item1-4;item2-1,item2-2,item2-3..."

        self.x1=0.0  ##last specified x1
        self.y1=0.0  ##last specified y1
        self.x2=0.0  ##last specified x2
        self.y2=0.0  ##last specified y2
        self.xc=0.0  ##last specified xc
        self.yc=0.0  ##last specified yc
        self.x1static=True # all x1 values are the same
        self.x2static=True # all x2 values are the same
        self.y1static=True # all y1 values are the same
        self.y2static=True # all y2 values are the same
        self.xdom='xc' ## dominant x anchor (center for default, also can be x1 or x2)
        self.ydom='yc' ## dominant x anchor (center for default, also can be x1 or x2)
        self.xcr=10.0  ## center of rotation, (dominant Anchor): X
        self.ycr=10.0  ## center of rotation, (dominant Anchor): Y

        self.autogrow=True ## autogrow the drawing as items are added, setting this to false means that everything will be cropped to set size
        self.autogrowh=True ## autogrow the drawing as items are added, setting this to false means that everything will be cropped to set size
        self.autogrowv=True ## autogrow the drawing as items are added, setting this to false means that everything will be cropped to set size

        self.scale="Auto"  ## number of pixels for each unit of the coordinant system (floating) "Auto" gives an automatic scaling depending on the nature of the canvas to be rendered (1.0 for vector, 3.0 for raster)
        self.fontscale='Auto' ## 'Auto' means that each character is scaled by self.scale (so 12 point font with a scale of 2.0 becomes 24 point)
                              ##, 1.0 for the font size to be used verbatim in canvas space (so 12 point font is 12 point no matter what the scale
                              ## r0.01 relative size (to canvas) r0.01 is a point size designed for 100 characters per line
        self.strokescale='Auto' ## 'Auto' means that each character is scaled by self.scale (so 2 point stroke with a scale of 2.0 becomes 4 point)
                              ##, 1.0 for the stroke width to be used verbatim in canvas space (so 2 point font is 2 point no matter what the scale
                              ## r0.01 relative size (to canvas) r0.01 is a point size designed for 100th of width+height
        
        ## margin variables -- how much of a margin around the drawing
        self.margint=10.0  ## top margin
        self.marginb=10.0  ## bottom margin
        self.marginl=10.0  ## left margin
        self.marginr=10.0  ## right margin
        self.marginh=10.0  ## horizontal margins
        self.marginv=10.0  ## vertical margins
        self.margin=10.0   ## all-side margins

        ## arc variables...  All angle positions are referred to as a fraction of the whole (so 0.25 is 90 degrees)
        self.a0=0.0     ## starting position for arc 
        self.cura=0.0   
        self.ad=0.25    ### total aperature for arc (
        self.arcscale=1.0 ## 1.0 means the entire circle is 1.0 unit, 2*pi for radians, 360.0 for degrees
        
        ## text variables
        self.font={'family':'Arial','size':14,'weight':'bold','underline':False,'overstrike':False,'slant':'roman'} ## the current default font
        self.fontcolor="black"    ## a default font color, mostly for vcolor and vgrid annotation
        self.underline=-1        ## point of underlining-- if the font is not set to 'underline',
                                 ##then there is a chance to underlining a single character (0 being the first character)
                                 ## no single-character underline=-1
        self.hjust='start'        ## text horizontal anchoring point "start", "middle", or "end"
        self.vjust='center'       ## text vertical anchoring point "top", "center", or "bottom"
                                  ## note that these are usually set by the way a point is specified

        self.points=[[10.0,10.0],[10.0,20.0],[20.0,20.0],[20.0,10.0],[10.0,10.0]]
        
        ## label variables
        self.labelfont='auto'  ## font used to label any object that has a 'label' in the specification
        self.labeljust='NE'           ## position of label relative to object
        self.labelcolor='auto'      ## color of label text
        
        ## current drawing defaults
        self.rotate=0.0    ## rotation in degrees (float).  0.0 for no rotation
        self.strokewidth=1.0  ## width of strokes.  Note that for image modes (e.g. tiff) polygon lines are always 1.0pt
        self.stroke='black'    ## current color of strokes
        self.strokeopacity=1.0 ## opacity of strokes (0.0-1.0) not all output systems handle this
        self.fill='white'     ## object fill
        self.fillopacity=1.0  ## not all output systems handle opacity 

        ## display defaults
        self.livetk=False   ## update canvas after each object is added... not implemented, use TKdisplay after items are defined
        self.tkdisplaylist=[] ## list of all items already displayed
        self.popups=False  ## Is there text to popup on click?
        self.xlinks=False  ## Is there text to popup on shift-click
        self.details=False ## Is there text to popup on control-click
        self.mouseovers=False ## Is there text to display on mouse-over

        ## justification for connection lines (if connecting a set of objects, which point to use for connection)
        self.cjust='c'

        ## default method (metric) for predicting the width and height of text strings in placing objects
        self.metric='pil'  ## 'pil' defaults to python imaging library, 'tk' to the tk library.
                           ## Each has "their moments", switching to self.metric('tk') with vset(metric='tk') may fix some rendering artefacts, will use whichever is available if neither is 

        ## whether a tkframe has been set up for a canvas
        self.tkframed=False
        
        ## a dictionary of color names (as keys) and their corresponding colors
        self.colorlist=[]
        self.logcolormax=1
        self.logcolormin=1088
        self.logcolorimax=0.0000000000000001
        self.logcolorimin=999999999999
        self.logcolor=False
        self.linearcolormax=0
        self.linearcolormin=1.0
        self.linearcolorimax=-999999999999
        self.linearcolorimin=+999999999999
        self.linearcolor=False

        ## now handle the definitions of parameters handed at initialization
        d4={}
        for c1 in d3:
            d4[c1.lower()]=d3[c1]

            if c1.lower()=='font':
                FD1=self.splitfont(d4['font'])
                del d4[c1]
                if not('family' in FD1):
                    FD1['family']=self.font['family']
                if not('size' in FD1):
                    FD1['size']=self.font['size']
                d4['font']=deepcopy(FD1)
                self.font=d4['font']

            d4c1=num1(d4[c1])
            if d4c1!='NAN':
                d4[c1]=float(d4[c1])
            setattr(self,c1.lower(),d4[c1])
            
        if 'margin' in d4:
            self.margint=self.margin 
            self.marginb=self.margin 
            self.marginl=self.margin 
            self.marginr=self.margin 
            self.marginh=self.margin 
            self.marginv=self.margin            
        if 'marginh' in d4:
            self.marginl=self.marginh 
            self.marginr=self.marginh 
        if 'marginv' in d4:
            self.margint=self.marginv 
            self.marginb=self.marginv
        if self.autogrow:
            self.autogrowv=True
            self.autogrowh=True

## need to open a tk window here to get proper text string sizes
    
        

    def transform(self,**dt1):
        'xd=<int>, yd=<int>, return copy of canvas translated xd,yd in x and y dimensions, while xs and ys can be used to scale in x and y dimensions'
        transformedcopy=deepcopy(self)
        xdel1=0
        if 'xd' in dt1:
            xdel1=float(dt1['xd'])
        ydel1=0
        if 'yd' in dt1:
            ydel1=float(dt1['yd'])
        xsc1=1.0
        if 'xs' in dt1:
            xsc1=float(dt1['xs'])
        ysc1=1.0
        if 'ys' in dt1:
            ysc1=float(dt1['ys'])
        il1='xcr,ycr,x1,y1,x2,y2,xc,yc,xmin,xmax,ymin,ymax,curx,cury'.split(',')
        for v1 in il1:
            if v1 in dir(transformedcopy):
                if v1[0]=='x' or v1[-1]=='x':
                    del1=xdel1
                    sc1=xsc1
                else:
                    del1=ydel1
                    sc1=ysc1
                setattr(transformedcopy,v1,sc1*getattr(transformedcopy,v1)+del1)
        if 'width' in dir(transformedcopy):
            transformedcopy.width*=xsc1
        if 'xr' in dir(transformedcopy):
            transformedcopy.xr*=xsc1
        if 'height' in dir(transformedcopy):
            transformedcopy.height*=ysc1
        if 'yr' in dir(transformedcopy):
            transformedcopy.yr*=ysc1
        if 'points' in dir(transformedcopy):
            pnew1=[]
            for p0 in transformedcopy.points:
                pnew1.append((xsc1*p0[0]+xdel1,ysc1*p0[1]+ydel1))
            transformedcopy.points=pnew1
        for s in transformedcopy:
            for v1 in il1:
                if v1 in dir(s):
                    if v1[0]=='x' or v1[-1]=='x':
                        del1=xdel1
                        sc1=xsc1
                    else:
                        del1=ydel1
                        sc1=ysc1
                    setattr(s,v1,sc1*getattr(s,v1)+del1)
            if 'points' in dir(s):
                pnew1=[]
                for p0 in s.points:
                    pnew1.append((xsc1*p0[0]+xdel1,ysc1*p0[1]+ydel1))
                s.points=pnew1
            if 'width' in dir(s):
                s.width*=xsc1
            if 'xr' in dir(s):
                s.xr*=xsc1
            if 'height' in dir(s):
                s.height*=ysc1
            if 'yr' in dir(transformedcopy):
                s.yr*=ysc1
        return transformedcopy

    def __add__(self,other):
    ## overlay a second canvas in place (first canvas is placed first...
        overlay=deepcopy(self)
        overlay+=other
        overlay.xmin=min(self.xmin,other.xmin)
        overlay.xmax=max(self.xmax,other.xmax)
        overlay.ymin=min(self.ymin,other.ymin)
        overlay.ymax=max(self.ymax,other.ymax)
        overlay.popups=self.popups or other.popups
        overlay.details=self.details or other.details
        overlay.mouseovers=self.mouseovers or other.mouseovers
        overlay.xlinks=self.xlinks or other.xlinks
        overlay.colorlist+=[ncl1 for ncl1 in other.colorlist if not(ncl1 in self.colorlist)] 
        overlay.linearcolormax=max(self.linearcolormax,other.linearcolormax)
        overlay.linearcolormin=min(self.linearcolormin,other.linearcolormin)
        overlay.linearcolorimax=max(self.linearcolorimax,other.linearcolorimax)
        overlay.linearcolorimin=min(self.linearcolorimin,other.linearcolorimin)
        overlay.linearcolor=self.linearcolor or other.linearcolor
        overlay.logcolormax=max(self.logcolormax,other.logcolormax)
        overlay.logcolormin=min(self.logcolormin,other.logcolormin)
        overlay.logcolorimax=max(self.logcolorimax,other.logcolorimax)
        overlay.logcolorimin=min(self.logcolorimin,other.logcolorimin)
        overlay.logcolor=self.logcolor or other.logcolor

        return overlay
        
    def __deepcopy__(self,memo):
        selfcopy=VSGcanvas()
        for s in self:
            del s.canvas
            selfcopy.append(deepcopy(s))
            s.canvas=self
            selfcopy[-1].canvas=selfcopy
        for si in list(self.__dict__.keys()):
            if type(getattr(self,si))==list:
                setattr(selfcopy,si,deepcopy(getattr(self,si)))
            else:
                setattr(selfcopy,si,copy(getattr(self,si)))
        return selfcopy
            
    def vinfo(self,*dz0,**dz2):
        """delimiter=<default '\n'>, lines=<default =0, all lines>.  vinfo provides some basic info on the canvas as it is made""" 
        if not "delimiter" in dz2:
            delimiter='|'
        else:
            delimiter=dz2['delimiter']
        if not "lines" in dz2:
            dz2['lines']=0
        vinfo1='VSG_Canvas_Info'
        vname1=str(find_names(self)).strip()
        if vname1!='canvas':
            vinfo1+='| Canvas_Name='+vname1+' '+delimiter
        vinfo1+='  Run_Time='+str(asctime())+' '
        if dz2['lines']==1: return vinfo1
        if sys.argv and sys.argv[0]!='-c':
            try:
                vinfo1+=delimiter+'  Script='+os.path.basename(sys.argv[0])+' | Ver='+str(modification_date(sys.argv[0]))+' | Dir='+os.path.dirname(sys.argv[0])+' '
            except:
                pass
        if dz2['lines']==2: return vinfo1
        allvar=set(globals().keys()+locals().keys())
        if1=0
        for vari1 in allvar:
            if vari1 in globals():
                if type(globals()[vari1])==file:
                    if1+=1
                    NN1=globals()[vari1]
                    vinfo1+=delimiter+'  Opened_File_'+str(if1)+': '+vari1+"='"+NN1.name+"' | Mode='"+NN1.mode +"' | ModStamp="+str(modification_date(NN1.name))+' '+delimiter
            elif vari1 in locals():
                if type(locals()[vari1])==file:
                    if1+=1
                    NN1=locals()[vari1]
                    vinfo1+=delimiter+'  Opened_File_'+str(if1)+': '+vari1+"='"+NN1.name+"' | Mode='"+NN1.mode +"' | ModStamp="+str(modification_date(NN1.name))+' '+delimiter
        return vinfo1[:-len(delimiter)-1]
    
    def windowcalc(self,*dz0,**dw1):
        ''' scale= this is a workhorse routine that defines values for the whole canvas.  The main paramater that might 
	be passed to this is "scale", which is the scale of the eventual drawing (recommended as ~3.0 for line drawings and 1.0 for vector)'''
        sc=copy(self.scale)
        self.cvxminfs=9999999
        if 'scale' in dw1:
            sc=float(dw1['scale'])
        if 'Scale' in dw1:
            sc=float(dw1['Scale'])
        if sc in ("auto","Auto"):
            sc=1.0
        self.cvwidth=sc*(self.xmax-self.xmin+self.marginl+self.marginr)
        self.cvheight=sc*(self.ymax-self.ymin+self.margint+self.marginb)
        self.cvxd=self.marginl-self.xmin
        self.cvyd=self.marginb-self.ymin
        for s in self:
            ## canvas x and y values
            s.cvx1=(s.x1+self.cvxd)*sc
            s.cvx2=(s.x2+self.cvxd)*sc
            s.cvwidth=s.cvx2-s.cvx1
            s.cvy1=self.cvheight-(s.y1+self.cvyd)*sc
            s.cvy2=self.cvheight-(s.y2+self.cvyd)*sc
            s.cvheight=s.cvy2-s.cvy1
            s.cvxc=(s.xc+self.cvxd)*sc
            s.cvyc=self.cvheight-(s.yc+self.cvyd)*sc
            s.cvmx1=min(s.cvx1,s.cvx2)
            s.cvmx2=max(s.cvx1,s.cvx2)
            s.cvmy1=min(s.cvy1,s.cvy2)
            s.cvmy2=max(s.cvy1,s.cvy2)
            ## canvas radius values
            s.cvxr=(s.xr)*sc
            s.cvyr=(s.yr)*sc
            ## canvas center of rotation values
            s.cvxcr=(s.xcr+self.cvxd)*sc
            s.cvycr=self.cvheight-(s.ycr+self.cvyd)*sc
            ## distances from gravity centers (MVG sets a gravity center at NW,NE, SE, N, C etc and
            ## uses this as a default center of rotation,
            s.cvgcx=s.cvxc-self.cvwidth/2.0
            if s.hjust=='start': s.cvgcx=s.cvx1
            if s.hjust=='end': s.cvgcx=self.cvwidth-s.cvx2
            s.cvgcy=s.cvyc-self.cvheight/2.0
            if s.vjust=='top': s.cvgcy-=s.cvyr/2.0
            if s.vjust=='bottom': s.cvgcy+=s.cvyr/2.0
            ## calculate font size to display
            if s.obj=='text':
                if type(self.fontscale)==str:
                    if self.fontscale.lower()=='auto':
                        s.cvfs=int(float(s.font['size'])*sc)
                    if self.fontscale[0]=='r':
                        s.cvfs=int(float(s.font['size']*float(self.fontscale[1:])*self.cvwidth))
                else:
                    s.cvfs=int(float(s.font['size'])*self.fontscale)
                if 'nonrotwidth' in dir(s) and s.nonrotwidth>0:
                    ## nonrotwidth allows the user to make sure a set of long tags fit into a specified width (nonrotwidth), scaling the related font so each fits and uses the same font
                    s.cvnonrotwidth=s.nonrotwidth*sc
                    if float(s.cvwidth)==0.0:
                        s.cvwidth=1.0
                    self.cvxminfs=int(min(self.cvxminfs,s.cvfs,float(s.cvnonrotwidth)*float(s.cvfs)/float(s.cvwidth)))
                    s.cvfs=self.cvxminfs
            if type(self.strokescale)==str:
                if self.strokescale.lower()=='auto':
                    s.cvstrokewidth=float(s.strokewidth)*sc
                if self.strokescale[0]=='r':
                    s.cvstrokewidth=float(float(self.strokescale[1:])*self.cvwidth*s.strokewidth)
            else:
                s.cvstrokewidth=float(s.strokewidth)*self.strokescale
            if s.strokewidth>0:
                s.cvistrokewidth=max(1,int(round(s.cvstrokewidth)))
            else:
                s.cvistrokewidth=0
            if s.fill:
                s.cvfill=copy(s.fill)
            else:
                s.cvfill=self.bg
            if s.strokewidth>0:
                s.cvstroke=copy(s.stroke)
            else:
                s.cvstroke=hexcolor(s.canvas.fontcolor)
            if s.obj in ('polygon','polyline'):
                s.cvpoints=[]
                for (xa1,ya1) in s.points:
                    s.cvpoints.append([(xa1+self.cvxd)*sc,self.cvheight-(ya1+self.cvyd)*sc])
                s.cvipoints=[]
                for (xa1,ya1) in s.points:
                    s.cvipoints.append((int((xa1+self.cvxd)*sc),int(self.cvheight-(ya1+self.cvyd)*sc)))
            if s.obj =='polyline':
                s.tkpoints=[]
                s.fill=none
                for (xa1,ya1) in s.points:
                    s.tkpoints.append([(xa1+self.cvxd)*sc,self.cvheight-(ya1+self.cvyd)*sc])
                for (xa1,ya1) in s.points[::-1]:
                    s.tkpoints.append([(xa1+self.cvxd)*sc,self.cvheight-(ya1+self.cvyd)*sc])
            if s.obj == 'arc':
                if self.arcscale==0.0:
                    self.arcscale=0.1
                s.cvx3=s.cvxc+s.cvxr*sin(pi-s.a0*2*pi/self.arcscale)
                s.cvx4=s.cvxc+s.cvxr*sin(pi-(s.a0+s.ad)*2*pi/self.arcscale)
                s.cvy3=s.cvyc+s.cvyr*cos(pi-s.a0*2*pi/self.arcscale)
                s.cvy4=s.cvyc+s.cvyr*cos(pi-(s.a0+s.ad)*2*pi/self.arcscale)
                if s.ad/self.arcscale<0.5:
                    s.arcpath='"M '+svnum(s.cvxc)[1:-1]+','+svnum(s.cvyc)[1:-1]+' L'+svnum(s.cvx3)[1:-1]+','+svnum(s.cvy3)[1:-1]+' A'+svnum(s.cvxr)[1:-1]+','+svnum(s.cvyr)[1:-1]+' 0,0,1 '+svnum(s.cvx4)[1:-1]+','+svnum(s.cvy4)[1:-1]+' L '+svnum(s.cvxc)[1:-1]+','+svnum(s.cvyc)[1:-1]+'"'       
                else:
                    s.arcpath='"M '+svnum(s.cvxc)[1:-1]+','+svnum(s.cvyc)[1:-1]+' L'+svnum(s.cvx3)[1:-1]+','+svnum(s.cvy3)[1:-1]+' A'+svnum(s.cvxr)[1:-1]+','+svnum(s.cvyr)[1:-1]+' 0,1,1 '+svnum(s.cvx4)[1:-1]+','+svnum(s.cvy4)[1:-1]+' L '+svnum(s.cvxc)[1:-1]+','+svnum(s.cvyc)[1:-1]+'"'       

    def TKwrite(self,filepath='temp.ps',display=True):
        '''filepath=<path.ps>, display=True/False
            Render the image as a TK canvas with active links
            Then
               1.  Display the canvas (if "display=True" in call)
               2.  Write the image to a postscript file ( "filepath=<filepath> in call)'''
        if not(tkimported1):
            print('Error: TK not available or import failed-- attempting alternative render')
            raise Exception('NoTK')
        else:
            if not(self.tkframed):
                self.tkwindow=tk.Tk()
                self.tkframe=tk.Frame(self.tkwindow)

        if self.scale in ('auto','Auto'):
            self.windowcalc(scale=1.0)
        else:
            self.windowcalc()
        def tkmouseover(event):
            tkevent=event.widget.find_closest(event.x, event.y)[0]
            tkcanvas=event.widget
            if not (tkcanvas,tkevent) in msgdict1: return 'error'
            self.mouseoverlist.insert('end',msgdict1[(tkcanvas,tkevent)]+'\n')
            self.mouseoverlist.yview_pickplace("end")
        def tkweblink(event):
            tkevent=event.widget.find_closest(event.x, event.y)[0]
            tkcanvas=event.widget
            if not (tkcanvas,tkevent) in sitedict1: return ''
            if type(sitedict1[(tkcanvas,tkevent)])=='function':
                return sitedict1[(tkcanvas,tkevent)]
            else:
                try:
                    webbrowser.open_new(sitedict1[(tkcanvas,tkevent)])
                except:
                    pass
            self.xlinklist.insert('end',sitedict1[(tkcanvas,tkevent)]+'\n')
            self.xlinklist.yview_pickplace("end")
        def tkpopup(event):
            tkevent=event.widget.find_closest(event.x, event.y)[0]
            tkcanvas=event.widget
            if not (tkcanvas,tkevent) in popupdict1: return ''
            self.popuplist.insert('end',popupdict1[(tkcanvas,tkevent)]+'\n')
            self.popuplist.yview_pickplace("end")
        def tkdetail(event):
            tkevent=event.widget.find_closest(event.x, event.y)[0]
            tkcanvas=event.widget
            if not (tkcanvas,tkevent) in detaildict1: return ''
            self.detaillist.insert('end',detaildict1[(tkcanvas,tkevent)]+'\n')
            self.detaillist.yview_pickplace("end")
        self.textboxes=sum(list(map(int,(self.popups,self.xlinks,self.mouseovers,self.details))))
        self.columnspan=1
        if self.textboxes>1:
            self.columnspan=self.textboxes
        self.tkframe.grid()
        self.tkwindow.title(str(find_names(self)))
        self.cv=tk.Canvas(self.tkframe,width=self.cvwidth,height=self.cvheight,bg=hexcolor(self.bg),bd=self.bd,takefocus=self.takefocus)
            ## the background rectangle is needed to get an accurate background on a postscript save, but
            ## also causes trouble with mouseactions on the live canvas.  This is a compromise that puts the background
            ## rectangle in only if there are no mouse actions specified.
            ## ideally run the whole tk drawing routine over (with a base rectangle) for a postscript save so that a background can be put in
        if self.textboxes==0: self.cv.create_rectangle([0,0,self.cvwidth,self.cvheight],fill=hexcolor(self.bg))
        self.cv.grid(row=0,column=0,columnspan=self.columnspan)
        self.tkcolumns=1
        self.tkobj=[]
        self.xminfont=99999999
        for s in self:
            if s.obj=='text':
                s.cvfont['size']=copy(s.cvfs)
                tempsize=copy(s.cvfont['size'])
                tkjustT=copy(s.tkjust)
                hjustT=copy(s.hjust)
                cvfs1=str(s.cvfont)
                if not(cvfs1) in OpenFontsTk:
                    OpenFontsTk[cvfs1]=tkFont.Font(**s.cvfont)
                s.cvtkfont=OpenFontsTk[cvfs1]
                s.tkobj=self.cv.create_text([s.cvxcr,s.cvycr],fill=hexcolor(s.fill),##underline=s.underline, Underline not implemented on mac TK as of 03/11s
                    text=s.text,font=s.cvtkfont,justify=tkjustT,anchor=anchordict[(hjustT,s.vjust)])  ##,angle=s.rotate) not implemented until Tk8.6
                s.cvfont['size']=copy(tempsize)
            if s.obj=='line':
                s.tkobj=self.cv.create_line([s.cvx1,s.cvy1,s.cvx2,s.cvy2],fill=hexcolor(s.stroke),width=s.cvstrokewidth)
            if s.obj =='polyline':
                s.tkobj=self.cv.create_polygon(s.tkpoints,outline=hexcolor(s.stroke),width=s.cvstrokewidth)
            if s.obj=='polygon':
                s.tkobj=self.cv.create_polygon(s.cvpoints,fill=hexcolor(s.fill),outline=hexcolor(s.stroke),width=s.cvstrokewidth)
            if s.obj=='rectangle':
                s.tkobj=self.cv.create_rectangle([s.cvx1,s.cvy1,s.cvx2,s.cvy2],fill=hexcolor(s.fill),outline=hexcolor(s.stroke),width=s.cvstrokewidth)
            if s.obj in ('ellipse','circle','oval'):
                s.tkobj=self.cv.create_oval([s.cvx1,s.cvy1,s.cvx2,s.cvy2],fill=hexcolor(s.fill),outline=hexcolor(s.stroke),width=s.cvstrokewidth)
            if s.obj in ('arc','pieslice'):
                if self.arcscale==0.0:
                    self.arcscale=0.1
                ## tk seems to draw arcs counterclockwse, hence the corrections
                s.tkobj=self.cv.create_arc([s.cvx1,s.cvy1,s.cvx2,s.cvy2],start=(360.0*(-s.a0-s.ad)/self.arcscale+90)%360.0,extent=360*s.ad/self.arcscale,fill=hexcolor(s.fill),outline=hexcolor(s.stroke),width=s.cvstrokewidth)
            if s.xlink!='':  ## shift-click to open link
                self.cv.tag_bind(s.tkobj,'<Shift-Button-1>',tkweblink)
                sitedict1[(self.cv,s.tkobj)]=s.xlink
            if s.detail!='':  ## cntrl-click for a detailed summary of this object
                self.cv.tag_bind(s.tkobj,'<Control-Button-1>',tkdetail)
                detaildict1[(self.cv,s.tkobj)]=s.detail
            if s.mouseover!='':
                self.cv.tag_bind(s.tkobj,'<Enter>',tkmouseover)
                msgdict1[(self.cv,s.tkobj)]=s.mouseover
            if s.popup!='':
                self.cv.tag_bind(s.tkobj,'<Button-1>',tkpopup)
                popupdict1[(self.cv,s.tkobj)]=s.popup
            self.tkdisplaylist.append(s)
        if filepath and (filepath!='none'):
            self.cv.update()
            self.cv.postscript(file=filepath,colormode='color',height=self.cvheight,width=self.cvwidth)
        self.boxwidth=int(self.cvwidth/8)
        if self.textboxes>0:
            self.boxwidth=int(self.cvwidth/(self.textboxes*8))
        if self.xlinks:
            self.mouseoverlabel=tk.Label(self.tkframe,text='Link:shift-click',font=("Serif",8,'bold'),wraplength=8*self.boxwidth)
            self.mouseoverlabel.grid(row=2,column=self.tkcolumns-1)
            self.xlinklist=ScrolledText(self.tkframe,fg="black", bg="lightgrey", height=10, width=self.boxwidth)
            self.xlinklist.grid(row=1,column=self.tkcolumns-1)
            self.tkcolumns+=1
        if self.popups:
            self.mouseoverlabel=tk.Label(self.tkframe,text='Summary:click',font=("Serif",8,'bold'),wraplength=8*self.boxwidth)
            self.mouseoverlabel.grid(row=2,column=self.tkcolumns-1)
            self.popuplist=ScrolledText(self.tkframe,fg="black", bg="lightgrey", height=10, width=self.boxwidth)
            self.popuplist.grid(row=1,column=self.tkcolumns-1)
            self.tkcolumns+=1
        if self.details:
            self.mouseoverlabel=tk.Label(self.tkframe,text='Detail:ctr-click',font=("Serif",8,'bold'),wraplength=8*self.boxwidth)
            self.mouseoverlabel.grid(row=2,column=self.tkcolumns-1)
            self.detaillist=ScrolledText(self.tkframe,fg="black", bg="lightgrey", height=10, width=self.boxwidth)
            self.detaillist.grid(row=1,column=self.tkcolumns-1)
            self.tkcolumns+=1
        if self.mouseovers:
            self.mouseoverlabel=tk.Label(self.tkframe,text='ItemID:mouseover',font=("Serif",8,'bold'),wraplength=8*self.boxwidth)
            self.mouseoverlabel.grid(row=2,column=self.tkcolumns-1)
            self.mouseoverlist=ScrolledText(self.tkframe,fg="black", bg="lightgrey", height=10, width=self.boxwidth)
            self.mouseoverlist.grid(row=1,column=self.tkcolumns-1)
            self.tkcolumns+=1
        self.cv.update()
        if not(self.live):
            if display:
                self.tkwindow.mainloop()
            else:
                self.tkwindow.destroy()

    def MVGwrite(self,filepath='temp.tif',display=True,tempfilepath="temp.mvg"):
        ''' filepath=<path.jpg/tif, etc>, display=True/False
            Use Magick-Vector Graphics format with GraphicsMagick or ImageMagick to render items into
            first a '*.mvg' file (a flexible graphics description language used by ImageMagick and GraphicsMagick
            second, a raster (not vector) graphics file with any format specified by the user that is supported by
            ImageMagick or GraphicsMagick.  TIF, PNG, and JPG are examples of this
            This will only work if MVGwrite is installed on the system, and requires that the python environment have access
            to the path variables from the main system (sometimes a problem on the MAC'''
        if self.scale in ('Auto',"auto"):
            self.windowcalc(scale=3.0)
        else:
            self.windowcalc()
        F1=open(tempfilepath,mode='w')
        F1.write('push graphic-context\n')
        F1.write('viewbox 0 0 '+str(self.cvwidth)+' '+str(self.cvheight)+'\n')
        F1.write('affine 1 0 0 1 -0 -0\n')
        F1.write('push graphic-context\n')
        F1.write('fill '+self.bg+'\n')

        F1.write('push graphic-context \n')
        F1.write('rectangle '+str(0)+','+str(0)+' '+str(self.cvwidth)+','+str(self.cvheight)+'\n')
        F1.write('pop graphic-context \n')
        F1.write('pop graphic-context \n')
        for s in self:
            F1.write('push graphic-context\n')
            if s.obj=='text':
                ## "Handle a bug in Graphics Magick that leaves objects too far above the top edge "gravity"
                GMcvgcycorr=copy(s.cvgcy)
                ##if s.vjust=='center': GMcvgcycorr+=s.cvyr
##                if s.rotate!=0:
##                    if s.vjust=='top': GMcvgcycorr+=s.cvxr
##                    if s.vjust=='bottom': GMcvgcycorr-=s.cvxr
                ##Could eventually tweak the above (and the translation statements below) for better rotation
                F1.write('fill '+s.fill+'\n')
                ## note that MVG documentation seems ambiguous on which to set.
                ## setting both "font" and "Font Family" seems to work at least on the mac
                ## the mac does  not do styles and weights properly though (sadly)
                F1.write('font "'+s.ttffile+'" \n')
                F1.write('font-size '+str(s.cvfs)+'\n')
                if s.font['underline']:
                    F1.write('decorate underline'+'\n')
                if s.font['overstrike']:
                    F1.write('decorate line-through'+'\n')
                if s.rotate!=0:
                    F1.write('gravity '+gravitydict[(s.hjust,'center')]+' \n')
                    F1.write('translate '+mstr(s.cvgcx)+','+mstr(GMcvgcycorr)+ ' \n')
                    F1.write('rotate '+mstr(s.rotate)+' \n')
                    F1.write('translate '+mstr(-s.cvgcx)+','+mstr(-GMcvgcycorr)+ ' \n')
                    F1.write('text '+mstr(s.cvgcx)+','+mstr(GMcvgcycorr)+' "'+s.text+'"'+' \n')
                else:
                    F1.write('gravity '+gravitydict[(s.hjust,'center')]+'\n')
                    F1.write('text '+mstr(s.cvgcx)+','+mstr(GMcvgcycorr)+' "'+s.text+'"'+' \n')
            if s.obj in ('rectangle','rect','square'):
                if s.fill:
                    F1.write('fill '+s.fill+'\n')
                    F1.write('fill-opacity '+mstr(s.fillopacity)+'\n')
                else:
                    F1.write('fill none\n')
                if s.stroke:
                    F1.write('stroke '+s.stroke+'\n')
                    F1.write('stroke-opacity '+mstr(s.strokeopacity)+'\n')
                    F1.write('stroke-width '+mstr(s.cvstrokewidth)+'\n')
                F1.write('rectangle '+mstr(s.cvx1)+','+mstr(s.cvy1)+' '+mstr(s.cvx2)+','+mstr(s.cvy2)+'\n')
            if s.obj in ('ellipse','circle','oval'):
                if s.fill:
                    F1.write('fill '+s.fill+'\n')
                    F1.write('fill-opacity '+mstr(s.fillopacity)+'\n')
                else:
                    F1.write('fill none\n')
                if s.stroke:
                    F1.write('stroke '+s.stroke+'\n')
                    F1.write('stroke-opacity '+mstr(s.strokeopacity)+'\n')
                    F1.write('stroke-width '+mstr(s.cvstrokewidth)+'\n')
                F1.write('ellipse '+mstr(s.cvxc)+','+mstr(s.cvyc)+' '+mstr(s.cvxr)+','+mstr(s.cvyr)+' 0,360 \n')
            if s.obj in ('arc','pieslice'):
                if s.fill:
                    F1.write('fill '+s.fill+'\n')
                    F1.write('fill-opacity '+mstr(s.fillopacity)+'\n')
                else:
                    F1.write('fill none\n')
                if s.stroke:
                    F1.write('stroke '+s.stroke+'\n')
                    F1.write('stroke-opacity '+mstr(s.strokeopacity)+'\n')
                    F1.write('stroke-width '+mstr(s.cvstrokewidth)+'\n')
                F1.write('path '+s.arcpath+'\n')
            if s.obj in ('line'):
                F1.write('stroke '+s.stroke+'\n')
                F1.write('stroke-opacity '+mstr(s.strokeopacity)+'\n')
                F1.write('stroke-width '+mstr(s.cvstrokewidth)+'\n')
                F1.write('line '+str(s.cvx1)+','+mstr(s.cvy1)+' '+mstr(s.cvx2)+','+mstr(s.cvy2)+'\n')
            if s.obj in ('polygon'):
                if s.fill:
                    F1.write('fill '+s.fill+'\n')
                    F1.write('fill-opacity '+mstr(s.fillopacity)+'\n')
                else:
                    F1.write('fill none\n')
                if s.stroke:
                    F1.write('stroke '+s.stroke+'\n')               
                    F1.write('stroke-opacity '+mstr(s.strokeopacity)+'\n')
                    F1.write('stroke-width '+mstr(s.cvstrokewidth)+'\n')
                F1.write('polygon '+pointstr(s.cvpoints)+'\n')
            if s.obj =='polyline':
                F1.write('fill '+'none'+'\n')
                F1.write('stroke '+s.stroke+'\n')
                F1.write('stroke-opacity '+mstr(s.strokeopacity)+'\n')
                F1.write('stroke-width '+mstr(s.cvstrokewidth)+'\n')
                F1.write('polyline '+pointstr(s.cvpoints)+'\n')
                
            F1.write('pop graphic-context\n')

        F1.write('pop graphic-context\n')
        F1.close()
        tempfilepath=os.path.abspath(tempfilepath)
        filepathfull=os.path.abspath(filepath)
        if '.' in filepathfull:
            altfilepath=filepathfull[:filepathfull.rfind('.')]+'.svg'
        else:
            altfilepath=filepathfull+'.svg'
        displayt1=copy(display)
        try:
            check_output(["gm","convert",tempfilepath,filepathfull]) ## try graphicsmagick first
        except:
            try:
                print('GraphicsMagick convert attempt failes, trying ImageMagick')
                check_output(["convert",tempfilepath,filepathfull]) ## then try imagemagick
            except:
                print('Unable to convert MVG File, trying PIL conversion')
                if Imageimported1:
                    try:
                        self.PILwrite(filepath=filepathfull,display=displayt1)
                    except:
                        self.SVGwrite(filepath=altfilepath,display=displayt1)
                else:
                    self.SVGwrite(filepath=altfilepath,display=displayt1)
                return ''
        ## serious doo doo here... make sure the windows addresses also work
        if display:
            displaysuccess=False
            if viPython and (filepath.endswith('.jpg') or filepath.endswith('.jpeg') or filepath.endswith('.png')) :
                try:
                    I_display(I_Image(filename=filepathfull,width=self.screenwidth))
                    displaysuccess=True
                    ##print("If this fails, it may work to triple-click, copy, and paste the following command into the iPython shell")
                    ##print("I_Image(filename='"+str(filepath)+"',width="+str(self.screenwidth)+")")
                except:
                    try:
                        I_display(I_Image(filename=filepathfull))
                        displaysuccess=True
                        ##print("If this fails, it may work to triple-click, copy, and paste the following command into the iPython shell")
                        ##print("I_Image(filename='"+str(filepath)+"')")
                    except:
                        print('Unsuccessful at inline display of image '+filepath+', using external display')
            if not(displaysuccess):
                try:
                    check_call(["open",filepathfull])
                except:
                    try:
                        check_call(["xdg-open",filepathfull])
                    except:
                        print('Unable to display MVG File, trying SVG display')
                        self.SVGwrite(filepath=altfilepath,display=displayt1)

    def SVGwrite(self,filepath='temp.svg',display=True):
        ''' filepath=<path.svg>, display=True/False
            Render the image as a SVG web page instance with active links
            Then
               1.  Display the canvas (if "display=True" in call)
               2.  Write the image to an svg file ( "filepath=<filepath> in call)'''

        if self.scale in ('auto','Auto'):
            if abs(self.xmax-self.xmin)>self.screenwidth:
                if self.xmax==self.xmin:
                    self.xmax=self.xmin+1
                sc=float(self.screenwidth)/abs(self.xmax-self.xmin)
                self.windowcalc(scale=sc)
            else:
                self.windowcalc(scale=1.0)
        else:
            self.windowcalc()
        file_output1=open(filepath,'w')

        svgheader='<svg width="'+str(int(self.cvwidth))+'px" height="'+str(int(self.cvheight))+'"'
        svgheader+=' viewBox="%i %i %i %i" preserveAspectRatio="xMidYMid meet"  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"> \n' % (0, 0,int(self.cvwidth+0.001),int(self.cvheight+0.001))
        svgbackground='<rect x="0" y="0" width="'+str(int(self.cvwidth+0.001))+'" height="'+str(int(self.cvheight+0.001))+'" fill="'+self.bg+'" />\n'
        file_output1.write(svgheader+svgbackground)
        for s in self:
            if s.obj=='text':
                s.htext=htmle(s.text)
                s.cvyt=s.cvy1-s.cvyr
                if s.vjust=='top':s.cvyt=s.cvy1-s.cvyr
                if s.vjust=='center':s.cvyt=s.cvy1-s.cvyr*0.5
                if s.vjust=='bottom':s.cvyt=s.cvy1
                outline1='<text x='+svnum(s.cvxcr)+' y='+svnum(s.cvyt)
                outline1+=' font-family="'+s.font['family']+'"'
                outline1+=' font-size="'+str(s.cvfs)+'"'
                outline1+=' font-weight="'+s.font['weight']+'"'
                outline1+=' font-style="'+s.font['slant']+'"'
                outline1+=' text-anchor="'+s.hjust+'"'                
                ##outline1+=' dominant-baseline="'+s.vjust+'"'
                ## Eventually the "dominant-baseline feature of svg (from CSS) will
                ## be implemented on standard browsers and this will be an appropriate
                ## and much more intuitive means of vertical justification.  For the moment
                ## though, dominant-baseline seems to mean nothing to most svg renderes (browsers)
                ## and different things to others, thus the following explicit corrections
                ## to positionint
                if s.fillopacity!=1.0:
                    outline1+=' fill-opacity='+svnum(s.fillopacity)
                if s.font['underline'] and s.font['overstrike']:
                    outline1+=' text-decoration="underline line-through"'
                elif s.font['underline']:
                    outline1+=' text-decoration="underline"'
                elif s.font['overstrike']:
                    outline1+=' text-decoration="line-through"'
                outline1+=' fill="'+s.fill+'"'
                if s.rotate!=0:outline1+=' transform="rotate('+svnum(s.rotate)[1:-1]+' '+svnum(s.cvxcr)[1:-1]+' '+svnum(s.cvyt)[1:-1]+')"'
                outline1+='>'+s.htext+'</text'

            else:
                outline1=''
                if s.obj=='line':
                    outline1='<line x1='+svnum(s.cvx1)+' y1='+svnum(s.cvy1)+ ' x2='+svnum(s.cvx2)+' y2='+svnum(s.cvy2)
                if s.obj in ('rect','rectangle'):
                    outline1='<rect x='+svnum(min(s.cvx1,s.cvx2))+' y='+svnum(min(s.cvy1,s.cvy2))+ ' width='+svnum(abs(2*s.cvxr))+' height='+svnum(abs(2*s.cvyr))
                if s.obj=='ellipse':
                    outline1='<ellipse cx='+svnum(s.cvxc)+' cy='+svnum(s.cvyc)+ ' rx='+svnum(s.cvxr)+' ry='+svnum(s.cvyr)        
                if s.obj in ('polyline','polygon'):
                    outline1='<'+s.obj+' points="'+svgpointstr(s.cvpoints)+'"'
                if s.obj=='arc':
                    outline1='<path d='+s.arcpath
                if s.cvstrokewidth>0:
                    outline1+=' stroke="'+s.stroke+'"'
                    outline1+=' stroke-width='+svnum(s.cvstrokewidth)
                    if s.strokeopacity!=1.0:
                        outline1+=' stroke-opacity='+svnum(s.strokeopacity)
                if s.fill:
                    outline1+=' fill="'+s.fill+'"'
                    if s.fillopacity!=1.0:
                        outline1+=' fill-opacity='+svnum(s.fillopacity)
                else:
                    outline1+=' fill-opacity="0"'
                if s.rotate!=0:outline1+=' transform="rotate('+svnum(s.rotate)[1:-1]+' '+svnum(s.cvxc)[1:-1]+' '+svnum(s.cvyc)[1:-1]+')"'                                                                                                                                                       
                outline1+=' /'
            if s.popup!='':
                ## outline1=outline1.rstrip('/')
                outline1='<a onclick="javascript:window.alert('+"'"+htmle(s.popup)+"');return false"+'" >'+outline1+'></a'
            elif s.detail!='':
                ## outline1=outline1.rstrip('/')
                outline1='<a onclick="javascript:window.alert('+"'"+htmle(s.detail)+"');return false"+'" >'+outline1+'></a'
            if s.xlink!='':
                outline1='<a xlink:href="'+htmle(s.xlink)+'" >'+outline1+'></a'
            if s.mouseover!='':
                outline1='<a xlink:href="http://#'+htmle(s.mouseover)+'" >'+outline1+'></a'

            outline1+='> \n'
            file_output1.write(outline1)
        svgtailer='</svg>'
        file_output1.write(svgtailer)
        file_output1.close()
        filepathfull=os.path.abspath(filepath)
        if display:
            displaysuccess=False
            if viPython:
                try:
                    I_display(I_SVG(filename=filepathfull))
                    displaysuccess=True
                    ##print("If this fails, it may work to triple-click, copy, and paste the following command into the iPython shell")
                    ##print("IPython.core.display.SVG(filename='"+str(filepath)+"')")
                except:
                    print('Unsuccessful at inline display of image '+filepath+', using browser display')
            if not(displaysuccess):
                try:
                    webbrowser.open_new('file://'+filepathfull)
                    print("Finished writing to file: browser should now start (could be a few seconds)")
                except:
                    print("File "+filepathfull+" is written but was not displayed due to a web-browser issue, try opening from the system file browser")
        else:
            print("Finished writing to file")
    def HTML5write(self,filepath='temp.html',display=True):
        ''' filepath=<path.svg>, display=True/False
            Render the image as a SVG web page instance with active links
            Then
               1.  Display the canvas (if "display=True" in call)
               2.  Write the image to an svg file ( "filepath=<filepath> in call)'''
        htmlHeader1='''<!doctype html>\r<html>\r<head>\r<meta charset="utf-8" />\r<title>'''+"VSG Canvas Viewer- HTML5"
        htmlHeader2='''</title>\r<script type="text/javascript">\r<!--\rfunction draw() {\rvar canvas = document.getElementById('cav1');\rif (canvas.getContext) {\rvar ctx = canvas.getContext('2d');\r'''
        if self.scale in ('auto','Auto'):
            if abs(self.xmax-self.xmin)>self.screenwidth:
                if self.xmin==self.xmax:
                    self.xmax+=1
                sc=float(self.screenwidth)/abs(self.xmax-self.xmin)
                self.windowcalc(scale=sc)
            else:
                self.windowcalc(scale=1.0)
        else:
            self.windowcalc()
        file_output1=open(filepath,'w')
        file_output1.write(htmlHeader1+htmlHeader2)
        outline1="ctx.fillStyle ='"+hexcolor(self.bg)+"';\r"
        outline1+="ctx.fillRect(0,0,"+svnum(self.cvwidth)+','+svnum(self.cvheight)+");\r"
        outline1+="ctx.lineJoin ='round';\r"
        
        for s in self:
            if s.rotate!=0:
                outline1+="ctx.save();\r"
                outline1+="ctx.translate(%.2f,%.2f);\r"%(s.cvxcr,s.cvycr)
                outline1+="ctx.rotate(%.2f);\r"%(2*pi*float(s.rotate)/360.0)
                outline1+="ctx.translate(%.2f,%.2f);\r"%(-s.cvxcr,-s.cvycr)

            if s.obj=='text':
                s.cvyt=s.cvy1-s.cvyr
                if s.vjust=='top':
                    outline1+="ctx.textBaseline='top';\r"
                    s.cvyt=s.cvy2+0
                if s.vjust=='center':
                    outline1+="ctx.textBaseline='middle';\r"
                    s.cvyt=s.cvyc+0
                if s.vjust=='bottom':
                    outline1+="ctx.textBaseline='bottom';\r"
                    s.cvyt=s.cvy1+0
                outline1+="ctx.fillStyle ='"+hexcolor(s.fill)+"';\r"
                outline1+="ctx.textAlign='%s';\r"%(htmljustD[s.hjust])
                outline1+="ctx.font='"
                if s.font['slant'].lower()=='italic':
                    outline1+='italic '
                if s.font['weight'].lower()=='bold':
                    outline1+='bold '
                outline1+=str(s.cvfs)+'px '+s.font['family']+"';\r"
                if s.strokeopacity!=1.0:
                    outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                outline1+='ctx.fillText(%s,%s,%s);\r'%('"'+s.text.replace('\r',' ').replace('\n',' ')+'"',svnum(s.cvxcr),svnum(s.cvyt))
                
            if s.obj=='line':
                outline1+="ctx.beginPath();\r"                    
                outline1+="ctx.strokeStyle='"+hexcolor(s.stroke)+"';\r"
                outline1+="ctx.lineWidth="+svnum(s.cvstrokewidth)+";\r"
                outline1+='ctx.moveTo('+svnum(s.cvx1)+','+svnum(s.cvy1)+');\r'
                outline1+='ctx.lineTo('+svnum(s.cvx2)+','+svnum(s.cvy2)+');\r'
                if s.strokeopacity!=1.0:
                    outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                outline1+='ctx.stroke();\r'
            if s.obj in ('rect','rectangle'):
                outline1+="ctx.beginPath();\r"                    
                if hexcolor(s.fill):
                    outline1+="ctx.fillStyle ='"+hexcolor(s.fill)+"';\r"
                    if s.fillopacity!=1.0:
                        outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                    outline1+='ctx.fillRect (%s,%s,%s,%s);\r'%(svnum(min(s.cvx1,s.cvx2)),svnum(min(s.cvy1,s.cvy2)),svnum(abs(s.cvxr*2)),svnum(abs(s.cvyr*2)))
                if hexcolor(s.stroke):
                    outline1+="ctx.strokeStyle='"+hexcolor(s.stroke)+"';\r"
                    outline1+="ctx.lineWidth="+svnum(s.cvstrokewidth)+";\r"
                    if s.strokeopacity!=1.0:
                        outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                    outline1+='ctx.strokeRect (%s,%s,%s,%s);\r'%(svnum(min(s.cvx1,s.cvx2)),svnum(min(s.cvy1,s.cvy2)),svnum(abs(s.cvxr*2)),svnum(abs(s.cvyr*2)))
            if s.obj in ('ellipse','circle'):
                if hexcolor(s.fill):
                    outline1+="ctx.fillStyle ='"+hexcolor(s.fill)+"';\r"
                if hexcolor(s.stroke):
                    outline1+="ctx.strokeStyle='"+hexcolor(s.stroke)+"';\r"
                    outline1+="ctx.lineWidth="+svnum(s.cvstrokewidth)+";\r"
                if s.cvxr==s.cvyr:
                    outline1+="ctx.beginPath();\r"                    
                    outline1+="ctx.arc(%.2f,%.2f,%.2f,0,2*Math.PI);\r"%(s.cvxc,s.cvyc,s.cvxr)
                    if hexcolor(s.fill):
                        if s.fillopacity!=1.0:
                            outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                        outline1+="ctx.fill();\r"
                    if hexcolor(s.stroke):
                        if s.strokeopacity!=1.0:
                            outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                        outline1+="ctx.stroke();\r"
                else:
                    if s.cvyr*s.cvxr==0:
                        outline1+="ctx.beginPath();\r"                    
                        outline1+='ctx.moveTo('+svnum(s.cvx1)+','+svnum(s.cvy1)+');\r'
                        outline1+='ctx.lineTo('+svnum(s.cvx2)+','+svnum(s.cvy2)+');\r'
                        if hexcolor(s.fill):
                            if s.fillopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                            outline1+="ctx.fill();\r"
                        if hexcolor(s.stroke):
                            if s.strokeopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                            outline1+="ctx.stroke();\r"
                    if s.cvxr>s.cvyr:
                        outline1+="ctx.save();\r"
                        outline1+="ctx.scale(1.0,%s);\r"%(str(float(s.cvyr)/float(s.cvxr)))
                        outline1+="ctx.beginPath();\r"                    
                        outline1+="ctx.arc(%.2f,%.2f,%.2f,0,2*Math.PI);\r"%(s.cvxc,float(s.cvyc)*float(s.cvxr)/float(s.cvyr),s.cvxr)
                        if hexcolor(s.fill):
                            if s.fillopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                            outline1+="ctx.fill();\r"
                        if hexcolor(s.stroke):
                            if s.strokeopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                            outline1+="ctx.stroke();\r"
                        outline1+="ctx.restore();\r"
                    if s.cvyr>s.cvxr:
                        outline1+="ctx.save();\r"
                        outline1+="ctx.scale(%s,1.0);\r"%(str(float(s.cvxr)/float(s.cvyr)))
                        outline1+="ctx.beginPath();\r"                    
                        outline1+="ctx.arc(%.2f,%.2f,%.2f,0,2*Math.PI);\r"%(float(s.cvxc)*float(s.cvyr)/float(s.cvxr),s.cvyc,s.cvyr)
                        if hexcolor(s.fill):
                            if s.fillopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                            outline1+="ctx.fill();\r"
                        if hexcolor(s.stroke):
                            if s.strokeopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                            outline1+="ctx.stroke();\r"
                        outline1+="ctx.restore();\r"
            if s.obj in ('arc','pieslice'):
                if hexcolor(s.fill):
                    outline1+="ctx.fillStyle ='"+hexcolor(s.fill)+"';\r"
                if hexcolor(s.stroke):
                    outline1+="ctx.strokeStyle='"+hexcolor(s.stroke)+"';\r"
                    outline1+="ctx.lineWidth="+svnum(s.cvstrokewidth)+";\r"
                if s.cvxr==s.cvyr:
                    outline1+="ctx.beginPath();\r"                    
                    outline1+="moveTo(%.2f,%.2f);\r"%(s.cvxc,s.cvyc)
                    outline1+="ctx.arc(%.2f,%.2f,%.2f,%.5f,%.5f);\r"%(s.cvxc,s.cvyc,s.cvxr,s.startrad,s.endrad)
                    outline1+="ctx.lineTo(%.2f,%.2f);\r"%(s.cvxc,s.cvyc)
                    outline1+="ctx.closePath();\r"
                    if hexcolor(s.fill):
                        if s.fillopacity!=1.0:
                            outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                        outline1+="ctx.fill();\r"
                    if hexcolor(s.stroke):
                        if s.strokeopacity!=1.0:
                            outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                        outline1+="ctx.stroke();\r"
                else:
                    if s.cvyr*s.cvxr==0:
                        outline1+="ctx.beginPath();\r"                    
                        outline1+='ctx.moveTo('+svnum(s.cvx1)+','+svnum(s.cvy1)+');\r'
                        outline1+='ctx.lineTo('+svnum(s.cvx2)+','+svnum(s.cvy2)+');\r'
                        if hexcolor(s.fill):
                            if s.fillopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                            outline1+="ctx.fill();\r"
                        if hexcolor(s.stroke):
                            if s.strokeopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                            outline1+="ctx.stroke();\r"
                    if s.cvxr>s.cvyr:
                        outline1+="ctx.save();\r"
                        outline1+="ctx.scale(1.0,%s);\r"%(str(float(s.cvyr)/float(s.cvxr)))
                        outline1+="ctx.beginPath();\r"                    
                        outline1+="moveTo(%.2f,%.2f);\r"%(s.cvxc,float(s.cvyc)*float(s.cvxr)/float(s.cvyr))
                        outline1+="ctx.arc(%.2f,%.2f,%.2f,%.5f,%.5f);\r"%(s.cvxc,float(s.cvyc)*float(s.cvxr)/float(s.cvyr),s.cvxr,s.startrad,s.endrad)
                        outline1+="ctx.lineTo(%.2f,%.2f);\r"%(s.cvxc,float(s.cvyc)*float(s.cvxr)/float(s.cvyr))
                        outline1+="ctx.closePath();\r"
                        if hexcolor(s.fill):
                            if s.fillopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                            outline1+="ctx.fill();\r"
                        if hexcolor(s.stroke):
                            if s.strokeopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                            outline1+="ctx.stroke();\r"
                        outline1+="ctx.restore();\r"
                    if s.cvyr>s.cvxr:
                        outline1+="ctx.save();\r"
                        outline1+="ctx.scale(%s,1.0);\r"%(str(float(s.cvxr)/float(s.cvyr)))
                        outline1+="ctx.beginPath();\r"
                        outline1+="moveTo(%.2f,%.2f);\r"%(float(s.cvxc)*float(s.cvyr)/float(s.cvxr),s.cvyc)
                        outline1+="ctx.arc(%.2f,%.2f,%.2f,%.5f,%.5f);\r"%(float(s.cvxc)*float(s.cvyr)/float(s.cvxr),s.cvyc,s.cvyr,s.startrad,s.endrad)
                        outline1+="ctx.lineTo(%.2f,%.2f);\r"%(float(s.cvxc)*float(s.cvyr)/float(s.cvxr),s.cvyc)
                        outline1+="ctx.closePath();\r"
                        if hexcolor(s.fill):
                            if s.fillopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                            outline1+="ctx.fill();\r"
                        if hexcolor(s.stroke):
                            if s.strokeopacity!=1.0:
                                outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                            outline1+="ctx.stroke();\r"
                        outline1+="ctx.restore();\r"
            if s.obj in ('polyline','polygon'):
                if hexcolor(s.fill):
                    outline1+="ctx.fillStyle ='"+hexcolor(s.fill)+"';\r"
                if hexcolor(s.stroke):
                    outline1+="ctx.strokeStyle='"+hexcolor(s.stroke)+"';\r"
                    outline1+="ctx.lineWidth="+svnum(s.cvstrokewidth)+";\r"
                outline1+="ctx.beginPath();\r"
                if s.cvpoints:
                    outline1+="moveTo(%.2f,%.2f);\r"%(s.cvpoints[0][0],s.cvpoints[0][1])
                    for [x5f,y5f] in s.cvpoints:
                        outline1+="ctx.lineTo(%.2f,%.2f);\r"%(x5f,y5f)
                    if s.obj=='polygon':
                        outline1+="ctx.closePath();\r"                            
                    if hexcolor(s.fill):
                        if s.fillopacity!=1.0:
                            outline1+="ctx.globalAlpha=%.2f;\r"%(s.fillopacity)
                        outline1+="ctx.fill();\r"
                    if hexcolor(s.stroke):
                        if s.strokeopacity!=1.0:
                            outline1+="ctx.globalAlpha=%.2f;\r"%(s.strokeopacity)
                        outline1+="ctx.stroke();\r"
            if s.rotate!=0:
                outline1+="ctx.restore();\r"
            if s.fillopacity*s.strokeopacity!=1.0:
                outline1+="ctx.globalAlpha=1.0;\r"

##            if s.popup!='':
##                outline1=outline1.rstrip('/')
##                outline1=outline1+' onclick="javascript:window.alert('+"'"+s.popup+"');return false"+'" /'
##            elif s.detail!='':
##                outline1=outline1.rstrip('/')
##                outline1=outline1+' onclick="javascript:window.alert('+"'"+s.detail+"');return false"+'" /'
##            if s.xlink!='':
##                outline1='<a xlink:href="'+s.xlink+'" >'+outline1+'></a'
##            if s.mouseover!='':
##                outline1='<a xlink:href="http://#'+s.mouseover+'" >'+outline1+'></a'
        htmlTailer1='''}\r}\rwindow.onload = draw;\r-->\r</script>\r</head>\r<body>\r'''
        htmlTailer2='''<canvas width="%i" height="%i" id="%s">\r</canvas>\r</body>\r</html>''' %(int(self.cvwidth+0.001),int(self.cvheight+0.001),'cav1')
        file_output1.write(outline1+htmlTailer1+htmlTailer2)
        file_output1.close()
        filepathfull=os.path.abspath(filepath)
        if display:
            displaysuccess=False
## Presently HTML display is not working "in line" for IPython, hence the following lines are commented out
##            if viPython:
##                try:
##                    I_html_display(I_HTML(filename=filepathfull))
##                    ##print("If this fails, it may work to triple-click, copy, and paste the following command into the iPython shell")
##                    ##print("IPython.core.display.HTML(filename='"+str(filepath)+"')")
##                    ##print("If that fails, try displaying the canvas with vdisplay(filepath='temp.svg') or some other svg/png file name")
##                except:
##                    print('Unsuccessful at inline display of image '+filepath+', using external display')
            if not(displaysuccess):
                try:
                    webbrowser.open_new('file://'+filepathfull)
                    print("Finished writing to file: browser should now start (could be a few seconds)")
                except:
                    print("File "+filepathfull+" is written but was not displayed due to a web-browser issue, try opening from the system file browser")

    def PILwrite(self,filepath='temp.png',display=True):
        ''' filepath=<path.jpg/tif.png>, display=True/False
            Render the image as a raster image using Python Imaging Library-no active links
            Then
               1.  Display the canvas (if "display=True" in call)
               2.  Write the image to a tif/jpg/png file (if "psfile=<filepath> in call)
			This will fail if the image package from python is not imported (in which case, VSG will try MVG instead)'''
	    
        if not(Imageimported1):
            print('Image/ImageDraw/ImageFont not imported, trying MVGwrite')
            self.MVGwrite(filepath=filepath)            
            return ''
        if self.scale in ('auto','Auto'):
            self.windowcalc(scale=3.0)
        else:
            self.windowcalc()
        
        self.pilimage=Image.new('RGB',(int(self.cvwidth),int(self.cvheight)),self.bg)
        self.draw1=ImageDraw.Draw(self.pilimage)
        for s in self:
            if s.obj=='line':
                if s.cvstroke:
                    self.draw1.line([int(s.cvx1),int(s.cvy1),int(s.cvx2),int(s.cvy2)],s.cvstroke,s.cvistrokewidth)
            if s.obj in ('square','rect','rectangle'):
                if s.fill==none and s.cvstroke:
                    self.draw1.line([int(s.cvx1),int(s.cvy1),int(s.cvx2),int(s.cvy1)],s.cvstroke,s.cvistrokewidth)
                    self.draw1.line([int(s.cvx1),int(s.cvy1),int(s.cvx1),int(s.cvy2)],s.cvstroke,s.cvistrokewidth)
                    self.draw1.line([int(s.cvx1),int(s.cvy2),int(s.cvx2),int(s.cvy2)],s.cvstroke,s.cvistrokewidth)
                    self.draw1.line([int(s.cvx2),int(s.cvy1),int(s.cvx2),int(s.cvy2)],s.cvstroke,s.cvistrokewidth)                    
                elif s.strokewidth>0:
                    if s.cvstroke:
                        self.draw1.rectangle([int(s.cvmx1),int(s.cvmy1),int(s.cvmx2),int(s.cvmy2)],s.cvstroke)
                    if s.cvfill:
                        self.draw1.rectangle([int(s.cvmx1+s.cvstrokewidth),int(s.cvmy1+s.cvstrokewidth),int(s.cvmx2-s.cvstrokewidth),int(s.cvmy2-s.cvstrokewidth)],s.cvfill)
                else:
                    if s.cvfill:
                        self.draw1.rectangle([int(s.cvmx1),int(s.cvmy1),int(s.cvmx2),int(s.cvmy2)],s.cvfill)
            if s.obj in ('circle','ellipse'):
                if s.strokewidth>0:
                    if s.cvstroke:
                        self.draw1.ellipse([int(s.cvmx1),int(s.cvmy1),int(s.cvmx2),int(s.cvmy2)],s.cvstroke)
                    if s.cvfill:
                        self.draw1.ellipse([int(s.cvmx1+s.cvstrokewidth),int(s.cvmy1+s.cvstrokewidth),int(s.cvmx2-s.cvistrokewidth),int(s.cvmy2-s.cvstrokewidth)],s.cvfill)
                else:
                    if s.cvfill:
                        self.draw1.ellipse([int(s.cvmx1),int(s.cvmy1),int(s.cvmx2),int(s.cvmy2)],s.cvfill)
            if s.obj in ('arc','pieslice'):
                if self.arcscale==0:
                    self.arcscale=0.1
                if s.strokewidth>0:
                    if s.cvstroke:
                        self.draw1.pieslice([int(s.cvmx1),int(s.cvmy1),int(s.cvmx2),int(s.cvmy2)], int((360.0*(s.a0)/self.arcscale-90)%360.0),int((360.0*(s.a0+s.ad)/self.arcscale-90)%360.0), fill=s.cvstroke)
                    if s.cvfill and s.cvstroke:
                        self.draw1.pieslice([int(s.cvmx1+s.cvstrokewidth),int(s.cvmy1+s.cvstrokewidth),int(s.cvmx2-s.cvstrokewidth),int(s.cvmy2-s.cvstrokewidth)],int((360.0*(s.a0)/self.arcscale-90)%360.0),int((360.0*(s.a0+s.ad)/self.arcscale-90)%360.0), fill=s.cvfill,outline=s.cvstroke)
                else:
                    if s.cvfill:
                        self.draw1.pieslice([int(s.cvmx1),int(s.cvmy1),int(s.cvmx2),int(s.cvmy2)],int((360.0*(s.a0)/self.arcscale-90)%360.0), int((360.0*(s.a0+s.ad)/self.arcscale-90)%360.0), fill=s.cvfill)
                    
            if s.obj in ('polyline','polygon'):
                if s.obj=='polygon' and s.cvfill:
                    self.draw1.polygon(s.cvipoints,s.cvfill)
                if s.strokewidth>0 and s.cvstroke:
                    self.draw1.line(s.cvipoints,s.cvstroke,s.cvistrokewidth)
            if s.obj=='text':
                cvttf1=str((s.ttffile,s.cvfs))
                if not cvttf1 in OpenFontsTTF1:
                    OpenFontsTTF1[cvttf1]=ImageFont.truetype(s.ttffile,s.cvfs)
                font11=OpenFontsTTF1[str((s.ttffile,s.cvfs))]
                ts1=font11.getsize(s.text)
                s.cvix1=copy(s.cvx1)
                if s.hjust=='middle':s.cvix1=s.cvxc-ts1[0]/2
                if s.hjust=='end':s.cvix1=s.cvx2-ts1[0]
                s.cviy1=copy(s.cvmy1)
                if s.vjust=='center':s.cviy1=s.cvyc-ts1[1]/2
                if s.vjust=='bottom':s.cviy1=s.cvmy2-ts1[1]
                if s.cvfill:
                    self.draw1.text([int(s.cvix1),int(s.cviy1)],s.text,fill=s.cvfill,font=font11)
        self.pilimage.save(filepath)
        if display:
            displaysuccess=False
            ## try inline display if running iPython
            if viPython and (filepath.endswith('.jpg') or filepath.endswith('.jpeg') or filepath.endswith('.png')) :
                try:
                    I_display(I_Image(filename=filepathfull,width=self.screenwidth))
                    ## newer versions of IPython will apparently have a width feature
                    displaysuccess=True
                    ##print("If this fails, it may work to triple-click, copy, and paste the following command into the iPython shell")
                    ##print("I_Image(filename='"+str(filepath)+"',width="+str(self.screenwidth)+")")
                except:
                    try:
                        I_display(I_Image(filename=filepathfull))
                        ##print("If this fails, it may work to triple-click, copy, and paste the following command into the iPython shell")
                        ##print("I_Image(filename='"+str(filepath)+"')")
                        displaysuccess=True
                    except:
                        print('Unsuccessful at inline display of image '+filepath+', using external display')
            if not(displaysuccess):
                self.pilimage.show()

    def vwrite(self,filepath='temp',display=True,live=False):
        ''' filepath=<path.html/jpg/tif/png/svg>, display=True/False
            Render the image as a raster image using Python Imaging Library-no active links
            Then
               1.  Display the canvas (if "display=True" in call)
               2.  Write the image to a tif/jpg/png file (if "psfile=<filepath> in call)
			This will fail if the image package from python is not imported (in which case, VSG will try MVG instead)'''
        self.sort(key=lambda u:(u.priority,u.ordinal))
        filepath=filepath.strip()
        if not('.' in filepath):
            if viPython:
                filepath+='.svg'
            else:
                filepath+='.html'
        self.live=live
        if self.live and filepath=='temp.html':
            try:
                self.TKwrite()
                return ""
            except:
                pass
        fpext1=filepath.split('.')[-1]
        if fpext1=='svg':
            self.SVGwrite(filepath=filepath,display=display)
            return ""
        if (fpext1=='htm') or (fpext1=='html') :
            self.HTML5write(filepath=filepath,display=display)
            return ""
        if fpext1=='ps':
            try:
                self.TKwrite(filepath=filepath,display=display)
                return ""
            except:
                self.MVGwrite(filepath=filepath,display=display)
                return ""
        try:
            self.MVGwrite(filepath=filepath,display=display)
            return ""
        except:
            try:
                self.PILwrite(filepath=filepath,display=display)
                return ""
            except:
                self.SVGwrite(filepath=filepath+'.svg',display=display)
                return ""

                
    vdisplay=vwrite
    vSVGwrite=SVGwrite
    vPILwrite=PILwrite
    vMVGwrite=MVGwrite
    vTKwrite=TKwrite
    def vclear(self):
        self.__init__()
			
    def splitfont(self,fontstr,*si1):
        ''' splitfont: Input is a text description of a font, output is a dictionary with entries for
        family1,size1,weight,slant,underline,overstrike, <options>
        an extra parameter si1[0] overrides the default canvas font'''
        if type(fontstr)!=str:
            return fontstr
        if fontstr in fontabbrevdict:
            return fontabbrevdict[(fontstr,si1)]
        family1=''
        size1=''
#        weight1=''  ## Not needed 6/7/13
#
#        slant1=''
#
#        underline1=''
#
#        overstrike1=''
#
        options1=''
        addto='family1'
        snde1=0
        for c1 in fontstr:
            if addto=='family1' and not(c1.isdigit()) and family1 and (family1[-1] in ' ,;\t'):
                fst1=fontstr.lower()[snde1:]
                if fst1.startswith('bold') or fst1.startswith('italic') or fst1.startswith('oblique') or fst1.startswith('underline') or fst1.startswith('overstrike'):
                    addto='options1'
            snde1+=1
            if addto=='family1' and c1.isdigit():
                addto='size1'
            if addto=='size1' and not(c1.isdigit()):
                addto='options1'
            if addto=='options1' and c1.isdigit():
                size1=''
                addto='size1'
            if addto=='family1':
                family1+=c1
            if addto=='size1':
                size1+=c1
            if addto=='options1':
                options1+=c1.lower()
        FDict={}
        if family1:
            FDict['family']=family1.strip()
        else:
            FDict['family']=copy(self.font['family'])
        if size1:
            FDict['size']=int(size1)
        else:
            if si1:
                ## override font size
                FDict['size']=int(si1[0])
            else:
                FDict['size']=copy(self.font['size'])
        FDict['weight']='normal'
        FDict['slant']='roman'
        FDict['underline']=False
        FDict['overstrike']=False
        if 'bold' in fontstr.lower():
            FDict['weight']='bold'
        if 'italic' in fontstr.lower() or 'oblique' in fontstr.lower():
            FDict['slant']='italic'
        if 'underline' in fontstr.lower():
            FDict['underline']=True
        if 'overstrike' in fontstr.lower():
            FDict['overstrike']=True
        fontabbrevdict[(fontstr,si1)]=FDict
        return FDict
        
##    def vdisplayupdate:
##        """updates a tk rendering without recalculating margins"""
##
##    def vline:
##        """adds a line to canvas"""
    def vrect(self,*dz0,**dz2):
        """adds a rectangle to canvas"""
        dz2['obj']='rectangle'
        return VSGitem(self,*dz0,**dz2)
    def vline(self,*dz0,**dz2):
        """adds a line to canvas"""
        dz2['obj']='line'
        return VSGitem(self,*dz0,**dz2)
    def vpolygon(self,*dz0,**dz2):
        """adds a polygon to canvas"""
        dz2['obj']='polygon'
        return VSGitem(self,*dz0,**dz2)
    def vpolyline(self,*dz0,**dz2):
        """adds a polyline to canvas"""
        dz2['obj']='polyline'
        return VSGitem(self,*dz0,**dz2)
    def varc(self,*dz0,**dz2):
        """adds an arc/pieslice to canvas"""
        dz2['obj']='arc'
        return VSGitem(self,*dz0,**dz2)
    def vellipse(self,*dz0,**dz2):
        """adds an ellipse to canvas"""
        dz2['obj']='ellipse'
        return VSGitem(self,*dz0,**dz2)
    def vtext(self,*dz0,**dz2):
        """adds a text-let to canvas"""
        dz2['obj']='text'
        return VSGitem(self,*dz0,**dz2)
    def vtitle(self,*dz0,**dz2):
        """ text=<text> ; adds a title to the top of a document"""
        fs1=int(max(abs(self.xmax-self.xmin)/30+1,abs(self.ymax-self.ymin)/30+1))
        if not('font' in dz2):
            dz2['font']='DejaVu Sans Bold '+str(fs1)
        else:
            num1=False
            for cz22 in dz2['font']:
                if cz22 in '1234567890':
                    num1=True
                    break
            if not(num1):
                dz2['font']=dz2['font']+' '+str(fs1)
        if not('x1' in dz2) and not('x2' in dz2) and not('xc' in dz2) and not('x' in dz2):
            dz2['xc']=(self.xmax+self.xmin)/2
        if not('y1' in dz2) and not('y2' in dz2) and not('yc' in dz2) and not('y' in dz2):
            dz2['y1']=self.ymax+2
        if not('text' in dz2):
            try:
                dz2['text']=os.path.basename(sys.argv[0])
            except:
                dz2['text']='Untitled Graphic'
        return self.vtext(*dz0,**dz2)
    def vlegend(self,*dz0,**dz2):
        """ text=<text> ; adds a legend to the bottom of a document, giving basic info if no text supplied"""
        fs1=int(max(abs(self.xmax-self.xmin)/60+1,abs(self.ymax-self.ymin)/60+1))
        if not('font' in dz2):
            dz2['font']='DejaVu Sans '+str(fs1)
        else:
            num1=False
            for cz22 in dz2['font']:
                if cz22 in '1234567890':
                    num1=True
                    break
            if not(num1):
                dz2['font']=dz2['font']+' '+str(fs1)
        if not('x1' in dz2) and not('x2' in dz2) and not('xc' in dz2) and not('x' in dz2):
            dz2['x1']=self.xmin
        if not('y1' in dz2) and not('y2' in dz2) and not('yc' in dz2) and not('y' in dz2):
            dz2['y2']=self.ymin-2        
        if not('text' in dz2):
            dz2['text']=self.vinfo(lines=0,delimiter='\n')
        return self.vtext(*dz0,**dz2)

    vcircle=vellipse
    vpieslice=varc
    velipse=vellipse
    voval=vellipse
    vrectangle=vrect
    vsquare=vrect
    vconnect=vpolyline
    def vrectangle(self,*dz0,**dz2):
        """adds a rectangle to canvas"""
        return vrect(*dz0,**dz2)

    def vset(self,*dz0,**dz2):
        """ sets any specific variable in a VSG canvas.  Some examples
        bg: background color. default is gray
        xmin,xmax,ymin,ymax: maximum values for x and y (default will be to grow these values to cover any elements added to canvas
        scale: scale in pixels in final image per assigned units in x and y values (default=1.0)
        margin: border on edges of drawing (default=10)
        bd: border on tk drawing (default is 2)
        autogrow: autogrow the image if items end up outside (default=True)"""
        for setting1 in dz2:
            setattr(self,setting1.lower(),dz2[setting1])

    def vcolorkey(self,*dz0,**xgd):
        '''<mincolorindex=>,<maxcolorindex=>,<colorvalue=(lambda x:rgb(x,x,x))>,<logmode=True/False>
        output a series of objects as a color scale default position is to add this onto the lower right of the current graph, but
        other positions can be set by parameters x=, y= (these will set the position of the upperleft corner of the color key)
        x2= can be used to set the right side of the colorkey, and keyheight= (or the size of ckfont) the overall height of each line
		the default with this is to try to set the colors up with the log or linear functions from vcolor, but if a function "colorvalue" is provides
		in the parameters for vcolorkey, then this will be used to color the colorswath.  To use an external function in log mode, use logmode=True in function call
		Other Optional Parameters
		mincolorindex=start colorswath at color with index value minindex
		maxcolorindex=end colorswath at color with index value minindex
		colorvalue=a defined function going from scalar values to interpretable colors
		logmode= True for working in log mode
        '''
        gprecise1=False
        for u in xgd.keys():
            xgd[u.lower()]=xgd[u]

        for mm1 in ('mincolorindex','maxcolorindex'):
            if mm1 in xgd:
                gprecise1=True
        if "precise" in xgd:
            gprecise1=bool(xgd['precise'])

        if 'mincolorindex' in xgd:
            mci1=float(xgd['mincolorindex'])
            if self.linearcolorimax-self.linearcolorimin==0:
                if self.linearcolorimin==0:
                    self.linearcolorimin=mci1
                else:
                    self.linearcolormin=mci1*self.linearcolormin/self.linearcolorimin
            else:
                self.linearcolormin=self.linearcolormin+(-self.linearcolorimin+mci1)*(self.linearcolormax-self.linearcolormin)/(self.linearcolorimax-self.linearcolorimin)          
            if self.logcolorimax-self.logcolorimin==0:
                if self.logcolorimin==0:
                    self.logcolorimin=mci1
                else:
                    self.logcolormin=mci1*self.logcolormin/self.logcolorimin
            else:
                self.logcolormin=self.logcolormin+(-self.logcolorimin+mci1)*(self.logcolormax-self.logcolormin)/(self.logcolorimax-self.logcolorimin)          
            self.linearcolorimin=mci1+0
            self.logcolormin=mci1+0
        if 'maxcolorindex' in xgd:
            mci1=float(xgd['maxcolorindex'])
            if self.linearcolorimin-self.linearcolorimax==0:
                if self.linearcolorimax==0:
                    self.linearcolorimax=mci1
                else:
                    self.linearcolormax=mci1*self.linearcolormax/self.linearcolorimax
            else:
                self.linearcolormax=self.linearcolormax+(-self.linearcolorimax+mci1)*(self.linearcolormin-self.linearcolormax)/(self.linearcolorimin-self.linearcolorimax)          
            if self.logcolorimin-self.logcolorimax==0:
                if self.logcolorimax==0:
                    self.logcolorimax=mci1
                else:
                    self.logcolormax=mci1*self.logcolormax/self.logcolorimax
            else:
                self.logcolormax=self.logcolormax+(-self.logcolorimax+mci1)*(self.logcolormin-self.logcolormax)/(self.logcolorimin-self.logcolorimax)          
            self.linearcolorimax=mci1+0
            self.logcolormax=mci1+0
            
        External=''
        if 'colorvalue' in xgd:
            colorvalue=xgd['colorvalue']
            if(not('logmode' in xgd) or xgd['logmode']==False):
                External='linear'
                clmin=self.linearcolorimin+0
                clmax=self.linearcolorimax+0
            else:
                External='log'
                clmin=self.logcolorimin+0
                clmax=self.logcolorimax+0
                if clmin==0:
                    if self.logcolorimin==0:
                        self.logcolorimin=1
                        clmin=1
                    else:
                        clmin=10**floor(log(clmin,10)) ## comment 7/14 This seems useless but harmless, this should never actually be executed
                if clmax==0:
                    if self.logcolorimax==0:
                        self.logcolorimax=1
                        clmax=1
                    else:
                        clmax=10**ceil(log(clmax,10))
                self.logcolorimin=clmin+0
                self.logcolorimax=clmax+0
        d=copy(xgd)
        if not('ckfontcolor' in d):
            if hexcolor(self.fontcolor)==hexcolor(self.bg):
                self.fontcolor="gray"
            if hexcolor(self.fontcolor)==hexcolor(self.bg):
                self.fontcolor="black"
            d['ckfontcolor']=deepcopy(self.fontcolor)
        if "keyheight" in d:
            keyheight=d['keyheight']
            mindim=keyheight+0
        else:
            mindim=min(self.ymax-self.ymin,self.xmax-self.xmin)/32
        if 'y2' in d:
            d['y']=d['y2']
        if 'x1' in d:
            d['x']=d['x1']
        if 'ckfont' in d:
            d['ckfont']=self.splitfont(d['ckfont'],mindim)
        else:
            d['ckfont']=self.splitfont(self.font['family']+' Bold',mindim)
        if not('y' in d):
            d['y']=self.ymin+0
        if not('x' in d):
            d['x']=(6*self.xmin+self.xmax)/7
        if not('x2' in d):
            d['x2']=(4*self.xmin+3*self.xmax)/7
        cgd=d['x2']-d['x']
        cgx=d['x']+0
        cgy=d['y']+0
        cge=d['ckfont']['size']+0
        if External=='linear':
            xginfo=griddivlinear((clmin,clmax),(cgx,cgx+cgd),precise=gprecise1)
            gxlistN=xginfo[3]
            gxlistT=('%G'%xl1 for xl1 in xginfo[2])
            gxlist=list(zip(gxlistN,gxlistT))
            gxlistNm=xginfo[6]
            gxlistTm=('%G'%xl1 for xl1 in xginfo[5])
            gxlistm=list(zip(gxlistNm,gxlistTm))
            gcticklength=float(cge)/2.0
            if 'spectrumtitle' in d:
                self.vtext(text=d['spectrumtitle'],xc=cgx+cgd/2,y2=cgy,font=d['ckfont'],color=d['ckfontcolor'])
                cgy-=cge   
            for i in range(255):
                self.vrect(y1=cgy,y2=cgy-cge,x1=cgx+float(i)*cgd/256.0,x2=cgx+float(i+1)*cgd/256.0+1,fill=colorvalue((clmax-clmin)*float(i)/256.0+clmin),stroke=none)
            cgyrect=cgy+0
            cgy-=cge
            for te1 in gxlist:
                self.vline(x1=te1[0],x2=te1[0],y1=cgy,y2=cgy-gcticklength,stroke="gray",strokewidth=2)
            for te1 in gxlistm:
                self.vline(x1=te1[0],x2=te1[0],y1=cgy,y2=cgy-gcticklength,stroke="gray",strokewidth=1)
            cgy-=gcticklength+2
            self.vrect(x1=cgx,x2=cgx+cgd,y1=cgyrect,y2=cgyrect-cge,stroke="black",strokewidth=1,fill=none)
            for nu1,te1 in enumerate(gxlist):
                te2=te1[1]
                if ('lastplus' in d) and d['lastplus'] and nu1==len(gxlist)-1:
                    te2+='+'
                self.vtext(text=te2,xc=te1[0],y2=cgy,font=d['ckfont'],color=d['ckfontcolor'])
            cgy-=cge*1.5

        if External=='log':
            xginfo=griddivlog((clmin,clmax),(cgx,cgx+cgd),10,precise=gprecise1)
            gxlistN=xginfo[3]
            gxlistT=('%G'%xl1 for xl1 in xginfo[2])
            gxlist=list(zip(gxlistN,gxlistT))
            gxlistNm=xginfo[6]
            gxlistTm=('%G'%xl1 for xl1 in xginfo[5])
            gxlistm=list(zip(gxlistNm,gxlistTm))
            gcticklength=float(cge)/2.0
            if 'spectrumtitle' in d:
                self.vtext(text=d['spectrumtitle'],xc=cgx+cgd/2,y2=cgy,font=d['ckfont'],color=d['ckfontcolor'])
                cgy-=cge
            if clmin==0:
                clmin=1
            for i in range(255):
                self.vrect(y1=cgy,y2=cgy-cge,x1=cgx+float(i)*cgd/256,x2=cgx+float(i+1)*cgd/256+1,fill=colorvalue((clmax/clmin)**(float(i)/256.0)*clmin),stroke=none)
            cgyrect=cgy+0
            cgy-=cge
            for te1 in gxlist:
                self.vline(x1=te1[0],x2=te1[0],y1=cgy,y2=cgy-gcticklength,stroke="gray",strokewidth=2)
            for te1 in gxlistm:
                self.vline(x1=te1[0],x2=te1[0],y1=cgy,y2=cgy-gcticklength,stroke="gray",strokewidth=1)
            cgy-=gcticklength+2
            self.vrect(x1=cgx,x2=cgx+cgd,y1=cgyrect,y2=cgyrect-cge,stroke="black",strokewidth=1,fill=none)
            for nu1,te1 in enumerate(gxlist):
                te2=te1[1]
                if ('lastplus' in d) and d['lastplus'] and nu1==len(gxlist)-1:
                    te2+='+'
                self.vtext(text=te2,xc=te1[0],y2=cgy,font=d['ckfont'],color=d['ckfontcolor'])
            cgy-=cge*1.5
        if self.logcolor:
            xginfo=griddivlog((self.logcolorimin,self.logcolorimax),(cgx,cgx+cgd),10,precise=gprecise1)
            gxlistN=xginfo[3]
            gxlistT=('%G'%xl1 for xl1 in xginfo[2])
            gxlist=list(zip(gxlistN,gxlistT))
            gxlistNm=xginfo[6]
            gxlistTm=('%G'%xl1 for xl1 in xginfo[5])
            gxlistm=list(zip(gxlistNm,gxlistTm))
            gcticklength=float(cge)/2.0
            if 'spectrumtitle' in d:
                self.vtext(text=d['spectrumtitle'],xc=cgx+cgd/2,y2=cgy,font=d['ckfont'],color=d['ckfontcolor'])
                cgy-=cge
            if self.logcolormin==0:
                self.logcolormin=1
            for i in range(255):
                self.vrect(y1=cgy,y2=cgy-cge,x1=cgx+float(i)*cgd/256,x2=cgx+float(i+1)*cgd/256+1,fill=1+int(((float(self.logcolormax)/float(self.logcolormin))**(float(i)/256.0))*self.logcolormin),stroke=none)
            cgyrect=cgy+0
            cgy-=cge
            for te1 in gxlist:
                self.vline(x1=te1[0],x2=te1[0],y1=cgy,y2=cgy-gcticklength,stroke="gray",strokewidth=2)
            for te1 in gxlistm:
                self.vline(x1=te1[0],x2=te1[0],y1=cgy,y2=cgy-gcticklength,stroke="gray",strokewidth=1)
            cgy-=gcticklength+2
            self.vrect(x1=cgx,x2=cgx+cgd,y1=cgyrect,y2=cgyrect-cge,stroke="black",strokewidth=1,fill=none)
            for nu1,te1 in enumerate(gxlist):
                te2=te1[1]
                if ('lastplus' in d) and d['lastplus'] and nu1==len(gxlist)-1:
                    te2+='+'
                self.vtext(text=te2,xc=te1[0],y2=cgy,font=d['ckfont'],color=d['ckfontcolor'])
            cgy-=cge*1.5
        if self.linearcolor:
            xginfo=griddivlinear((self.linearcolorimin,self.linearcolorimax),(cgx,cgx+cgd),precise=gprecise1)
            gxlistN=xginfo[3]
            gxlistT=('%G'%xl1 for xl1 in xginfo[2])
            gxlist=list(zip(gxlistN,gxlistT))
            gxlistNm=xginfo[6]
            gxlistTm=('%G'%xl1 for xl1 in xginfo[5])
            gxlistm=list(zip(gxlistNm,gxlistTm))
            gcticklength=float(cge)/2.0
            if 'spectrumtitle' in d:
                self.vtext(text=d['spectrumtitle'],xc=cgx+cgd/2,y2=cgy,font=d['ckfont'],color=d['ckfontcolor'])
                cgy-=cge   
            for i in range(255):
                self.vrect(y1=cgy,y2=cgy-cge,x1=cgx+float(i)*cgd/256.0,x2=cgx+float(i+1)*cgd/256.0+1,fill=(self.linearcolormax-self.linearcolormin)*float(i)/256.0+self.linearcolormin,stroke=none)
            cgyrect=cgy+0
            cgy-=cge
            for te1 in gxlist:
                self.vline(x1=te1[0],x2=te1[0],y1=cgy,y2=cgy-gcticklength,stroke="gray",strokewidth=2)
            for te1 in gxlistm:
                self.vline(x1=te1[0],x2=te1[0],y1=cgy,y2=cgy-gcticklength,stroke="gray",strokewidth=1)
            cgy-=gcticklength+2
            self.vrect(x1=cgx,x2=cgx+cgd,y1=cgyrect,y2=cgyrect-cge,stroke="black",strokewidth=1,fill=none)
            for nu1,te1 in enumerate(gxlist):
                te2=te1[1]
                if ('lastplus' in d) and d['lastplus'] and nu1==len(gxlist)-1:
                    te2+='+'
                self.vtext(text=te2,xc=te1[0],y2=cgy,font=d['ckfont'],color=d['ckfontcolor'])
            cgy-=cge*1.5
        cgy-=cge*1.5
        for (cg1,cn1) in self.colorlist:
            if type(cn1)==str:
                self.vrect(x1=cgx,width=cge,yc=cgy,height=cge,fill=cn1,strokewidth=0)
            elif len(cn1)<=2:
                self.vrect(x1=cgx,width=cge,yc=cgy,height=cge,fill=cn1[0],fillopacity=cn1[1],strokewidth=0)
            else:
                if len(cn1)<=4:
                    sw11=float(cge)/6.0
                else:
                    sw11=min(float(cge)/6.0,cn1[4])
                self.vrect(x1=cgx,width=cge,yc=cgy,height=cge,fill=cn1[0],stroke=cn1[1],strokewidth=sw11,fillopacity=cn1[2],strokeopacity=cn1[3],)
            self.vtext(x1=cgx+1.2*cge,yc=cgy,text=str(cg1),font=d['ckfont'],color=d['ckfontcolor'])
            cgy-=cge*1.5
    def vgrid(self,gxlog=False,gylog=False,gylabelrotate=True,**xgd):
        '''output a series of lines and text elements to define X,Y axes of a graph
        input items
        gxgrid: draw an x grid (false for just y)
        gygrid: draw a y grid (false for just x)
        gxdom: the parameter denoting "x position" for any given point (e.g., xc for middle, x1 for left, x2 for right)
        gydom: the parameter denoting "y position" for any given point (e.g., xc for center, y1 for bottom, y2 for top)
        gxmin: minimum value of x (if not using the default based on recorded points) 2-ple: (minimum value [for label], minimum x position)
        gxmax: maximum value of x (if not using the default based on recorded points) 2-ple: (maximum value [for label], maximum x position)
        gymin: minimum value of x (if not using the default based on recorded points) 2-ple: (minimum value [for label], minimum y position)
        gymax: maximum value of x (if not using the default based on recorded points) 2-ple: (maximum value [for label], maximum y position)
        
        gx1: left edge for graph grid
        gx2: right edge for graph grid
        gy1: bottom edge for graph grid
        gy2: top edge for graph grid
        gaxisfont,gaxisfontsize: for drawing numbers or other divisions on axes
        glabelfont,glabelfontsize,glabelcolor: for drawing labels on axes
        gxlabel,gylabel: Axis text labels
        gylabelrotate: rotate the Y axis label (=True for -90, or give angle in degrees)
        gynumrotate: rotate the Y axis numbers (=True for -90, or give angle in degrees)
        glabelxcolor,glabelycolor: colors for x and y axis
        gxaxis: label for x axis
        gyaxis: label for y axis
        gtitle: title of graph
        gtitlefont,gtitlefontsize,gtitlecolor: for drawing graph title
        gborderwidth,gbordercolor: border rectangle width and color
        gxmajor=draw major grid lines (alternative is just ticks)
        gxminor=draw major grid lines (alternative is just ticks)
        gymajor=draw major grid lines (alternative is just ticks)
        gyminor=draw major grid lines (alternative is just ticks)
        gmajorwidth,gmajorcolor:width and color of major grid lines
        gminorwidth,gminorcolor: width and color of minor grid lines
        gticklength: length of ticks on x and y axis
         
        ''' 
        gprecise1=False
        FontSizeSpecified1=True
        for u in xgd.keys():
            xgd[u.lower()]=xgd[u]

        for mm1 in ('gx1','gx2','gy1','gy2','gxmin','gxmax','gymin','gymax'):
            if mm1 in xgd:
                gprecise1=True
        if "precise" in xgd:
            gprecise1=bool(xgd['precise'])
        d=deepcopy(xgd)
        if 'gxmin' in d:
            d['gx1']=copy(d['gxmin'][1])
        if 'gxmax' in d:
            d['gx2']=copy(d['gxmax'][1])
        if ('gxmin' in d) and ('gxmax' in d):
            d['gx1']=min(d['gxmin'][1],d['gxmax'][1])
            d['gx2']=max(d['gxmin'][1],d['gxmax'][1])
        if 'gymin' in d:
            d['gy1']=copy(d['gymin'][1])
        if 'gymax' in d:
            d['gy2']=copy(d['gymax'][1])
        if ('gymin' in d) and ('gymax' in d):
            d['gy1']=min(d['gymin'][1],d['gymax'][1])
            d['gy2']=max(d['gymin'][1],d['gymax'][1])
                
        if not('gx1' in d):
            d['gx1']=self.xmin
        if not('gx2' in d):
            d['gx2']=self.xmax
        if not('gy1' in d):
            d['gy1']=self.ymin
        if not('gy2' in d):
            d['gy2']=self.ymax
        if not('gxmajor' in d):
            d['gxmajor']=True
        if not('gymajor' in d):
            d['gymajor']=True
        if not('gxminor' in d):
            d['gxminor']=False
        if not('gyminor' in d):
            d['gyminor']=False
        if 'font' in d:
            d['gaxisfont']=d['font']
        if 'gfont' in d:
            d['gaxisfont']=d['gfont']
        if not('glabelfont' in d):
            if 'gaxisfont' in d:
                d['glabelfont']=deepcopy(d['gaxisfont'])
            else:
                d['glabelfont']=deepcopy(self.font)
        if not('gxlabelfont' in d):
            d['gxlabelfont']=deepcopy(d['glabelfont'])
        if not('gylabelfont' in d):
            d['gylabelfont']=deepcopy(d['glabelfont'])

        if not('gaxisfont' in d):
            if 'glabelfont' in d:
                d['gaxisfont']=deepcopy(d['glabelfont'])
            else:
                d['gaxisfont']=deepcopy(self.font)
        if not('gxaxisfont' in d):
            d['gxaxisfont']=deepcopy(d['gaxisfont'])
        if not('gyaxisfont' in d):
            d['gyaxisfont']=deepcopy(d['gaxisfont'])
        if not('glabelfontsize' in d):
            d['glabelfontsize']=int(min(abs(int(d['gx2']-d['gx1']))/12,abs(int(d['gy2']-d['gy1']))/8))
        if not('gxlabelfontsize' in d):
            d['gxlabelfontsize']=deepcopy(d['glabelfontsize'])
        if not('gylabelfontsize' in d):
            d['gylabelfontsize']=deepcopy(d['glabelfontsize'])
        if not('gxlabel' in d):
            d['gxlabel']='X value'
        if not('gylabel' in d):
            d['gylabel']='Y value'
        if not('gaxisfontsize' in d):
            if not('gxaxisfontsize') in d:
                d['gxaxisfontsize']=int(min(abs(int(d['gx2']-d['gx1']))/12,abs(int(d['gy2']-d['gy1']))/10))
                FontSizeSpecified1=False
            if not('gyaxisfontsize') in d:
                d['gyaxisfontsize']=int(min(abs(int(d['gx2']-d['gx1']))/12,abs(int(d['gy2']-d['gy1']))/10))
            d['gaxisfontsize']=min(d['gxaxisfontsize'],d['gyaxisfontsize'])
        if not('gxaxisfontsize' in d):
            d['gxaxisfontsize']=deepcopy(d['gaxisfontsize'])
        if not('gyaxisfontsize' in d):
            d['gyaxisfontsize']=deepcopy(d['gaxisfontsize'])
        if 'glabelcolor' in d:
            d['gxlabelcolor']=d['glabelcolor']
            d['gylabelcolor']=d['glabelcolor']
        else:
            if not('gxlabelcolor' in d):
                if hexcolor(self.fontcolor)==hexcolor(self.bg):
                    self.fontcolor="gray"
                if hexcolor(self.fontcolor)==hexcolor(self.bg):
                    self.fontcolor="black"
                d['gxlabelcolor']=self.fontcolor
            if not('gylabelcolor' in d):
                if hexcolor(self.fontcolor)==hexcolor(self.bg):
                    self.fontcolor="gray"
                if hexcolor(self.fontcolor)==hexcolor(self.bg):
                    self.fontcolor="black"
                d['gylabelcolor']=self.fontcolor
        if not('gxaxiscolor' in d):
            d['gxaxiscolor']=d['gxlabelcolor']
        if not('gyaxiscolor' in d):
            d['gyaxiscolor']=d['gylabelcolor']
        if not('gtitle' in d):
            try:
                d['gtitle']=os.path.basename(sys.argv[0])
            except:
                d['gtitle']='Untitled Graphic'
        if not('gtitlefontsize' in d):
            d['gtitlefontsize']=max(d['gxaxisfontsize'],d['gyaxisfontsize'],int((d['gx2']-d['gx1'])/24),d['glabelfontsize'])
        if not('gtitlefont' in d):
            d['gtitlefont']=deepcopy(d['glabelfont'])
        if not('gtitlecolor' in d):
            if hexcolor(self.fontcolor)==hexcolor(self.bg):
                self.fontcolor="gray"
            if hexcolor(self.fontcolor)==hexcolor(self.bg):
                self.fontcolor="black"
            d['gtitlecolor']=deepcopy(self.fontcolor)
        if not('gtitlehjust' in d):
            d['gtitlehjust']='middle'
        if not('gtitlevjust' in d):
            d['gtitlevjust']='bottom'
        if not('gborderwidth' in d):
            d['gborderwidth']=1+(int(d['gx2'])-int(d['gx1']))/400.0
        if not('gbordercolor' in d):
            d['gbordercolor']="black"
        if not('gmajorwidth' in d):
            d['gmajorwidth']=max(2,(int(d['gx2'])-int(d['gx1']))/500.0)
        if not('gmajorcolor' in d):
            d['gmajorcolor']="gray"
            if hexcolor("gray")==hexcolor(self.bg):
                d['gmajorcolor']="black"
        if not('gminorwidth' in d):
            d['gminorwidth']=max(1,(int(d['gx2'])-int(d['gx1']))/1000.0)
        if not('gminorcolor' in d):
            d['gminorcolor']="gray"
            if hexcolor("gray")==hexcolor(self.bg):
                d['gminorcolor']="black"
        d['gaxisfont']=self.splitfont(d['gaxisfont'])
        d['gxaxisfont']=self.splitfont(d['gxaxisfont'])
        d['gyaxisfont']=self.splitfont(d['gyaxisfont'])
        d['glabelfont']=self.splitfont(d['glabelfont'])
        d['gxlabelfont']=self.splitfont(d['gxlabelfont'])
        d['gylabelfont']=self.splitfont(d['gylabelfont'])
        d['gtitlefont']=self.splitfont(d['gtitlefont'])
        d['gaxisfont']['size']=d['gaxisfontsize']
        d['gxaxisfont']['size']=d['gxaxisfontsize']
        d['gyaxisfont']['size']=d['gyaxisfontsize']
        d['glabelfont']['size']=d['glabelfontsize']
        d['gxlabelfont']['size']=d['gxlabelfontsize']
        d['gylabelfont']['size']=d['gylabelfontsize']
        d['gtitlefont']['size']=d['gtitlefontsize']
        if 'gynumrotate' in d and d['gynumrotate']==True:
            d['gynumrotate']=-90
        if gylabelrotate==True:
            gylabelrotate=-90
        if gylabelrotate==False:
            gylabelrotate=0
        self.gylabelrotate=gylabelrotate
        for e1 in d:
            setattr(self,e1,deepcopy(d[e1]))
        self.xglist=[]
        self.yglist=[]
        self.xclist=[]
        self.yclist=[]

        if 'gxmin' in d:
            self.xglist.append(d['gxmin'][0])
            self.xclist.append(d['gxmin'][1])
        if 'gxmax' in d:
            self.xglist.append(d['gxmax'][0])
            self.xclist.append(d['gxmax'][1])
        if 'gymin' in d:
            self.yglist.append(d['gymin'][0])
            self.yclist.append(d['gymin'][1])
        if 'gymax' in d:
            self.yglist.append(d['gymax'][0])
            self.yclist.append(d['gymax'][1])
                
        for s in self:
            if 'xg' in dir(s):
                self.xglist.append(copy(s.xg))
                if 'gxdom' in dir(s):
                    self.xclist.append(getattr(s,s.gxdom))
                else:
                    if not 'gxdom' in d:
                        self.gxdom=s.xdom+''
                        if self.x1static and self.gxdom=='x1':
                            self.gxdom='x2'
                        if self.x2static and self.gxdom=='x2':
                            self.gxdom='x1'
                    self.xclist.append(getattr(s,self.gxdom))
            if 'yg' in dir(s):
                self.yglist.append(copy(s.yg))
                if 'gydom' in dir(s):
                    self.yclist.append(getattr(s,s.gydom))
                else:
                    if not 'gydom' in d:
                        self.gydom=s.ydom+''
                        if self.y1static and self.gydom=='y1':
                            self.gydom='y2'
                        if self.y2static and self.gydom=='y2':
                            self.gydom='y1'
                    self.yclist.append(getattr(s,self.gydom))
        if not('gxgrid' in d) and not(self.xglist):
            if self.yglist:
                self.gxgrid=False
                d['gxgrid']=False
            else:
                self.gxgrid=True
                d['gxgrid']=True
        if not('gygrid' in d) and not(self.yglist):
            if self.xglist:
                self.gygrid=False
                d['gygrid']=False
            else:
                self.gygrid=True
                d['gygrid']=True
        if not('gxgrid' in d):
            d['gxgrid']=True
            self.gxgrid=True
        if not('gygrid' in d):
            d['gygrid']=True
            self.gygrid=True

        if not self.xglist:
            self.xglist=[self.xmin+0,self.xmax+0]
            self.xclist=[self.xmin+0,self.xmax+0]
            try:
                self.gxdom=self[0].xdom+''
            except:
                self.gxdom='xc'
        if not self.yglist:
            self.yglist=[self.ymin+0,self.ymax+0]
            self.yclist=[self.ymin+0,self.ymax+0]
            try:
                self.gydom=self[0].ydom+''
            except:
                self.gydom='yc'
            
        if gxlog:
            xginfo=griddivlog(self.xglist,self.xclist,10,precise=gprecise1)
        else:
            xginfo=griddivlinear(self.xglist,self.xclist,precise=gprecise1)
        if self.xlabels!=[]:
            d['gxlist']=list(zip([(self.xmax-self.xmin)*(2*float(inde)+1)/(2*len(self.xlabels))+self.xmin for inde in range(len(self.xlabels))],self.xlabels))
            self.gxlist=d['gxlist']
        if not('gxlist' in d):
            gxlistN=xginfo[3]
            gxlistT=('%G'%xl1 for xl1 in xginfo[2])
            self.gxlist=list(zip(gxlistN,gxlistT))
            gxlistNm=xginfo[6]
            gxlistTm=('%G'%xl1 for xl1 in xginfo[5])
            self.gxlistm=list(zip(gxlistNm,gxlistTm))
        else:
            self.gxlistm=[]
        if gylog:
            yginfo=griddivlog(self.yglist,self.yclist,10,precise=gprecise1)
        else:
            yginfo=griddivlinear(self.yglist,self.yclist,precise=gprecise1)
        if self.ylabels!=[]:
            d['gylist']=list(zip([(self.ymax-self.ymin)*(2*float(inde)+1)/(2*len(self.ylabels))+self.ymin for inde in range(len(self.ylabels))],self.ylabels))
            self.gylist=d['gylist']
        if not('gylist' in d):
            gylistN=yginfo[3]
            gylistT=('%G'%ya1 for ya1 in yginfo[2])
            self.gylist=list(zip(gylistN,gylistT))
            gylistNm=yginfo[6]
            gylistTm=('%G'%ya1 for ya1 in yginfo[5])
            self.gylistm=list(zip(gylistNm,gylistTm))
        else:
            self.gylistm=[]
        if self.gylist:
            gyspan=abs(self.gylist[-1][0]-self.gylist[0][0])
            if len(self.gylist)*self.gaxisfont['size']>gyspan:
                self.gaxisfont['size']=int(gyspan/len(self.gylist))
            self.gy2=max(self.gy2,self.gylist[-1][0],self.gylist[0][0])
            self.gy1=min(self.gy1,self.gylist[-1][0],self.gylist[0][0])
        if self.gxlist:
            self.gx2=max(self.gx2,self.gxlist[-1][0],self.gxlist[0][0])
            self.gx1=min(self.gx1,self.gxlist[-1][0],self.gxlist[0][0])
        if not('gtitlex' in d):
            self.gtitlex=(int(self.gx2)+int(self.gx1))/2.0
        if not('gtitley' in d):
            self.gtitley=int(self.gy2)
        self.vset(drawtop=False)
        if not('gticklength' in dir(self)):
            self.gticklength=(self.gxaxisfontsize+self.gyaxisfontsize)/7.0
        lastter1=self.xmin+0
        if len(self.gxlist)>1:
            lastter1=self.gxlist[0][0]-(self.gxlist[1][0]-self.gxlist[0][0])/2
        if self.gborderwidth:
            self.vrect(x1=self.gx1,x2=self.gx2,y1=self.gy1,y2=self.gy2,stroke=self.gbordercolor,fill='',strokewidth=self.gborderwidth)
        if self.gxgrid:
            for te1 in self.gxlist:
                self.vline(x1=te1[0],x2=te1[0],y1=self.gy1-self.gticklength,y2=self.gy1,stroke=self.gmajorcolor,strokewidth=self.gmajorwidth)
                if self.gxmajor:
                    self.vline(x1=te1[0],x2=te1[0],y1=self.gy1,y2=self.gy2,stroke=self.gmajorcolor,strokewidth=self.gmajorwidth)
                if FontSizeSpecified1:
                    itemwidth1=0.0
                else:
                    itemwidth1=1.8*(te1[0]-lastter1)
                if 'gxnumrotate' in dir(self) and self.gxnumrotate!=0:
                    self.vtext(text=te1[1],xc=te1[0]-self.gxaxisfontsize/3,y2=self.gy1-self.gticklength-2*self.gborderwidth-self.gxaxisfontsize/3,font=self.gxaxisfont,color=self.gxlabelcolor,rotate=self.gxnumrotate,nonrotwidth=itemwidth1)
                else:
                    self.vtext(text=te1[1],xc=te1[0],y2=self.gy1-self.gticklength-2*self.gborderwidth,font=self.gxaxisfont,color=self.gxlabelcolor,nonrotwidth=itemwidth1)                    
                lastter1=te1[0]+te1[0]-lastter1
            for te1 in self.gxlistm:
                self.vline(x1=te1[0],x2=te1[0],y1=self.gy1-self.gticklength,y2=self.gy1,stroke=self.gminorcolor,strokewidth=self.gminorwidth)
                if self.gxminor:
                    self.vline(x1=te1[0],x2=te1[0],y1=self.gy1,y2=self.gy2,stroke=self.gminorcolor,strokewidth=self.gminorwidth)
            if 'gxnumrotate' in dir(self) and self.gxnumrotate!=0:## don't know why this is needed, probably a bug elsewhere
               self.ymin-=self.gxaxisfontsize/2 
            self.vtext(text=self.gxlabel,xc=(self.gx2+self.gx1)/2,y2=self.ymin-self.gxlabelfontsize/8,font=self.gxlabelfont,color=self.gxlabelcolor)
        if self.gygrid:
            for te1 in self.gylist:
                self.vline(y1=te1[0],y2=te1[0],x1=self.gx1-self.gticklength,x2=self.gx1,stroke=self.gmajorcolor,strokewidth=self.gmajorwidth)
                if self.gymajor:
                    self.vline(y1=te1[0],y2=te1[0],x1=self.gx1,x2=self.gx2,stroke=self.gmajorcolor,strokewidth=self.gmajorwidth)
                if 'gynumrotate' in dir(self) and self.gynumrotate!=0:
                    self.vtext(text=te1[1],yc=te1[0],x2=self.gx1-self.gticklength-self.gborderwidth,font=self.gyaxisfont,rotate=self.gynumrotate,color=self.gylabelcolor)
                else:
                    self.vtext(text=te1[1],yc=te1[0],x2=self.gx1-self.gticklength-self.gborderwidth,font=self.gyaxisfont,color=self.gylabelcolor)                    
            for te1 in self.gylistm:
                self.vline(y1=te1[0],y2=te1[0],x1=self.gx1-self.gticklength,x2=self.gx1,stroke=self.gminorcolor,strokewidth=self.gminorwidth)
                if self.gyminor:
                    self.vline(y1=te1[0],y2=te1[0],x1=self.gx1,x2=self.gx2,stroke=self.gminorcolor,strokewidth=self.gminorwidth)
            if gylabelrotate!=0:
                self.vtext(text=self.gylabel,xc=self.xmin-self.gylabelfontsize/2,yc=(self.gy2+self.gy1)/2,font=self.gylabelfont,rotate=gylabelrotate,color=self.gylabelcolor)
                ## self.xmin-=self.gylabelfontsize/2 ## don't know why this is needed, probably a bug elsewhere
            else:
                self.vtext(text=self.gylabel,x2=self.xmin-self.gylabelfontsize/2,yc=(self.gy2+self.gy1)/2,font=self.gylabelfont,color=self.gylabelcolor)
   
        self.vtext(text=self.gtitle,x=self.gtitlex,hjust=self.gtitlehjust,y1=self.gtitley+self.gaxisfontsize/2,vjust=self.gtitlevjust,font=self.gtitlefont,color=self.gtitlecolor)
        self.vset(drawtop=True)

    def vread(self,vs1):
        ## takes a string of format '<object_type item1="value" item2="value2".../> turns it into a new VSG command
        vs2=vs1.strip().strip('')
        vs2=vs2.strip("'VSGvsg\t\r\n,<>!/\\")
        vs7=vs2.split(' ',1)
        vs8=vs7[0].strip()
        vs2=vs7[1].strip()
        keys2=[]
        values2=[]
        
        while '=' in vs2:
            vs3=vs2.split('=',1)
            vs11=vs3[0].strip().replace('-','')
            keys2.append(vs11)
            vs4=vs3[1].strip()
            if vs4[0]=='"':
                vs5=vs4[1:].split('"',1)
                vs6=vs5[0]
            elif vs4[0]=="'":
                vs5=vs4[1:].split("'",1)
                vs6=vs5[0]
            else:
                vs5=vs4.split(' ',1)
                vs6=num1(vs5[0])
                if vs6=='NAN':
                    try:
                        vs6=eval(vs5[0])
                    except:
                        vs6=copy(vs5[0])
            if not vs8.lower() in ('text','tag','xlink','popup','mouseover'):
                vs9=num1(vs6)
                if vs9!='NAN':
                    vs6=copy(vs9)
            values2.append(vs6)
            if len(vs5)>1:
                vs2=vs5[1].strip()
            else:
                vs2=''
        dz2={}
        dz0=[]
        dz2['obj']=vs8.lower()
        for (v9,v10) in list(zip(keys2,values2)):
            dz2[v9]=copy(v10)
        if vs8.lower=='et':
            ## e.g. if the initial call was '<vset...>'
            self.vset(*dz0,**dz2)
        elif vs8.lower=='write':
            ## e.g. if the initial call was '<vwrite...>'
            self.vwrite(*dz0,**dz2)
        else:
            VSGitem(self,*dz0,**dz2)                              

##VSG is a single instance of a VSGcanvas that gets automatically initiated
VSG=VSGcanvas()
texttags=('popup','detail','xlink','mouseover','tag','text','font','stet')
class VSGitem:
    def __init__(s,parentcanvas,*pr1,**d1):
        """initialize a new VSG item, with significant state parameters **d1)"""
        s.canvas=parentcanvas
        for t0 in texttags:
            setattr(s,t0,'')
        d2={}  ## dictionary of parameters for item, lower case if needed, convert everything that looks like a number to float
        for d0 in d1:
            if d0.lower()=='points':
                d1[d0]=pointarray(d1[d0])
            if not d0.lower() in texttags:
                d1d0=num1(d1[d0])
                if not(d1d0=='NAN'):
                    d1[d0]=copy(d1d0)
            d2[d0.lower()]=d1[d0]
            if d0.lower()=='detail':
                s.canvas.details=True
            if d0.lower()=='xlink':
                s.canvas.xlinks=True
            if d0.lower()=='mouseover':
                s.canvas.mouseovers=True
            if d0.lower()=='popup':
                s.canvas.popups=True
            if d0.lower()=='metric':
                s.canvas.metric=d2[d0].lower()
                s.metric=d2[d0].lower()
                d2['metric']=d2[d0].lower()
        s.metric=s.canvas.metric.lower()
        ##s.obj= object types line,rect=rectangle,circle=ellipse,polygon,polyline,arc,text,space
        if 'obj' in d2:
            s.obj=d2['obj']
        else:
            s.obj='space'
        objectabbreviations1={'rectangle':'rect','circle':'ellipse','connect':'polyline'}
        if s.obj in objectabbreviations1:
            s.obj=objectabbreviations1[s.obj]

        if 'xlabel' in d2:
            if d2['xlabel'] in s.canvas.xlabels:
                d2['xc']=float(2*s.canvas.xlabels.index(d2['xlabel'])+1)*(s.canvas.xmax-s.canvas.xmin)/float(2*len(s.canvas.xlabels))+s.canvas.xmin
            else:
                if s.canvas.xlabels!=[]:
                    s.xc=d2['xc']=s.canvas.xmax+float(s.canvas.xmax-s.canvas.xmin)/float(2*len(s.canvas.xlabels))
                    s.canvas.xmax+=float(s.canvas.xmax-s.canvas.xmin)/float(2*len(s.canvas.xlabels))
                else:
                    s.xc=d2['xc']=float(s.canvas.xmax-s.canvas.xmin)/2.0
            s.canvas.xlabels.append(d2['xlabel'])
        if 'ylabel' in d2:
            if d2['ylabel'] in s.canvas.ylabels:
                s.yc=d2['yc']=float(2*s.canvas.ylabels.index(d2['ylabel'])+1)*(s.canvas.ymax-s.canvas.ymin)/float(2*len(s.canvas.ylabels))+s.canvas.ymin
            else:
                if s.canvas.ylabels!=[]:                   
                    s.yc=d2['yc']=s.canvas.ymax+float(s.canvas.ymax-s.canvas.ymin)/float(2*len(s.canvas.ylabels))
                    s.canvas.ymax+=float(s.canvas.ymax-s.canvas.ymin)/float(2*len(s.canvas.ylabels))
                else:
                    s.yc=d2['yc']=float(s.canvas.ymax-s.canvas.ymin)/2.0
            s.canvas.ylabels.append(d2['ylabel'])
    
        ## synonyms, x=x1,y=y1,cx=xc,cy=yc,dy=yd,dx=xd, etc        
        if ('x' in d2):  ## default, x, and y are upperleft of objects
            if 'hjust' in d2:
                if d2['hjust'].lower()=='start':
                    d2['x1']=d2['x']
                if d2['hjust'].lower()=='middle':
                    d2['xc']=d2['x']
                if d2['hjust'].lower()=='end':
                    d2['x2']=d2['x']
            else:
                d2['x1']=d2['x']
        if ('y' in d2):
            if 'hjust' in d2:
                if d2['vjust'].lower()=='top':
                    d2['y1']=d2['y']
                if d2['vjust'].lower()=='center':
                    d2['yc']=d2['y']
                if d2['vjust'].lower()=='bottom':
                    d2['y2']=d2['y']
            else:
                d2['y1']=d2['y']
        if ('cx' in d2):  ## default, x, and y are upperleft of objects
            d2['xc']=d2['cx']
        if ('cy' in d2):
            d2['yc']=d2['cy']
        if ('rx' in d2):  ## default, x, and y are upperleft of objects
            d2['xr']=d2['rx']
        if ('ry' in d2):
            d2['yr']=d2['ry']
        if ('rotation' in d2):
            d2['rotate']=d2['rotation']
        if ('dy' in d2):
            d2['yd']=d2['dy']
        if ('dx' in d2):
            d2['xd']=d2['dx']
        if ('color' in d2):
            if s.obj in ('rect','ellipse','line','polygon','polyline'):
                d2['stroke']=copy(d2['color'])
            else:
                d2['fill']=copy(d2['color'])

        ## if user specifies a single radius 'r' use it for both x and y axis
        if ('radius' in d2):
            d2['r']=d2['radius']
        if ('r' in d2):
            d2['xr']=d2['r']
            d2['yr']=d2['r']

        ## calculate new positions based on a displacement value (xd or yd) 
        if ('xd' in d2):
            s.canvas.xd=d2['xd']
            d2[s.canvas.xdom]=getattr(s.canvas,s.canvas.xdom)+s.xd
        if ('yd' in d2):
            s.canvas.yd=d2['yd']
            d2[s.canvas.ydom]=getattr(s.canvas,s.canvas.ydom)+s.yd

        if s.obj in ('arc','pieslice'):
            if 'ad' in d2 and not('a0' in d2):
                d2['a0']=s.canvas.cura
            
        ## whether to specify text color with stroke or fill is not intuitive.  For now, specify with either (so no chance to have outlined fonts).  This could be changed later for fancy effects.    
        if s.obj=='text':
            if 'stroke' in d2 and not('fill' in d2):
                d2['fill']=d2['stroke']

        ## deal with lists of points for polygon and polyline
        if s.obj in ['polygon','polyline']:
            if not('points' in d2):
                if len(pr1)==1:
                    d2['points']=pr1[0]
                elif len(pr1)>1:
                    d2['points']=pr1
                else:
                    if not('xd' in d2 or 'packleft' in d2 or 'packright' in d2 or 'packabove' in d2 or 'packbelow' in d2):
                        d2['xd']=copy(s.canvas.xd)
                    if not('yd' in d2 or 'packleft' in d2 or 'packright' in d2 or 'packabove' in d2 or 'packbelow' in d2):
                        d2['yd']=copy(s.canvas.yd)
                    if 'xd' in d2:
                        for px1 in s.canvas.points:
                            px1[0]+=d2['xd']
                    if 'yd' in d2:
                        for px1 in s.canvas.points:
                            px1[1]+=d2['yd']
                    d2['points']=deepcopy(s.canvas.points)
            try:
                len(d2['points'])
            except:
                d2['points']=[d2['points']]
            p0=d2['points'][:]
            s.x1=9999999999
            s.y1=9999999999
            s.x2=-9999999999
            s.y2=-9999999999
            d2['points']=[]
            cj='c'
            if 'cjust' in d2:
                cj=d2['cjust'].lower()
                s.canvas.cjust=copy(cj)
            else:
                cj=s.canvas.cjust
                
            for p1 in p0:
                try:   ## for numerical values, assume alternating x,y coordinants
                    xp=float(p1)
                    yp=float(next(p0))
                except:
                    try: ## for tuples, assume (x,y) positions
                        xp=float(p1[0])
                        yp=float(p1[1])
                    except: ## if none of the above, assume that the elements are vsg items
                        xp=p1.xc+0
                        yp=p1.yc+0
                        if 'w' in cj:
                            xp=p1.x1+0
                        if 'e' in cj:
                            xp=p1.x2+0
                        if 'n' in cj:
                            yp=p1.y1+0
                        if 'e' in cj:
                            yp=p1.y2+0
                d2['points'].append((xp,yp))
                s.x1=min(s.x1,xp)
                s.y1=min(s.y1,yp)
                s.x2=max(s.x2,xp)
                s.y2=max(s.y2,yp)
            d2['x1']=s.x1*1.0
            d2['x2']=s.x2*1.0
            d2['y1']=s.y1*1.0
            d2['y2']=s.y2*1.0
 
        ## calculate width if the user has specified radius (w=2*xr), height if the user specified height (h=2*yr); calculate yr and xr if height and width specified
        if ('width' in d2):
            d2['xr']=d2['width']/2
        if ('height' in d2):
            d2['yr']=d2['height']/2
        if ('xr' in d2):
            d2['width']=d2['xr']*2
        if ('yr' in d2):
            d2['height']=d2['yr']*2
                
        ## calculate coordinants based on whatever partial information the user has provided
        xlist1=['x1','x2','xr','xc']
        xspec1=0  ## the number of variable specified for x, 0 means use defaults for position (increment x by canvas.dx), 1 means use last width for this object also
        for i1 in xlist1:
            if i1 in d2:
                xspec1+=1
        if xspec1==0:
            d2['x1']=s.canvas.curx+min(1,len(s.canvas))*s.canvas.xd
            d2['width']=s.canvas.curwidth*1.0
            d2['xr']=s.canvas.curwidth*0.5
        ylist1=['y1','y2','yr','yc']
        if xspec1==1 and ('xr' in d2):
            d2['x1']=s.canvas.curx+s.canvas.xd
        if xspec1==1 and not('xr' in d2):
            d2['width']=s.canvas.curwidth*1.0
            d2['xr']=s.canvas.curwidth*0.5
        yspec1=0
        for i1 in ylist1:
            if i1 in d2:
                yspec1+=1
        if yspec1==0:
            d2['y1']=s.canvas.cury
            if 'x1' in d2 and d2['x1']<=s.canvas.curx:
                d2['y1']+=s.canvas.yd
            d2['height']=s.canvas.curheight*1.0
            d2['yr']=s.canvas.curheight*0.5

        if yspec1==1 and ('yr' in d2):
            d2['y1']=s.canvas.cury+s.canvas.yd
        if yspec1==1 and not('yr' in d2):
            d2['height']=s.canvas.curheight*1.0
            d2['yr']=s.canvas.curheight*0.5

        ## literal versus implicit translation of assigned values
        for d0 in d2:

            if d0.lower()=='font':
                FD1=s.canvas.splitfont(d2['font'])
                del d2[d0]
                if not('family' in FD1):
                    FD1['family']=copy(s.canvas.font['family'])
                if not('size' in FD1):
                    FD1['size']=copy(s.canvas.font['size'])
                d2['font']=deepcopy(FD1)
                s.font=deepcopy(d2['font'])
            else:
                setattr(s,d0,d2[d0])

        if s.obj=='text':
            if not('text' in d2) and len(pr1)>0:
                d2['text']=str(pr1[0])
                s.text=str(pr1[0])
            if 'x1' in d2:
                d2['hjust']='start'
                s.hjust='start'
            if 'x2' in d2:
                d2['hjust']='end'
                s.hjust='end'
            if 'xc' in d2:
                d2['hjust']='middle'
                s.hjust='middle'
            if 'y1' in d2:
                d2['vjust']='bottom'
                s.vjust='bottom'
            if 'y2' in d2:
                d2['vjust']='top'
                s.vjust='top'
            if 'yc' in d2:
                d2['vjust']='center'
                s.vjust='center'
            if 'font' not in d2:
                s.font=deepcopy(s.canvas.font)
            s.cvfont=deepcopy(s.font)
            s.font['size']=int(s.font['size'])
            s.ttffont=deepcopy(s.font)
            emb1=''
            if 'bold' in s.font['weight'].lower(): emb1+='bold '
            if 'italic' in s.font['slant'].lower(): emb1+='italic'
            if 'oblique' in s.font['slant'].lower(): emb1+='italic'
            emb1=' '+emb1.strip()
            s.ttffile=font_ttf(s.font['family']+emb1)
            s.ttffont['family']=fontbase(s.ttffile)

            if s.metric.lower()=='tk' and tkFontimported1:
                try:
                    if not(s.canvas.tkframed):
                        s.canvas.tkwindow=tk.Tk()
                        s.canvas.tkframe=tk.Frame(self.tkwindow)
                    stkf1='p'+str(s.font)
                    if not stkf1 in OpenFontsTk:
                        OpenFontsTk[stkf1]=tkFont.Font(**s.font)
                    s.tkfont=OpenFontsTk[stkf1]
                    d2['height']=s.tkfont.metrics('linespace')
                    d2['width']=s.tkfont.measure(d2['text'])
                except:
                    s.metric='pil'
                    s.canvas.metric='pil'
            if s.metric.lower()=='pil' and Imageimported1:
                try:
                    cvttf2=str((s.ttffile,s.font['size']))
                    if not cvttf2 in OpenFontsTTF1:
                        OpenFontsTTF1[cvttf2]=ImageFont.truetype(s.ttffile,s.font['size'])
                    s.pilfont=OpenFontsTTF1[cvttf2]
                    d2['width']=s.pilfont.getsize(s.text)[0]
                    d2['height']=s.pilfont.getsize(s.text)[1]
                except:
                    s.canvas.metric='lastditch'
                    s.metric='lastditch'
            if (s.metric.lower()=='pil' and not(Imageimported1)) or (s.metric.lower()=='lastditch'):
                ## A 'last ditch' attempt to make this work:
                if "mono" in str(s.font).lower() or "courier" in str(s.font).lower():
                    AveWidRatio1=1.67-0.67*(1/(2*len(s.text)+1))**0.5
                else:
                    AveWidRatio1=2.0-1.0*(1/(2*len(s.text)+1))**0.5
                if AveWidRatio1==0.0:
                    AveWidRatio1=1.0
                d2['height']=s.font['size']
                d2['width']=len(s.text)*s.font['size']/AveWidRatio1
            ## this may eventually slow the program down for large text-rich displays.
            ## an alternative would be to have a dictionary of known fonts, then check first if the current font was in that dictionary
            multilinetext1=s.text.splitlines()
            multilinenum1=len(multilinetext1)
            d2['xr']=float(d2['width'])/2
            d2['yr']=float(d2['height'])/2
            if multilinenum1>1:
                d2['text']=copy(multilinetext1[0])
                s.text=copy(multilinetext1[0])
                if 'y1' in d2:
                    d2['y1']+=d2['height']*(multilinenum1-1)
                    s.y1+=d2['height']*(multilinenum1-1)
                if 'yc' in d2:
                    d2['yc']+=float(d2['height']*(multilinenum1-1))/2.0
                    s.yc+=float(d2['height']*(multilinenum1-1))/2.0
            s.xr=d2['xr']
            s.yr=d2['yr']
            s.tkjust=tkjustD[s.hjust]
            
        if ('x1' in d2) and ('x2' in d2):
            s.xc=(s.x1+s.x2)/2.0
            s.width=s.x2-s.x1
            s.xr=s.width/2.0
            s.xdom='xc'
        if ('x1' in d2) and ('xc' in d2):
            s.xr=s.xc-s.x1
            s.width=s.xr*2
            s.x2=s.x1+s.width
            s.xdom='xc'
        if ('x1' in d2) and ('xr' in d2):
            s.xc=s.xr+s.x1
            s.width=s.xr*2
            s.x2=s.x1+s.width
            s.xdom='x1'
        if ('x2' in d2) and ('xc' in d2):
            s.xr=s.x2-s.xc
            s.width=s.xr*2
            s.x1=s.x2-s.width
            s.xdom='xc'
        if ('x2' in d2) and ('xr' in d2):
            s.xc=s.x2-s.xr
            s.width=s.xr*2
            s.x1=s.x2-s.width
            s.xdom='x2'
        if ('xc' in d2) and ('xr' in d2):
            s.x2=s.xc+s.xr
            s.width=s.xr*2
            s.x1=s.x2-s.width
            s.xdom='xc'
        if ('y2' in d2) and ('yr' in d2):
            s.yc=s.y2-s.yr
            s.height=s.yr*2
            s.y1=s.y2-s.height
            s.ydom='y2'
        if ('y1' in d2) and ('y2' in d2):
            s.yc=(s.y1+s.y2)/2.0
            s.height=s.y2-s.y1
            s.yr=s.height/2.0
            s.ydom='yc'
        if ('y1' in d2) and ('yc' in d2):
            s.yr=s.yc-s.y1
            s.height=s.yr*2
            s.y2=s.y1+s.height
            s.ydom='yc'
        if ('y1' in d2) and ('yr' in d2):
            s.yc=s.yr+s.y1
            s.height=s.yr*2
            s.y2=s.y1+s.height
            s.ydom='y1'
        if ('y2' in d2) and ('yc' in d2):
            s.yr=s.y2-s.yc
            s.height=s.yr*2
            s.y1=s.y2-s.height
            s.ydom='yc'
        if ('yc' in d2) and ('yr' in d2):
            s.y2=s.yc+s.yr
            s.height=s.yr*2
            s.y1=s.y2-s.height
            s.ydom='yc'

        s.ycr=getattr(s,s.ydom)
        s.xcr=getattr(s,s.xdom)

        ## for several items, either take the default value from the last item added to canvas or from the explicit constructor for the current object
        ## setting stet=True in the new object call avoids resetting the underlying canvas values
        cannonicals1=['strokewidth','stroke','fill','fillopacity','font','hjust','vjust','underline','rotate','strokeopacity','a0','ad','labelfont','labeljust','labelcolor','priority','metric']
        cannonicals2=['x1','x2','y1','y2','xc','yc','strokewidth','stroke','fill','font','a0','ad','labelfont','labeljust','labelcolor']
        for v1 in cannonicals1:
            if v1 in d2:
                if (v1 in cannonicals2) and not(('stet' in d2) and d2['stet']):
                    setattr(s.canvas,v1,getattr(s,v1))
            else:
                setattr(s,v1,getattr(s.canvas,v1))
        if 'colorindex' in d2:
            if 'fill' in d2 and not 'stroke' in d2:
                d2['fillindex']=d2['colorindex']
                s.fillindex=copy(d2['colorindex'])                
            elif 'stroke' in d2 and not 'fill' in d2:
                d2['strokeindex']=d2['colorindex']
                s.strokeindex=copy(d2['colorindex'])
            else:
                d2['fillindex']=d2['colorindex']
                s.fillindex=copy(d2['colorindex'])
        if 'strokeindex' in d2:
            s.stroke=vcolor(s.stroke,self1=s.canvas,index1=s.strokeindex)
        else:
            s.stroke=vcolor(s.stroke,self1=s.canvas)
        if 'fillindex' in d2:
            s.fill=vcolor(s.fill,self1=s.canvas,index1=s.fillindex)
        else:
            s.fill=vcolor(s.fill,self1=s.canvas)        
        if 'fillkey' in d2:
            if not((s.fillkey,s.fill) in s.canvas.colorlist):
                s.canvas.colorlist.append(deepcopy((s.fillkey,(s.fill,s.fillopacity))))
        if 'strokekey' in d2:
            if not((s.strokekey,s.stroke) in s.canvas.colorlist):
                s.canvas.colorlist.append(deepcopy((s.strokekey,(s.stroke,s.strokeopacity))))
        if 'colorkey' in d2:
            if 'fill' in d2 and not 'stroke' in d2:
                NewCLitem1=deepcopy((s.colorkey,(s.fill,s.fillopacity)))
            elif 'stroke' in d2 and not 'fill' in d2:
                NewCLitem1=deepcopy((s.colorkey,(s.fill,s.stroke,s.fillopacity,s.strokeopacity,s.strokewidth)))
            elif 'stroke' in d2 and 'fill' in d2:
                NewCLitem1=deepcopy((s.colorkey,(s.fill,s.stroke,s.fillopacity,s.strokeopacity,s.strokewidth)))
            elif s.obj in ('rect','ellipse','line','polygon','polyline'):
                NewCLitem1=deepcopy((s.colorkey,(s.fill,s.stroke,s.fillopacity,s.strokeopacity,s.strokewidth)))
            else:
                NewCLitem1=deepcopy((s.colorkey,(s.canvas.fill,s.canvas.fillopacity)))                
            if not(NewCLitem1 in s.canvas.colorlist):
                s.canvas.colorlist.append(NewCLitem1)
        s.packover=False
        ## 'packover' (pack objects over the current object with no intere
        if 'packover' in d2 and d2['packover'].lower()=='true':
            s.packover=True

        ## update the canvas' points current if this has been specified
        if 'points' in dir(s) and not(('stet' in d2) and d2['stet']):
            s.canvas.points=s.points

        ## calculate minimum and maximum values for item
            ## note this assumes the TK choice of font (not the ttf font), so some
            ## text may slightly overlap edges.  Also note that this makes space for rotated
            ## text using the original font definition from Tk, may be slightly different for MVG or SVG
        if s.rotate!=0:
            x11=s.xcr+(s.x1-s.xcr)*cos(s.rotate*2*pi/360)-(s.y1-s.ycr)*sin(s.rotate*2*pi/360)
            x21=s.xcr+(s.x2-s.xcr)*cos(s.rotate*2*pi/360)-(s.y1-s.ycr)*sin(s.rotate*2*pi/360)
            x12=s.xcr+(s.x1-s.xcr)*cos(s.rotate*2*pi/360)-(s.y2-s.ycr)*sin(s.rotate*2*pi/360)
            x22=s.xcr+(s.x2-s.xcr)*cos(s.rotate*2*pi/360)-(s.y2-s.ycr)*sin(s.rotate*2*pi/360)
            s.xmin=min(x11,x12,x21,x22,s.x1,s.x2)
            s.xmax=max(x11,x12,x21,x22,s.x1,s.x2)
            y11=s.ycr+(s.y1-s.ycr)*cos(s.rotate*2*pi/360)-(s.x1-s.xcr)*sin(s.rotate*2*pi/360)
            y21=s.ycr+(s.y2-s.ycr)*cos(s.rotate*2*pi/360)-(s.x1-s.xcr)*sin(s.rotate*2*pi/360)
            y12=s.ycr+(s.y1-s.ycr)*cos(s.rotate*2*pi/360)-(s.x2-s.xcr)*sin(s.rotate*2*pi/360)
            y22=s.ycr+(s.y2-s.ycr)*cos(s.rotate*2*pi/360)-(s.x2-s.xcr)*sin(s.rotate*2*pi/360)
            s.ymin=min(y11,y12,y21,y22,s.y1,s.y2)
            s.ymax=max(y11,y12,y21,y22,s.y1,s.y2)
        else:
            s.xmin=min(s.x1,s.x2)-s.strokewidth/2.0
            s.xmax=max(s.x1,s.x2)+s.strokewidth/2.0
            s.ymin=min(s.y1,s.y2)-s.strokewidth/2.0
            s.ymax=max(s.y1,s.y2)+s.strokewidth/2.0
            
        ## pack above objects where packover has not been specified    
        if "packabove" in d2:
            da1=d2['packabove']
            packlist=[]
            for s1 in s.canvas:
                if s1.xmax+da1<s.xmin or s1.xmin>s.xmax+da1 or s1.packover or s1.ymax+da1<s.ymin:
                    continue
                packlist.append((s1.ymin-da1-s.height,s1.ymax+da1))
            packlist=sorted(packlist)
            ytemp=copy(s.ymin)
            for (ymina,yminb) in packlist:
                if ymina<ytemp:
                    ytemp=copy(yminb)
                else:
                    break
            ydel=ytemp-s.ymin
            s.y1+=ydel
            s.y2+=ydel
            s.yc+=ydel
            s.ymin+=ydel
            s.ymax+=ydel
            if 'points' in d2:
                for inde1 in range(len(s.points)): s.points[inde1][1]+=ydel

        ## pack to the left of objects where packover has not been specified    
        if "packright" in d2:
            da1=d2['packright']
            packlist=[]
            for s1 in s.canvas:
                if s1.ymax+da1<s.ymin or s1.ymin>s.ymax+da1 or s1.packover or s1.xmax+da1<s.xmin:
                    continue
                packlist.append((s1.xmin-da1-s.width,s1.xmax+da1))
            packlist=sorted(packlist)
            xtemp=s.xmin+0
            for (xmina,xminb) in packlist:
                if xmina<xtemp:
                    xtemp=copy(xminb)
                else:
                    break
            xdel=xtemp-s.xmin
            s.x1+=xdel
            s.x2+=xdel
            s.xc+=xdel
            s.xmin+=xdel
            s.xmax+=xdel
            if 'points' in d2:
                for inde1 in range(len(s.points)): s.points[inde1][0]+=xdel
            
        ## pack below objects where packover has not been specified    
        if "packbelow" in d2:
            da1=d2['packbelow']
            packlist=[]
            for s1 in s.canvas:
                if s1.xmax+da1<s.xmin or s1.xmin>s.xmax+da1 or s1.packover or s1.ymin-da1>s.ymax:
                    continue
                packlist.append((s1.ymin-da1-s.height,s1.ymax+da1))
            packlist=sorted(packlist)
            ytemp=copy(s.ymin)
            for (ymina,yminb) in packlist[::-1]:
                if yminb>ytemp:
                    ytemp=copy(ymina)
                else:
                    break
            ydel=ytemp-s.ymin
            s.y1+=ydel
            s.y2+=ydel
            s.yc+=ydel
            s.ymin+=ydel
            s.ymax+=ydel
            if 'points' in d2:
                for inde1 in range(len(s.points)): s.points[inde1][1]+=ydel

        ## pack to the right of objects where packover has not been specified    
        if "packleft" in d2:
            da1=d2['packleft']
            packlist=[]
            for s1 in s.canvas:
                if s1.ymax+da1<s.ymin or s1.ymin>s.ymax+da1 or s1.packover or s1.xmin-da1>s.xmax:
                    continue
                packlist.append((s1.xmin-da1-s.width,s1.xmax+da1))
            packlist=sorted(packlist)
            xtemp=s.xmin+0
            for (xmina,xminb) in packlist[::-1]:
                if xminb>xtemp:
                    xtemp=copy(xmina)
                else:
                    break
            xdel=xtemp-s.xmin
            s.x1+=xdel
            s.x2+=xdel
            s.xc+=xdel
            s.xmin+=xdel
            s.xmax+=xdel
            if 'points' in d2:
                for inde1 in range(len(s.points)): s.points[inde1][0]+=xdel

        ## adjust values for canvas to fit this item and to update current positions                
        ## if moving in a positive direction, reset dx and dy
        if s.x1>s.canvas.curx:
            s.canvas.xd=s.x1-s.canvas.curx
        if s.y1>s.canvas.cury:
            s.canvas.yd=s.y1-s.canvas.cury

        if not(s.stet):
            s.canvas.curx=s.x1*1.0
            s.canvas.cury=s.y1*1.0
            s.canvas.curwidth=s.width*1.0
            s.canvas.curheight=s.height*1.0

        ## keep track of whether every item in the canvas has the same x1, x2, y1, and y2 coordinants
        if len(s.canvas) and not(s.stet)>0:
               if s.x1!=s.canvas.x1: s.canvas.x1static=False
               if s.x2!=s.canvas.x2: s.canvas.x2static=False
               if s.y1!=s.canvas.y1: s.canvas.y1static=False
               if s.y2!=s.canvas.y2: s.canvas.y2static=False
        
        if s.canvas.autogrowh and not(s.stet):
            if len(s.canvas)==0:
                s.canvas.xmin=s.xmin+0
                s.canvas.xmax=s.xmax+0
            else:
                s.canvas.xmin=min(s.canvas.xmin,s.xmin)
                s.canvas.xmax=max(s.canvas.xmax,s.xmax)
        if s.canvas.autogrowv and not(s.stet):
            if len(s.canvas)==0:
                s.canvas.ymin=s.ymin+0
                s.canvas.ymax=s.ymax+0
            else:
                s.canvas.ymin=min(s.canvas.ymin,s.ymin)
                s.canvas.ymax=max(s.canvas.ymax,s.ymax)
        if s.obj in ('arc','pieslice'):
            if s.canvas.arcscale==0.0:
                s.canvas.arcscale=0.1
            s.startrad=2*pi*(0.75+s.a0/s.canvas.arcscale)
            s.endrad=2*pi*(0.75+(s.a0+s.ad)/s.canvas.arcscale)
        if s.obj in ('circle','ellipse'):
            s.startrad=0.0
            s.endrad=2*pi

        if s.canvas.drawtop:
            s.canvas.append(s)
            s.canvas.posordinal+=1
            s.ordinal=s.canvas.posordinal+0
        else:
            s.canvas[:0]=[s]
            s.canvas.negordinal-=1
            s.ordinal=s.canvas.negordinal+0
            
        if s.obj=='text' and multilinenum1>1:
            for inde in range(1,multilinenum1):
                dm1=deepcopy(d1)
                if 'Y1' in d1 or 'y1' in d1:
                    dm1['y1']=s.y1-s.height*inde
                if 'Y2' in d1 or 'y2' in d1:
                    dm1['y2']=s.y2-s.height*inde
                if 'Yc' in d1 or 'yc' in d1 or 'YC' in d1 or 'yC' in d1:
                    dm1['yc']=s.yc-s.height*inde
                dm1['text']=multilinetext1[inde]
                ## clean up dm1 of odd capitalized values
                for keym1 in dm1:
                    if keym1.lower() in ('y1','y2','yc','text') and not(keym1 in ('y1','y2','yc','text')):
                        del(dm1[keym1])
                s.canvas.vtext(**dm1)

        if 'label' in dir(s):
            s.label=str(s.label)
            if s.labelfont.lower()=='auto':
                s.labelfont=deepcopy(s.font)
            if s.labelcolor.lower()=='auto':
                if s.strokewidth>0 and s.stroke and s.stroke!='none':
                    s.labelcolor=s.stroke
                else:
                    s.labelcolor=s.fill
            if s.labeljust.lower() in ('ne','northeast'):
                s.canvas.vtext(text=s.label,font=s.labelfont,x1=s.x2+0,y1=s.y2+0,priority=1,fill=s.labelcolor,stet=True)
            if s.labeljust.lower() in ('nw','northwest'):
                s.canvas.vtext(text=s.label,font=s.labelfont,x2=s.x1+0,y1=s.y2+0,priority=1,fill=s.labelcolor,stet=True)
            if s.labeljust.lower() in ('se','southeast'):
                s.canvas.vtext(text=s.label,font=s.labelfont,x1=s.x2+0,y2=s.y1+0,priority=1,fill=s.labelcolor,stet=True)
            if s.labeljust.lower() in ('sw','southwest'):
                s.canvas.vtext(text=s.label,font=s.labelfont,x2=s.x1+0,y2=s.y1+0,priority=1,fill=s.labelcolor,stet=True)
            if s.labeljust.lower() in ('n','north'):
                s.canvas.vtext(text=s.label,font=s.labelfont,xc=s.xc+0,y1=s.y2+0,priority=1,fill=s.labelcolor,stet=True)
            if s.labeljust.lower() in ('s','south'):
                s.canvas.vtext(text=s.label,font=s.labelfont,xc=s.xc+0,y2=s.y1+0,priority=1,fill=s.labelcolor,stet=True)
            if s.labeljust.lower() in ('e','east'):
                s.canvas.vtext(text=s.label,font=s.labelfont,x1=s.x2+0,yc=s.yc+0,priority=1,fill=s.labelcolor,stet=True)
            if s.labeljust.lower() in ('w','west'):
                s.canvas.vtext(text=s.label,font=s.labelfont,x2=s.x1+0,yc=s.yc+0,priority=1,fill=s.labelcolor,stet=True)
            if s.labeljust.lower() in ('c','center','m','middle',''):
                s.canvas.vtext(text=s.label,font=s.labelfont,xc=s.xc+0,yc=s.yc+0,priority=1,fill=s.labelcolor,stet=True)


            
    def __deepcopy__(self,memo):
        selfcopy=copy(self)
        for si in list(self.__dict__.keys()):
            if si=='canvas':
                si.canvas=self.canvas
                continue
            if type(getattr(self,si))==list:
                setattr(selfcopy,si,deepcopy(getattr(self,si)))
            else:
                setattr(selfcopy,si,copy(getattr(self,si)))
        return selfcopy

# the following are routines that add and operate on elements from the default canvas, named VSG

def vline(*dz0,**dz1):
    return VSG.vline(*dz0,**dz1)
def vrect(*dz0,**dz1):
    return VSG.vrect(*dz0,**dz1)
def varc(*dz0,**dz1):
    return VSG.varc(*dz0,**dz1)
def vpolygon(*dz0,**dz1):
    return VSG.vpolygon(*dz0,**dz1)
def vpolyline(*dz0,**dz1):
    return VSG.vpolyline(*dz0,**dz1)
def vellipse(*dz0,**dz1):
    return VSG.vellipse(*dz0,**dz1)
def vdisplay(*dz0,**dz1):
    return VSG.vdisplay(*dz0,**dz1)
def vwrite(*dz0,**dz1):
    return VSG.vwrite(*dz0,**dz1)
voval=vellipse
vcircle=vellipse
velipse=vellipse
vrectangle=vrect
vsquare=vrect
vpieslice=varc
vconnect=vpolyline
def vtext(*dz0,**dz1):
    return VSG.vtext(*dz0,**dz1)
def vlegend(*dz0,**dz1):
    return VSG.vlegend(*dz0,**dz1)
def vtitle(*dz0,**dz1):
    return VSG.vtitle(*dz0,**dz1)
def vgrid(*dz0,**dz1):
    return VSG.vgrid(*dz0,**dz1)
def vcolorkey(*dz0,**dz1):
    return VSG.vcolorkey(*dz0,**dz1)
def vTKwrite(*dz0,**dz1):
    VSG.TKwrite(*dz0,**dz1)
def vMVGwrite(*dz0,**dz1):
    VSG.MVGwrite(*dz0,**dz1)
def vSVGwrite(*dz0,**dz1):
    VSG.SVGwrite(*dz0,**dz1)
def vHTML5write(*dz0,**dz1):
    VSG.HTML5write(*dz0,**dz1)
def vPILwrite(*dz0,**dz1):
    VSG.PILwrite(*dz0,**dz1)
def vclear():
    VSG.vclear()

def vset(**dz1):
    return VSG.vset(**dz1)
def vread(vt11):
    return VSG.vread(vt11)
def vinfo(**dz1):
    return VSG.vinfo(**dz1)

def svnum(a):
    ##returns a string that is an integer for any number that would round to an integer
    ## otherwise returns a string with input number at three decimal precision
    q=int(round(a*1000))
    if q%1000==0:
        return '"'+str(q//1000)+'"'
    return '"'+ '%.3f' %a+'"'
def mstr(a):
    ##returns a string that is an integer for any number that would round to an integer
    ## otherwise returns a string with input number at three decimal precision
    try:
        b=float(a)
    except:
        return str(s)
    q=int(round(b*1000))
    if q%1000==0:
        return str(q//1000)
    return '%.3f' %a

def quantaldivide(numlist,groupnum,PanelBuffer):
    '''input is
        numlist: a list of column heights or row widths
        groupnum: a number of groups to divide these items into (e.g. rows of columns)
       output is
        mindim: the minimum dimension allowing the items to be fit
        numcols: generally groupnum but may be less in special cases''' 
    n1=len(numlist)
    clmin=n1
    clheight=sum(numlist)
    clfloor=max(numlist)
    colassigntemp=[0]*n1
    heightoffsettemp=[0]*n1
    colassign=[0]*n1
    heightoffset=[0.0]*n1
    for i1 in range(n1):
        for j1 in range(i1+1,n1):
            c11=sum(numlist[i1:j1])
            if clfloor<c11<clheight:
                colsnow1=0
                j1=list(numlist[:])
                while j1!=[]:
                    y1=0
                    while (j1!=[]) and (y1+j1[0]<=c11) and (y1==0 or y1+j1[0]+PanelBuffer<=c11):
                        if y1!=0:
                            y1+=PanelBuffer
                        y1+=j1[0]            
                        j1=j1[1:]
                        colassigntemp[n1-len(j1)-1]=colsnow1
                        heightoffsettemp[n1-len(j1)-1]=y1
                    if y1>0:
                        colsnow1+=1
                if colsnow1<=groupnum:
                    clmin=colsnow1+0
                    clheight=c11+0
                    colassign=colassigntemp[:]
                    heightoffset=heightoffsettemp[:]
                else:
                    clfloor=max(c11,clfloor)
    return (clmin,clheight,colassign,heightoffset)

def VSGmontage(vl1,columns=3,PanelBuffer=0,align='RU'):
    '''takes vl1, which is a list of canvases, and columns, which is the number of columns
    and returns a new canvas which is a montage of the input canvases.  PanelBuffer is a distance between canvases.
    Align is where an element of the montage will default to if it is smaller than the unit cell (TL=Upper Left, TR=Upper Right, TC=Upper Center
    ML=Middle Left, MR=Middle Right, MC=Middle Center, BL=Bottom Left, BC=Bottom Center, BR=Bottom Right'''
    columns=int(columns)
    if columns<1:
        columns=1
    align=align.upper()
    vn1=len(vl1)
    vnew=[]
    if not('P' in align):
        rows=int(ceil(float(len(vl1))/columns))
        columnMaxWidth=[0.0 for i1 in range(columns)]
        rowMaxHeight=[0.0 for i1 in range(rows)]
        columnOffset1=[0.0 for i1 in range(columns)]
        rowOffset1=[0.0 for i1 in range(rows)]
        for i11,vs1 in enumerate(vl1):
            row11=i11//columns
            col11=i11%columns
            columnMaxWidth[col11]=max(vs1.xmax-vs1.xmin,columnMaxWidth[col11])
            rowMaxHeight[row11]=max(vs1.ymax-vs1.ymin,rowMaxHeight[row11])
        for i1 in range(rows):
            for j1 in range(i1):
                rowOffset1[i1]+=rowMaxHeight[j1]+PanelBuffer
        for i1 in range(columns):
            for j1 in range(i1):
                columnOffset1[i1]+=columnMaxWidth[j1]+PanelBuffer
        if len(vl1)==0:
            return VSGcanvas()
        for i11,vs1 in enumerate(vl1):
            row11=i11//columns
            col11=i11%columns
            if 'L' in align: xd1=vs1.xmin+0
            if 'R' in align: xd1=vs1.xmin-(columnMaxWidth[col11]-(vs1.xmax-vs1.xmin))
            if 'C' in align: xd1=vs1.xmin-(columnMaxWidth[col11]-(vs1.xmax-vs1.xmin))/2.0
            if 'U' in align: yd1=vs1.ymax+0
            if 'B' in align: yd1=vs1.ymax-(rowMaxHeight[row11]-(vs1.ymax-vs1.ymin))
            if 'C' in align: yd1=vs1.ymax-(rowMaxHeight[row11]-(vs1.ymax-vs1.ymin))/2.0
            vnew.append(vl1[i11].transform(xd=-xd1+columnOffset1[col11],yd=-yd1-rowOffset1[row11]))
        for i1 in range(len(vl1)-1):
            vnew.append(vnew[-1]+vnew[i1])
    if 'P' in align:
        itemwidths=[vs1.xmax-vs1.xmin for vs1 in vl1]
        itemheights=[vs1.ymax-vs1.ymin for vs1 in vl1]
        (h1,q1,ca1,ho1)=quantaldivide(itemheights,columns,PanelBuffer)
        columnMaxWidth=[max([0]+[itemwidths[j1] for j1 in range(vn1) if ca1[j1]==i1]) for i1 in range(columns)]
        columnOffset1=[sum(columnMaxWidth[:i1]) for i1 in range(columns)]
        for i11,vs1 in enumerate(vl1):
            vnew.append(vl1[i11].transform(xd=-vs1.xmin+columnOffset1[ca1[i11]],yd=-vs1.ymin-ho1[i11]))
        for i1 in range(len(vl1)-1):
            vnew.append(vnew[-1]+vnew[i1])
    return vnew[-1]

print('Successful import of VSG Version='+VSGVersion)

if __name__=='__main__':
    if len(sys.argv)>1:
        if os.path.isfile(sys.argv[1]):
            readexternalfile(sys.argv[1])
    else:
        ##just display some stuff
        for i1 in range(500): 
            vellipse(xc=i1*2,yc=20*sqrt(i1),r=3,xg=(i1-250)*0.001,yg=sqrt(i1)/100-0.1,fill=rgb(i1/2,255-i1/2,0),stroke="none")
            if i1%100==0:
                vsquare(xc=i1*2,yc=20*sqrt(i1),r=5,xg=(i1-250)*0.001,yg=sqrt(i1)/100-0.1,fill=blue,stroke="none",label=(i1,sqrt(i1)))
        vgrid(gxlog=False,gylog=False,gxlabel='i',gylabel='sqrt(i)',gtitle='Y=Sqrt(X): This is the VSG Test Image')
        vcolorkey(logmode=False, mincolorindex=0, maxcolorindex=500, colorvalue=(lambda x:rgb(x/2,255-x/2,0)))
        vlegend(text='VSG2 Precision Drawing Module, version '+VSGVersion)
        vlegend(text='If you are getting this image, you have run the VSG_Module.py File as a __Main__ program')
        vlegend(text='To apply VSG, import VSG_Module into your own drawing script (from VSG_Module import * )')
        vlegend(text='For Current Version of VSG_Module and Documentation, see:  https://www.dropbox.com/sh/bnn7edxaeqndohl/qxBKpqJBk7', font='Georgia 12')
        vlegend(text='Copywrite 2009-2013 Andrew Fire and Stanford University, All Rights Reserved', font='Georgia 8')

        vdisplay(filepath='VSG_Example_Image.html')
##if __name__=='__main__':
##    if len(sys.argv)>1:
##        if isfile(sys.argv[1]):
##            readexternalfile(sys.argv[1])
##    else:
##        ##just display some stuff
##        for i1 in range(500): 
##            vellipse(xc=i1*2,yc=20*sqrt(i1),r=3,xg=i1,yg=sqrt(i1),fill=rgb(i1/2,255-i1/2,0),stroke="none")
##            if i1%100==0:
##                vsquare(xc=i1*2,yc=20*sqrt(i1),r=5,xg=i1,yg=sqrt(i1),fill=blue,stroke="none",label=(i1,sqrt(i1)))
##        vgrid(gxlog=False,gylog=False,gxlabel='i',gylabel='sqrt(i)',gylabelrotate=-90,gtitle='Y=Sqrt(X): This is the VSG Test Image')
##        vcolorkey(logmode=False, mincolorindex=0, maxcolorindex=500, colorvalue=(lambda x:rgb(x/2,255-x/2,0)))
##        vlegend(text='VSG2 Precision Drawing Module, version '+VSGVersion)
##        vlegend(text='If you are getting this image, you have run the VSG_Module.py File as a __Main__ program')
##        vlegend(text='To apply VSG, import VSG_Module into your own drawing script (from VSG_Module import * )')
##        vlegend(text='For Current Version of VSG_Module and Documentation, see:  https://www.dropbox.com/s/8gsn92gejp3wblq/VSG_Module_Current.zip', font='Georgia 12')
##        vlegend(text='Copywrite 2009-2013 Andrew Fire and Stanford University, All Rights Reserved', font='Georgia 8')
##
##        vdisplay(filepath='VSG_Example_Image.html')

