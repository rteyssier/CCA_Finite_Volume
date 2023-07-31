# Computing infrastructure: setting up your rusty environment

We will first explain how to connect to `rusty` using `ssh` on the Terminal window of your laptop or using a Web interface. We will then explain how to set up the software environment on `rusty` using the `module load` command.

## Using the Terminal window on your laptop

You first need to install an X sever and a Terminal window manager.

For MacOS, use:

- iTerm for the Terminal window [click here to download](https://iterm2.com)
- XQuartz for the X server [click here to download](https://www.xquartz.org)

For Windows, use:

- PuTTY or KiTTY to connect remotely using the ssh protocol [click here to download](https://www.putty.org)
- Xming for the X server [click here to download](http://www.straightrunning.com/XmingNotes/)


## Connection to rusty

The simplest option to connect to the `rusty` supercomputing cluster is using the ssh protocol from a Terminal window on your laptop or using a ssh client such as PuTTY. Type in the Terminal window the following command line:

		ssh -p 61022 yourlogin@gateway.flatironinstitute.org

You will see the following prompt:

		(yourlogin@gateway.flatironinstitute.org) Verification code:

Use Google authentificator to enter the correct code. You will then see another prompt:

		(yourlogin@gateway.flatironinstitute.org) Password:

Type your own password. You have now arrived to the gateway. You can now finally enter `rusty` using:

		ssh rusty

You are now using the Terminal window on `rusty`. You need to get familiar with the Linux operating system and the corresponding language called `bash`. A few basic commands are listed here:

| Command | Examples | Description |
| :----------- | :----------- | :----------- |
| ``ls`` | ``ls``<br> ``ls -als`` | List files in current directory <br> List in long format including hidden files and file sizes|
| ``cd`` | ``cd ..`` <br> ``cd week9`` <br> ``cd ~bob/se-for-sci/content``| Change to parent directory <br> Change to directory ``week9`` <br> Change to target directory inside Bob's SE course directory|
| ``mkdir`` | ``mkdir test``| Creating a new directory called ``test`` |
| ``rmdir`` | ``rmdir test`` | Removing the directory called ``test`` |
| ``cp`` | ``cp file1.txt file2.txt`` <br> ``cp ~bob/file1.txt .`` <br> ``cp ~bob/* .`` <br> ``cp -r ~bob/se-for-sci .`` | Copy ``file1.txt`` into a new file called ``file2.txt`` <br> Copy the file called ``file1.txt`` in Bob's home directory into a new file locally keeping the same name <br> Copy all the files in Bob's home directory locally giving them the same name <br> Copy recursively the entire content of Bob's SE course directory locally keeping the same names | 
| ``rm`` | ``rm file1.txt`` <br> ``rm -rf *`` | Remove only the file called ``file1.txt`` <br> Remove recursively all files and directories without asking permission (very dangerous) |
| ``mv`` | ``mv ~bob/file1.txt file2.txt`` | Move one file into another location and with a new name |
| ``more`` | ``more file1.txt`` | Look at the file content one page at a time |
| ``man`` | ``man more`` | Look at the manual for a given Linux command |
| ``grep`` | ``grep Hello file1.txt`` | Search for string ``Hello`` inside the file ``file1.txt`` |


## Setting up your rusty environment

The software environment can be configured using the **Environment Module Package** on `rusty`. 

In order to see what software packages are available on `rusty`, type:

		module avail
		
You will see a long list of software like:

```
------------------------------------------------------------------------------------------- Global Aliases -------------------------------------------------------------------------------------------
   Blast       -> blast-plus/2.13.0       lib/arpack -> arpack-ng/3.8.0    lib/gmp     -> gmp/6.2.1       lib/mpfr     -> mpfr/3.1.6                  nvidia/nvhpc -> nvhpc/23.1
   amd/aocc    -> aocc/4.0.0              lib/boost  -> boost/1.80.0       lib/gsl     -> gsl/2.7.1       lib/netcdf   -> netcdf-c/4.9.0              openmpi4     -> openmpi/4.0.7
   healpix-cxx -> healpix/3.82            lib/eigen  -> eigen/3.4.0        lib/hdf5    -> hdf5/1.10.9     lib/openblas -> openblas/threaded-0.3.21    perl5        -> perl/5.36.0
   intel/mkl   -> intel-mkl/2020.4.304    lib/fftw2  -> fftw/2.1.5         lib/healpix -> healpix/3.82    lib/openmm   -> openmm/7.7.0                python3      -> python/3.9.15
   lib/NFFT    -> nfft/3.5.2              lib/fftw3  -> fftw/3.3.10        lib/mpc     -> mpc/1.1.0       nodejs       -> node-js/18.12.1             qt5          -> qt/5.15.7

------------------------------------------------------------------------------------------- Core (rocky8) --------------------------------------------------------------------------------------------
   amdlibm/4.0                ghostscript/9.56.1                                 libzmq/4.3.4                        pixz/1.0.7
   aocc/4.0.0                 git-lfs/3.1.2                                      likwid/5.2.2                        postgresql/12.2
   apptainer/1.1.5            git/2.39.1                                         llvm/11.1.0                         proj/7.2.1
   arpack-ng/3.8.0            gmp/6.2.1                                          magma/2.7.0                         python/3.8.15
   autotools                  gnuplot/5.4.3                                      mathematica/12.3.0                  python/3.9.15                       (D)
   blast-plus/2.13.0          go/1.19.5                                          mathematica/13.1.0       (D)        python/3.10.8
   blender/3.3.1-nix          gperftools/2.10                                    matlab/R2022b                       qt/5.15.7
   boost/libcpp-1.80.0        gpu-burn/1.1                                       mercurial/5.8                       r/4.2.2
   boost/1.80.0        (D)    grace/5.1.25                                       mpc/1.1.0                           rav1e/0.5.1-nix
   cfitsio/3.49               graphviz/2.49.0                                    mpfr/3.1.6                          rclone/1.61.1
   cgal/5.4.1                 gromacs/singlegpunode-2022.4              (D)      mplayer/2022-02-03-nix              rockstar/galaxies.2022-12-29.a9d865
   cmake/3.20.6               gromacs/skylake-singlegpunode-2022.4               mpv/0.35.0-nix                      rockstar/main.2021-09-04.36ce9e     (D)
   cmake/3.25.1        (D)    gsl/2.7.1                                          mupdf/1.18.0                        rust/1.65.0
   cuda/11.8.0         (D)    hdf5/1.8.22                                        nccl/2.14.3-1                       singularity/3.8.7
   cuda/12.0.0                hdf5/1.10.9                               (D)      netcdf-c/4.9.0                      slack/4.28.184-nix
   cudnn/8.4.0.27-11.6        hdf5/1.12.2                                        netcdf-fortran/4.6.0                slurm                               (S,L)
   curl/7.87.0                hdfview/3.1.1                                      nfft/3.5.2                          smartmontools/6.6
   disBatch/2.5               healpix/3.82                                       nix/2.11.1-nix                      sra-tools/3.0.3
   distcc/3.3.5               hwloc/2.9.0                                        nlopt/2.7.0                         stress-ng/0.12.06
   doxygen/1.9.6              idl/8.8.3                                          node-js/18.12.1                     subversion/1.14.1
   eigen/3.4.0                imagemagick/7.0.8-7                                npm/9.3.1                           swig/4.1.1
   elinks/0.15.1-nix          intel-mkl/2017.4.239                      (S)      nvhpc/23.1                          texlive/20220321
   emacs/28.2                 intel-mkl/2020.4.304                      (S,D)    nvtop/3.0.1                         texstudio/3.0.1
   feh/3.9-nix                intel-oneapi-compilers/2023.0.0                    octave/7.3.0                        tmux/3.3a
   ffmpeg/4.4.1               intel-oneapi-mkl/2023.0.0                 (S)      openblas/openmp-0.3.21   (S)        ucx/1.13.1
   ffmpeg/4.4.2-nix    (D)    intel-oneapi-mpi/2021.8.0                          openblas/single-0.3.21   (S)        udunits/2.2.28
   fftw/2.1.5                 intel-oneapi-tbb/2021.8.0                          openblas/threaded-0.3.21 (S,L,D)    unison/2.51.2
   fftw/3.3.10         (D)    intel-oneapi-vtune/2023.0.0                        openjdk/11.0.17_8                   valgrind/3.20.0
   fio/3.26                   intel-parallel-studio/professional.2020.4          openmm/7.7.0                        vim/9.0.0045
   flexiblas/3.3.0            intel-tbb/2021.7.0                                 openmpi/cuda-4.0.7                  vmd/1.9.3
   gcc/7.5.0                  jemalloc/5.2.1                                     openmpi/4.0.7            (D)        vscode/1.73.1-nix
   gcc/10.4.0          (D)    keepassxc/2.7.1                                    openvdb/10.0.0                      vtk/9.2.2
   gcc/11.3.0                 kubectl/1.25.4-nix                                 p7zip/16.02                         wecall/2.0.0
   gcc/12.2.0                 latex2html/2022.2                                  papi/6.0.0.1-fi                     xscreensaver/6.04-nix
   gdal/3.6.2                 lftp/4.9.2                                         paraview/5.10.1                     zsh/5.8
   gdb/12.1                   libffi/3.4.3                                       perl/5.36.0
   gdrcopy/2.3                libtirpc/1.2.6                                     petsc/3.18.3
   geos/3.11.1                libxc/6.1.0                                        pgplot/5.2.2

-------------------------------------------------------------------------------------- Module releases (rocky8) --------------------------------------------------------------------------------------
   cuda-dcgm            elkcat     fi-utils    jupyter-kernels             modules/2.1-20230203 (S)    modules/2.1.1-20230405 (S,L,D)
   disBatch/beta (D)    fdcache    gpfs        modules/2.0-20220630 (S)    modules/2.1-20230222 (S)
```
In order to see the list of packages already installed in your environment, type:

		module list
		Currently Loaded Modules:
  		1) modules/2.1.1-20230405 (S)   2) slurm (S)   3) openblas/threaded-0.3.21 (S)

We want now to install the Message Passing Interface (MPI) library. For this, type:

		module load openmpi4

You can check that it has been properly loaded by typing:

		module list
		Currently Loaded Modules:
  		1) modules/2.1.1-20230405 (S)   2) slurm (S)   3) openblas/threaded-0.3.21 (S)   4) openmpi/4.0.7

You can unload it by typing:

		module unload openmpi

You can check it is gone by typing:

		module list
		Currently Loaded Modules:
  		1) modules/2.1.1-20230405 (S)   2) slurm (S)   3) openblas/threaded-0.3.21 (S)

You can load these 2 important packages that we will need later for running hydro simulations:

		module load openmpi4
		module load python3

