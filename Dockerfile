FROM gcc:6

WORKDIR /usr/local/src
COPY . /usr/local/src/hdt-cpp/

# new openssl install
RUN curl https://www.openssl.org/source/openssl-1.1.1a.tar.gz | tar xz && cd openssl-1.1.1a && ./config shared --prefix=/usr/local/ && make && make install

# Python install script
# RUN export LDFLAGS="-L/usr/local/lib/"
# RUN export LD_LIBRARY_PATH="/usr/local/lib/"
# RUN export CPPFLAGS="-I/usr/local/include -I/usr/local/include/openssl"
RUN apt-get update && apt-get install build-essential checkinstall -y && apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
RUN tar -xzvf Python-3.7.2.tgz
WORKDIR /usr/local/src/Python-3.7.2
RUN export LDFLAGS="-L/usr/local/lib/" && export LD_LIBRARY_PATH="/usr/local/lib/" && export CPPFLAGS="-I/usr/local/include -I/usr/local/include/openssl" && ./configure
RUN export LDFLAGS="-L/usr/local/lib/" && export LD_LIBRARY_PATH="/usr/local/lib/" && export CPPFLAGS="-I/usr/local/include -I/usr/local/include/openssl" && make
RUN export LDFLAGS="-L/usr/local/lib/" && export LD_LIBRARY_PATH="/usr/local/lib/" && export CPPFLAGS="-I/usr/local/include -I/usr/local/include/openssl" && make install

# #python 3.7
# RUN apt-get update && apt-get upgrade -y
# RUN apt-get install build-essential -y
# # libreadline-gplv2-dev
# RUN apt-get install libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev zlib1g libncursesw5-dev libsqlite3-dev tk-dev libc6-dev libbz2-dev openssl -y
# RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
# RUN tar -xzvf Python-3.7.2.tgz
# WORKDIR /usr/local/src/Python-3.7.2
# # RUN ./configure --enable-optimizations
# RUN ./configure
# RUN make
# # RUN make altinstall
# RUN make install
WORKDIR /usr/local/src
RUN python3 --version
RUN pip3 --version

# # Install dependencies
# RUN apt-get update && apt-get -y install \
# 	build-essential \
# 	libraptor2-dev \
# 	#libserd-dev \
# 	autoconf \
# 	libtool \
# 	liblzma-dev \
# 	liblzo2-dev \
# 	zlib1g-dev 
# 	# python3.4-dev \
# 	# python3-pip

ENV PYTHONIOENCODING=utf-8

RUN ls /usr/lib/
RUN pip3 install python-config
RUN python3 /usr/lib/python3.4/config-3.4m-x86_64-linux-gnu/python-config.py --ldflags
RUN python3 /usr/lib/python3.4/config-3.4m-x86_64-linux-gnu/python-config.py --cflags

# Install more recent serd
RUN wget https://github.com/drobilla/serd/archive/v0.28.0.tar.gz \
	&& tar -xvzf *.tar.gz \
	&& rm *.tar.gz \
	&& cd serd-* \
	&& ./waf configure && ./waf && ./waf install

# Install HDT tools
# RUN cd hdt-cpp && ./autogen.sh && ./configure && make -j2 LDFLAGS='-lpython3.4m -lpthread -ldl -lutil -lm -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions' CXXFLAGS='-I/usr/include/python3.4m -I/usr/include/python3.4m -Wno-unused-result -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -flto -fuse-linker-plugin -ffat-lto-objects'
RUN cd hdt-cpp && ./autogen.sh && ./configure && make -j2 LDFLAGS='-lpython3.4m -lpthread -ldl -lutil -lm -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions' CXXFLAGS='-I/usr/include/python3.4m -I/usr/include/python3.4m -Wno-unused-result -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -flto -fuse-linker-plugin -ffat-lto-objects'

# Expose binaries
ENV PATH /usr/local/src/hdt-cpp/libhdt/tools:$PATH
RUN cd /usr/local/src/hdt-cpp/hdt_py && pip3 install .

# reset WORKDIR
WORKDIR /scripts

# Default command
CMD ["/bin/echo", "Use it with: docker run -it --rm -v /hdt/file/drirectory:/data  -v /your/script/directory:/scripts hdt_commands python3 your_script.py"]
# docker run -it --rm -v D:/dev/hdt:/data  -v D:/dev/cpp/hdt-cpp-ph/scripts:/scripts hdt_commands python3 hdt_py_script.py