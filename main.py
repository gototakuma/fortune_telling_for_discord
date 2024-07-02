import os

import discord
import openai

# ローカルで使用する際はコメントアウトを外す
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

# 自分のBotのアクセストークンに置き換えてください
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# OpenAIのAPIキーをセットアップする
openai.api_key = os.environ["OPENAI_API_KEY"]

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# ChatGPTというクラスを定義する
class ChatGPT:
    # ユーザーからの入力を受け取り、OpenAI APIを使って回答を生成する
    def input_message(self, input_text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは占い師です。今日の運勢を占ってください。"},
                {"role": "user", "content": input_text}
            ],
            temperature=0
        )

        # 応答の表示
        text = response['choices'][0]['message']['content']

        return text


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログイン！！！')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # Bot自身が送信したメッセージには反応しない
    if message.author == client.user:
        return
    # 占いbotチャンネル以外では反応しない
    elif message.channel.name != "占いbot":
        return

    # ユーザーからの質問を受け取る
    question = message.content[4:]

    # ChatGPTクラスを使って回答を生成する
    api = ChatGPT()
    answer = api.input_message(question)

    # 回答を送信する
    await message.channel.send(answer)

# Botの起動とDiscordサーバーへの接続
client.run(DISCORD_TOKEN)
