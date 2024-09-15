import argparse
import colorama
import datetime
import os
import json
import urllib.parse

from telethon import T sync
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.contacts import ImportContacts DeleteContactsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoneContact, InputUser
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.types import UserStatusEmpty, UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth

colorama.init()

parser = argparse.ArgumentParser(description='Get information about a Telegram user, channel group.')
parser.add_argument('-u', '--username', type=str, help='The username (with without the @ symbol)')
parser.add_argument('-i', '--id', type=int, help='The ID (a numerical value)')
parser.add_argument('-p', '--phone', type=str, help='The phone number (with the country code)')
parser.add_argument('-l', '--url', type=str, help='The URL of a message in a public channel or group')
args = parser.parse_args()_id = int(os.environ.get('TELEGRAM_API_ID'))
api_hash = os.environ.get('TELEGRAM_API_HASH')
phone = os.environ.get('TELEGRAM_PHONE_NUMBER')
code = os.environ.get('TELEGRAM_CODE')

client = TelegramClient('session_name', api_id, api_hash)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, code)
    except SessionPasswordNeededError:
        password = os.environ.get('TELEGRAM_PASSWORD')
        client_in(password=password)

def main():
    entity = None 
    alias = '' 

    if args.username is not None:
        alias = args.username
        try:
            entity = client.get_entity(alias)
            entity_type = entity.__class__.__name__
            if entity_type == 'User':            
                get_user_info(entity, alias)
             == 'Channel':
                if entity.megagroup: 
                    get_chat_info(entity)
                else: 
                    get_channel_info(entity)
        except ValueError as e: 
            print(f"Could not find the user with username {colorama.Fore.RED}@{aliasStyle.RESET_ALL}")
            print(f"Please check that the username is correct and that the user exists")

    elif args.id is not None:
        user_id = args.id
        try:
            entity = client.get_entity(user_id)
            entity_type = entity.__class__.__name__
            if entity_type == 'User':            
                get_user_info(entity, user_id)
            elif entity_type == 'Channel':
                get_channel_info(entity)
            elif entity_type == 'Chat':
                get_chat_info(entity)
        except ValueError as e: 
            print(f"Could not find the user with ID {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL}")
            print(f"Please use the parameter -i only with users that are in your contacts list")

    elif args.phone is not None:
        phone_number = args.phone
        contact = InputPhoneContact(client_id=0, phone= first_name='Contacto', last_name='Temporal')
        result = client(ImportContactsRequest([contact]))

        if result.users:
            user = result.users[get_user_info(user, phone_number)
            client(DeleteContactsRequest(id=[InputUser(user_id=user.id, access_hash=user.access_hash)]))
        else:
            print(f'No user was phone number {colorama.Fore.RED}{phone_number}{colorama.Style.RESET_ALL}')

    elif args.url is not None:
        url = args.url 
        result = urllib.parse.urlparse(url) 
        path = result.path 
        parts = path.split('/') 
        channel_name = parts[1] 
        message_id = int(parts[2]) 
        message = client.get_messages(entity=channel_name, ids=message_id, limit=1) 
        message_json = json.dumps(message.to_dict(), indent=2, default=bytes_to_str) 
        print(message_json) 
    else:
        print('You must pass an argument -u, -i or -p to obtain information about a Telegram user')

def get_user_info(user, identifier):
    user_id = user.id
    name = user.first_name
    username = user.username
    last_name = user.last_name
    full = client(GetFullUserRequest(user))
    bio = full.full_user.about
    status = user.status
    last_seen = get_user_status(status)

    print(f'User ID: {colorama.Fore.RED}{user_id}{colorama.Style.RESET_ALL}')
    print(f'First Name: {colorama.Fore.RED}{name}{colorama.Style.RESETf'Last Name: {colorama.Fore.RED}{last_name}{colorama.Style.RESET_ALL}')
    Last seen: {colorama.Fore.RED}{last_seen}{colorama.Style.RESET_ALL}')
    if username:
        print(f'Username: {colorama.Fore.RED}@{username}{colorama.Style.RESET_ALL}')
    else:
        print(f'The user does not have a username')
    print(f'Biography: {colorama.Fore.RED}{bio}{colorama.Style.RESET_ALL}')

    # Note: Profile picture download is commented out as it might not work in Render
    # client.download_profile_photo(user, file=f'{user_id}.jpg')
    # print(f'Profile picture downloaded as {colorama.Fore.RED}{user_id}.jpg{colorama.Style.RESET_ALL}')

def get__info(channel):
    channel_id = channel.id
    title = channel.title
    username = channel.username
    ch_fullFullChannelRequest(channel=channel))
    about = ch_full.full_chat.about
    date = channel

    print(f'Channel ID: {colorama.Fore.RED}{channel_id}{colorama.Style.RESET_ALL}')
    print(f'Title: {colorama.Fore.RED}{title}{colorama.Style.RESET_ALL}')
     username:
        print(f'Username: {colorama.Fore.RED}@{username}{colorama.Style.RESET_ALL}')
    else:
        print(f'The channel does not have a username')
    print(f'Description: {colorama.Fore.RED}{about}{colorama.Style.RESET_ALL}')
    print(f'Creation date: {colorama.Fore.RED}{date.strftime("%Y-%m-%d %H:%M:%S (UTC)")}{colorama.Style.RESET_ALL}')

def get_chat_info(chat):
    chat_id = chat.id
    title = chat.title
    date = chat.date
    participants = client.get_participants(chat)    
    participants(participants) 

    print(f'Group ID: {colorama.Fore.RED}{chat_id}{colorama.Style.RESET_ALL}')
    print(f'Title: {colorama.Fore.RED}{title}{colorama.Style.RESET_ALL}')
    print(f'Number of participants: {colorama.Fore.RED}{participants_count}{colorama.Style.RESET_ALL}')
    print(f'Creation date: {colorama.Fore.RED}{date.strftime("%Y-%m-%d %H:%M:%S (UTC)")}{colorama.Style.RESET_ALL}')

def get_user_status(status):
    if isinstance(status, UserStatusEmpty): 
        return "never" 
    elif isinstance(status, UserStatusOnline): 
        return "now" 
    elif isinstance(status, UserStatusOffline): 
        return status.was_online.isoformat() 
    elif isinstance(status, UserStatusRecently): 
        return "recently" 
    elif isinstance(status, UserStatusLastWeek): 
        return "last week" 
    elif isinstance(status, UserStatusLastMonth): 
        return "last month" 

def bytes_to_str(b):
    if isinstance(b, bytes): 
        return b.hex() 
    elif isinstance(b,.datetime): 
        return b.strftime('%Y-%m-%d %H:%M:%S (UTC)') 
    else: 
        return str(b) 

if __name__ == '__main__':
    main()
