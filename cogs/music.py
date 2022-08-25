import discord
from discord.ext import commands
import os
import asyncio
from glob import glob
import pathlib
import re
#bgmコマンドで使う再生キュー
class AudioQueue(asyncio.Queue):
    def __init__(self):
        super().__init__(0)         #再生キューの上限を設定しない
    def __getitem__(self, idx):
        return self._queue[idx]     #idx番目を取り出し
    def to_list(self):
        return list(self._queue)    #キューをリスト化
    def reset(self):
        self._queue.clear()         #キューのリセット
#bgmコマンドで使う，現在の再生状況を管理するクラス
class AudioStatus:
    def __init__(self, vc):
        self.vc = vc                                #自分が今入っているvc
        self.queue = AudioQueue()                   #再生キュー
        self.playing = asyncio.Event()
        asyncio.create_task(self.playing_task())
    #曲の追加
    async def add_audio(self, title, path, isloop = False):
        await self.queue.put([title, path, isloop])
    #曲の再生（再生にはffmpegが必要）    
    async def playing_task(self):
        while True:
            self.playing.clear()
            try:
                title, path, isloop = await asyncio.wait_for(self.queue.get(), timeout = 100)
            except asyncio.TimeoutError:
                asyncio.create_task(self.leave())
            selfpath = os.path.dirname(__file__)
            self.vc.play(discord.FFmpegPCMAudio(executable=selfpath+"/bin/ffmpeg.exe", source=path), after = self.play_next)
            if (isloop):
                await self.add_audio(title, path, isloop = True)
            activity = discord.Activity(name=title, type=discord.ActivityType.listening)    #アクティビティの作成
            self.bgminfo = path #後で使います
            await self.bot.change_presence(activity=activity)    #アクティビティの更新
            await self.playing.wait()
    
    #playing_taskの中で呼び出される
    #再生が終わると次の曲を再生する
    def play_next(self, err=None):
        self.bgminfo = None
        self.playing.set()
        return
            
    #vcから切断
    async def leave(self):
        self.queue.reset()  #キューのリセット
        if self.vc:
            await self.vc.disconnect()
            self.vc = None
        return    
    #曲が再生中ならtrue
    def is_playing(self):
        return self.vc.is_playing()
    def playing_info(self):
        if (self.bgminfo is None):
            return 'This bot is not playing an Audio File'
        return self.bgminfo
    #再生する曲が無くなる等でweb socketが切断されていればtrue
    def is_closed(self):
        return (self.vc is None or (self.vc.is_connected() == False))
#多重リストを区切り文字で展開する
def list2str(list_, delimiter):
    result = ''
    #区切り文字が存在しなければスペースを区切り文字とする
    if (len(delimiter) == 0):
        d = ' ' #区切り文字
        for s in list_:
            result += str(s) + d
        return result[:-1]
    
    #区切り文字=delimiterの第一要素
    d = delimiter[0]
    for s in list_:
        #list_の中にリストがあれば再帰呼び出し
        if (type(s) is list):
            result += list2str(s, delimiter[1:]) + d
        else:
            result += str(s) + d
    return result[:-1*len(d)]
def make_filetree(path, layer=0, is_last=False, nest = -1):
    if (nest == 0):
        return ''
    if (nest == 1):
        is_last = True
    d = []
    #pathが相対パスなら絶対パスに直す
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())
    # カレントディレクトリの表示
    current = path.split(os.sep)[::-1][0]
    d.append(pathlib.Path(current).parts[-1])
    # 下の階層のパスを取得
    paths = [p for p in glob(path+'/*') if os.path.isdir(p) or os.path.isfile(p)]
    def is_last_path(i):
        return i == len(paths)-1
    # 再帰的に表示
    for i, p in enumerate(paths):
        if os.path.isdir(p):    #フォルダなら自身を再帰呼び出し
            d.append(make_filetree(p, layer=layer+1, is_last=is_last_path(i), nest = nest-1))
        if (nest == 1):
            break
    return d    #フォルダの一覧をリストで返す
