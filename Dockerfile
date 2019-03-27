FROM gcc:8

WORKDIR /usr/local/src
COPY . /usr/local/src/hdt-cpp/

#python 3.7
RUN apt-get update && apt-get install build-essential checkinstall -y && apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
RUN tar -xzvf Python-3.7.2.tgz
WORKDIR /usr/local/src/Python-3.7.2
RUN ./configure --enable-shared
# RUN ./configure --enable-shared --enable-optimizations
# RUN ./configure --enable-optimizations
RUN make
RUN make install
# RUN find /usr -name "Python.h"
# RUN find / -name "libpython3.7m.so.1.0"
ENV LD_LIBRARY_PATH=/usr/local/lib/
# RUN /usr/local/bin/python3.7-config --cflags
# RUN /usr/local/bin/python3.7-config --ldflags
# RUN /usr/local/bin/python3.7-config --ldflags

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

ENV PYTHONIOENCODING=utf-8

WORKDIR /usr/local/src

# Install dependencies
RUN apt-get update && apt-get -y install \
	build-essential \
	libraptor2-dev \
	autoconf \
	libtool \
	liblzma-dev \
	liblzo2-dev \
	zlib1g-dev

# Install more recent serd
RUN wget https://github.com/drobilla/serd/archive/v0.28.0.tar.gz \
	&& tar -xvzf *.tar.gz \
	&& rm *.tar.gz \
	&& cd serd-* \
	&& ./waf configure && ./waf && ./waf install

# Install HDT tools -fPIC 
RUN cd hdt-cpp && ./autogen.sh && ./configure && make -j2 LDFLAGS='-L/usr/local/lib/python3.7/config-3.7m-x86_64-linux-gnu -L/usr/local/lib -lpython3.7m -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic' CXXFLAGS='-I/usr/local/include/python3.7m -I/usr/local/include/python3.7m  -Wno-unused-result -Wsign-compare  -DNDEBUG -g -fwrapv -O3 -Wall'

# Expose binaries
ENV PATH /usr/local/src/hdt-cpp/libhdt/tools:$PATH
# install hdt py
RUN cd /usr/local/src/hdt-cpp/hdt_py && pip3 install .

# reset WORKDIR
WORKDIR /scripts

# Default command
CMD ["/bin/echo", "Use it with: docker run -it --rm -v /hdt/file/directory:/data  -v /your/script/directory:/scripts hdt_commands python3 your_script.py"]
# docker run -it --rm -v D:/dev/hdt:/data  -v D:/dev/cpp/hdt-cpp-ph/scripts:/scripts hdt_commands python3 hdt_py_script.py