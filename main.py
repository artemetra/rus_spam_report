from typing import List, Union, Tuple
import random
import time

from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import UsernameInvalid

from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.base import InputPeer, ReportReason
from pyrogram.raw.types import (
    InputPeerChannel, 
    
    InputReportReasonViolence, 
    InputReportReasonOther
)


app = Client("spamreport")

reasons_msg = [
    "Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainians and Ukrainian soldiers.",
    "The channel undermines the integrity of the Ukrainian state. Spreading fake news, misleading people. Block it as soon as possible!",
]

reason_types = [
    InputReportReasonOther,
    InputReportReasonViolence,
]

def to_peer(client: Client, link: str) -> Union[InputPeer, None]:
    try:
        return client.resolve_peer(link)
    except (KeyError, UsernameInvalid):
        return None

def get_working_peer_list(app: Client) -> List[Tuple[str, InputPeer]]:
    with open("links.txt", encoding="UTF-8") as _links:
        links = [link.strip() for link in _links]
    
    working = []
    for l in links:
        peer = to_peer(app, l)
        if peer:
            working.append((l, peer))
        else:
            print(f"Skipping '{l}'...")
    
    return working

def send_report(app: Client, peer: InputPeerChannel) -> bool:
    report_reason_type: ReportReason = random.choice(reason_types)()
    report_reason_message = random.choice(reasons_msg)
    rp = ReportPeer(
        peer=peer, 
        reason=report_reason_type, 
        message=report_reason_message
    )

    result = app.send(rp)
    return result

def main(app: Client) -> None:
    links = get_working_peer_list(app)
    while True:
        for link in links:
            report = send_report(app, link[1])
            print(f"Successfully sent report to {link[0]}!") if report else print(f"!!Failed to send report to {link[0]}.")
            time.sleep(random.randint(1, 9999)/3333)

if __name__ == '__main__':
    with app:
        main(app)