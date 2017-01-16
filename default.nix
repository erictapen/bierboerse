{pkgs, stdenv, buildEnv, ...}:
#with import <nixpkgs> {};
let myPythonEnv = stdenv.mkDerivation rec {
  name = "myPythonEnv";
  env = buildEnv { name = name; paths = buildInputs; };
  builder = builtins.toFile "builder.sh" ''
    source $stdenv/setup; ln -s $env $out
  '';

  buildInputs = [
    pkgs.python27Packages.influxdb
    pkgs.python27Packages.requests
    pkgs.python27
  ];
};

in

stdenv.mkDerivation {
  name = "bierboerse-0.0.1-SNAPSHOT";

  src = pkgs.fetchgit {
    url =  "https://github.com/erictapen/bierboerse.git";
    rev = "a8c8cd35ecf9e6cfeac4706ca9017727297f06bd";
    sha256 = "14m0gy75hqyrmid68d15r7cskxnf7w4526n8l5vrpmizgralvr8k";
  };
  
  buildInputs = [
    myPythonEnv
  ];

  buildPhase = ''
    echo buildfase
  '';

  installPhase = ''
    echo installfase
    mkdir -p $out/bin
    echo '#!${myPythonEnv}/bin/python2.7' > temp
    cat temp bierboerse.py > $out/bin/bierboerse.py
#    cp bierboerse.py $out/bin
    chmod +x $out/bin/bierboerse.py
#    ln -s ${myPythonEnv}/lib $out
    exit 0
  '';
 
}
