#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import sys
import json


def send_alert(final_text, webhook_url):
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        url=webhook_url, headers=headers, data=json.dumps(final_text)
    ).json()
    return response


def main():
    payload = json.loads(sys.stdin.read())
    config = payload.get("configuration", dict())
    print(config)
    message = config.get("message")
    severity = config.get("severity")
    webhook_url = config.get("webhook_url")
    result_link = config.get("result_link")
    link = ""
    final_text = {}
    color_map = {
        "LOW": 16776960,
        "MEDIUM": 16753920,
        "HIGH": 16733525,
        "CRITICAL": 16711680,
    }
    if severity in color_map:
        color = color_map[severity]
    else:
        color = None

    if result_link == "0":
        fields = [
            {"name": "Severity", "value": severity, "inline": False},
            {
                "name": "Alert Owner",
                "value": str(payload.get("owner")),
                "inline": False,
            },
        ]
        data = {
            "embeds": [
                {
                    "title": str(payload.get("search_name")),
                    "description": str(message),
                    "color": color,
                    "fields": fields,
                }
            ]
        }
        final_text = data
    elif result_link == "1":
        fields = [
            {"name": "Severity", "value": severity, "inline": False},
            {
                "name": "Link",
                "value": str(payload.get("results_link")),
                "inline": False,
            },
            {
                "name": "Alert Owner",
                "value": str(payload.get("owner")),
                "inline": False,
            },
        ]
        data = {
            "embeds": [
                {
                    "title": str(payload.get("search_name")),
                    "description": str(message),
                    "color": color,
                    "fields": fields,
                }
            ]
        }
        final_text = data
    send_alert(final_text, webhook_url)


if __name__ == "__main__":
    main()
