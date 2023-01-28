#!/usr/bin/env python3

"""Script to send Icinga2 notifications to Discord channel via webhook"""
import sys
import argparse
import urllib.parse
import requests

parser = argparse.ArgumentParser(
    prog = 'Icinga2 Discord Notification',
    description = 'Script to send Icinga2 notifications to Discord channel via webhook',
)

parser.add_argument('-v', dest = 'verbose', action = 'count', default = 0)

parser.add_argument('-r', dest = 'discord_url', metavar = 'Discord webhook url', required = True)
parser.add_argument('-i', dest = 'icinga2_url', metavar = 'Icinga2 web url')

parser.add_argument('-t', dest = 'notification_type', metavar = 'Notification type', required = True)
parser.add_argument('-b', dest = 'notification_author', metavar = 'Notification author', nargs = '?', default = '')
parser.add_argument('-c', dest = 'notification_comment', metavar = 'Notification comment', nargs = '?', default = '')
parser.add_argument('-d', dest = 'notification_timestamp', metavar = 'Notification timestamp', required = True)
parser.add_argument('-x', dest = 'notification_notes', metavar = 'Notification notes', nargs = '?', default = '')

parser.add_argument('-s', dest = 'check_state', metavar = 'Host/Service state', required = True)
parser.add_argument('-o', dest = 'check_output', metavar = 'Host/Service output', required = True)

parser.add_argument('-l', dest = 'host_name', metavar = 'Host name', required = True)
parser.add_argument('-n', dest = 'host_display_name', metavar = 'Host display name', required = True)
parser.add_argument('-4', dest = 'host_address', metavar = 'Host IPv4 address', nargs = '?', default = '')
parser.add_argument('-6', dest = 'host_address6', metavar = 'Host IPv6 address', nargs = '?', default = '')

parser.add_argument('-e', dest = 'service_name', metavar = 'Service name', nargs = '?')
parser.add_argument('-u', dest = 'service_display_name', metavar = 'Service display name', nargs = '?')

args = parser.parse_args()


# Dict
NOTIFICATION_VARS = {
    'check_type': 'host',
    'discord_username': 'Icinga2 Monitoring',
    'embed_color': 0,
    'embed_title': f'[{args.notification_type} Notification] ',
    'embed_fields': [],
}


# Is check host or service check?
if args.service_name is not None:
    NOTIFICATION_VARS['check_type'] = 'service'


# Embed color based on state
if args.check_state in ('UP', 'OK'):
    #006400
    NOTIFICATION_VARS['embed_color'] = 25600
elif args.check_state == 'WARNING':
    #B96500
    NOTIFICATION_VARS['embed_color'] = 12150016
elif args.check_state in ('DOWN', 'CRITICAL'):
    #8B0000
    NOTIFICATION_VARS['embed_color'] = 9109504
elif args.check_state == 'UNKNOWN':
    #800080
    NOTIFICATION_VARS['embed_color'] = 8388736


# Embed title
if NOTIFICATION_VARS['check_type'] == 'host':
    NOTIFICATION_VARS['embed_title'] += f'Host {args.host_display_name}'
else:
    NOTIFICATION_VARS['embed_title'] += f'Service {args.service_display_name} on {args.host_display_name}'

NOTIFICATION_VARS['embed_title'] += f' - {args.check_state})'


# Embed fields
NOTIFICATION_VARS['embed_fields'].append({
    'name': 'Hostname',
    'value': args.host_name,
})

if args.host_address != '':
    NOTIFICATION_VARS['embed_fields'].append({
        'name': 'IPv4 address',
        'value': args.host_address,
    })

if args.host_address6 != '':
    NOTIFICATION_VARS['embed_fields'].append({
        'name': 'IPv6 address',
        'value': args.host_address6,
    })

NOTIFICATION_VARS['embed_fields'].append({
    'name': 'Notification date',
    'value': args.notification_timestamp,
})

if args.notification_comment != '':
    embed_comment = args.notification_comment

    if args.notification_author != '':
        embed_comment += f' ({args.notification_author})'

    NOTIFICATION_VARS['embed_fields'].append({
        'name': 'Comment',
        'value': embed_comment,
    })

if args.notification_notes != '':
    NOTIFICATION_VARS['embed_fields'].append({
        'name': 'Notes',
        'value': args.notification_notes,
    })

if args.icinga2_url is not None:
    args.icinga2_url = args.icinga2_url.rstrip('/')
    args.icinga2_url += '/monitoring/'

    if NOTIFICATION_VARS['check_type'] == 'host':
        args.icinga2_url += \
            f'host/show?host={urllib.parse.quote(args.host_name)}'
    else:
        args.icinga2_url += \
            f'service/show?host={urllib.parse.quote(args.host_name)}' \
            f'&service={urllib.parse.quote(args.service_name)}'

    NOTIFICATION_VARS['embed_fields'].append({
        'name': 'Icinga2 web',
        'value': args.icinga2_url,
    })


# Request
req_data = {
    'username': NOTIFICATION_VARS['discord_username'],
    'embeds': [{
        'title': NOTIFICATION_VARS['embed_title'],
        'color': NOTIFICATION_VARS['embed_color'],
        'author': {
            'name': NOTIFICATION_VARS['discord_username'],
        },
        'description': args.check_output,
        'fields': NOTIFICATION_VARS['embed_fields'],
    }],
}

if args.verbose >= 1:
    print(req_data)

try:
    res = requests.post(args.discord_url, json = req_data, timeout = 10)

    if args.verbose >= 1:
        print(res.text)
except requests.exceptions.RequestException as e:
    raise SystemExit(e) from e


sys.exit(0)
