from janome.tokenizer import Tokenizer
import zipfile
import os.path, urllib.request as request

# ファイルをダウンロードする
url = "https://www.aozora.gr.jp/cards/000081/files/43737_ruby_19028.zip"
localfile = "43737_ruby_19028.zip"

if not os.path.exists(localfile): # もしも、システムのファイルパス上にlocalfileで指定した名称のファイルが存在しないならば
    print("ファイルをダウンロードします")
    request.urlretrieve(url,localfile) # urlretrieve つぎのurlからとってきて、localfileに設定した名称で保存

# ファイルを読み込んでいく
# インポートしたzipfileモジュールのZipFileメソッドを利用してzipファイルを解凍する、localfileで指定した名称のファイルを'r'読み取り専用で解凍する
zipfile = zipfile.ZipFile(localfile,'r')
# 上記で解凍したzipファイルを開く
file = zipfile.open('gingatetsudono_yoru.txt','r')
# 解凍したデータをバイナリとしてよみこむ
bindata = file.read()
# バイナリをデコードする
textdata = bindata.decode('shift_jis')
# janomeの読み込み
t = Tokenizer()
# データ格納用リストを用意
worddic = {}
# データの区切りを指定 改行コードでデータを分割　行でデータを区切る
lines = textdata.split("\r\n")
# 単語の個数を数えていく
for line in lines:
    malist = t.tokenize(line) # 1行ごとにデータを形態素解析していく
    for w in malist: # 1行ごとに取り出したデータに対して、処理をする
        word = w.surface # surfaceにデータが入っているのでこれを利用してデータを取り出す
        part = w.part_of_speech # part_of_speechで品詞情報を取り出す
        if part.find('名詞') < 0:  # part_of_speechで取り出した品詞情報の中から、名詞のものを探す
            continue 
        if not word in worddic: # さきほど定義したworddicという辞書型のオブジェクトにwordがない場合
            worddic[word]=0 #worddicにそのword名のキーを用意して初期化する
        worddic[word]+=1

keys = sorted(worddic.items(), key= lambda x:x[1], reverse=True)        
for word,cnt in keys[:50]:
    print("{0}({1})\n".format(word,cnt), end="")
        











