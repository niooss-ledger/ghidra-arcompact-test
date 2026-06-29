# Testing Ghidra ARCompact support

This repository contains some instructions useful to test the support of ARCompact instruction set introduced by [Ghidra Pull Request #3006](https://github.com/NationalSecurityAgency/ghidra/pull/3006).
The instructions were previously published as part of [commit `f4262bc2b5b4` ("ARCompact: wire-up pcodetests")](https://github.com/niooss-ledger/ghidra/commit/f4262bc2b5b4efb32d455406f9d25ec5f3a0e7f7).

## Ghidra Dependencies

The testing environment requires some dependencies. On a system with a running X11 server, a container can be launched:

```sh
podman run -ti --rm -e DISPLAY="$DISPLAY" -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$(pwd):/ghidra" --workdir /ghidra \
    -ti docker.io/library/debian:13-slim bash
```

Then, dependencies required to build Ghidra can be installed with these commands (which are similar to the ones published to [work on eBPF](https://github.com/Ledger-Donjon/ghidra-ebpf-tests/blob/8ebec84828c32d804647564a02798b63b19a9d8c/using_ghidra_master.md)):

```sh
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install --no-install-recommends --no-install-suggests -y \
    ca-certificates \
    curl \
    file \
    gcc \
    git \
    g++ \
    make \
    patch \
    python3 \
    python3-pip \
    python3-venv \
    python3-wheel \
    unzip \
    libfontconfig1 \
    libfreetype6 \
    libgtk-3-0 \
    libx11-6 \
    libxi6 \
    libxrender1 \
    libxtst6 \
    openjdk-25-jdk

(cd /opt && \
    curl -sSL --output gradle.zip https://services.gradle.org/distributions/gradle-9.4.1-bin.zip && \
    echo '2ab2958f2a1e51120c326cad6f385153bb11ee93b3c216c5fccebfdfbb7ec6cb  gradle.zip' | sha256sum -c && \
    unzip gradle.zip && \
    rm gradle.zip ) && \
    export PATH="/opt/gradle-9.4.1/bin:$PATH"

# Ensure Gradle runs with an UTF-8 locale (select one from "locale -a")
# If Gradle failed to unzip a jar file with unicode characters, define the local and stop the Gradle server: gradle --stop
export LANG=C.utf8

# Fetch Ghidra dependencies
cd /ghidra
gradle -I gradle/support/fetchDependencies.gradle
```

## ARCompact toolchain

Ghidra relies on being able to compile some C programs to test the processor implementations, in a test suite called "pcodetests".

To build ARCompact files, the latest release for "Linux/uClibc ARC700, Little Endian" can be downloaded from <https://github.com/foss-for-synopsys-dwc-arc-processors/toolchain/releases> and extracted to a directory, here `/local/ToolChains/ARC`:

```sh
wget https://github.com/foss-for-synopsys-dwc-arc-processors/toolchain/releases/download/arc-2021.03-rc2/arc_gnu_2021.03-rc2_prebuilt_uclibc_le_arc700_linux_install.tar.gz

mkdir -p /local/ToolChains/ARC
tar -C /local/ToolChains/ARC -xzf arc_gnu_2021.03-rc2_prebuilt_uclibc_le_arc700_linux_install.tar.gz
mv /local/ToolChains/ARC/arc_gnu_2021.03-rc2_prebuilt_uclibc_le_arc700_linux_install /local/ToolChains/ARC/arc700-elf

# Create symlinks to directly invoke the compiler, with "gcc", "nm", "objdump"...
ln -s arc-linux-gcc /local/ToolChains/ARC/arc700-elf/bin/gcc
ln -s arc-linux-nm /local/ToolChains/ARC/arc700-elf/bin/nm
ln -s arc-linux-objdump /local/ToolChains/ARC/arc700-elf/bin/objdump
ln -s arc-linux-readelf /local/ToolChains/ARC/arc700-elf/bin/readelf
```

Then the test programs from Ghidra can be compiled from [`Ghidra/Extensions/SleighDevTools/pcodetest/`](https://github.com/NationalSecurityAgency/ghidra/tree/Ghidra_12.1_build/Ghidra/Extensions/SleighDevTools/pcodetest):

```sh
# Build test programs
cd /ghidra
pushd Ghidra/Extensions/SleighDevTools/pcodetest
./build --test ARC700
popd

# Copy the test programs to the test directory
mkdir -p Ghidra/Processors/ARC/data/pcodetests/
cp ../ghidra.bin/Ghidra/Test/TestResources/data/pcodetests/ARC700_GCC_O0_pcodetest.out \
    Ghidra/Processors/ARC/data/pcodetests/
cp ../ghidra.bin/Ghidra/Test/TestResources/data/pcodetests/ARC700_GCC_O3_pcodetest.out \
    Ghidra/Processors/ARC/data/pcodetests/

# Build ghidra
gradle buildGhidra

# Build Eclipse development environment
gradle prepdev eclipse buildNatives_linux64
```

The compiled files are also available in this repository, in directory [`ARC-pcodetests/`](./ARC-pcodetests/`).

## Using Eclipse

Running pcodetests requires using Eclipse, to run the right tests.
The following steps can be followed:

* Download Eclipse IDE for Java Developers from <https://eclipseide.org/>, <https://www.eclipse.org/downloads/packages/installer>, <https://www.eclipse.org/downloads/download.php?file=/oomph/epp/2024-03/R/eclipse-inst-jre-linux64.tar.gz>
* Extract the installer and run `eclipse` in it.
* Import the Ghidra project in Eclipse by following the steps documented in <https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_9.2.4_build/DevGuide.md#import-eclipse-projects>, which were later superseded by <https://github.com/NationalSecurityAgency/ghidra/blob/Ghidra_12.1_build/README.md#advanced-development>
* Select the project named `Processors ARC`
* Right click on it and select "Run As -> JUnit Test"
