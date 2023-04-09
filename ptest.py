import regex
import json
import gptAPIs
import apiManager
import time
import io
import asyncio

question = "根据最新的存款利率，我的50万存款应该拿出多少来购买哪些稳健的股票，使我的年收益可以达到5%？"
start_time = time.time()
# response = gptAPIs.invoke_gpt3(apiManager.system_init_promote + " Human: " + question)


async def write_data(stream):
    while True:
        # 模拟异步线程每隔 1 秒写入数据
        data = b'Hello World!\n'
        stream.write(data)
        print(f'Write {len(data)} bytes to buffer')
        await asyncio.sleep(1)


async def read_data(stream):
    await asyncio.sleep(1)
    while True:
        # 在主线程中不停读取输出数据
        stream.seek(0)
        data = stream.readlines()
        stream.seek(0)
        stream.truncate()
        if not data:
            break
        print(f'Read {len(data)} bytes from buffer: {data}')
        await asyncio.sleep(0.1)


async def main():
    stream = io.BytesIO()
    task_write = asyncio.create_task(write_data(stream))
    task_read = asyncio.create_task(read_data(stream))
    await asyncio.gather(task_write, task_read)

if __name__ == '__main__':
    asyncio.run(main())

