{pkgs, stdenv, buildEnv, ...}:
let myPythonEnv = stdenv.mkDerivation rec {
  name = "myPythonEnv";
  env = buildEnv { name = name; paths = buildInputs; };
  builder = builtins.toFile "builder.sh" ''
    source $stdenv/setup; ln -s $env $out
  '';

  buildInputs = [
    pkgs.python27Packages.influxdb
    pkgs.python27Packages.requests2
    pkgs.python27Packages.pytz
    pkgs.python27Packages.dateutil
    pkgs.python27Packages.six
    pkgs.python27
  ];
};

in

stdenv.mkDerivation rec {
  name = "bierboerse-${version}";
  version = "0.0.1-SNAPSHOT";

  src = ./.;
  
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
    cp data.json $out/bin
    chmod +x $out/bin/bierboerse.py
#    ln -s ${myPythonEnv}/lib $out
    exit 0
  '';
}
