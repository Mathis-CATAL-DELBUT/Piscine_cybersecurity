NAME = stockolm

all: $(NAME)

$(NAME):
						docker build -t stockolm_image .
						docker run -d --name stockolm_run stockolm_image

file:
						touch test.der test.pfx test.key test.crt test.csr test.p12 test.pem test.odt test.ott test.sxw test.stw test.uot test.3ds test.max test.3dm test.ods test.ots test.sxc test.stc test.dif test.slk test.wb2 test.odp test.otp test.sxd test.std test.uop test.odg test.otg test.sxm test.mml test.lay test.lay6 test.asc test.sqlite3 test.sqlitedb test.sql test.accdb test.mdb test.db test.dbf test.odb test.frm test.myd test.myi test.ibd test.mdf test.ldf test.sln test.suo test.cs test.c test.cpp test.pas test.h test.asm test.js test.cmd test.bat test.ps1 test.vbs test.vb test.pl test.dip test.dch test.sch test.brd test.jsp test.php test.asp test.rb test.java test.jar test.class test.sh test.mp3 test.wav test.swf test.fla test.wmv test.mpg test.vob test.mpeg test.asf test.avi test.mov test.mp4 test.3gp test.mkv test.3g2 test.flv test.wma test.mid test.m3u test.m4u test.djvu test.svg test.ai test.psd test.nef test.tiff test.tif test.cgm test.raw test.gif test.png test.bmp test.jpg test.jpeg test.vcd test.iso test.backup test.zip test.rar test.7z test.gz test.tgz test.tar test.bak test.tbk test.bz2 test.PAQ test.ARC test.aes test.gpg test.vmx test.vmdk test.vdi test.sldm test.sldx test.sti test.sxi test.602 test.hwp test.snt test.onetoc2 test.dwg test.pdf test.wk1 test.wks test.123 test.rtf test.csv test.txt test.vsdx test.vsd test.edb test.eml test.msg test.ost test.pst test.potm test.potx test.ppam test.ppsx test.ppsm test.pps test.pot test.pptm test.pptx test.ppt test.xltm test.xltx test.xlc test.xlm test.xlt test.xlw test.xlsb test.xlsm test.xlsx test.xls test.dotx test.dotm test.dot test.docm test.docb test.docx test.doc; \
						for file in test.der test.pfx test.key test.crt test.csr test.p12 test.pem test.odt test.ott test.sxw test.stw test.uot test.3ds test.max test.3dm test.ods test.ots test.sxc test.stc test.dif test.slk test.wb2 test.odp test.otp test.sxd test.std test.uop test.odg test.otg test.sxm test.mml test.lay test.lay6 test.asc test.sqlite3 test.sqlitedb test.sql test.accdb test.mdb test.db test.dbf test.odb test.frm test.myd test.myi test.ibd test.mdf test.ldf test.sln test.suo test.cs test.c test.cpp test.pas test.h test.asm test.js test.cmd test.bat test.ps1 test.vbs test.vb test.pl test.dip test.dch test.sch test.brd test.jsp test.php test.asp test.rb test.java test.jar test.class test.sh test.mp3 test.wav test.swf test.fla test.wmv test.mpg test.vob test.mpeg test.asf test.avi test.mov test.mp4 test.3gp test.mkv test.3g2 test.flv test.wma test.mid test.m3u test.m4u test.djvu test.svg test.ai test.psd test.nef test.tiff test.tif test.cgm test.raw test.gif test.png test.bmp test.jpg test.jpeg test.vcd test.iso test.backup test.zip test.rar test.7z test.gz test.tgz test.tar test.bak test.tbk test.bz2 test.PAQ test.ARC test.aes test.gpg test.vmx test.vmdk test.vdi test.sldm test.sldx test.sti test.sxi test.602 test.hwp test.snt test.onetoc2 test.dwg test.pdf test.wk1 test.wks test.123 test.rtf test.csv test.txt test.vsdx test.vsd test.edb test.eml test.msg test.ost test.pst test.potm test.potx test.ppam test.ppsx test.ppsm test.pps test.pot test.pptm test.pptx test.ppt test.xltm test.xltx test.xlc test.xlm test.xlt test.xlw test.xlsb test.xlsm test.xlsx test.xls test.dotx test.dotm test.dot test.docm test.docb test.docx test.doc; do \
							echo "Hello comment ca va ?! :D" > "$$file"; \
						done


exec:
						docker exec -it stockolm_run /bin/bash

clean:
						if [ $$(docker ps -aq) ]; then docker stop $$(docker ps -aq); fi
						if [ $$(docker ps -aq) ]; then docker rm $$(docker ps -aq); fi
						rm test*

fclean: clean
						if [ $$(docker images -q) ]; then docker rmi $$(docker images -q); fi
						docker system prune -af

re :    fclean $(NAME)

.PHONY: all clean fclean re