def depth(k):
    if not k:
        return 0
    else:
        if isinstance(k, list):
            return 1 + max(depth(i) for i in k)
        else:
            return 0
async def send_list(send_method, mention, mes, title = 'Result', delimiter = ['\n'], isembed = True, senderr = True, half = False, ishalf = False):
    if (len(mes) == 0): #listの長さ=0
        await send_method(f'{mention} 該当するデータがありません')
    else:
        #listを文字列に変換
        reply = list2str(mes, delimiter)
        if (ishalf):
            reply += "\n………"
        if (isembed):
            try:
                embed = discord.Embed(title=title, description=reply)
                await send_method(f'{mention} ', embed=embed)
            except:
                if (half and len(mes) > 1):
                    result = await send_list(send_method, mention, mes[:int(len(mes)/2)], title, delimiter, isembed, senderr, half, ishalf = True)
                    return result
                if (senderr):
                    await send_method(f'{mention} エラー：該当するデータが多すぎます')
                    return False
        else:
            await send_method(f'{mention} \n'+reply)
    return True
class __BGM(commands.Cog, name= 'BGM'): #BGMという名前でCogを定義する
    def search_audiofiles(self):
        cur_path   = os.getcwd()    #カレントディレクトリ
        MUSIC_PATH = os.path.dirname(__file__)
        os.chdir(MUSIC_PATH)    #オーディオファイルがある場所の頂点に移動
        self.music_pathes = [p for p in glob('bgm/**', recursive=True) if os.path.isfile(p)] #オーディオファイルの検索（相対パス）
        self.music_titles = [os.path.splitext(os.path.basename(path))[0] for path in self.music_pathes]     #オーディオファイルの名前から拡張子とパスを除去したリストを作成
        self.music_pathes = [MUSIC_PATH + os.sep + p for p in self.music_pathes]             #絶対パスに変換
        self.music_dirs = glob(os.path.join('bgm', '**' + os.sep), recursive=True)                 #ディレクトリの一覧を作成（相対パス）
        self.mdir_name  = [pathlib.Path(f).parts[-1] for f in self.music_dirs]
        os.chdir(cur_path)          #カレントディレクトリを戻す
        return
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.audio_status = None
        self.path = os.path.dirname(__file__)    #このファイルが置いてあるディレクトリまでのファイルパス
        self.search_audiofiles()
    #embedに収まる範囲でファイル構造を送信する
    #path：送るファイル構造の頂点のファイルパス
    #nest：何階層分を送信するか
    async def send_tree(self, ctx, path, nest = -1):
        if (nest == 0):
            await ctx.send('エラー：該当するデータが多すぎます')
        if (nest == -1):    #とりあえずネスト上限無しで送信してみる
            tree = make_filetree(path)
            nest = depth(tree)
        else:
            tree = make_filetree(path, nest = nest)
        result = await send_list(ctx.send, '', tree, delimiter = ['\n'+'....'*i+'├' for i in range(nest)], senderr = False)
        if (result is False):
            await self.send_tree(ctx, path, nest = nest-1)  #ネストを1つ浅くしてやり直し
        return
    #再生キューが空の状態で放置しているとvcから切断されるため，bgm及びremoveコマンドで現在の接続状況を再読み込みする
    async def reload_state(self):
        if (self.audio_status == None or self.audio_status.is_closed()):    #vcから切断済みである場合
            global voice, now_vc
            activity = discord.Activity(name='Python', type=discord.ActivityType.playing)   #アクティビティも修正する
            await self.bot.change_presence(activity=activity)
            now_vc = None
            voice = None
        return
    @commands.command()
    async def bgm(self, ctx, *name):
        """play music"""
        await self.reload_state()
        if (ctx.author.voice is None):  #送信者がボイスチャンネルにいなければエラーを返す
            await ctx.send(f'{ctx.author.mention} ボイスチャンネルが見つかりません')
            return
        if ((self.audio_status is None) or (self.audio_status.vc is None)): #botがボイスチャンネルに入っていなければ
            voice_channel = ctx.author.voice.channel.id                     #送信者の入っているボイスチャンネルのID
            vc = await self.bot.get_channel(voice_channel).connect()             #ボイスチャンネルに入る
            self.audio_status = AudioStatus(vc)
        #filenameの作成（nameの連結）
        filename = ''
        for s in name:
            filename += s + ' '
        filename = filename[:-1]
        if (len(filename) == 0):    #引数無しなら全曲を追加
            for i in range(len(self.music_titles)):
                await self.audio_status.add_audio(self.music_titles[i], self.music_pathes[i])
        elif filename in self.music_titles: #指定された曲がある場合
            idx = self.music_titles.index(filename) #リストの何番目にあるかを探す
            await self.audio_status.add_audio(filename, self.music_pathes[idx])  #対応する絶対パスを再生キューに追加
        elif (filename in self.mdir_name):       #ディレクトリ名に一致した場合，該当するディレクトリ下にある全ての曲を再生キューに追加
            idx = self.mdir_name.index(filename)
            cur_path = os.getcwd()
            os.chdir(self.path + os.sep + self.music_dirs[idx]) #指定したフォルダに移動
            music_pathes = [p for p in glob('**', recursive=True) if os.path.isfile(p)] #音楽ファイル一覧
            music_titles = [os.path.splitext(os.path.basename(path))[0] for path in music_pathes]
            os.chdir(cur_path)          #カレントディレクトリを戻す
            length = len(music_titles)
            for i in range(length): #トラック番号の除去
                if (re.fullmatch(r'[0-9][0-9] .*', music_titles[i])):
                    music_titles[i] = (music_titles[i])[3:]
            numbers = len(music_pathes)
            for i in range(numbers):
                await self.audio_status.add_audio(music_titles[i], self.path + os.sep + self.music_dirs[idx] + os.sep + music_pathes[i])
        else:   #それ以外
            await ctx.send('Audio File Not Found')
        return
    @commands.command()
    async def loopbgm(self, ctx, *name):
        """loop music"""
        await self.reload_state()
        if (ctx.author.voice is None):  #送信者がボイスチャンネルにいなければエラーを返す
            await ctx.send(f'{ctx.author.mention} ボイスチャンネルが見つかりません')
            return
        if ((self.audio_status is None) or (self.audio_status.vc is None)): #botがボイスチャンネルに入っていなければ
            voice_channel = ctx.author.voice.channel.id                     #送信者の入っているボイスチャンネルのID
            vc = await self.bot.get_channel(voice_channel).connect()             #ボイスチャンネルに入る
            self.audio_status = AudioStatus(vc)
        #filenameの作成（nameの連結）
        filename = ''
        for s in name:
            filename += s + ' '
        filename = filename[:-1]
        if (len(filename) == 0):    #引数無しなら全曲を追加
            for i in range(len(self.music_titles)):
                await self.audio_status.add_audio(self.music_titles[i], self.music_pathes[i], isloop = True)
        elif filename in self.music_titles: #指定された曲がある場合
            idx = self.music_titles.index(filename) #リストの何番目にあるかを探す
            await self.audio_status.add_audio(filename, self.music_pathes[idx], isloop = True)  #対応する絶対パスを再生キューに追加
        elif (filename in self.mdir_name):       #ディレクトリ名に一致した場合，該当するディレクトリ下にある全ての曲を再生キューに追加
            idx = self.mdir_name.index(filename)
            cur_path = os.getcwd()
            os.chdir(self.path + os.sep + self.music_dirs[idx]) #指定したフォルダに移動
            music_pathes = [p for p in glob('**', recursive=True) if os.path.isfile(p)] #音楽ファイル一覧
            music_titles = [os.path.splitext(os.path.basename(path))[0] for path in music_pathes]
            os.chdir(cur_path)          #カレントディレクトリを戻す
            length = len(music_titles)
            for i in range(length): #トラック番号の除去
                if (re.fullmatch(r'[0-9][0-9] .*', music_titles[i])):
                    music_titles[i] = (music_titles[i])[3:]
            numbers = len(music_pathes)
            for i in range(numbers):
                await self.audio_status.add_audio(music_titles[i], self.path + os.sep + self.music_dirs[idx] + os.sep + music_pathes[i], isloop = True)
        else:   #それ以外
            await ctx.send('Audio File Not Found')
        return
    #botをボイスチャンネルから切断する
    @commands.command()
    async def remove(self, ctx):
        await self.audio_status.leave()
        await self.reload_state()
        return
    @commands.command()
    async def bgmlist(self, ctx, *dir_name):
        """一覧"""
        cur_path = os.getcwd()
        MUSIC_PATH = os.path.dirname(__file__)
        os.chdir(MUSIC_PATH)        #カレントディレクトリの移動
        dirname = ''
        for s in dir_name:          #引数を1つの文字列に纏める
            dirname += s + ' '
        dirname = dirname[:-1]
        if (len(dirname) == 0):     #引数無しなら全てのディレクトリを表示
            await self.send_tree(ctx=ctx, path=MUSIC_PATH+os.sep+'bgm')
        else:
            for f in self.music_dirs:
                if (dirname == pathlib.Path(f).parts[-1]):                  #ディレクトリ名と引数が一致した場合，表示
                    current = f.split(os.sep)[1:][0]
                    tree = make_filetree(MUSIC_PATH+os.sep+f[:-1*len(os.sep)])
                    if (len(tree) != 1):                                    #該当ディレクトリの下にディレクトリがあった場合は木構造を表示
                        result = await send_list(ctx.send, '', tree, delimiter = ['\n'+'....'*i+'├' for i in range(10)])
                        if (result is None):
                            nest = depth(tree)
                            await self.send_tree(ctx=ctx, path=MUSIC_PATH+os.sep+f, nest = nest-1)
                    else:                                                   #ディレクトリを持たなければオーディオファイルの一覧を表示
                        os.chdir(MUSIC_PATH + os.sep + f)
                        music_titles = [os.path.splitext(os.path.basename(p))[0] for p in glob('*', recursive=True) if os.path.isfile(p)]
                        length = len(music_titles)
                        for i in range(length):
                            if (re.fullmatch(r'[0-9][0-9] .*', music_titles[i])):
                                music_titles[i] = (music_titles[i])[3:]
                        await send_list(ctx.send, '', music_titles)
                    break
        os.chdir(cur_path)      #カレントディレクトリを戻す
        return
    @commands.command()
    async def pause(self, ctx):
        """再生中のbgmの一時停止"""
        if (self.audio_status.is_playing()):
            self.audio_status.vc.pause()
        return
        
    @commands.command()
    async def resume(self, ctx):
        """再生中のbgmの再開"""
        self.audio_status.vc.resume()
        return
    @commands.command()
    async def stop(self, ctx):
        """再生中のbgmの中断"""
        if (self.audio_status.is_playing()):
            self.audio_status.vc.stop()
        return
    @commands.command()
    async def clear(self, ctx):
        """再生キューのリセット"""
        self.audio_status.queue.reset()
        return
    
    @commands.command()
    async def queue(self, ctx):
        """再生キューの表示"""
        await send_list(ctx.send, '', [x[0] for x in self.audio_status.queue], title = '再生キュー', isembed = True, half = True)
        return
    @commands.command()
    async def bgminfo(self, ctx):
        """再生中のBGMのパスを表示"""
        if (self.audio_status is None):
            await ctx.send(f'{ctx.author.mention} This bot is not playing an Audio File')
        else:
            await ctx.send(f'{ctx.author.mention} {self.audio_status.playing_info()[len(self.path)+1:]}')
        return
async def setup(bot):
    await bot.add_cog(__BGM(bot=bot))