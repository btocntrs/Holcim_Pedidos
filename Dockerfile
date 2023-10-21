FROM python
 
ENV DEBIAN_FRONTEND noninteractive
 
RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       firefox-esr \
       tesseract-ocr \
   && pip install  \
       requests \
       selenium

RUN pip install pillow pytesseract openpyxl

# Add latest FireFox
RUN set -x \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://ftp.mozilla.org/pub/firefox/releases/118.0/linux-x86_64/en-US/firefox-118.0.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox
  
# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/
 
COPY ./app /app
 
WORKDIR /app
 
CMD python ./main.py
