{ pkgs }: {
  deps = [
    pkgs.python312
    pkgs.python312Packages.pip
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
    ];
  };
}