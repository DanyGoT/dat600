{
  description = "DAT560 - Python 3.12 development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.uv
            pkgs.stdenv.cc.cc.lib
          ];

          shellHook = ''
            export PYTHON=${python}/bin/python
            export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"
            if [ ! -d .venv ]; then
              echo "Creating virtual environment with Python 3.12..."
              uv venv --python ${python}/bin/python
            fi
            source .venv/bin/activate
            find . -type f -name "requirements.txt" | sort | while read req; do
              echo "Installing from $req..."
              uv pip install -r "$req"
            done
          '';
        };
      }
    );
}
