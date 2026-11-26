import math
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.graphics.shapes import Drawing, Rect, Line, Polygon, String, Circle
D="/usr/share/fonts/truetype/dejavu/"
for n,f in [("DV","DejaVuSans.ttf"),("DVB","DejaVuSans-Bold.ttf"),("DVI","DejaVuSans-Oblique.ttf"),("DVM","DejaVuSansMono.ttf")]:
    pdfmetrics.registerFont(TTFont(n,D+f))
addMapping("DV",0,0,"DV");addMapping("DV",1,0,"DVB");addMapping("DV",0,1,"DVI");addMapping("DV",1,1,"DVB")
NAVY=colors.HexColor("#1F3A5F"); ACC=colors.HexColor("#E07A2E"); LIGHT=colors.HexColor("#F4F6FA"); LINE=colors.HexColor("#D5DBE5")
GREY=colors.HexColor("#5A6472"); WARM=colors.HexColor("#FFF4EA"); RED=colors.HexColor("#C0392B"); REDL=colors.HexColor("#FDECEA")
GREEN=colors.HexColor("#1E8449"); GREENL=colors.HexColor("#E9F7EF"); BLUEL=colors.HexColor("#E8F0FB"); KAF=colors.HexColor("#2C2C2C")
PURP=colors.HexColor("#6C3483"); PURPL=colors.HexColor("#F4ECF7"); FADE=colors.HexColor("#E3E3E3")
body=ParagraphStyle("b",fontName="DV",fontSize=9.4,leading=13.4,textColor=colors.HexColor("#222"))
small=ParagraphStyle("sm",parent=body,fontSize=8.4,leading=11.5,textColor=GREY)
lab=ParagraphStyle("l",parent=body,fontName="DVB",textColor=NAVY)
title=ParagraphStyle("t",fontName="DVB",fontSize=24,leading=29,textColor=NAVY)
sub=ParagraphStyle("s",fontName="DV",fontSize=10.5,leading=14,textColor=GREY)
h1=ParagraphStyle("h1",fontName="DVB",fontSize=14.5,leading=19,textColor=NAVY,spaceBefore=8,spaceAfter=6,keepWithNext=1)
h1n=ParagraphStyle("h1n",parent=h1,keepWithNext=0)
h3=ParagraphStyle("h3",fontName="DVB",fontSize=10.5,leading=14,textColor=NAVY,spaceBefore=4,spaceAfter=3,keepWithNext=1)
cap=ParagraphStyle("cap",parent=small,alignment=1,fontName="DVI")
kw=ParagraphStyle("kw",parent=small,keepWithNext=1)
W=A4[0]-36*mm; DW=W-16
def M(t): return f"<font name='DVM' size='8.6'>{t}</font>"
def dbox(d,x,y,w,h,text,fill,stroke,fs=8,tc=colors.black,bold=True):
    d.add(Rect(x,y,w,h,rx=5,ry=5,fillColor=fill,strokeColor=stroke,strokeWidth=1.2))
    lines=text.split("\n"); lh=fs+2.5; start=y+h/2+(len(lines)-1)*lh/2-fs/3
    for i,l in enumerate(lines):
        d.add(String(x+w/2,start-i*lh,l,fontName="DVB" if (bold and i==0) else "DV",fontSize=fs if i==0 else fs-1,fillColor=tc,textAnchor="middle"))
def arrow(d,x1,y1,x2,y2,col=GREY,w=1.3,dash=None,head=6):
    d.add(Line(x1,y1,x2,y2,strokeColor=col,strokeWidth=w,strokeDashArray=dash)); a=math.atan2(y2-y1,x2-x1)
    d.add(Polygon([x2,y2,x2-head*math.cos(a-0.4),y2-head*math.sin(a-0.4),x2-head*math.cos(a+0.4),y2-head*math.sin(a+0.4)],fillColor=col,strokeColor=col))
def txt(d,x,y,s,fs=7.5,col=GREY,anchor="middle",font="DV"):
    d.add(String(x,y,s,fontName=font,fontSize=fs,fillColor=col,textAnchor=anchor))
def frame(drw,bg=colors.white):
    t=Table([[drw]],colWidths=[W]); t.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.6,LINE),("BACKGROUND",(0,0),(-1,-1),bg),("ALIGN",(0,0),(-1,-1),"CENTER"),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),6)])); return t
