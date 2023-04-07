import pandas as pd
import kbsHelper


def read_excel(excel_file):
    # 使用pandas读取Excel文件中的工作表
    xls = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')

    texts = []
    # `xls`现在是一个字典，其中键是工作表名称，值是对应的数据框
    for sheet_name, df in xls.items():
        question_column = df.columns[1]
        answer_column = df.columns[3]

        # 将DataFrame转换为字典列表
        data_list = df.to_dict(orient='records')

        for row in data_list:
            question = row[question_column]
            answer = row[answer_column]
            text = f"{question}:\n{answer}"
            texts.append(text)

    return texts


def upsert_kbs(texts):
    documents = []
    index = 0
    for text in texts:
        index += 1
        document = {
            "id": f"r{index}",
            "text": text
        }
        documents.append(document)
    processed_count = kbsHelper.upsert_kbs(documents)
    print(f"processed {processed_count}")


def main():
    excel_file = 'SAP_Ariba_AI.xlsx'
    texts = read_excel(excel_file)
    upsert_kbs(texts)


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
