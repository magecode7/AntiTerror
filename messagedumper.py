from telethon import TelegramClient

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

# Присваиваем значения внутренним переменным
api_id = 16670629
api_hash = '548d486d95af4295d0db13ae3699394b'
username = "antiterror"

client = TelegramClient(username, api_id, api_hash)

client.start()

async def dump_all_messages(channel: str, limit_msg: int = 100, total_count_limit: int = 1) -> list:
	offset_msg = 0    # номер записи, с которой начинается считывание

	all_messages = []   # список всех сообщений
	total_messages = 0

	while True:
		print("[DEBUG] Start dumping:", channel)
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			if len(str(message.message)) > 0: all_messages.append(message.message)
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break
	
	return all_messages

async def main():
	url = input("Введите ссылку на канал или чат: ")

	dumped_messages = await dump_all_messages(url)
	text = ('\n' + 50 * '_' + '\n').join(dumped_messages)
	
	print(text)
	
if __name__ == "__main__":
	with client:
		client.loop.run_until_complete(main())