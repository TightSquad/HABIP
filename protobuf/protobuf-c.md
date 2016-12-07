# Building Protoc-c and libprotobuf-c locally

1. Download from: https://github.com/protobuf-c/protobuf-c/releases

2. Configure with: `$ mkdir -p out && ./configure --prefix=$(pwd)/out --disable-shared`

3. Build and install with: `$ make && make install`

4. Compile with:

	`$ gcc example/Accessor.c example/tutorial.pb-c.c -o example/Accessor -I protobuf-c-1.2.1/out/include/ -L protobuf-c-1.2.1/out/lib/ -lprotobuf-c`

# Cross compiling libprotobuf-c

1. Install the MSP430 cross compiler, add to system path

	TODO: WRITE UP HOW TO INSTALL THAT

2. Download from: https://github.com/protobuf-c/protobuf-c/releases

3. Configure with: 

	> `$ export CFLAGS="-g -O2 -s"`

	> `$ mkdir -p out && ./configure --prefix=$(pwd)/out --disable-shared --disable-protoc --host msp430-elf`

4. Build and install with: `$ make && make install`

5. Strip the shared library of any unnecessary symbols: `$ msp430-elf-strip --strip-unneeded out/lib/libprotobuf-c.a`

# Cross compile the program for the MSP430

1. Build the program against the static library from the previous step

2. Strip the symbols except debug with: `$ msp430-elf-strip --only-keep-debug output-executable`