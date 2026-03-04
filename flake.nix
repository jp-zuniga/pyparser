{
  description = "Local development environment!";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";

  outputs = {
    self,
    nixpkgs,
  }: let
    systems = [
      "x86_64-darwin"
      "x86_64-linux"
      "aarch64-darwin"
      "aarch64-linux"
    ];

    forAllSystems = nixpkgs.lib.genAttrs systems;
    nixpkgsFor = forAllSystems (system: nixpkgs.legacyPackages.${system});
  in {
    devShells = forAllSystems (system: let
      pkgs = nixpkgsFor.${system};
    in {
      default = pkgs.mkShell {
        buildInputs = [
          pkgs.just
          pkgs.just-lsp
          pkgs.uv
        ];
      };
    });
  };
}