def box(html,bg=WARM,bar=ACC,style=body):
    t=Table([[Paragraph(html,style)]],colWidths=[W]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("LINEBEFORE",(0,0),(0,-1),3,bar),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)])); return t
def table(rows,widths,header=True,hbg=NAVY):
    data=[[Paragraph(c,ParagraphStyle("th",parent=body,fontName="DVB",textColor=colors.white) if (header and r==0) else body) for c in row] for r,row in enumerate(rows)]
    t=Table(data,colWidths=widths,repeatRows=1 if header else 0)
    st=[("BOX",(0,0),(-1,-1),0.6,LINE),("INNERGRID",(0,0),(-1,-1),0.4,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]
    if header: st.append(("BACKGROUND",(0,0),(-1,0),hbg))
    for r in range(1 if header else 0,len(rows)):
        if r%2==0: st.append(("BACKGROUND",(0,r),(-1,r),LIGHT))
    t.setStyle(TableStyle(st)); return t
def _ans(a,follow):
    rows=[[Paragraph(a,body)]]
    if follow: rows.append([Paragraph(f'<font color="#E07A2E"><b>Likely follow-up:</b></font> {follow}',small)])
    b=Table(rows,colWidths=[W]); b.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.6,LINE),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)])); return b
def qa(n,q,a,follow=None,tag="S"):
    head=Table([[Paragraph(f'<font color="white"><b>{tag}{n}</b></font>',body),Paragraph(f"<b>{q}</b>",body)]],colWidths=[13*mm,W-13*mm])
    head.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),PURP),("BACKGROUND",(1,0),(1,0),PURPL),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return KeepTogether([head,_ans(a,follow),Spacer(1,8)])
def qa_l(n,q,a,label,follow=None):
    lc={"Very common":RED,"Common":ACC,"Good to know":GREEN}[label]
    head=Table([[Paragraph(f'<font color="white"><b>Q{n}</b></font>',body),Paragraph(f"<b>{q}</b>",body),Paragraph(f'<font color="white"><b>{label}</b></font>',ParagraphStyle("lb",parent=small,alignment=1,textColor=colors.white))]],colWidths=[12*mm,W-40*mm,28*mm])
    head.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),NAVY),("BACKGROUND",(1,0),(1,0),LIGHT),("BACKGROUND",(2,0),(2,0),lc),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    return KeepTogether([head,_ans(a,follow),Spacer(1,8)])
def code(t):
    st=ParagraphStyle("code",fontName="DVM",fontSize=8.4,leading=11.6,textColor=colors.HexColor("#1b1b1b"))
    p=Paragraph(t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>").replace("  ","&nbsp;&nbsp;"),st)
    tb=Table([[p]],colWidths=[W]); tb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F7F7F9")),("BOX",(0,0),(-1,-1),0.6,LINE),("LEFTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)])); return tb
def mkfoot(label):
    def foot(cv,doc):
        cv.saveState(); cv.setFont("DV",8); cv.setFillColor(GREY)
        cv.drawString(18*mm,10*mm,label); cv.drawRightString(A4[0]-18*mm,10*mm,f"Page {doc.page}")
        cv.setStrokeColor(ACC); cv.setLineWidth(2); cv.line(18*mm,A4[1]-12*mm,A4[0]-18*mm,A4[1]-12*mm); cv.restoreState()
    return foot
def build(path,title_,flow):
    doc=SimpleDocTemplate(path,pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=16*mm,title=title_)
    doc.build(flow,onFirstPage=mkfoot(title_),onLaterPages=mkfoot(title_))
def preview(path,prefix,cols=3,res=40):
    import subprocess,glob
    from PIL import Image
    for f in glob.glob(prefix+"-*.png"):
        import os; os.remove(f)
    subprocess.run(["pdftoppm","-r",str(res),"-png",path,prefix])
    f=sorted(glob.glob(prefix+"-*.png")); ims=[Image.open(x) for x in f]; n=len(ims); rows=(n+cols-1)//cols
    o=Image.new('RGB',(ims[0].width*cols,ims[0].height*rows),'white')
    for i,im in enumerate(ims): o.paste(im,((i%cols)*im.width,(i//cols)*im.height))
    o.save(prefix+"_all.png"); return n
