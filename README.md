# Monitoring Discord Webhook
Script to send monitoring (e.g. Icinga2) notifications to Discord via webhook

## Usage

```
usage: Icinga2 Discord Notification [-h] [-v] -r Discord webhook url
                                    [-i Icinga2 web url] -t Notification type -b
                                    Notification author -c Notification comment -d
                                    Notification timestamp [-x Notification notes] -s
                                    Host/Service state -o Host/Service output -l Host
                                    name -n Host display name [-4 Host IPv4 address]
                                    [-6 Host IPv6 address] [-e Service name]
                                    [-u Service display name]
```


## Arguments

| Argument | Description | Required |
| - | - | - |
| -r | Discord webhook | y |
| -i | Icinga2 web url | n |
| -t | `$notification.type$` | y |
| -b | `$notification.author$` | n |
| -c | `$notification.comment$` | n |
| -d | `$icinga.long_date_time$` | y |
| -x | `$notification.notes$` | n |
| -s | `$host.state$` / `$service.state$` | y |
| -o | `$host.output$` / `$service.output$` | y |
| -l | `$host.name$` | y |
| -n | `$host.display_name$` | y |
| -4 | `$host.address$` | n |
| -6 | `$host.address6$` | n |
| -e | `$service.name$` | n |
| -u | `$service.display_name$` | n |


## Requirements

Debian based distributions (e.g. Ubuntu):

```sh
apt install python3 python3-requests python3-urllib3
```
