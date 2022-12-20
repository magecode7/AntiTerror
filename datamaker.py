import asyncio
import messagedumper
import pandas

async def main():
    channnels = [
        "https://t.me/toporlive",
        "https://t.me/oldlentach",
        "https://t.me/d_code",
        "https://t.me/rhymestg",
        "https://t.me/rkn_tg",
        "https://t.me/sndkgram",
        "https://t.me/durov_russia",
        "https://t.me/alukatsky",
        "https://t.me/RKadyrov_95",
        "https://t.me/yurasumy",
        "https://t.me/labkovskiy",
        "https://t.me/marketingold",
        "https://t.me/tolstoy_life"
        ]

    messages = []
    for channel in channnels:
        m = await messagedumper.dump_all_messages(channel, 50)
        messages = messages + m

    train_labels = [0] * len(messages)

    train_data = pandas.DataFrame()
    train_data['messages'] = messages
    train_data['labels'] = train_labels

    print(train_data)

    train_data.to_csv('normal1.csv', sep=';', index=False)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())