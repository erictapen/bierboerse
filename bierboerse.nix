{ config, pkgs, lib, ... }:

with lib;

let 

  cfg = config.bierboerse;

in

{

  options = {
    bierboerse = {
      enable = mkOption {
        default = false;
        description = ''
          Hier kann die Bierbörse aktiviert werden.
        '';
        type = types.bool;
      }; 
    };
  };

  config = mkIf cfg.enable {
    services.influxdb.enable = true;
    services.grafana = {
      enable = true;
      addr = "0.0.0.0";
      security.adminUser = "admin";
      security.adminPassword = "I2uKPanFTaRCVEG";
    };
    environment.systemPackages = [
      pkgs.influxdb
    ];
    systemd.services.bierboerse = {
      after = [ "network.target" "influxdb.service" ];
      wantedBy = [ "multi-user.target" ];
    };
    preStart = ''
      ${pkgs.influx} -execute "create database bierboerse"
    '';
  };
}
