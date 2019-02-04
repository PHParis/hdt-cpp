FROM gcc:6

WORKDIR /usr/local/src
COPY . /usr/local/src/hdt-cpp/

# Install dependencies
RUN apt-get update && apt-get -y install \
	build-essential \
	libraptor2-dev \
	#libserd-dev \
	autoconf \
	libtool \
	liblzma-dev \
	liblzo2-dev \
	zlib1g-dev \
	python3.4-dev \
	python3-pip

ENV PYTHONIOENCODING=utf-8

# RUN pip3 install python-config
# RUN python3 /usr/lib/python3.4/config-3.4m-x86_64-linux-gnu/python-config.py --ldflags
# RUN python3 /usr/lib/python3.4/config-3.4m-x86_64-linux-gnu/python-config.py --cflags
# # RUN find / -name "*python-config*"
# # RUN python3-config --cflags --ldflags
# # REPONSE: python3-config: not found

# Install more recent serd
RUN wget https://github.com/drobilla/serd/archive/v0.28.0.tar.gz \
	&& tar -xvzf *.tar.gz \
	&& rm *.tar.gz \
	&& cd serd-* \
	&& ./waf configure && ./waf && ./waf install

# Install HDT tools
# RUN cd hdt-cpp && ./autogen.sh && ./configure && make -j2 LDFLAGS='-lpython3.4m -lpthread -ldl -lutil -lm -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions' CXXFLAGS='-I/usr/include/python3.4m -I/usr/include/python3.4m -Wno-unused-result -DNDEBUG -g -fwrapv -O2-Wall -Wstrict-prototypes -g -fstack-protector-strong -Wformat -Werror=format-security -g -flto -fuse-linker-plugin -ffat-lto-objects'
RUN cd hdt-cpp && ./autogen.sh && ./configure && make -j2 LDFLAGS='-lpython3.4m -lpthread -ldl -lutil -lm -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions' CXXFLAGS='-I/usr/include/python3.4m -I/usr/include/python3.4m -Wno-unused-result -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -flto -fuse-linker-plugin -ffat-lto-objects'
# RUN cd hdt-cpp && ./autogen.sh && ./configure && make -j2 LDFLAGS='-L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu -L/usr/lib -lpython3.7m -lpthread -ldl  -lutil -lm  -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions' CXXFLAGS='-I/usr/include/python3.7m -I/usr/include/python3.7m  -Wno-unused-result -Wsign-compare -g -fdebug-prefix-map=/build/python3.7-OVBDgQ/python3.7-3.7.1=. -specs=/usr/share/dpkg/no-pie-compile.specs -fstack-protector -Wformat -Werror=format-security  -DNDEBUG -g -fwrapv -O3 -Wall'

# Expose binaries
ENV PATH /usr/local/src/hdt-cpp/libhdt/tools:$PATH
# ENV PATH /usr/local/src/hdt-cpp/hdt_py/hdt_py:$PATH
RUN cd /usr/local/src/hdt-cpp/hdt_py && pip3 install .

# reset WORKDIR
WORKDIR /scripts

# Default command
CMD ["/bin/echo", "Use it with: docker run -it --rm -v /hdt/file/drirectory:/data  -v /your/script/directory:/scripts hdt_commands python3 your_script.py"]
# docker run -it --rm -v D:/dev/hdt:/data  -v D:/dev/cpp/hdt-cpp-ph/scripts:/scripts hdt_commands python3 hdt_py_script.py