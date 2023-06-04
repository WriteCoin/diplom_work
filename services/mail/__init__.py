from typing import TypedDict
from WebAutomation.general_utils import *
import imaplib
import email
from email.header import decode_header
import base64
import re
from bs4 import BeautifulSoup
from datetime import datetime
import quopri
from pprint import pprint


def connection(imap_server: str, username: str, password: str):
    imap = imaplib.IMAP4_SSL(imap_server)
    sts, res = imap.login(username, password)
    if sts == "OK":
        return imap
    else:
        raise Exception(f"Не удалось подключиться к сервису {imap_server}")


def date_parse(msg_date):
    if not msg_date:
        return datetime.now()
    else:
        dt_obj = "".join(str(msg_date[:6]))
        dt_obj = dt_obj.strip("'(),")

        dt_obj = datetime.strptime(dt_obj, "%Y, %m, %d, %H, %M, %S")
        return dt_obj


def from_subj_decode(msg_from_subj):
    if msg_from_subj:
        encoding = decode_header(msg_from_subj)[0][1] or 'utf-8'
        msg_from_subj = decode_header(msg_from_subj)[0][0]
        if isinstance(msg_from_subj, bytes):
            msg_from_subj = msg_from_subj.decode(encoding)
        if isinstance(msg_from_subj, str):
            pass
        msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
        return msg_from_subj
    else:
        return None


def encode_att_names(str_pl):
    enode_name = re.findall("\=\?.*?\?\=", str_pl)
    if len(enode_name) == 1:
        encoding = decode_header(enode_name[0])[0][1]
        decode_name = decode_header(enode_name[0])[0][0]
        decode_name = decode_name.decode(encoding)
        str_pl = str_pl.replace(enode_name[0], decode_name)
    if len(enode_name) > 1:
        nm = ""
        for part in enode_name:
            encoding = decode_header(part)[0][1]
            decode_name = decode_header(part)[0][0]
            decode_name = decode_name.decode(encoding)
            nm += decode_name
        str_pl = str_pl.replace(enode_name[0], nm)
        for c, i in enumerate(enode_name):
            if c > 0:
                str_pl = str_pl.replace(enode_name[c], "").replace('"', "").rstrip()
    return str_pl


def get_attachments(msg):
    attachments = list()
    for part in msg.walk():
        if (
            part["Content-Type"]
            and "name" in part["Content-Type"]
            and part.get_content_disposition() == "attachment"
        ):
            str_pl = part["Content-Type"]
            str_pl = encode_att_names(str_pl)
            attachments.append(str_pl)
    return attachments


def get_letter_text_from_html(body):
    body = body.replace("<div><div>", "<div>").replace("</div></div>", "</div>")
    try:
        soup = BeautifulSoup(body, "html.parser")
        paragraphs = soup.find_all("div")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.text + "\n"
        return text.replace("\xa0", " ")
    except Exception as exp:
        print("text ftom html err ", exp)
        return False


def letter_type(part):
    if part["Content-Transfer-Encoding"] in (None, "7bit", "8bit", "binary"):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:  # all possible types: quoted-printable, base64, 7bit, 8bit, and binary
        return part.get_payload()


def get_letter_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            count = 0
            if part.get_content_maintype() == "text" and count == 0:
                extract_part = letter_type(part)
                if part.get_content_subtype() == "html":
                    letter_text = get_letter_text_from_html(extract_part)
                else:
                    letter_text = extract_part.rstrip().lstrip()
                count += 1
                return (
                    letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")
                )
    else:
        count = 0
        if msg.get_content_maintype() == "text" and count == 0:
            extract_part = letter_type(msg)
            if msg.get_content_subtype() == "html":
                letter_text = get_letter_text_from_html(extract_part)
            else:
                letter_text = extract_part
            count += 1
            return letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")


def post_construct(msg_subj, msg_from, msg_email, letter_text, attachments):
    att_txt = "\n".join(attachments)
    postparts = [
        "\U0001F4E8 <b>",
        str(msg_subj),
        "</b>\n\n",
        "<pre>",
        str(msg_from),
        "\n",
        msg_email,
        "</pre>\n\n",
        letter_text,
        "\n\n",
        "\U0001F4CE<i> вложения: </i>",
        str(len(attachments)),
        "\n\n",
        att_txt,
    ]
    txt = "".join(postparts)

    return txt


class MailMessage(TypedDict):
    msg_subj: str
    msg_from: str
    msg_email: str
    text: str
    attachments_count: int
    date: datetime


def get_email_data(
    imap: imaplib.IMAP4_SSL,
    mailbox: str = "INBOX",
    charset: Optional[str] = None,
    criteria: str = "ALL",
    message_func: Optional[Callable[[MailMessage], None]] = None,
) -> List[MailMessage]:
    # Из всей папки
    status, all_messages = imap.select(mailbox)
    # Получение указателей всех писем
    result, messages = imap.uid("search", charset, criteria)

    # Получение номеров
    messages = messages[0].decode("utf-8").split(" ")

    results = []

    if messages[0]:
        for letter in messages:
            attachments = []
            res, msg = imap.uid("fetch", letter, "(RFC822)")
            if res == "OK":
                # Извлечение письма
                msg = email.message_from_bytes(msg[0][1])
                # Дата получения
                msg_date = date_parse(email.utils.parsedate_tz(msg["Date"]))

                msg_from = from_subj_decode(msg["From"])
                msg_subj = from_subj_decode(msg["Subject"])

                # ID письма
                if msg["Message-ID"]:
                    msg_id = msg["Message-ID"].lstrip("<").rstrip(">")
                else:
                    msg_id = msg["Received"]

                # Email отправителя
                if msg["Return-path"]:
                    msg_email = msg["Return-path"].lstrip("<").rstrip(">")
                else:
                    msg_email = msg_from

                if not msg_email:
                    encoding = decode_header(msg["From"])[0][1]  # не проверено
                    msg_email = (
                        decode_header(msg["From"])[1][0]
                        .decode(encoding)
                        .replace("<", "")
                        .replace(">", "")
                        .replace(" ", "")
                    )

                letter_text = get_letter_text(msg)
                attachments = get_attachments(msg)

                # post_text = post_construct(
                #     msg_subj, msg_from, msg_email, letter_text, attachments
                # )
                # if len(post_text) > 4000:
                #     post_text = post_text[:4000]

                message_result = MailMessage(
                    msg_subj=msg_subj or "",
                    msg_from=msg_from or "",
                    msg_email=msg_email,
                    text=letter_text or "",
                    attachments_count=len(attachments),
                    date=msg_date,
                )

                # pprint(message_result)
                # return

                if not message_func is None:
                    message_func(message_result)

                results.append(message_result)

    return results
