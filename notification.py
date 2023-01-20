#!/usr/bin/env python3

import sys
import argparse
import requests
import urllib.parse

parser = argparse.ArgumentParser(
    prog = 'Icinga2 Discord Notification',
    description = 'Script to send Icinga2 notifications to Discord channel via webhook',
)

parser.add_argument('-v', dest = 'verbose', action = 'count', default = 0)

parser.add_argument('-r', dest = 'discord_url', metavar = 'Discord webhook url', required = True)
parser.add_argument('-i', dest = 'icinga2_url', metavar = 'Icinga2 web url')

parser.add_argument('-t', dest = 'notification_type', metavar = 'Notification type', required = True)
parser.add_argument('-b', dest = 'notification_author', metavar = 'Notification author')
parser.add_argument('-c', dest = 'notification_comment', metavar = 'Notification comment')
parser.add_argument('-d', dest = 'notification_timestamp', metavar = 'Notification timestamp', required = True)
parser.add_argument('-x', dest = 'notification_notes', metavar = 'Notification notes')

parser.add_argument('-s', dest = 'check_state', metavar = 'Host/Service state', required = True)
parser.add_argument('-o', dest = 'check_output', metavar = 'Host/Service output', required = True)

parser.add_argument('-l', dest = 'host_name', metavar = 'Host name', required = True)
parser.add_argument('-n', dest = 'host_display_name', metavar = 'Host display name', required = True)
parser.add_argument('-4', dest = 'host_address', metavar = 'Host IPv4 address', default = '')
parser.add_argument('-6', dest = 'host_address6', metavar = 'Host IPv6 address', default = '')

parser.add_argument('-e', dest = 'service_name', metavar = 'Service name')
parser.add_argument('-u', dest = 'service_display_name', metavar = 'Service display name')

args = parser.parse_args()


# Username
discord_username = 'Icinga2 Monitoring'


# Is check host or service check?
check_type = 'host'
if args.service_name is not None:
    check_type = 'service'


# Embed color based on state
embed_color = 0

if args.check_state == 'UP' or args.check_state == 'OK':
    #006400
    embed_color = 25600
elif args.check_state == 'WARNING':
    #B96500
    embed_color = 12150016
elif args.check_state == 'DOWN' or args.check_state == 'CRITICAL':
    #8B0000
    embed_color = 9109504
elif args.check_state == 'UNKNOWN':
    #800080
    embed_color = 8388736


# Embed title
embed_title = '[{} Notification]'.format(args.notification_type)

if check_type == 'host':
    embed_title = '{} Host {} - {}'.format(embed_title, args.host_display_name, args.check_state)
else:
    embed_title = '{} {} - ({} - {})'.format(embed_title, args.check_state, args.host_display_name, args.service_display_name)


# Embed fields
embed_fields = []

embed_fields.append({
    'name': 'Hostname',
    'value': args.host_name,
})

if args.host_address != '':
    embed_fields.append({
        'name': 'IPv4 address',
        'value': args.host_address,
    })

if args.host_address6 != '':
    embed_fields.append({
        'name': 'IPv6 address',
        'value': args.host_address6,
    })

embed_fields.append({
    'name': 'Notification date',
    'value': args.notification_timestamp,
})

if args.notification_comment is not None:
    embed_comment = args.notification_comment

    if args.notification_author is not None:
        embed_comment += ' ({})'.format(args.notification_author)

    embed_fields.append({
        'name': 'Comment',
        'value': embed_comment,
    })

if args.notification_notes is not None:
    embed_fields.append({
        'name': 'Notes',
        'value': args.notification_notes,
    })

if args.icinga2_url is not None:
    args.icinga2_url = args.icinga2_url.rstrip('/')
    args.icinga2_url += '/monitoring/'

    if check_type == 'host':
        args.icinga2_url += 'host/show?host={}'.format(urllib.parse.quote(args.host_name))
    else:
        args.icinga2_url += 'service/show?host={}&service={}'.format(urllib.parse.quote(args.host_name), urllib.parse.quote(args.service_name))

    embed_fields.append({
        'name': 'Icinga2 web',
        'value': args.icinga2_url,
    })


# Request
req_data = {
    'username': discord_username,
    'embeds': [{
        'title': embed_title,
        'color': embed_color,
        'author': {
            'name': discord_username,
        },
        'description': args.check_output,
        'fields': embed_fields,
    }],
}

if args.verbose >= 1:
    print(req_data)

try:
    res = requests.post(args.discord_url, json = req_data)

    if args.verbose >= 1:
        print(res.text)
except requests.exceptions.RequestException as e:
    raise SystemExit(e)


sys.exit(0)
