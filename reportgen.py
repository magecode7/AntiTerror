from io import TextIOWrapper
from catboost import CatBoostClassifier
import semantic
import aiofiles

model = CatBoostClassifier()
model.load_model('terror.model')

async def create_report(texts: list[str], path: str) -> TextIOWrapper:
    report = ''
    for text in texts:
        lemma_tokens = semantic.tokenize(text)
        if len(lemma_tokens) < 5: continue

        report += 'Сообщение:\n\n'
        report += text + '\n\n'

        report += 'Лемматизированный текст:\n\n'
        lemma_text = ' '.join(lemma_tokens)
        report += lemma_text + '\n\n'

        report += 'ОТЧЕТ\n\n'
        report += 'Вероятность террористического содержания: '
        report += str(round(model.predict_proba([lemma_text])[1] * 100, 2)) + '%\n\n'

        report += 'Самые популярные слова:\n'
        for tup in semantic.top_tokens(lemma_text.split())[:5]:
            report += f'{tup[0]}: {tup[1]}\n'

        report += '_'*100 + '\n'

    async with aiofiles.open(path, 'w', encoding='utf-8') as file:
        await file.write(report)

def main():
    while True:
        input_text = input('Введите сообщение: ')
        create_report([input_text], 'test')

if __name__ == "__main__":
    main()