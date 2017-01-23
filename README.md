This is more a practice in deploying services on NixOS than an actual serious project.

# Deployment

Clone this repository and add this code to your global NixOS conf, e.g. in your `/etc/nixos/configuration.nix`:
```
imports = [
  ... stuff you already had there
  /path/to/bierboerse/bierboerse.nix
];

...

services.bierboerse.enable = true;
```

This is experimental yet.
